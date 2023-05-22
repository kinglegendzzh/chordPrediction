from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt


class KeyLogger(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle("虚拟MIDI监听器")

        # 创建一个 QVBoxLayout 并将 QLabel 添加到其中
        self.layout = QVBoxLayout(self)
        self.label = QLabel("键盘虚拟映射和弦组：\n"
                            "(C->C大和弦; c->C小和弦)")
        self.layout.addWidget(self.label)

        # 设置标签的样式为居中和加粗
        self.label.setStyleSheet("font-weight: bold; text-align: center;")

    def keyPressEvent(self, event):
        # 获取按下的键码
        key = event.key()

        # 将键码转换为可读文本
        text = self.convert_keycode_to_text(key)

        # 更新 QLabel
        oldText = self.label.text()
        self.label.setText(oldText + "\n" + text)

    def convert_keycode_to_text(self, keycode):
        # Key_unknown 相当于无效的按键
        if keycode == Qt.Key_unknown:
            return "Invalid Key"

        # 如果是字母或数字键，则直接返回键的文本
        elif (keycode >= Qt.Key_A and keycode <= Qt.Key_Z) or (keycode >= Qt.Key_0 and keycode <= Qt.Key_9):
            return chr(keycode)

        # 处理其他按键
        else:
            return "Key Code : {}".format(str(keycode))


if __name__ == '__main__':
    # 创建 QApplication 对象
    app = QApplication([])

    # 创建 KeyLogger 对象并显示
    logger = KeyLogger()
    logger.show()

    # 运行 PyQt5 应用
    app.exec_()