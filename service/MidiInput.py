import pygame
import pygame.midi
from PyQt5.QtCore import *

class MidiInput(QObject):
    """
    MIDI输入类，负责监听并处理MIDI键盘事件，并将其转换为自定义虚拟键盘事件并发送出去。
    """
    v_key_pressed = pyqtSignal(int)  # 虚拟钢琴键盘按下事件
    v_key_released = pyqtSignal(int)  # 虚拟钢琴键盘释放事件

    choosed = True

    def __init__(self):
        """
        初始化MIDI输入设备并启动监听循环。
        """
        super().__init__()
        pygame.init()
        pygame.midi.init()
        print("读取所有MIDI输入设备：")
        # 遍历所有MIDI设备并输出信息
        device_count = pygame.midi.get_count()
        for i in range(device_count):
            device_info = pygame.midi.get_device_info(i)
            print('MIDI device {}: {}'.format(i, device_info))

        device_count = pygame.midi.get_count()
        input_device_id = None
        if device_count == 0:
            self.choosed = False
        else:
            #手动指定设备id
            choose = input("手动指定一个设备id（回车跳过）")
            input_device_id = int(choose)

        if input_device_id is None:
            raise ValueError('Cannot find MIDI device')

        self.midi_input = pygame.midi.Input(input_device_id)
        self.running = True

    def run(self):
        """
        MIDI监听循环。
        """
        while self.running:
            if self.midi_input.poll():
                # 处理MIDI输入事件
                events = self.midi_input.read(10)
                for event in events:
                    status = event[0][0]
                    note = event[0][1]
                    velocity = event[0][2]
                    print(f"status:{status}, note:{note}, velocity{velocity}")

                    if status == 144 and velocity > 0:
                        # MIDI按键按下事件
                        virtual_key = note - 36  # 将Note Number转换为虚拟钢琴键盘键号
                        # print(self.virtual_key_pressed.signatures)
                        self.v_key_pressed.emit(virtual_key)
                        print("MIDI按键按下事件"+str(virtual_key))
                    elif status == 144 and velocity == 0:
                        # MIDI按键释放事件
                        virtual_key = note - 36  # 将Note Number转换为虚拟钢琴键盘键号
                        self.v_key_released.emit(virtual_key)
                        print("MIDI按键释放事件"+str(virtual_key))

    def stop(self):
        """
        停止MIDI监听循环并关闭MIDI输入设备。
        """
        self.running = False
        self.midi_input.close()
        pygame.midi.quit()
        pygame.quit()