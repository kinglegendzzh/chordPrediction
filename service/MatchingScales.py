class MatchingScale:
    # 定义音符到 MIDI 编号的映射
    NOTE_TO_MIDI = {
        'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4,
        'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9,
        'A#': 10, 'B': 11
    }
    # 定义音阶调式及其音符集合
    SCALES = {
        "Major (Ionian)": [0, 2, 4, 5, 7, 9, 11],  # 大调（爱奥尼亚）
        "Major Pentatonic": [0, 2, 4, 7, 9],  # 大调五声音阶
        "Major Blues": [0, 2, 3, 4, 7, 9],  # 大调蓝调
        "Lydian": [0, 2, 4, 6, 7, 9, 11],  # 里第亚调式
        "Mixolydian": [0, 2, 4, 5, 7, 9, 10],  # 混合里第亚调式
        "Superlocrian (Altered)": [0, 1, 3, 4, 5, 6, 8],  # 超级洛克里亚调式（变化）
        "Bebop Major": [0, 2, 4, 5, 7, 8, 9, 11],  # 比波普大调
        "Bebop Dominant": [0, 2, 4, 5, 7, 8, 9, 10],  # 比波普属音
        "Half Dim": [0, 2, 3, 5, 6, 8, 9],  # 半全减
        "Natural Minor (Aeolian)": [0, 2, 3, 5, 7, 8, 10],  # 自然小调（伊奥利亚）
        "Minor Pentatonic": [0, 3, 5, 7, 10],  # 小调五声音阶
        "Melodic Minor": [0, 2, 3, 5, 7, 9, 11],  # 旋律小调
        "Harmonic Minor": [0, 2, 3, 5, 7, 8, 11],  # 和声小调
        "Minor Blues": [0, 3, 5, 6, 7, 10],  # 小调蓝调
        "Dorian": [0, 2, 3, 5, 7, 9, 10],  # 多利安调式
        "Phrygian": [0, 1, 3, 5, 7, 8, 10],  # 弗里吉亚调式
        "Locrian": [0, 1, 3, 5, 6, 8, 10],  # 洛克里亚调式
        "Locrian #9": [0, 1, 3, 5, 6, 8, 9],  # 洛克里亚调式9
        "Bebop Melodic Minor": [0, 2, 3, 5, 7, 8, 9, 11],  # 比波普旋律小调
        "Bebop Harmonic Minor": [0, 2, 3, 5, 7, 8, 9, 11],  # 比波普和声小调
        "Full Dim": [0, 2, 3, 5, 6, 8, 9],  # 全半减
        "Southeast Asian": [0, 1, 3, 4, 5, 7, 9],  # 东南亚调式
        "Japanese": [0, 2, 5, 7, 10],  # 都节（日式）
        "Double Harmonic (Byzantine)": [0, 1, 4, 5, 7, 8, 11],  # 双和声（拜占庭）
    }

    def __init__(self, root_note, input_notes, threshold=1.0):
        self.root_note = root_note
        self.input_notes = input_notes
        self.threshold = threshold

    def find_matching_scales(self):
        # 将根音转换为 MIDI 音高类编号
        root_value = self.NOTE_TO_MIDI[self.root_note]

        # 合并所有和弦的音符并去重
        input_notes = [note for chord in self.input_notes for note in chord]
        input_pcs = list(set(note % 12 for note in input_notes))
        print(f'input_notes: {input_notes} to input_pcs: {input_pcs}')

        matching_scales = []

        for scale_name, scale_degrees in self.SCALES.items():
            # 将音阶转调到根音
            transposed_scale = [(degree + root_value) % 12 for degree in scale_degrees]
            # 计算匹配的音符数量
            matched_notes = [note for note in input_pcs if note in transposed_scale]
            match_ratio = len(matched_notes) / len(input_pcs)
            if match_ratio >= self.threshold:
                matching_scales.append((scale_name, match_ratio))

        # 按匹配度排序
        matching_scales.sort(key=lambda x: x[1], reverse=True)

        return matching_scales


if __name__ == '__main__':
    # 定义 MIDI 音符到音符名称的映射（可选，用于显示）
    MIDI_TO_NOTE = {
        0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E',
        5: 'F', 6: 'F#', 7: 'G', 8: 'G#', 9: 'A',
        10: 'A#', 11: 'B'
    }
    # 示例使用
    root_note = 'C'
    chords = [
        # [0, 4, 7],
        [2, 5, 9],
    ]  # Cmaj 和 Dm 和弦
    ms = MatchingScale(root_note, chords, threshold=0.7)
    matching_scales = ms.find_matching_scales()
    for scale_name, match_ratio in matching_scales:
        print(f"{scale_name}: 匹配度 {match_ratio:.2f}")
