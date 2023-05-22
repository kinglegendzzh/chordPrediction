from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt


class KeyDialog(QDialog):
    def __init__(self, key):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle("Key Pressed")

        # 创建一个 QLabel 显示用户最后一次按下的按键
        label = QLabel("You Pressed: {}".format(key))

        # 创建一个 QVBoxLayout，并将 QLabel 添加到其中
        layout = QVBoxLayout()
        layout.addWidget(label)

        # 设置 QDialog 的布局
        self.setLayout(layout)

    def keyPressEvent(self, event):
        # 监听键盘按键事件，当用户按下键盘时会调用该方法
        key = event.key()

        # 打开弹窗显示用户最后一次按下的按键
        dialog = KeyDialog(key)
        dialog.exec_()


if __name__ == '__main__':
    # 创建 QApplication 对象
    app = QApplication([])

    # 创建 KeyDialog 对象并显示
    dialog = KeyDialog(Qt.Key_unknown)
    dialog.show()

    # 运行 PyQt5 应用
    app.exec_()