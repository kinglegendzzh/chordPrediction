# 创建和弦预测系统
from hmm.hmm1.ChordPredictionSystem import ChordPredictionSystem

system = ChordPredictionSystem('jazz')

# 加载训练数据
system.load_data()

# 训练模型
system.train_model()

# 预测和弦
notes_seq = [6, 5, 4]
predicted_chord = system.predict_chord(notes_seq)
print('Predicted chord for {}: {}'.format(notes_seq, predicted_chord))

# 计算听感匹配度
chord1 = 'G7'
chord2 = 'Dm7'
match_score = system.calculate_match_score(chord1, chord2)
print('Match score between {} and {}: {:.2f}'.format(chord1, chord2, match_score))