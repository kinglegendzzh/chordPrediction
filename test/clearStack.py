from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget

app = QApplication([])
stacked_widget = QStackedWidget()

# 向QStackedWidget中添加三个QWidget
widget1 = QPushButton('Widget 1')
widget2 = QPushButton('Widget 2')
widget3 = QPushButton('Widget 3')
stacked_widget.addWidget(widget1)
stacked_widget.addWidget(widget2)
stacked_widget.addWidget(widget3)

# 清空QStackedWidget中所有QWidget
while stacked_widget.count() > 0:
    widget = stacked_widget.widget(0)
    stacked_widget.removeWidget(widget)
    print("remove")