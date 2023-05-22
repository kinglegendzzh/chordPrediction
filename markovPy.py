
import numpy as np


# 定义状态
class ChordState:
    def __init__(self, chord_num):
        self.chord_num = chord_num


# 估计转移概率
class MarkovChain:
    def __init__(self, chord_list, chord_seq):
        self.transitions = np.zeros((len(chord_list), len(chord_list)))
        for i in range(len(chord_seq) - 1):
            cur_state = chord_seq[i]
            next_state = chord_seq[i + 1]
            self.transitions[cur_state][next_state] += 1
        for i in range(len(chord_list)):
            row_sum = sum(self.transitions[i])
            if row_sum > 0:
                self.transitions[i] /= row_sum


# 基于概率计算和弦预测
def predict_chords(chord_list, markov_model, current_chord, num_predictions=5, threshold=0.1):
    probabilities = markov_model.transitions[current_chord]
    sorted_probabilities = sorted(enumerate(probabilities), key=lambda x: x[1], reverse=True)
    predictions = []
    for i in range(len(sorted_probabilities)):
        if sorted_probabilities[i][1] < threshold or len(predictions) >= num_predictions:
            break
        predictions.append((chord_list[sorted_probabilities[i][0]], sorted_probabilities[i][1]))
    return predictions


# 读取 MIDI 文件中的和弦
def get_chord_list(midi_file):
    pm = pretty_midi.PrettyMIDI(midi_file)
    note_seq = pm.get_chords()
    chord_list = []
    for chord in note_seq:
        if chord not in chord_list:
            chord_list.append(chord)
    return chord_list


# 将和弦转换为数字表示
def chords_to_numbers(chord_list):
    chord_dict = {}
    for i, chord in enumerate(chord_list):
        chord_dict[chord] = i
    return [chord_dict[chord] for chord in chord_list]


# 测试
def test_chord_prediction(chord_file, style):
    # 预处理
    chord_list = get_chord_list(chord_file)
    chord_seq = chords_to_numbers(chord_list)

    # 训练模型
    markov_model = MarkovChain(chord_list, chord_seq)

    # 预测输出
    current_chord = chord_seq[0]
    predictions = predict_chords(chord_list, markov_model, current_chord)
    print('Initial chord:', chord_list[current_chord])
    print('Predictions:')
    for pred in predictions:
        print(pred[0], pred[1] * 100, '%')


# 主程序
if __name__ == "__main__":
    chord_file = 'example.mid'
    style = 'jazz'
    test_chord_prediction(chord_file, style)