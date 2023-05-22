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

        # 从马尔科夫链中获取下一个和弦
        if current_state in self.markov_chain:
            next_chord = random.choice(self.markov_chain[current_state])
        else:
            next_chord = random.choice(self.chord_progression)

        # 计算听感匹配度（这里仅简单返回一个随机数）
        match_percentage = random.uniform(0, 100)

        return next_chord, match_percentage