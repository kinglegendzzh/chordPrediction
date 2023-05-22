from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout
from PyQt5.QtCore import Qt

class Piano(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口大小和标题
        self.setFixedSize(630, 240)
        self.setWindowTitle('Piano')

        # 添加标题
        title = QLabel('Piano')
        title.setAlignment(Qt.AlignCenter)

        # 添加按键
        white_color = '#FFFFFF'
        black_color = '#000000'
        keys = ['w', 'b', 'w', 'b', 'w', 'w', 'b', 'w', 'b', 'w', 'b', 'w',
                'w', 'b', 'w', 'b', 'w', 'w', 'b', 'w', 'b', 'w', 'b', 'w',
                'w', 'b', 'w', 'b', 'w', 'w', 'b', 'w', 'b', 'w', 'b', 'w']

        key_width = 25
        white_key_height = 120
        black_key_height = 90

        grid = QGridLayout()
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        for i in range(len(keys)):
            key = QPushButton('')
            key.setObjectName(keys[i])
            if keys[i] == 'w':
                key.setFixedSize(key_width, white_key_height)
                key.setStyleSheet('background-color: ' + white_color + '; border: 1px solid black')
            else:
                key.setFixedSize(int(key_width/2), black_key_height)
                key.setStyleSheet('background-color: ' + black_color + '; border: 1px solid black; margin-left: -' + str(int(key_width/4)) + 'px')
            # 绑定事件
            key.clicked.connect(lambda state, i=i: self.onPressed(i))
            grid.addWidget(key, 0, i)

        grid.setAlignment(Qt.AlignCenter)

        # 添加布局
        vbox = QVBoxLayout()
        vbox.addWidget(title)
        vbox.addLayout(grid)
        self.setLayout(vbox)

    def onPressed(self, i):
        # 在这里添加你想要的逻辑
        print('Key ' + str(i) + ' was pressed.')

if __name__ == '__main__':
    app = QApplication([])
    piano = Piano()
    piano.show()
    app.exec_()