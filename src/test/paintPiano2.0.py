from PyQt5.QtWidgets import QApplication, QListWidget, QWidget, QStackedLayout, QVBoxLayout, QLabel


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.listWidget = QListWidget(self)

        for i in range(5):
            item = 'Item ' + str(i)
            self.listWidget.addItem(item)

        self.stackedWidget = QStackedLayout()

        for i in range(5):
            item = QLabel('Widget ' + str(i), self)
            self.stackedWidget.addWidget(item)

        self.listWidget.currentRowChanged.connect(self.stackedWidget.setCurrentIndex)

        vbox = QVBoxLayout()
        vbox.addWidget(self.listWidget)
        vbox.addLayout(self.stackedWidget)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('QStackedLayout')
        self.show()

if __name__ == '__main__':
    app = QApplication([])
    ex = Example()
    app.exec_()