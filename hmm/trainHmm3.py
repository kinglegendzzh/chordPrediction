import numpy as np
import pandas as pd

# 定义和弦
chords = ["C", "F", "G"]

# 定义符号音高
pitch_mapping = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11, "N": None}

# 生成一个音符序列
def gen_melody(length):
    return np.random.randint(60, 72, size=length)

# 生成一个和弦序列
def gen_chord(melody, chord_len):
    chord_seq = []
    for i in range(0, len(melody), chord_len):
        pitch = pitch_mapping[np.random.choice(chords)]
        chord = [pitch] * chord_len
        chord_seq.extend(chord)
    chord_seq = chord_seq[:len(melody)]
    return chord_seq

# 生成多个样例数据
data = []
n_samples = 2
for i in range(n_samples):
    # 生成一个长度为10的旋律序列
    melody = gen_melody(10)

    # 根据旋律生成和弦序列
    chord_len = 1
    chord_seq = gen_chord(melody, chord_len)

    # 将旋律和和弦序列保存到DataFrame中
    df = pd.DataFrame({"melody": melody, "chord": chord_seq})
    data.append(df)

# 将所有样例数据合并成一个DataFrame
data = pd.concat(data)

# 将DataFrame保存为CSV文件
data.to_csv("training_data.csv", index=False)