import numpy as np
from hmmlearn import hmm
from scipy.spatial.distance import cosine


class ChordPredictionSystem:
    def __init__(self, style):
        self.style = style
        self.chords = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        self.states = list(range(len(self.chords)))
        self.notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        self.start_prob, self.trans_prob, self.emit_prob = None, None, None
        self.model = None
        self.chord_to_int = {chord: i for i, chord in enumerate(self.chords)}

        self.hidden_states = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        self.observation_states = [0, 1, 2, 3, 4, 5, 6]
        self.num_states = len(self.hidden_states)
        self.num_obs = len(self.observation_states)

        # 初始化计数矩阵
        self.start_counts = np.zeros(self.num_states)
        self.trans_counts = np.zeros((self.num_states, self.num_states))
        self.emit_counts = np.zeros((self.num_states, self.num_obs))

    def load_data(self):
        # 此处需要你根据不同的风格，读取并生成相应的训练数据
        # 以jazz为例，此处我们使用以下数据
        if self.style == 'jazz':
            self.training_data = np.array([[0, 1, 2, 3],
                                           [0, 1, 3, 4],
                                           [2, 3, 4, 5],
                                           [0, 2, 4, 5],
                                           [1, 3, 5, 6]])

        else:
            self.training_data = np.array([[0, 1, 2, 3],
                                           [0, 2, 4, 5],
                                           [1, 3, 5, 6],
                                           [1, 2, 4, 6],
                                           [0, 3, 4, 5]])
        # 在水平方向上翻转
        flipped_horizontal = np.fliplr(self.training_data)

        # 在垂直方向上翻转
        flipped_vertical = np.flipud(self.training_data)

        # 将翻转后的数据加入训练数据集
        self.training_data = np.concatenate((self.training_data, flipped_horizontal, flipped_vertical))

        # 添加随机高斯噪声
        noisy_data = []
        for i in range(len(self.training_data)):
            noisy_img = self.training_data[i].reshape(2, 2)
            mean = 0
            var = 10
            sigma = var ** 0.5
            gaussian = np.random.normal(mean, sigma, (2, 2))
            noisy_img = noisy_img + gaussian
            # 将浮点数转换为整数
            noisy_img = noisy_img.astype(int)
            noisy_data.append(noisy_img.flatten())

        noisy_data = np.array(noisy_data)

        # 将噪声数据加入训练数据集
        self.training_data = np.concatenate((self.training_data, noisy_data))

    def train_model(self):
        # 计算初始概率矩阵
        self.start_prob = np.ones(len(self.states)) / len(self.states)

        # 计算转移概率矩阵
        trans_counts = np.zeros((len(self.states), len(self.states)))
        for seq in self.training_data:
            for i in range(len(seq) - 1):
                trans_counts[seq[i], seq[i + 1]] += 1
        self.trans_prob = trans_counts / np.maximum(1, trans_counts.sum(axis=1, keepdims=True))

        # 计算发射概率矩阵
        emit_counts = np.zeros((len(self.states), len(self.notes)))
        for seq in self.training_data:
            for i in range(len(seq)):
                emit_counts[seq[i], i] += 1
        self.emit_prob = emit_counts / np.maximum(1, emit_counts.sum(axis=1, keepdims=True))

        # 训练模型
        self.model = hmm.MultinomialHMM(n_components=len(self.states), init_params='', params='ste')
        self.model.startprob_ = self.start_prob
        self.model.transmat_ = self.trans_prob
        self.model.emissionprob_ = self.emit_prob
        self.model.fit(self.training_data)

    def predict_chord(self, notes_seq):
        # 使用模型预测和弦
        notes_seq_int = [self.chord_to_int.get(note, -1) for note in notes_seq]
        predicted_chord = self.model.predict([notes_seq_int])[0]
        return self.chords[predicted_chord]

    def calculate_match_score(self, chord1, chord2):
        # 根据和弦中音的余弦相似度计算听感匹配度
        # 此处可以根据需要改进算法
        notes_vec1 = np.zeros(len(self.notes))
        for note in chord1:
            notes_vec1[self.notes.index(note)] = 1
        notes_vec2 = np.zeros(len(self.notes))
        for note in chord2:
            notes_vec2[self.notes.index(note)] = 1
        match_score = 1 - cosine(notes_vec1, notes_vec2)
        return match_score