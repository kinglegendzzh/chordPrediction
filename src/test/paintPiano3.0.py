from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Original Text", self)
        self.line_edit = QLineEdit(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_text)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        self.setLayout(layout)

    @pyqtSlot()
    def update_text(self):
        new_text = self.line_edit.text()
        self.label.setText(new_text)

    def start_timer(self):
        self.timer.start(1000)

    def stop_timer(self):
        self.timer.stop()


if __name__ == '__main__':
    app = QApplication([])
    window = Widget()
    window.show()
    window.start_timer()
    app.exec_()