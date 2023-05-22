import pandas as pd
import numpy as np
from hmmlearn import hmm

# from hmm.usingHmm import get_rel_pitch

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
    return [CHORD_CODE_MAP[chord] for chord in str(chord_code).split(',')]


def read_data(filename):
    # 读取训练数据
    data = pd.read_csv(filename)
    # 将和弦的名称转成相对音高
    data["chord"] = data["chord"].apply(get_rel_pitch)
    return data


def train_test_split(data, test_ratio=0.2):
    # 拆分训练集和验证集
    data_len = len(data)
    test_len = int(data_len * test_ratio)
    train_len = data_len - test_len
    train_data = data.iloc[:train_len, :]
    test_data = data.iloc[train_len:, :]
    return train_data, test_data


def train_hmm(X_train, y_train, n_components=4, n_iter=1000, covariance_type="diag"):
    # 训练HMM模型
    model = hmm.GaussianHMM(n_components=n_components, covariance_type=covariance_type, n_iter=n_iter, verbose=True)
    model.fit(X_train)

    # 获取每个状态的相关参数
    state_params = []
    for i in range(n_components):
        mean = model.means_[i]
        covar = model.covars_[i]
        state_params.append([mean, covar])

    style = "train"
    # 保存模型
    pd.to_pickle(model, f"{style}_model.pkl")
    pd.to_pickle(model.state_sequence, f"{style}_state_chord_seq.pkl")

    return model, state_params


# 示例：训练模型并对其进行评估
data = read_data("training_data.csv")
train_data, test_data = train_test_split(data)
X_train = np.vstack(train_data["melody"])
y_train = train_data["chord"]
model, _ = train_hmm(X_train, y_train)
X_test = np.vstack(test_data["melody"])
y_test = test_data["chord"]
score = model.score(X_test)
print(f"模型评估得分为{score:.2f}")