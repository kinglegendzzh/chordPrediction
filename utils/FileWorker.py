import os
import io
import sys

from MatrixView import MatrixView

from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from musicpy.musicpy import N

from utils.filePath import filePath


class FileWriteWorker(QRunnable):
    """
    文件写入工作线程，用于异步写入缓存文件，避免阻塞主线程。
    """

    def __init__(self, chord_name, pressing_notes):
        super().__init__()
        self.chord_name = chord_name
        self.pressing_notes = pressing_notes

    def run(self):
        mapping_file = filePath('models/pressing_chord_mappings.cache')
        # 创建文件夹如果不存在
        os.makedirs(os.path.dirname(mapping_file), exist_ok=True)

        print(f"{self.chord_name} and {self.pressing_notes}")

        # 将按下的音符转换为音符名称和音符索引
        root_note = self.pressing_notes[0]['name']  # 第一个音符为根音
        note_indices = [str(note['index']) for note in self.pressing_notes]
        note_indices_str = ','.join(note_indices)
        pressing_str = f"{root_note}@{note_indices_str}"

        # 读取现有的映射文件，检查去重
        lines = []
        if os.path.exists(mapping_file):
            with open(mapping_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

        # 查找是否已经存在相同的和弦名称
        found_chord = False
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            parts = line.split('::')
            if parts[0] == self.chord_name:
                found_chord = True
                # 检查是否已经存在相同的根音音符
                if pressing_str not in parts[1:]:
                    lines[i] = line + '::' + pressing_str + '\n'
                break

        # 如果没有找到相同的和弦名称，添加新的记录
        if not found_chord:
            new_line = f"{self.chord_name}::{pressing_str}\n"
            lines.append(new_line)

        # 写回文件
        with open(mapping_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
