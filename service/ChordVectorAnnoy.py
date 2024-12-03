import os
import pickle
from annoy import AnnoyIndex

from utils.filePath import filePath


class ChordVectorIndex:
    def __init__(self, vector_dim=128, index_path='chord_index.ann',
                 mapping_path='id_mapping.pkl'):
        self.vector_dim = vector_dim
        self.index_path = index_path
        self.mapping_path = mapping_path

        self.index = AnnoyIndex(self.vector_dim, 'hamming')
        self.id_mapping = {}

        if os.path.exists(self.index_path) and os.path.exists(self.mapping_path):
            self.index.load(self.index_path)
            with open(self.mapping_path, 'rb') as f:
                self.id_mapping = pickle.load(f)
            self.next_id = max(self.id_mapping.keys()) + 1
            self.index.unbuild()
        else:
            self.next_id = 0

    def midi_notes_to_vector(self, midi_notes):
        """
        将 MIDI 音符序列转换为向量表示（One-Hot 编码）
        """
        vector = [0] * self.vector_dim
        for note in midi_notes:
            if 0 <= note < self.vector_dim:
                vector[note] = 1
        return vector

    def add_chord(self, chord_name, pressing_str):
        root_note, notes_str = pressing_str.split('@')
        midi_notes = list(map(int, notes_str.split(',')))
        vector = self.midi_notes_to_vector(midi_notes)
        self.index.add_item(self.next_id, vector)
        self.id_mapping[self.next_id] = {
            'chord_name': chord_name,
            'pressing_str': pressing_str,
            'midi_notes': midi_notes
        }
        self.next_id += 1

    def build_index(self, n_trees=10):
        self.index.build(n_trees)
        self.index.save(self.index_path)
        with open(self.mapping_path, 'wb') as f:
            pickle.dump(self.id_mapping, f)

    def search_chord(self, midi_notes, top_k=5):
        """
        根据给定的 MIDI 音符序列搜索最相似的和弦
        """
        vector = self.midi_notes_to_vector(midi_notes)
        ids = self.index.get_nns_by_vector(vector, top_k, include_distances=True)

        results = []
        for idx, distance in zip(ids[0], ids[1]):
            chord_info = self.id_mapping[idx]
            results.append({
                'chord_name': chord_info['chord_name'],
                'pressing_str': chord_info['pressing_str'],
                'distance': distance
            })
        return results

    def delete_chord(self, chord_name):
        """
        从索引中删除指定的和弦
        """
        ids_to_delete = [idx for idx, info in self.id_mapping.items() if info['chord_name'] == chord_name]
        for idx in ids_to_delete:
            self.index.unbuild()
            self.index.remove_item(idx)
            del self.id_mapping[idx]
        self.build_index()

    def update_chord(self, chord_name, new_pressing_str):
        """
        更新指定和弦的 MIDI 音符序列
        """
        self.delete_chord(chord_name)
        self.add_chord(chord_name, new_pressing_str)
        self.build_index()


def data_cut(index, cache_file):
    with open(cache_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('::')
            chord_name = parts[0]
            pressing_strs = parts[1:]
            for pressing_str in pressing_strs:
                index.add_chord(chord_name, pressing_str)
    index.build_index()


if __name__ == '__main__':
    # 数据割接
    index = ChordVectorIndex()

    # 导入数据
    cache_file = filePath('models/') + 'pressing_chord_mappings.cache'
    data_cut(index, cache_file)

    # 搜索示例
    search_midi_notes = [12, 16, 19]  # Cmajor 的音符序列
    results = index.search_chord(search_midi_notes, top_k=5)
    for res in results:
        print(f"Chord Name: {res['chord_name']}, Distance: {res['distance']}")
