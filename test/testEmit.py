from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import time


# 主程序窗体
class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Price Monitor")
        self.resize(400, 200)

        # 创建价格文本框
        self.price = QLineEdit(self)
        self.price.setReadOnly(True)
        self.price.resize(400, 100)
        self.price.move(0, 20)

        # 创建退出按钮
        self.exitbutton = QPushButton("Exit", self)
        self.exitbutton.resize(self.exitbutton.sizeHint())
        self.exitbutton.move(135, 150)

        # 将退出按钮连接到QApplication的退出动作
        self.exitbutton.clicked.connect(QCoreApplication.instance().quit)
        self.loadUI()

    # 创建终止信号，用于控制终止后台监控线程
    terminal_sig = pyqtSignal()

    @pyqtSlot(str)  # 更新价格信号槽，用于更新GUI的价格显示
    def update_price(self, price):
        self.price.setText(price)
        print("更新价格信号槽，用于更新GUI的价格显示")

    @pyqtSlot()  # 通知信号槽，用于发出“达到目标价格”通知，并结束监控线程
    def notification(self):
        self.moniterThread.quit()
        self.price.setText(self.price.text() + "Reached Target Price!")
        # 向监控线程发出终止信号
        self.terminal_sig.emit()
        print("通知信号槽，用于发出“达到目标价格”通知，并结束监控线程")

    def loadUI(self):
        # 创建价格监控线程
        self.moniterThread = MonitorThread(1000, 900)
        # 连接监控线程的槽函数
        self.moniterThread.update_price.connect(self.update_price)
        self.moniterThread.notification.connect(self.notification)
        self.terminal_sig.connect(self.moniterThread.terminate)
        # 启动监控线程
        self.moniterThread.start()


# 价格监控线程
class MonitorThread(QThread):
    # 声明两个信号，更新价格信号与提醒信号
    update_price = pyqtSignal(str)
    notification = pyqtSignal()

    def __init__(self, initPrice, targetPrice):
        super().__init__()
        self.init_price = initPrice
        self.target_price = targetPrice

    def run(self):
        while True:
            # 为方便测试，价格每0.5秒减少10
            self.init_price -= 10
            # 向主进程发送通知，更新价格
            self.update_price.emit(str(self.init_price))
            if self.init_price == self.target_price:
                # 当达到目标价格时，向主进程发送通知
                self.notification.emit()
            time.sleep(0.5)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    monitor = MainWindow()
    monitor.show()
    sys.exit(app.exec_())
