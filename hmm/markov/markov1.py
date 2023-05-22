import numpy as np
from collections import defaultdict

# 定义多阶马尔科夫链模型类
class MarkovChain(object):
    def __init__(self, order):
        self.order = order
        self.transition_dict = defaultdict(list)
        self.count_dict = defaultdict(int)

    # 将和弦序列切割成多个状态，并统计状态和转移出现的次数
    def fit(self, seq):
        state = [''] * self.order
        for chord in seq:
            self.count_dict[tuple(state)] += 1
            self.transition_dict[tuple(state)].append(chord)
            state.pop(0)
            state.append(chord)

    # 根据当前状态预测下一个和弦
    def predict(self, state):
        count = self.count_dict.get(tuple(state), 0)
        chords = self.transition_dict.get(tuple(state), [])
        if count == 0:
            return np.random.choice(['C', 'D', 'E', 'F', 'G', 'A', 'B'])
        else:
            return np.random.choice(chords)

# 定义训练数据集
jazz = ['C', 'Am', 'Dm', 'G7', 'C', 'Am', 'Dm', 'G7',
        'C', 'Am', 'Dm', 'G7', 'G', 'E7', 'Am', 'Dm',
        'G7', 'C', 'Am', 'Dm', 'G7', 'C', 'F', 'C', 'G',
        'C', 'Am', 'Dm', 'G7', 'C', 'Am', 'Dm', 'G7']

rock = ['C', 'G', 'Am', 'F', 'C', 'G', 'Am', 'F',
        'C', 'G', 'Am', 'F', 'G', 'D', 'Am', 'F',
        'G', 'C', 'G', 'Am', 'F', 'C', 'F', 'C', 'G',
        'C', 'G', 'Am', 'F', 'C', 'G', 'Am', 'F']

# 训练多个马尔科夫链模型，每个模型对应着一个音乐风格
jazz_model = MarkovChain(order=1)
jazz_model.fit(jazz)

rock_model = MarkovChain(order=1)
rock_model.fit(rock)

# 定义测试数据集的初始状态
state = ['C']

# 分别使用不同的模型根据初始状态预测5个和弦
for i in range(5):
    chord1 = jazz_model.predict(state)
    chord2 = rock_model.predict(state)
    print(f"Jazz Model Predicts: {chord1}, Rock Model Predicts: {chord2}")
    state.pop(0)
    state.append(chord1)
