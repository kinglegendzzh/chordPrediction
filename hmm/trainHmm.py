from numpy import NAN
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from hmmlearn import hmm

from hmm.usingHmm import get_rel_pitch_seq, NUM_STATES, train_hmm


# 将和弦序列转化为状态序列
def chord_seq_to_state_seq(chord_seq):
    code_dict = {}
    next_code = 0
    state_seq = []
    for chord in chord_seq:
        if chord not in code_dict:
            code_dict[chord] = next_code
            next_code += 1
        state_seq.append(code_dict[chord])
    return state_seq, code_dict


# 将相对音高序列分为多个状态
def rel_pitch_seq_to_state_seq(rel_pitch_seq, num_states):
    state_seq = []
    state_size = len(rel_pitch_seq) // num_states
    for i, pitch in enumerate(rel_pitch_seq):
        state_seq.append(i // state_size)
    return state_seq


# 获取每个状态对应的和弦编码集合
def get_state_code_set(state_seq, chord_seq):
    state_code_set_dict = {}
    for state, chord_code in zip(state_seq, chord_seq):
        if state not in state_code_set_dict:
            state_code_set_dict[state] = set()
        state_code_set_dict[state].add(chord_code)
    for _, code_set in state_code_set_dict.items():
        if len(code_set) > 1:
            # 如果同一状态下有多个编码，仅保留最频繁出现的编码
            code_freq_dict = {}
            for code in code_set:
                code_freq_dict[code] = chord_seq.count(code)
            freq_code = max(code_freq_dict, key=code_freq_dict.get)
            state_code_set_dict[_] = {freq_code}

    return state_code_set_dict


# 处理训练数据，返回模型和状态序列
def process_training_data(style, melody, chords):
    # 将和弦序列转化为状态序列
    chord_seq = [chord[0] for chord in chords]
    state_seq, code_dict = chord_seq_to_state_seq(chord_seq)

    # 将旋律序列转化为相对音高序列
    rel_pitch_seq = get_rel_pitch_seq(melody)

    # 将相对音高序列转化为状态序列
    state_seq = rel_pitch_seq_to_state_seq(rel_pitch_seq, NUM_STATES)

    # 将编码集合保存至本地
    state_code_set_dict = get_state_code_set(state_seq, chord_seq)
    pd.to_pickle(state_code_set_dict, f"{style}_state_code_set_dict.pkl")

    # 训练HMM模型
    model, state_params = train_hmm(rel_pitch_seq, state_seq)
    print("shape:" + str(np.array(state_params).shape))
    model.means_ = np.array(state_params)[:, 0, :]
    print(state_params)
    model.covars_ = np.array(state_params)[:, 1, :]

    # 保存模型至本地
    pd.to_pickle(model, f"{style}_model.pkl")
    pd.to_pickle(state_seq, f"{style}_state_chord_seq.pkl")

#模型用例
style = "jazz"
melody = [60,63,68,67,66,63,62,60,63,65,62,60,63,68,67,66,63,62,60,63,65,62,60,58,62,62,62,65,68
,67,65,63,63,63,68,70,68,67,63,60,63,65,68,70,68,68,65,63,60,63,62,60,58,60,63,67,65,65,63
,60,63,68,67,66,63,62,60,63,65,62,60,63,68,67,66,63,62,60,63,65,62,60,58,62,62,62,65,68
,67,65,63,63,63,68,70,68,67,63,60,63,65,68,70,68,68,65,63,60,63,62,60,58,60,63,67,65,65,63]
chords = ["C","Dm7","G7","C","F",""F",m","C","G7","C","Dm7","G7","C","F",""F",m","C","G7",
"C","Dm7","G7","C","F",""F",m","C","G7","C","Dm7","G7","C","F",""F",m","C","G7",
"C","Dm7","G7","C","F",""F",m","C","G7","C","Dm7","G7","C","F",""F",m","C","G7",
"C","Dm7","G7","C","F",""F",m","C","G7","C","Dm7","G7","C","F","G7","C"]
process_training_data(style, melody, chords)