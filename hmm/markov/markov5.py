import random


class ChordPredictor:

    # 初始化函数，用于加载训练数据并构建马尔科夫链
    def __init__(self, style, chord_sequences):
        self.chord_progression = []  # 所有和弦的列表
        self.markov_chain = {}  # 马尔科夫链

        # 将所有和弦汇总到一个列表中
        for sequence in chord_sequences:
            self.chord_progression += sequence

        # 构建二阶马尔科夫链
        for i in range(len(self.chord_progression) - 2):
            current_state = (self.chord_progression[i], self.chord_progression[i + 1])
            next_state = self.chord_progression[i + 2]
            if current_state in self.markov_chain:
                self.markov_chain[current_state].append(next_state)
            else:
                self.markov_chain[current_state] = [next_state]

    # 预测函数，用于根据当前状态生成下一个和弦并评估其听感匹配度
    def predict_chord(self, current_chords):
        # 获取当前状态
        if len(current_chords) < 2:
            current_state = (current_chords[0], '')
        else:
            current_state = (current_chords[-2], current_chords[-1])

        # 从马尔科夫链中获取下一个和弦及其概率
        if current_state in self.markov_chain:
            next_chords = self.markov_chain[current_state]
            next_chord_probs = [1 / len(next_chords)] * len(next_chords)
        else:
            next_chords = self.chord_progression
            next_chord_probs = [1 / len(next_chords)] * len(next_chords)

        # 计算听感匹配度（概率）
        match_percentage = next_chord_probs[next_chords.index(next_chords)]

        return next_chords, match_percentage