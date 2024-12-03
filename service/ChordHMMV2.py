import time

import numpy as np
import matplotlib.pyplot as plt
import pickle  # 导入pickle模块用于保存和加载模型

from utils.filePath import filePath


class ChordHMM:
    def __init__(self, chord_sequences=None, emotion_labels=None, style_labels=None, n_states=3):
        """
        初始化HMM模型，用于和弦序列预测，支持情绪标签和风格标签作为上下文。
        :param chord_sequences: 和弦序列的列表，每个序列是一个和弦列表
        :param emotion_labels: 每个序列对应的情绪标签列表（列表的列表，支持多个情绪标签）
        :param style_labels: 每个序列对应的风格标签列表（单个标签）
        :param n_states: HMM的隐藏状态数
        """
        self.n_states = n_states  # 隐藏状态数
        if chord_sequences is not None:
            self.chord_sequences = chord_sequences
            self.emotion_labels = emotion_labels
            self.style_labels = style_labels
            self.chord_index = self.index_chords(chord_sequences)  # 为每个和弦分配唯一索引
            self.n_chords = len(self.chord_index)  # 不同和弦的数量
            self.index_chord = {i: chord for chord, i in self.chord_index.items()}  # 索引到和弦的映射
            self.contexts = self.build_contexts(emotion_labels, style_labels)  # 构建上下文
            self.context_index = {ctx: i for i, ctx in enumerate(self.contexts)}
            self.n_contexts = len(self.contexts)
            self.initialize_parameters()  # 初始化HMM参数
        else:
            self.chord_sequences = []
            self.emotion_labels = []
            self.style_labels = []
            self.chord_index = {}
            self.n_chords = 0
            self.index_chord = {}
            self.context_index = {}
            self.n_contexts = 0
            # A, B, pi将在加载模型时被设置

    def index_chords(self, sequences):
        """
        为每个和弦分配唯一的索引。
        :param sequences: 和弦序列的列表
        :return: 和弦到索引的映射字典
        """
        unique_chords = set()
        for seq in sequences:
            unique_chords.update(seq)
        return {chord: i for i, chord in enumerate(unique_chords)}

    def build_contexts(self, emotion_labels, style_labels):
        """
        构建上下文（情绪标签和风格标签的组合）。
        :param emotion_labels: 情绪标签列表的列表
        :param style_labels: 风格标签列表
        :return: 上下文的集合
        """
        contexts = set()
        for emotions, style in zip(emotion_labels, style_labels):
            # 将情绪标签列表转换为元组，以便哈希
            emotions = tuple(sorted(emotions))
            context = (emotions, style)
            contexts.add(context)
        return list(contexts)

    def initialize_parameters(self):
        """
        随机初始化HMM参数：状态转移矩阵A，发射矩阵B（上下文依赖），初始状态概率pi。
        """
        self.A = np.random.rand(self.n_states, self.n_states)
        self.A /= self.A.sum(axis=1, keepdims=True)  # 行归一化

        # 发射矩阵B，现在是三维的 (n_states, n_chords, n_contexts)
        self.B = np.random.rand(self.n_states, self.n_chords, self.n_contexts)
        self.B /= self.B.sum(axis=1, keepdims=True)  # 对和弦维度归一化

        self.pi = np.random.rand(self.n_states)
        self.pi /= self.pi.sum()  # 归一化

    def chords_to_indices(self, sequence):
        """
        将和弦序列转换为对应的索引序列。
        :param sequence: 和弦列表
        :return: 和弦索引列表
        """
        return [self.chord_index.get(chord, -1) for chord in sequence]

    def context_to_index(self, emotions, style):
        """
        将情绪标签和风格标签转换为上下文索引。
        :param emotions: 情绪标签列表
        :param style: 风格标签
        :return: 上下文索引
        """
        emotions = tuple(sorted(emotions))
        context = (emotions, style)
        return self.context_index.get(context, -1)

    def forward(self, O, context_index, A, B, pi):
        """
        前向算法，计算alpha值。
        :param O: 观察序列（和弦索引列表）
        :param context_index: 上下文索引
        :param A: 状态转移矩阵
        :param B: 发射矩阵
        :param pi: 初始状态概率
        :return: Alpha矩阵
        """
        T = len(O)
        N = self.n_states
        alpha = np.zeros((T, N))
        b = B[:, O[0], context_index]
        alpha[0] = pi * b
        for t in range(1, T):
            for j in range(N):
                b = B[j, O[t], context_index]
                alpha[t, j] = b * np.sum(alpha[t - 1] * A[:, j])
        return alpha

    def backward(self, O, context_index, A, B):
        """
        后向算法，计算beta值。
        :param O: 观察序列
        :param context_index: 上下文索引
        :param A: 状态转移矩阵
        :param B: 发射矩阵
        :return: Beta矩阵
        """
        T = len(O)
        N = self.n_states
        beta = np.zeros((T, N))
        beta[T - 1] = np.ones(N)
        for t in range(T - 2, -1, -1):
            for i in range(N):
                b = B[:, O[t + 1], context_index]
                beta[t, i] = np.sum(beta[t + 1] * A[i, :] * b)
        return beta

    def baum_welch(self, max_iters=10):
        """
        Baum-Welch算法，用于训练HMM参数，考虑上下文依赖。
        :param max_iters: 最大迭代次数
        """
        N = self.n_states
        M = self.n_chords

        sequences = [self.chords_to_indices(seq) for seq in self.chord_sequences]

        for iteration in range(max_iters):
            A_num = np.zeros((N, N))
            A_den = np.zeros(N)
            B_num = np.zeros((N, M, self.n_contexts))
            B_den = np.zeros((N, self.n_contexts))

            pi_sum = np.zeros(N)

            for O, emotions, style in zip(sequences, self.emotion_labels, self.style_labels):
                context_idx = self.context_to_index(emotions, style)
                if context_idx == -1:
                    continue  # 跳过未知上下文

                T = len(O)
                alpha = self.forward(O, context_idx, self.A, self.B, self.pi)
                beta = self.backward(O, context_idx, self.A, self.B)
                xi = np.zeros((T - 1, N, N))
                gamma = np.zeros((T, N))

                # 计算xi和gamma
                for t in range(T - 1):
                    denom = np.sum(alpha[t] * beta[t])
                    for i in range(N):
                        gamma[t, i] = alpha[t, i] * beta[t, i] / denom
                        b = self.B[:, O[t + 1], context_idx]
                        xi[t, i, :] = alpha[t, i] * self.A[i, :] * b * beta[t + 1] / denom

                gamma[T - 1] = alpha[T - 1] * beta[T - 1] / np.sum(alpha[T - 1] * beta[T - 1])

                # 累积A和B的更新量
                A_num += np.sum(xi, axis=0)
                A_den += np.sum(gamma[:-1], axis=0)
                for t in range(T):
                    B_num[:, O[t], context_idx] += gamma[t]
                B_den[:, context_idx] += np.sum(gamma, axis=0)

                pi_sum += gamma[0]

            # 更新模型参数
            self.A = A_num / A_den[:, None]
            # 防止除零
            self.A = np.nan_to_num(self.A)
            self.B = B_num / B_den[:, None, :]
            self.B = np.nan_to_num(self.B)
            self.pi = pi_sum / len(sequences)

            # 防止数值问题，进行归一化
            self.A /= self.A.sum(axis=1, keepdims=True)
            self.B /= self.B.sum(axis=1, keepdims=True)
            self.pi /= self.pi.sum()

    def viterbi(self, O, context_index):
        """
        Viterbi算法，寻找最可能的隐藏状态序列，考虑上下文。
        :param O: 观察序列
        :param context_index: 上下文索引
        :return: 最可能的状态序列
        """
        T = len(O)
        N = self.n_states
        delta = np.zeros((T, N))
        psi = np.zeros((T, N), dtype=int)

        delta[0] = self.pi * self.B[:, O[0], context_index]
        for t in range(1, T):
            for j in range(N):
                temp = delta[t - 1] * self.A[:, j]
                psi[t, j] = np.argmax(temp)
                delta[t, j] = np.max(temp) * self.B[j, O[t], context_index]

        states = np.zeros(T, dtype=int)
        states[T - 1] = np.argmax(delta[T - 1])
        for t in range(T - 2, -1, -1):
            states[t] = psi[t + 1, states[t + 1]]

        return states

    def predict_next_chords(self, current_sequence, emotions, style, threshold=0.1):
        """
        根据当前和弦序列预测下一个和弦，支持情绪标签和风格标签。
        :param current_sequence: 当前和弦列表
        :param emotions: 情绪标签列表
        :param style: 风格标签
        :param threshold: 概率阈值，控制预测结果的数量
        :return: 预测的和弦及其匹配概率的列表
        """
        # 将和弦转换为索引
        O = self.chords_to_indices(current_sequence)
        # 如果序列中有未知和弦，返回None
        if -1 in O:
            print("当前序列包含未知和弦，无法预测。")
            return None
        context_idx = self.context_to_index(emotions, style)
        if context_idx == -1:
            print("未知的情绪或风格标签，无法预测。")
            return None
        # 获取最可能的隐藏状态序列
        states = self.viterbi(O, context_idx)
        last_state = states[-1]
        # 获取可能的下一个和弦及其概率
        next_chord_probs = self.B[last_state, :, context_idx]
        # 过滤概率高于阈值的和弦
        chord_indices = np.where(next_chord_probs >= threshold)[0]
        chords_probs = [(self.index_chord[i], next_chord_probs[i]) for i in chord_indices]
        # 按概率降序排序
        chords_probs.sort(key=lambda x: x[1], reverse=True)
        return chords_probs

    def generate_chord_sequence(self, length, emotions, style):
        """
        使用训练好的HMM生成和弦序列，支持情绪标签和风格标签。
        :param length: 要生成的序列长度
        :param emotions: 情绪标签列表
        :param style: 风格标签
        :return: 生成的和弦序列
        """
        context_idx = self.context_to_index(emotions, style)
        if context_idx == -1:
            print("未知的情绪或风格标签，无法生成序列。")
            return None

        states = []
        observations = []

        state = np.random.choice(self.n_states, p=self.pi)
        for _ in range(length):
            states.append(state)
            chord_probs = self.B[state, :, context_idx]
            chord_probs /= chord_probs.sum()  # 归一化
            chord = np.random.choice(self.n_chords, p=chord_probs)
            observations.append(chord)
            state_probs = self.A[state]
            state = np.random.choice(self.n_states, p=state_probs)

        chords = [self.index_chord[chord] for chord in observations]
        return chords

    def visualize_emission_matrix(self):
        """
        可视化发射矩阵B（仅针对单个上下文）。
        """
        # 选择第一个上下文进行可视化
        if self.n_contexts == 0:
            print("没有可视化的数据。")
            return
        plt.figure(figsize=(10, 8))
        plt.imshow(self.B[:, :, 0], cmap='hot', interpolation='nearest')
        plt.colorbar()
        plt.title("Emission Matrix Heatmap (Context 0)")
        plt.xlabel("Chord Index")
        plt.ylabel("Hidden State Index")
        plt.show()

    def print_model_parameters(self):
        """
        打印HMM的参数。
        """
        print("状态转移矩阵 (A):")
        print(self.A)
        print("\n发射矩阵 (B):")
        print(self.B)
        print("\n初始状态概率 (pi):")
        print(self.pi)

    def save_model(self, filepath):
        """
        将模型参数保存到文件。
        :param filepath: 保存模型的文件路径
        """
        model_data = {
            'A': self.A,
            'B': self.B,
            'pi': self.pi,
            'chord_index': self.chord_index,
            'n_states': self.n_states,
            'n_chords': self.n_chords,
            'index_chord': self.index_chord,
            'context_index': self.context_index,
            'contexts': self.contexts
        }
        with open(filePath('models/') + filepath, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"模型已保存到 {filepath}")

    def load_model(self, filepath):
        """
        从文件加载模型参数。
        :param filepath: 模型文件的路径
        """
        with open(filePath('models/') + filepath, 'rb') as f:
            model_data = pickle.load(f)
        self.A = model_data['A']
        self.B = model_data['B']
        self.pi = model_data['pi']
        self.chord_index = model_data['chord_index']
        self.n_states = model_data['n_states']
        self.n_chords = model_data['n_chords']
        self.index_chord = model_data['index_chord']
        self.context_index = model_data['context_index']
        self.contexts = model_data['contexts']
        print(f"模型已从 {filepath} 加载")


