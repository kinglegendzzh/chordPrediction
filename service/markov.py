import random


class ChordPredictor:

    # 初始化函数，用于加载模型数据并构建马尔科夫链
    def __init__(self, style, chord_sequences, order=2):
        self.chord_progression = []  # 所有和弦的列表
        self.markov_chain = {}  # 马尔科夫链

        # 将所有和弦汇总到一个列表中
        for sequence in chord_sequences:
            self.chord_progression += sequence
        # 构建马尔科夫链
        for i in range(len(self.chord_progression) - order + 1):
            current_state = tuple(self.chord_progression[i:i + order])
            next_state = self.chord_progression[i + order] if i + order < len(self.chord_progression) else None
            if current_state in self.markov_chain:
                if next_state is not None:
                    self.markov_chain[current_state].append(next_state)
            else:
                if next_state is not None:
                    self.markov_chain[current_state] = [next_state]
                else:
                    self.markov_chain[current_state] = []
        # 记住最后一组状态和对应的下一个状态
        self.last_state = tuple(self.chord_progression[-order:])
        self.next_choice = self.markov_chain[self.last_state]
        print(f"马尔可夫链初始化完成{self.markov_chain}")

    # 预测函数，用于根据当前状态生成下一个和弦并评估其听感匹配度
    def predict_chord(self, current_chords):
        # 获取当前状态
        current_state = tuple(current_chords[-len(self.last_state):]) if len(current_chords) >= len(
            self.last_state) else tuple(current_chords)

        # 如果当前状态能够在马尔科夫链中匹配到
        if current_state in self.markov_chain:
            next_choice = self.markov_chain[current_state]
            next_chord = random.choice(next_choice) if next_choice else self.chord_progression[0]
            next_chord_prob = next_choice.count(next_chord) / len(next_choice)
        else:
            next_chord = random.choice(self.next_choice) if self.next_choice else self.chord_progression[0]
            if len(self.next_choice) == 0:
                next_chord_prob = 0
            else:
                next_chord_prob = self.next_choice.count(next_chord) / len(self.next_choice)

        # 更新最后一组状态和对应的下一个状态
        self.last_state = current_state + (next_chord,) if len(current_chords) >= len(self.last_state) else (
        next_chord,)
        self.next_choice = self.markov_chain.get(self.last_state, [])

        return next_chord, next_chord_prob