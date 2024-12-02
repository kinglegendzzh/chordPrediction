import os
import io
import sys

from MatrixView import MatrixView

from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from musicpy.musicpy import N

from service.MidiInput import MidiInput
from service.numpyMarkov import ChordPredictor
from utils import QueueUtil
from utils import musicUtils
from utils.FileWorker import FileWriteWorker
from utils.filePath import filePath
import logging

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class VirtualKeyboard(QWidget):
    """
    虚拟钢琴键盘类，包含钢琴键盘上所有按键，并能够根据键盘事件实时更新某些按键的显示状态。
    """
    keys = ['w', 'b', 'w', 'b', 'w', 'w', 'b', 'w', 'b', 'w', 'b', 'w',
            'w', 'b', 'w', 'b', 'w', 'w', 'b', 'w', 'b', 'w', 'b', 'w',
            'w', 'b', 'w', 'b', 'w', 'w', 'b', 'w', 'b', 'w', 'b', 'w',
            'w', 'b', 'w', 'b', 'w', 'w', 'b', 'w', 'b', 'w', 'b', 'w',
            'w']
    values = [N('C1'), N('Db1'), N('D1'), N('Eb1'), N('E1'), N('F1'), N('F#1'), N('G1'), N('Ab1'), N('A1'), N('Bb1'),
              N('B1'),
              N('C2'), N('Db2'), N('D2'), N('Eb2'), N('E2'), N('F2'), N('F#2'), N('G2'), N('Ab2'), N('A2'), N('Bb2'),
              N('B2'),
              N('C3'), N('Db3'), N('D3'), N('Eb3'), N('E3'), N('F3'), N('F#3'), N('G3'), N('Ab3'), N('A3'), N('Bb3'),
              N('B3'),
              N('C4'), N('Db4'), N('D4'), N('Eb4'), N('E4'), N('F4'), N('F#4'), N('G4'), N('Ab4'), N('A4'), N('Bb4'),
              N('B4'),
              N('C5')]
    key_pressed = [False] * 49

    keys_button = []

    white_color = '#FFFFFF'
    black_color = '#000000'

    key_width = 50
    white_key_height = 160
    black_key_height = 100

    MAX_QUEUE = 10
    # QUEUE = QueueUtil.Queue(["", "", "", "", "", "", "", "", "", ""])
    QUEUE = QueueUtil.Queue([])

    # 预缓存和弦
    PRE_CHORD = None
    PRE_COUNT = 0

    # 预测终止标识符
    ENDING = 'ENDING'

    # 无设备标识
    NoneMIDI = False

    listening_enabled = True

    current_chord_sequences = []
    predictor = None
    last_order = None

    image_window = None

    def __init__(self, NoneMIDI=False):
        super().__init__()
        sys.stdout.flush()
        self.NoneMIDI = NoneMIDI
        # 添加布局
        self.vbox = QVBoxLayout()
        self.initUI()
        # 当前和弦展示项
        self.chords = self.findChild(QLabel, "chords")
        self.next = self.findChild(QLabel, "next")
        self.listWidget = self.findChild(QListWidget, "listO")
        self.stackedWidget = self.findChild(QStackedLayout, "stackO")
        self.labelBox = self.findChild(QVBoxLayout, "labelO")
        self.scroll_content = self.findChild(QWidget, "labelContent")
        self.scroll_area = self.findChild(QScrollArea, "scroll")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateChords)

        self.updateTimer = QTimer(self)
        self.updateTimer.timeout.connect(self.updateButtonColor)
        self.updateTimer.timeout.connect(self.updateMIDI)
        self.clearFocus()

    def initUI(self):
        # 设置窗口大小和标题
        self.setFixedSize(1200, 850)
        self.setWindowTitle('智能化音乐创作工具')
        if self.NoneMIDI:
            logging.info('使用<英文键盘>映射模式')
            title = QLabel("使用<英文键盘>映射模式")
        else:
            logging.info('成功接入MIDI键盘')
            title = QLabel('虚拟MIDI键盘')
        title.setAlignment(Qt.AlignCenter)

        grid = QGridLayout()
        grid.setObjectName("midi")
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        grid.setAlignment(Qt.AlignTop)
        for i in range(len(self.keys)):
            key = QPushButton('')
            key.setObjectName(self.values[i].name)
            if self.keys[i] == 'w':
                key.setFixedSize(self.key_width, self.white_key_height)
                self.changeWhiteSheet(key)
            else:
                key.setFixedSize(int(self.key_width / 2), self.black_key_height)
                self.changeBlackSheet(key)
            # key.clicked.connect(lambda state, i=i: self.onPressed(i))
            grid.addWidget(key, 0, i)
            self.keys_button.append(key)

        grid.setAlignment(Qt.AlignCenter)

        ch = QLabel('识别当前和弦: ')
        ch.setAlignment(Qt.AlignCenter)
        ch.setObjectName("chords")
        self.vbox.addWidget(ch)

        ch = QLabel('预测下一个和弦: ')
        ch.setAlignment(Qt.AlignCenter)
        ch.setObjectName("next")
        self.vbox.addWidget(ch)

        self.buttonV = QPushButton("打开概率转移矩阵分析图", self)
        self.buttonV.clicked.connect(self.open_image_window)
        self.vbox.addWidget(self.buttonV)

        # 初始化和弦序列
        chTitle = QLabel("实时记录最新十条和弦(松开琴键以写入,点击和弦以移出序列)：")
        chTitle.setObjectName("chordsQueueTitle")
        self.vbox.addWidget(chTitle)
        self.chordsQueue = QHBoxLayout()
        self.chordsQueue.setSpacing(0)
        self.chordsQueue.setObjectName("chordsQueue")
        # 初始化渲染和弦序列
        for i in range(0, self.MAX_QUEUE):
            ql = QPushButton("")
            ql.setObjectName("ch" + str(i))
            font = QFont('Calibri', 16)
            ql.setFont(font)
            # self.reShaderButton(ql)
            ql.clicked.connect(lambda state, i=i: self.onPressed(i))
            self.chordsQueue.addWidget(ql)
        self.vbox.addLayout(self.chordsQueue)

        # 创建3个单选按钮
        self.radio_btn1 = QRadioButton('一阶')
        self.radio_btn2 = QRadioButton('二阶')
        self.radio_btn3 = QRadioButton('三阶')
        # 设置默认选中
        self.radio_btn2.setChecked(True)
        self.hbox_radio = QHBoxLayout()
        self.hbox_radio.setObjectName("radio")
        self.hbox_radio.addWidget(QLabel('预测模型准确度'))
        self.hbox_radio.addWidget(self.radio_btn1)
        self.hbox_radio.addWidget(self.radio_btn2)
        self.hbox_radio.addWidget(self.radio_btn3)
        self.vbox.addLayout(self.hbox_radio)

        ch = QLabel('预选音乐风格/标签（上下滑动选择更多）: ')
        ch.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(ch)
        # 遍历目录下的文件，添加到多选框中
        self.labelBox = QVBoxLayout()
        self.labelBox.setObjectName("labelO")
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll")
        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_content.setObjectName("labelContent")
        self.scroll_content.setLayout(self.labelBox)
        self.scroll_area.setWidget(self.scroll_content)
        labelhbox = QHBoxLayout()
        count = 0  # 记录已添加的多选框数量
        for file_name in os.listdir(filePath('labels/')):
            name, extension = os.path.splitext(file_name)
            check_box = QCheckBox(name, self)
            check_box.setText(name)
            labelhbox.addWidget(check_box)
            count += 1
            if count >= 5:  # 超过x个数量，则另起一行继续水平排列
                self.labelBox.addLayout(labelhbox)
                labelhbox = QHBoxLayout()
                count = 0
        if count > 0:  # 处理剩余不到x个的多选框
            self.labelBox.addLayout(labelhbox)
        self.vbox.addWidget(self.scroll_area)

        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        hbox5 = QHBoxLayout()
        self.label_1 = QLabel("序列命名：", self)
        self.edit_1 = QLineEdit(self)
        self.label_2 = QLabel("标签：", self)
        self.edit_2 = QLineEdit(self)
        self.label_3 = QLabel("备注：", self)
        self.edit_3 = QLineEdit(self)
        # 创建“保存”和“标注”按钮
        self.save_btn = QPushButton("保存序列", self)
        self.save_btn.clicked.connect(lambda state, i=i: self.onRecord())
        self.label_btn = QPushButton("设为标注库", self)
        self.label_btn.clicked.connect(lambda state, i=i: self.onLabel())
        self.clear_btn = QPushButton("清除序列", self)
        self.clear_btn.clicked.connect(lambda state, i=i: self.onClear())
        hbox2.addWidget(self.label_1)
        hbox2.addWidget(self.edit_1)
        hbox2.addWidget(self.label_2)
        hbox2.addWidget(self.edit_2)
        hbox3.addWidget(self.save_btn)
        hbox3.addWidget(self.label_btn)
        hbox4.addWidget(self.label_3)
        hbox4.addWidget(self.edit_3)
        hbox3.addWidget(self.clear_btn)
        self.vbox.addLayout(hbox2)
        self.vbox.addLayout(hbox4)
        self.vbox.addLayout(hbox3)
        self.vbox.addLayout(hbox5)

        listTitle = QLabel("所有库：")
        self.vbox.addWidget(listTitle)
        self.shaderLists(self.vbox)

        self.vbox.addWidget(title)
        self.vbox.addLayout(grid)
        # 添加状态展示框
        self.status_label = QLabel("<~键>控制当前监听状态：已开启", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 12px; color: green;")
        self.vbox.addWidget(self.status_label)
        self.setLayout(self.vbox)

    def open_image_window(self):
        if not self.image_window:
            self.image_window = MatrixView()
        self.image_window.show()

    def shaderLists(self, vbox, listWidget=None, stackedWidget=None):
        type = 0
        # 读取模型
        if listWidget is None and stackedWidget is None:
            listWidget = QListWidget(self)
            stackedWidget = QStackedLayout()
            listWidget.setObjectName("listO")
            stackedWidget.setObjectName("stackO")
            listWidget.setMaximumWidth(250)
            type = 1
        directory_labels = "labels/"
        directory_records = "records/"
        for file_name in os.listdir(filePath(directory_labels)):
            item = '标注库- ' + str(file_name)
            listWidget.addItem(item)
            text = ""
            # 创建一个多行文本域控件
            text_edit = QTextEdit(text, self)
            # 设置文本域为只读
            text_edit.setReadOnly(True)
            cursor = text_edit.textCursor()
            with open(filePath(directory_labels) + str(file_name), 'r', encoding='utf-8') as f:
                lineNum = 1
                for line in f:
                    if lineNum != 1:
                        text += line + '\n'
                        cursor.insertText(line)
                        cursor.insertText('\n')
                    lineNum += 1

            stackedWidget.addWidget(text_edit)
        for file_name in os.listdir(filePath(directory_records)):
            item = '历史记录- ' + str(file_name)
            listWidget.addItem(item)
            text = ""
            # 创建一个多行文本域控件
            text_edit = QTextEdit(text, self)
            # 设置文本域为只读
            text_edit.setReadOnly(True)
            cursor = text_edit.textCursor()
            with open(filePath(directory_records) + str(file_name), 'r', encoding='utf-8') as f:
                lineNum = 1
                for line in f:
                    if lineNum != 1:
                        text += line + "\n"
                        cursor.insertText(line)
                        cursor.insertText('\n')
                    lineNum += 1
            stackedWidget.addWidget(text_edit)
        listWidget.currentRowChanged.connect(stackedWidget.setCurrentIndex)
        if type == 1:
            hbox = QHBoxLayout()
            hbox.addWidget(listWidget)
            hbox.addLayout(stackedWidget)
            vbox.addLayout(hbox)

    def reShaderLabels(self):
        # 清空QHBoxLayout
        for ch in self.scroll_content.children():
            ch.deleteLater()

        self.labelBox = QVBoxLayout()
        self.labelBox.setObjectName("labelO")
        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_content.setObjectName("labelContent")
        self.scroll_content.setLayout(self.labelBox)
        self.scroll_area.setWidget(self.scroll_content)
        labelhbox = QHBoxLayout()
        count = 0  # 记录已添加的多选框数量
        for file_name in os.listdir(filePath('labels/')):
            name, extension = os.path.splitext(file_name)
            check_box = QCheckBox(name, self)
            check_box.setText(name)
            labelhbox.addWidget(check_box)
            count += 1
            if count >= 5:  # 超过x个数量，则另起一行继续水平排列
                self.labelBox.addLayout(labelhbox)
                labelhbox = QHBoxLayout()
                count = 0
        if count > 0:  # 处理剩余不到x个的多选框
            self.labelBox.addLayout(labelhbox)

    def reShaderLists(self):
        self.listWidget.clear()
        # 删除所有的QWidget
        while self.stackedWidget.count() > 0:
            widget = self.stackedWidget.widget(0)
            self.stackedWidget.removeWidget(widget)
        self.shaderLists(self.vbox, self.listWidget, self.stackedWidget)

    def onRecord(self):
        if self.edit_1.text() != "":
            directory = filePath("records/")
            filename = self.edit_1.text() + ".model"
            file_path = os.path.join(directory, filename)
            if os.path.exists(file_path):
                with open(os.path.join(directory, filename), 'a', encoding='utf-8') as f:
                    f.write("\n")
                    csv_str = ',,'.join(self.QUEUE.array)
                    f.write(csv_str + "||" + self.edit_3.text())
            else:
                with open(os.path.join(directory, filename), 'w', encoding='utf-8') as f:
                    f.write(self.edit_2.text())
                    f.write("\n")
                    csv_str = ',,'.join(self.QUEUE.array)
                    f.write(csv_str + "||" + self.edit_3.text())

            # 刷新list
            self.reShaderLists()
        else:
            logging.info("填写为空")

    def onLabel(self):
        if self.edit_2.text() != "":
            directory = filePath("labels/")
            filenames = self.edit_2.text().split(',')
            for filename in filenames:
                filename += ".model"
                logging.info(filename)
                file_path = os.path.join(directory, filename)
                if filename != "":
                    if os.path.exists(file_path):
                        with open(os.path.join(directory, filename), 'a', encoding='utf-8') as f:
                            f.write("\n")
                            csv_str = ',,'.join(self.QUEUE.array)
                            f.write(csv_str + "||" + self.edit_3.text())

                    else:
                        with open(os.path.join(directory, filename), 'w', encoding='utf-8') as f:
                            f.write(self.edit_2.text())
                            f.write("\n")
                            csv_str = ',,'.join(self.QUEUE.array)
                            f.write(csv_str + "||" + self.edit_3.text())
            # 刷新list
            self.reShaderLists()
            # 刷新label
            self.reShaderLabels()
        else:
            logging.info("填写为空")

    def onClear(self):
        self.QUEUE.clear()
        for i in range(0, self.MAX_QUEUE):
            self.findChild(QPushButton, "ch" + str(i)).setText("")

    def onPressed(self, i):
        logging.info('Key ' + str(i) + ' was pressed.')
        if self.QUEUE.length() > i:
            self.QUEUE.remove(i)

    # def paintEvent(self, event: QtGui.QPaintEvent):
    #     # 寻找所有按钮
    #     buttons = self.findChildren(QPushButton)
    #
    #     # 调用父类的 paintEvent 方法
    #     super().paintEvent(event)

    @pyqtSlot()
    def updateButtonColor(self):
        # # 获取正在按下的所有琴键
        # j = 0
        # pressing = []
        # for isPressed in self.key_pressed:
        #     if isPressed:
        #         pressing.append(self.values[j])
        #     j += 1
        #
        # if self.QUEUE.length()!=0:
        # detectElement = musicUtils.detectElement(pressing)
        # ch = detectElement.getChordAttr()
        # logging.info(ch)
        # get_chord(ch.root, ch.chord_type)
        i = 0
        for button in self.keys_button:
            if self.key_pressed[i] == True:
                if self.keys[i] == 'w':
                    self.changeWhiteSheet(button, True)
                else:
                    self.changeBlackSheet(button, True)
            else:
                if self.keys[i] == 'w':
                    self.changeWhiteSheet(button)
                else:
                    self.changeBlackSheet(button)
            i += 1

    @pyqtSlot()
    def updateMIDI(self):
        # 渲染实时和弦序列
        if self.QUEUE.length() > 10:
            for i in range(0, self.MAX_QUEUE):
                label = self.findChild(QPushButton, "ch" + str(i))
                font = QFont('Calibri', 16)
                label.setFont(font)
                # self.reShaderButton(label)
                label.setText(self.QUEUE.array[i])
        else:
            for i in range(0, self.QUEUE.length()):
                label = self.findChild(QPushButton, "ch" + str(i))
                font = QFont('Calibri', 16)
                label.setFont(font)
                # self.reShaderButton(label)
                label.setText(self.QUEUE.array[i])
            for j in range(self.QUEUE.length(), self.MAX_QUEUE):
                label = self.findChild(QPushButton, "ch" + str(j))
                font = QFont('Calibri', 16)
                label.setFont(font)
                # self.reShaderButton(label)
                label.setText("")

    @pyqtSlot()
    def pressingEvent(self):
        # 获取正在按下的所有琴键
        i = 0
        pressingCache = []
        pressing = []
        for isPressed in self.key_pressed:
            if isPressed:
                pressingCache.append({'index': i, 'name': self.values[i]})
                pressing.append(self.values[i])
            i += 1
        if 3 <= len(pressing) <= 5:
            logging.info(f"正在按下的所有琴键：{pressing}")
            detectElement = musicUtils.detectElement(pressing)
            chord_name = detectElement.getNormalChord()
            item = QLabel('当前和弦： ' + chord_name)
            self.chords.setText(item.text())
            if len(pressing) > self.PRE_COUNT:
                self.PRE_CHORD = (chord_name, pressingCache)
            logging.info(self.QUEUE.array)
        elif len(pressing) == 0:
            item = QLabel('当前和弦： ')
            self.chords.setText(item.text())
            if self.PRE_CHORD is not None:
                chord_name, pressing_notes = self.PRE_CHORD
                if chord_name != self.QUEUE.last():
                    if self.QUEUE.length() < self.MAX_QUEUE:
                        logging.info("push")
                        self.QUEUE.push(chord_name)
                    else:
                        logging.info("pop")
                        self.QUEUE.pop()
                        self.QUEUE.push(chord_name)
                    # 将 pressing（当前按下的音符）与 self.PRE_CHORD（当前和弦）的映射关系缓存到本地
                    # 启动异步线程进行文件写入
                    worker = FileWriteWorker(chord_name, pressing_notes)
                    QThreadPool.globalInstance().start(worker)

                else:
                    logging.info(f"重复和弦{self.QUEUE.last()}")
        self.PRE_COUNT = len(pressing)

    def changeWhiteSheet(self, button, isGray=False):
        if isGray:
            button.setStyleSheet('border: 1px solid gray; border-radius: 3px;' + "background-color: #878787;")
        else:
            button.setStyleSheet(
                'border: 1px solid gray; border-radius: 3px;' + "background-color: " + self.white_color)

    def changeBlackSheet(self, button, isGray=False):
        if isGray:
            button.setStyleSheet('border: 1px solid gray; border-radius: 3px; margin-left: -' + str(
                int(self.key_width / 5)) + 'px;' + "background-color: #787878;")
        else:
            button.setStyleSheet('border: 1px solid gray; border-radius: 3px; margin-left: -' + str(
                int(self.key_width / 5)) + 'px;' + "background-color: " + self.black_color)

    def reShaderButton(self, button):
        # 获取按钮的最大宽度
        max_width = button.width()

        # 获取按钮的字体
        font = button.font()

        # 创建一个QFontMetrics对象，用于计算不同字体/大小下的文本大小
        metrics = QFontMetrics(font)

        # 计算当前字体下文本的宽度
        text_width = metrics.width(button.text())

        logging.info(f"按钮宽度{max_width}和文本宽度{text_width}")

        # 如果文本太长，则根据按钮宽度自动调整字体大小，使文本填充按钮
        if text_width > max_width:
            # 计算调整后的字体大小
            font_size = max_width * font.pointSize() // text_width
            font.setPointSize(font_size)
            button.setFont(font)

    def virtual_key_pressed(self, index):
        """
        处理虚拟钢琴键盘按下事件。
        """
        if index >= 0 and index < 88:
            # 更新键盘按键状态
            self.key_pressed[index] = True
            self.update()
            self.pressingEvent()
            self.updateButtonColor()

    def virtual_key_released(self, index):
        """
        处理虚拟钢琴键盘释放事件。
        """
        if index >= 0 and index < 88:
            # 更新键盘按键状态
            self.key_pressed[index] = False
            self.update()
            self.pressingEvent()
            self.updateButtonColor()

    def closeEvent(self, event):
        """
        处理窗口关闭事件。
        """
        super().closeEvent(event)
        self.close()

    def keyPressEvent(self, event):
        self.setFocusPolicy(Qt.StrongFocus)
        logging.info(f"Key pressed: {event.key()}")
        if str(event.key()) == '96' or str(event.key()) == '126' or str(event.key()) == '183':
            if self.NoneMIDI:
                # 切换监听模式
                self.listening_enabled = not self.listening_enabled
                if self.listening_enabled:
                    self.status_label.setText("<~键>控制当前监听状态：已开启")
                    self.status_label.setStyleSheet("font-size: 12px; color: green;")
                else:
                    self.status_label.setText("<~键>控制当前监听状态：已关闭")
                    self.status_label.setStyleSheet("font-size: 12px; color: red;")
                logging.info(f"监听模式：{'开启' if self.listening_enabled else '关闭'}")
        else:
            # 调用父类的按键处理
            super().keyPressEvent(event)

    @pyqtSlot()
    def updateChords(self):
        chord_sequences = []
        for cbox in self.findChildren(QCheckBox):
            if cbox.isChecked():
                logging.info(cbox)
                with open(filePath('labels/') + cbox.text() + '.model', 'r', encoding='utf-8'
                          ) as f:
                    lineNum = 1
                    for line in f:
                        if lineNum != 1:
                            cline = line.split('||')
                            arr_str = cline[0].split(',,')
                            chord_sequences.append(arr_str)
                            chord_sequences.append([self.ENDING])
                        lineNum += 1
        if len(chord_sequences) != 0:
            logging.info(f"构建马尔科夫链{chord_sequences}")
            if self.image_window:
                self.image_window.set_chord_sequences(chord_sequences)
        else:
            if self.image_window:
                self.image_window.set_chord_sequences([])

        order = 1 if self.radio_btn1.isChecked() else 2 if self.radio_btn2.isChecked() else 3

        if self.QUEUE.length() >= order and len(chord_sequences) > 0:
            logging.info(f"阶数: {order}")
            if chord_sequences != self.current_chord_sequences or self.last_order is None or self.last_order != order:
                self.current_chord_sequences = chord_sequences
                self.predictor = ChordPredictor(chord_sequences, order)
                self.last_order = order
                logging.info(f"初始化预测器，阶数：{order}")
            if order == 3:
                current_chords = [self.QUEUE.index(self.QUEUE.length() - 3), self.QUEUE.index(self.QUEUE.length() - 2),
                                  self.QUEUE.index(self.QUEUE.length() - 1)]
            else:
                current_chords = [self.QUEUE.index(self.QUEUE.length() - 2), self.QUEUE.index(self.QUEUE.length() - 1)]
            predictions = self.predictor.predict_chord(current_chords)

            check_sequence = []
            for sequence in chord_sequences:
                check_sequence += sequence
            logging.info(f'预测结果: {predictions}')
            self.next.setText(
                "预测下一个和弦：(<和弦名称>,<匹配比率%>) " + str(predictions))
        else:
            self.next.setText("预测下一个和弦: ")

    def start_timer(self):
        self.timer.start(1000)
        self.updateTimer.start(120)

    def stop_timer(self):
        self.timer.stop()
        self.updateTimer.stop()


def on_virtual_key_pressed(index):
    virtual_keyboard.virtual_key_pressed(index)


def on_virtual_key_released(index):
    virtual_keyboard.virtual_key_released(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 创建虚拟钢琴键盘对象和MIDI输入对象，并将MIDI输入对象的虚拟键盘事件与虚拟钢琴键盘对象的虚拟键盘事件相连
    midi_input = MidiInput()
    logging.info(f'是否开启键盘映射：{midi_input.use_keyboard_mapping}')
    if midi_input.use_keyboard_mapping:
        virtual_keyboard = VirtualKeyboard(True)

    else:
        virtual_keyboard = VirtualKeyboard()
    midi_input.v_key_pressed.connect(on_virtual_key_pressed)
    midi_input.v_key_released.connect(on_virtual_key_released)
    midi_input_thread = QThread()
    midi_input.moveToThread(midi_input_thread)
    midi_input_thread.started.connect(midi_input.run)
    midi_input_thread.start()
    virtual_keyboard.show()
    virtual_keyboard.start_timer()
    # 启动Qt的事件循环
    sys.exit(app.exec_())
