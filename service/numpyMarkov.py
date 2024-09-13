import numpy as np
import matplotlib.pyplot as plt


class ChordPredictor:
    def __init__(self, chord_sequences, order=1):
        # 初始化预测器，order表示马尔科夫链的阶数
        self.order = order
        # 构建和弦索引字典，每个和弦对应一个唯一的整数索引
        self.chord_index = self.index_chords(chord_sequences)
        # 计算唯一和弦的数量
        self.n_chords = len(self.chord_index)
        # 初始化概率转移矩阵，大小为 (n_chords^order, n_chords)
        self.transitions = np.zeros((self.n_chords ** self.order, self.n_chords))
        # 构建转移概率矩阵
        self.build_transition_matrix(chord_sequences)

    def index_chords(self, sequences):
        """
        为每个和弦分配一个唯一的索引
        :param sequences: 和弦序列
        :return: 和弦索引字典
        """
        unique_chords = set()  # 用于存储唯一的和弦
        for seq in sequences:
            unique_chords.update(seq)  # 更新唯一和弦集合
        # 返回和弦到索引的映射字典
        self.unknown_chord_index = len(unique_chords)  # A unique index for unknown chords
        return {chord: i for i, chord in enumerate(unique_chords)}

    def build_transition_matrix(self, sequences):
        """
        根据输入的和弦序列构建概率转移矩阵
        :param sequences: 和弦序列
        """
        for seq in sequences:
            # 根据马尔科夫链阶数，构建转移概率
            for i in range(len(seq) - self.order):
                cur_state = tuple(seq[i:i + self.order])  # 当前状态（和弦组合）
                cur_state_index = self.state_to_index(cur_state)  # 当前状态的索引
                next_chord_index = self.chord_index.get(seq[i + self.order],
                                                        self.unknown_chord_index)  # 获取下一个和弦的索引，处理未知和弦
                if next_chord_index < len(self.transitions[0]):  # 确保索引不越界
                    self.transitions[cur_state_index, next_chord_index] += 1  # 计数转移

        for i in range(len(self.transitions)):
            row_sum = np.sum(self.transitions[i])
            if row_sum > 0:
                self.transitions[i] /= row_sum

        # 将每行的计数归一化为概率
        for i in range(len(self.transitions)):
            row_sum = np.sum(self.transitions[i])
            if row_sum > 0:
                self.transitions[i] /= row_sum  # 归一化处理

    def state_to_index(self, state):
        """
        将和弦状态转换为对应的索引
        :param state: 当前和弦状态
        :return: 状态的索引
        """
        index = 0
        # 根据和弦组合的每个和弦计算状态索引
        for j, chord in enumerate(state):
            # 处理未知和弦，使用默认的未知和弦索引
            chord_index = self.chord_index.get(chord, self.unknown_chord_index)  # Use the index for unknown chords
            chord_index = min(chord_index, self.n_chords - 1)  # Ensure within bounds
            index += chord_index * (self.n_chords ** (self.order - j - 1))
        index = min(index, len(self.transitions) - 1)  # Ensure final index is within bounds
        return index

    def predict_chord(self, current_chords, threshold=0.1):
        """
        根据当前和弦预测下一个和弦
        :param current_chords: 当前和弦列表
        :param threshold: 概率阈值，过滤低概率的预测结果
        :return: 预测的和弦及其概率
        """
        if len(current_chords) < self.order:
            raise ValueError("当前和弦的数量少于马尔科夫链的阶数。")

        cur_state = tuple(current_chords[-self.order:])
        cur_state_index = self.state_to_index(cur_state)
        probabilities = self.transitions[cur_state_index]
        # 过滤出概率大于阈值的和弦
        next_chords = [(list(self.chord_index.keys())[i], prob) for i, prob in enumerate(probabilities) if
                       prob > threshold]

        # 按概率降序排序并规范化概率
        next_chords = sorted(next_chords, key=lambda x: x[1], reverse=True)
        total_prob = sum(prob for _, prob in next_chords)
        next_chords = [(chord, prob / total_prob) for chord, prob in next_chords] if total_prob > 0 else []

        return next_chords

    def visualize_transition_matrix(self):
        """
        可视化概率转移矩阵并输出为图片
        """
        plt.figure(figsize=(10, 8))
        # 使用热图展示转移矩阵
        plt.imshow(self.transitions, cmap='hot', interpolation='nearest')
        plt.colorbar()  # 添加颜色条
        plt.title("Transition Matrix Heatmap")
        plt.xlabel("Next Chord Index")
        plt.ylabel("Current State Index")
        plt.show()

    def transition_matrix_to_string(self):
        """
        将概率转移矩阵转换为字符串形式
        :return: 转移矩阵的字符串
        """
        matrix_str = np.array2string(self.transitions, precision=2, separator=', ')
        return matrix_str


if __name__ == '__main__':
    chord_sequences = [
        ['C', 'Am', 'F', 'G', 'C'],
        ['Am', 'F', 'C', 'G', 'Am']
    ]
    predictor = ChordPredictor(chord_sequences, order=1)
    current_chords = ['C', 'Dsus']  # 测试包含未知和弦的情况
    try:
        next_chords = predictor.predict_chord(current_chords, threshold=0.1)
        # 打印预测结果
        print('Predictions:')
        for chord, prob in next_chords:
            print(f"{chord}: {prob:.2f}")
    except IndexError as e:
        print(f"IndexError: {e}")

    # 可视化转移矩阵
    predictor.visualize_transition_matrix()

    # 打印转移矩阵的字符串形式
    print("\nTransition Matrix as String:")
    print(predictor.transition_matrix_to_string())