if __name__ == '__main__':
    # 示例和弦序列，每个序列是一个和弦列表
    chord_sequences = [
        ['Cmajor', 'Gmajor/B', 'Aminor/C', 'Cmajor', 'Eminor/B', 'Bdim', 'A#major', 'Dminor/A'],
        ['Aminor', 'Fmajor', 'Cmajor', 'Gmajor', 'Aminor'],
        ['Fmajor', 'Cmajor', 'Gmajor', 'Cmajor'],
        ['Dminor', 'Gmajor', 'Cmajor', 'Fmajor'],
        ['Cmajor', 'Aminor', 'Dminor', 'Gmajor', 'Cmajor']
    ]

    # 对应的情绪标签列表，每个序列对应一个情绪标签列表
    emotion_labels = [
        ['happy', 'relaxed'],
        ['sad', 'melancholic'],
        ['happy'],
        ['energetic'],
        ['happy', 'uplifting']
    ]

    # 对应的风格标签列表，每个序列对应一个风格标签（单个）
    style_labels = [
        'pop',
        'folk',
        'pop',
        'rock',
        'pop'
    ]

    # 创建HMM实例，设置隐藏状态数为3
    hmm = ChordHMM(chord_sequences, emotion_labels, style_labels, n_states=3)

    # 使用Baum-Welch算法训练HMM
    hmm.baum_welch(max_iters=20)

    # 保存模型到文件
    current = str(time.time())
    model_filepath = f'chord_hmm_model_v2_test_{current}.pk'
    # model_filepath = 'chord_hmm_model_v2_test_1733125030.687974.pk'
    hmm.save_model(model_filepath)

    # 预测时，加载模型而无需重新训练
    # 创建一个新的HMM实例
    hmm_loaded = ChordHMM()
    hmm_loaded.load_model(model_filepath)

    # 根据当前和弦序列预测下一个和弦
    current_sequence = ['Cmajor', 'Gmajor/B', 'Aminor/C']
    emotions = ['happy', 'relaxed']
    style = 'pop'
    print(f"当前和弦序列: {current_sequence}")
    predicted_chords = hmm_loaded.predict_next_chords(current_sequence, emotions, style, threshold=0.05)
    if predicted_chords:
        print("预测的下一个和弦及其匹配概率:")
        for chord, prob in predicted_chords:
            print(f"{chord}: {prob:.4f}")

    # 生成新的和弦序列
    generated_sequence = hmm_loaded.generate_chord_sequence(length=8, emotions=emotions, style=style)
    print(f"\n生成的和弦序列: {generated_sequence}")

    # 可视化发射矩阵
    hmm_loaded.visualize_emission_matrix()

    # 打印模型参数（可选）
    # hmm_loaded.print_model_parameters()
