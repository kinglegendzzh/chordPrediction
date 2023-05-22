
circle_of_fifths = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Db', 'Ab', 'Eb', 'Bb', 'F']

def predict_next_chord(current_chord, interval):
    # 使用 index() 方法获取当前和弦在五度圈中的索引
    index_of_current_chord = circle_of_fifths.index(current_chord)

    # 计算下一个和弦的索引，注意要处理索引超出范围的情况
    index_of_next_chord = (index_of_current_chord + interval) % len(circle_of_fifths)

    # 返回预测的下一个和弦
    return circle_of_fifths[index_of_next_chord]


# 下面是调用示例，当前和弦为 C，预测下一个二度的和弦
current_chord = 'C'
predicted_chord = predict_next_chord(current_chord, 2)
print(f"The predicted chord is {predicted_chord}")