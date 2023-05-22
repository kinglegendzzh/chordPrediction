from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QLabel


class ScrollableWidget(QWidget):
    def __init__(self):
        super().__init__()

        vbox_scroll = QVBoxLayout()
        for i in range(30):
            vbox_scroll.addWidget(QLabel(f"Label {i+1}"))

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        scroll_content = QWidget(self.scroll_area)
        scroll_content.setLayout(vbox_scroll)
        self.scroll_area.setWidget(scroll_content)

        self.layout_main = QVBoxLayout()
        self.layout_main.addWidget(self.scroll_area)
        self.setLayout(self.layout_main)


if __name__ == '__main__':
    app = QApplication([])
    window = ScrollableWidget()
    window.show()
    app.exec_()