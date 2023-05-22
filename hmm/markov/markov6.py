# 创建预测器
from hmm.markov.markov5 import ChordPredictor

style = 'rock'
chord_sequences = [['C', 'G', 'Am'], ['F', 'G', 'C']]
predictor = ChordPredictor(style, chord_sequences)

# 生成新的和弦进行
current_chords = ['C', 'G']
next_chords, match_percentage = predictor.predict_chord(current_chords)
print('Next Chords:', next_chords)
print('Match Percentage:', match_percentage)