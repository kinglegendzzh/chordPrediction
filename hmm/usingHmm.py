import numpy as np
import pandas as pd
from hmmlearn import hmm
from sklearn.cluster import KMeans

# 定义和弦编码和乐理相关参数
CHORD_CODE_MAP = {
    'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4,
    'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9,
    'A#': 10, 'Bb': 10, 'B': 11
}
SCALE_STEPS = [2, 2, 1, 2, 2, 2, 1]  # 7个音符，分别间隔2、2、1、2、2、2、1
NUM_STATES = 3  # 状态数
NUM_GAUSSIANS = 3  # 高斯分布的数量


# 根据和弦编码获取相对音高
def get_rel_pitch(chord_code):
    return [CHORD_CODE_MAP[chord] for chord in chord_code.split(',')]


# 根据旋律编码生成相对音高序列
def get_rel_pitch_seq(melody_code):
    rel_pitch_seq = []
    current_note = 0
    for step in SCALE_STEPS:
        rel_pitch_seq.append(current_note)
        current_note += step
        if current_note > 11:
            current_note -= 12
    rel_pitch_seq = [rel_pitch_seq[idx % 7] for idx in melody_code]
    return rel_pitch_seq


# 使用训练好的HMM模型预测下一个和弦
def predict_chord(model, state_rel_pitch_dict, current_chord, current_rel_pitch, num_predictions=3):
    predictions = []
    probas = []
    for _ in range(num_predictions):
        # 进行预测，输出下一个状态的编码
        next_rel_pitch, proba = model.sample(n_samples=1, X=np.array([current_rel_pitch[-1]]).reshape(-1, 1))
        next_state = int(next_rel_pitch[0])
        probas.append(proba)

        # 根据状态编码获取下一个和弦
        possible_next_chords = state_rel_pitch_dict[next_state]
        next_chord = possible_next_chords[0]
        if current_chord in possible_next_chords:
            # 如果当前和弦在下一个状态的可能和弦中，则以当前和弦为优先选择
            next_chord = current_chord
        predictions.append(next_chord)
    # 计算听感匹配度
    total_proba = np.sum(probas)
    match_scores = [proba / total_proba * 100 for proba in probas]

    return predictions, match_scores


# 训练HMM模型
def train_hmm(rel_pitch_seq, state_chord_seq):
    # 使用GaussianHMM初始化模型
    model = hmm.GaussianHMM(n_components=NUM_STATES, n_iter=100)

    # 生成HMM输入数据
    X = np.array(rel_pitch_seq).reshape(-1, 1)
    lengths = [len(X)]

    # 训练模型
    model.fit(X, lengths)

    # 获取模型中每个状态对应的高斯分布参数
    state_params = []
    for state_idx in range(NUM_STATES):
        start_idx, end_idx = get_state_rel_pitch_indices(state_idx, state_chord_seq)
        state_params.append(get_gaussian_params(X[start_idx: end_idx]))

    return model, state_params


# # 获取HMM模型中每个状态对应的高斯分布参数
# def get_gaussian_params(X):
#     # 使用k-means算法对数据进行聚类，确定高斯分布数量
#     kmeans = KMeans(n_clusters=NUM_GAUSSIANS, random_state=0).fit(X)
#
#     # 获取每个高斯分布的均值和协方差矩阵
#     mean_list = kmeans.cluster_centers_.ravel().tolist()
#     cov_list = []
#     for i in range(NUM_GAUSSIANS):
#         samples = X[kmeans.labels_ == i]
#         cov = np.cov(samples, rowvar=0)
#         cov_list.append(cov.tolist())
#
#     return mean_list, cov_list

def get_gaussian_params(X):
    # 使用k-means算法对数据进行聚类，确定高斯分布数量
    kmeans = KMeans(n_clusters=NUM_GAUSSIANS, random_state=0).fit(X)

    # 获取每个高斯分布的均值和协方差矩阵
    mean_list = kmeans.cluster_centers_.ravel().tolist()
    cov_list = []

    # 检查是否出现了奇异矩阵
    for i in range(NUM_GAUSSIANS):
        samples = X[kmeans.labels_ == i]
        cov = np.cov(samples, rowvar=0)

        # 处理奇异矩阵
        if np.isnan(np.sum(cov)):
            cov += np.eye(cov.shape[0]) * 0.01  # 增加噪声
            cov_list.append(cov.tolist())
        else:
            cov_list.append(cov.tolist())

    return mean_list, cov_list

# 获取状态序列中与状态对应的相对音高的起始和终止位置
def get_state_rel_pitch_indices(state_idx, state_chord_seq):
    start_idx = 0
    for i, chord in enumerate(state_chord_seq):
        if i == 0:
            continue
        if chord != state_chord_seq[i - 1]:
            start_idx = i
        if start_idx + state_idx == i:
            break
    end_idx = start_idx + 1
    for i in range(start_idx + 1, len(state_chord_seq)):
        if state_chord_seq[i] != state_chord_seq[start_idx]:
            end_idx = i
            break
    return start_idx, end_idx


# 处理输入的音乐风格和旋律，返回预测结果和听感匹配度百分比
def process_input(style, melody):
    # 读取训练好的模型和和弦状态序列
    model = pd.read_pickle(f"{style}_model.pkl")
    state_chord_seq = pd.read_pickle(f"{style}_state_chord_seq.pkl")

    # 获取状态和和弦的映射关系字典
    state_rel_pitch_dict = {}
    for state, chords in enumerate(pd.unique(state_chord_seq)):
        state_rel_pitch_dict[state] = get_rel_pitch(chords)

    # 根据输入旋律生成相对音高序列
    rel_pitch_seq = get_rel_pitch_seq(melody)

    # 训练HMM模型
    model, state_params = train_hmm(rel_pitch_seq, state_chord_seq)
    model.means_ = np.array(state_params)[:, 0, :]
    model.covars_ = np.array(state_params)[:, 1, :, :]

    # 预测下一个和弦
    current_chord = state_chord_seq[0]
    current_rel_pitch = get_rel_pitch(current_chord)
    predictions, match_scores = predict_chord(model, state_rel_pitch_dict, current_chord, current_rel_pitch)

    return predictions, match_scores


# 示例：使用模型预测下一个和弦和听感匹配度百分比
predictions, match_scores = process_input("jazz", [7, 2, 4, 0, 5, 2, 4, 0])
for i, prediction in enumerate(predictions):
    print(f"预测第{i+1}个和弦为{prediction}，听感匹配度为{match_scores[i]:.2f}%")