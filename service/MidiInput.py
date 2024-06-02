import pygame
import pygame.midi
from PyQt5.QtCore import *


class MidiInput(QObject):
    v_key_pressed = pyqtSignal(int)
    v_key_released = pyqtSignal(int)
    choosed = True

    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.midi.init()
        print("读取所有MIDI输入设备：")

        device_count = pygame.midi.get_count()
        for i in range(device_count):
            device_info = pygame.midi.get_device_info(i)
            print('MIDI device {}: {}'.format(i, device_info))

        if device_count == 0:
            self.choosed = False
            raise ValueError('No MIDI devices found')

        # 手动指定设备id
        choose = input("手动指定一个设备id（回车跳过）：")
        if choose.strip() == "":
            input_device_id = None
        else:
            input_device_id = int(choose)

        if input_device_id is None:
            raise ValueError('No MIDI device ID specified')

        try:
            self.midi_input = pygame.midi.Input(input_device_id)
        except pygame.midi.MidiException as e:
            raise ValueError(f"Failed to initialize MIDI input device: {e}")

        self.running = True

    def run(self):
        while self.running:
            if self.midi_input.poll():
                events = self.midi_input.read(10)
                for event in events:
                    status = event[0][0]
                    note = event[0][1]
                    velocity = event[0][2]
                    print(f"status:{status}, note:{note}, velocity:{velocity}")

                    if 144 <= status <= 159 and velocity > 0:
                        # Note On event
                        virtual_key = note - 36
                        self.v_key_pressed.emit(virtual_key)
                        print("MIDI按键按下事件" + str(virtual_key))
                    elif (128 <= status <= 143) or (144 <= status <= 159 and velocity == 0):
                        # Note Off event
                        virtual_key = note - 36
                        self.v_key_released.emit(virtual_key)
                        print("MIDI按键释放事件" + str(virtual_key))

    def stop(self):
        self.running = False
        self.midi_input.close()
        pygame.midi.quit()
        pygame.quit()
