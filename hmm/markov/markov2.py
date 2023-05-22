import random

# 定义和弦列表和初始三个和弦
chord_progression = ['C', 'Am', 'F', 'G', 'Em', 'Dm']
current_chords = ['Dm', 'G', 'C']

# 定义三阶马尔科夫链
markov_chain = {}
for i in range(len(chord_progression) - 2):
    current_state = (chord_progression[i], chord_progression[i+1], chord_progression[i+2])
    next_state = chord_progression[i+3]
    if current_state in markov_chain:
        markov_chain[current_state].append(next_state)
    else:
        markov_chain[current_state] = [next_state]

# 根据马尔科夫链生成和弦进行
for i in range(10):
    # 获取当前和弦
    current_state = tuple(current_chords[-3:])
    # 从马尔科夫链中随机选择下一个和弦
    next_chord = random.choice(markov_chain[current_state])
    # 将下一个和弦添加到当前和弦序列中
    current_chords.append(next_chord)

print(current_chords)