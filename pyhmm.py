from music21 import *

# 收集和弦序列数据
chordSeqs = []

choraleList = corpus.chorales.ChoraleListRKBWV()
for i, chorale in enumerate(choraleList):
    for part in chorale.parts:
        # 设置输入和弦序列的最小长度（4个和弦）
        if len(part.getElementsByClass('Chord')) < 4:
            continue
        # 从音乐中获取和弦序列
        chordList = []
        for note in part.flat.notes:
            if isinstance(note, chord.Chord):
                chordList.append(str(note.pitchedCommonName))
        # 将和弦序列转化为二元组的列表
        for i, chord1 in enumerate(chordList[:-2]):
            chord2 = chordList[i+1]
            chord3 = chordList[i+2]
            chordSeqs.append(((chord1, chord2), chord3))

# 建立马尔科夫链模型
chain = {}
for seq in chordSeqs:
    # 使用字典构建状态转化矩阵
    if seq[0] not in chain:
        chain[seq[0]] = {}
    if seq[1] not in chain[seq[0]]:
        chain[seq[0]][seq[1]] = 0
    chain[seq[0]][seq[1]] += 1

# 预测函数
def predict(chord1, chord2):
    if (chord1, chord2) not in chain:
        return None
    # 按照概率随机选取下一个和弦
    chordDict = chain[(chord1, chord2)]
    total = sum(chordDict.values())
    rand = randint(1, total)
    for chord in chordDict:
        rand -= chordDict[chord]
        if rand <= 0:
            return chord