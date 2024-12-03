import os
import pickle
import numpy as np
import faiss

from utils.filePath import filePath


class ChordVectorIndex:
    def __init__(self, vector_dim=128, index_path='chord_index.faiss', mapping_path='id_mapping.pkl'):
        self.vector_dim = vector_dim
        self.index_path = index_path
        self.mapping_path = mapping_path

        # 初始化索引
        self.index = None

        # 用于存储内部 ID 与和弦信息的映射
        self.id_mapping = {}

        # 加载已有的索引和映射
        if os.path.exists(self.index_path) and os.path.exists(self.mapping_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.mapping_path, 'rb') as f:
                self.id_mapping = pickle.load(f)
            self.next_id = max(self.id_mapping.keys()) + 1
        else:
            # 使用 L2 距离的平面索引
            self.index = faiss.IndexFlatL2(self.vector_dim)
            self.next_id = 0

    def midi_notes_to_vector(self, midi_notes):
        """
        将 MIDI 音符序列转换为向量表示（One-Hot 编码）
        """
        vector = np.zeros(self.vector_dim, dtype='float32')
        for note in midi_notes:
            if 0 <= note < self.vector_dim:
                vector[note] = 1.0
        return vector

    def add_chord(self, chord_name, pressing_str):
        """
        添加和弦到索引中
        """
        # 解析 pressing_str，提取 MIDI 音符序列
        # 格式示例：C2@12,16,19
        root_note, notes_str = pressing_str.split('@')
        midi_notes = list(map(int, notes_str.split(',')))

        # 将 MIDI 音符序列转换为向量
        vector = self.midi_notes_to_vector(midi_notes)

        # 获取当前索引的总数，作为新向量的 ID
        vector_id = self.index.ntotal

        # 添加到索引中
        self.index.add(np.array([vector]))

        # 更新映射
        self.id_mapping[vector_id] = {
            'chord_name': chord_name,
            'pressing_str': pressing_str,
            'midi_notes': midi_notes
        }

        self.next_id = vector_id + 1

    def save_index(self):
        """
        保存索引和映射
        """
        faiss.write_index(self.index, self.index_path)
        with open(self.mapping_path, 'wb') as f:
            pickle.dump(self.id_mapping, f)

    def search_chord(self, midi_notes, top_k=5):
        """
        根据给定的 MIDI 音符序列搜索最相似的和弦
        """
        vector = self.midi_notes_to_vector(midi_notes)
        vector = np.array([vector], dtype='float32')

        distances, indices = self.index.search(vector, top_k)

        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx == -1:
                continue
            chord_info = self.id_mapping.get(idx)
            if chord_info:
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
        # FAISS 的索引不支持直接删除，需要重建索引
        vectors = []
        new_id_mapping = {}
        new_index = 0

        for idx, info in self.id_mapping.items():
            if info['chord_name'] != chord_name:
                vector = self.midi_notes_to_vector(info['midi_notes'])
                vectors.append(vector)
                new_id_mapping[new_index] = info
                new_index += 1

        # 重置索引和映射
        self.index = faiss.IndexFlatL2(self.vector_dim)
        self.id_mapping = new_id_mapping
        self.next_id = new_index

        # 重新添加剩余的向量
        if vectors:
            self.index.add(np.array(vectors, dtype='float32'))

        # 保存索引
        self.save_index()

    def update_chord(self, chord_name, new_pressing_str):
        """
        更新指定和弦的 MIDI 音符序列
        """
        self.delete_chord(chord_name)
        self.add_chord(chord_name, new_pressing_str)
        self.save_index()


def import_data(index, cache_file):
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
    index.save_index()


if __name__ == '__main__':
    # 创建索引实例
    index = ChordVectorIndex()

    # 导入数据
    cache_file = filePath('models/') + 'pressing_chord_mappings.cache'
    import_data(index, cache_file)

    # 搜索示例
    search_midi_notes = [12, 16, 19]  # Cmajor 的音符序列
    results = index.search_chord(search_midi_notes, top_k=5)
    for res in results:
        print(f"Chord Name: {res['chord_name']}, Distance: {res['distance']}")

    # 添加新的和弦
    index.add_chord('Am', 'A2@21,24,28')
    index.save_index()

    # 更新和弦
    index.update_chord('Am', 'A2@21,24,27')

    # 删除和弦
    index.delete_chord('Am')
