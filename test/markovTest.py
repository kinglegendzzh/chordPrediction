# 创建预测器
from service.markov import ChordPredictor

style = 'rock'
chord_sequences = [['C', 'G', 'Am'], ['F', 'G', 'C']]
predictor = ChordPredictor(style, chord_sequences)

# 生成新的和弦进行
current_chords = ['C', 'G']
next_chord, next_chord_prob = predictor.predict_chord(current_chords)
print('预测和弦:', next_chord)
print('匹配度:', next_chord_prob)

# 定义训练数据集
jazzTest = ['C', 'Am', 'Dm', 'G7', 'C', 'Am', 'Dm', 'G7',
        'C', 'Am', 'Dm', 'G7', 'G', 'E7', 'Am', 'Dm',
        'G7', 'C', 'Am', 'Dm', 'G7', 'C', 'F', 'C', 'G',
        'C', 'Am', 'Dm', 'G7', 'C', 'Am', 'Dm', 'G7']

rockTest = ['C', 'G', 'Am', 'F', 'C', 'G', 'Am', 'F',
        'C', 'G', 'Am', 'F', 'G', 'D', 'Am', 'F',
        'G', 'C', 'G', 'Am', 'F', 'C', 'F', 'C', 'G',
        'C', 'G', 'Am', 'F', 'C', 'G', 'Am', 'F']

style = 'Tests'
chord_sequences = [jazzTest, rockTest]
predictor = ChordPredictor(style, chord_sequences, order=3)

# 生成新的和弦进行
current_chords = ['C', 'Am', 'Dm']
next_chord, next_chord_prob = predictor.predict_chord(current_chords)
print('预测和弦:', next_chord)
print('匹配度:', next_chord_prob)

