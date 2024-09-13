import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
import random
from PyQt5.QtGui import QColor
import random
from PyQt5.QtGui import QImage, QPixmap
from service.numpyMarkov import ChordPredictor
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

class MatrixView(QWidget):
    def __init__(self):
        super().__init__()
        self.needs_update = True
        self.setWindowTitle("概率转移矩阵分析图")
        self.setGeometry(300, 300, 800, 600)  # 调整窗口大小以适应图片

        # 使用 QLabel 显示图片
        self.label = QLabel(self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # 创建 ChordPredictor 实例
        chord_sequences = [
            ['C', 'Am', 'F', 'G', 'C'],
            ['Am', 'F', 'C', 'G', 'Am']
        ]
        self.predictor = ChordPredictor(chord_sequences, order=1)

        # 定时器用于定时刷新图片
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(1000)  # 每1000毫秒（1秒）刷新一次

    def update_image(self):
        """更新显示的图片"""
        if not self.needs_update:
            return
        # 创建一个 matplotlib 图表
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        cax = ax.imshow(self.predictor.transitions, cmap='hot',
                        interpolation='nearest')
        fig.colorbar(cax)
        ax.set_title("Transition Matrix Heatmap")
        ax.set_xlabel("Next Chord Index")
        ax.set_ylabel("Current State Index")

        # 将图表渲染到缓冲区
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)  # 关闭图表以释放内存

        # 从缓冲区加载图像并转换为 QPixmap
        img = QImage.fromData(buf.getvalue())
        pixmap = QPixmap.fromImage(img)

        # 更新 QLabel 显示
        self.label.setPixmap(pixmap)

        # 关闭缓冲区
        buf.close()
        # 刷新界面
        self.update()
        self.needs_update = False
