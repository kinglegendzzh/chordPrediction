import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

# 准备数据：和弦序列
chord_seq = ['C', 'G', 'Am', 'F', 'C', 'G', 'F', 'G', 'C']

# 将和弦序列转换为相对音高序列
rel_pitch_seq = [0, 7, 9, 5, 0, 7, 5, 7, 0]

# 对相对音高序列进行聚类并划分为状态序列，假设有3个状态
kmeans = KMeans(n_clusters=3, random_state=0).fit(np.array(rel_pitch_seq).reshape(-1, 1))
state_seq = kmeans.labels_.tolist()

# 将状态序列和相对音高序列进行对应
state_rel_pitch_dict = {0: 'C', 1: 'G', 2: 'Am'}
state_chord_seq = [state_rel_pitch_dict[state] for state in state_seq]
print(state_chord_seq)  # ['C', 'G', 'Am', 'G', 'C', 'G', 'G', 'G', 'C']