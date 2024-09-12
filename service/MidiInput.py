import pygame
import pygame.midi
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from noise import on_midi_input
from pynput import keyboard  # 用于监听键盘输入


class MidiInput(QObject):
    v_key_pressed = pyqtSignal(int)
    v_key_released = pyqtSignal(int)
    choosed = True

    # 键盘到MIDI音符的映射
    key_mapping = {
        'A': 48,  # C2
        'W': 49,  # C#2
        'S': 50,  # D2
        'E': 51,  # D#2
        'D': 52,  # E2
        'F': 53,  # F2
        'T': 54,  # F#2
        'G': 55,  # G2
        'Y': 56,  # G#2
        'H': 57,  # A2
        'U': 58,  # A#2
        'J': 59,  # B2
        'K': 60,  # C3
        'O': 61,  # C#3
        'L': 62,  # D3
        'P': 63,  # D#3
        ';': 64,  # E3
        '；': 64,  # E3
        '\'': 65,  # F3
    }

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
        choose = input("手动指定一个设备id（回车跳过使用键盘映射）：")
        if choose.strip() == "":
            input_device_id = None
        else:
            input_device_id = int(choose)

        if input_device_id is None:
            print("使用键盘映射模式")
            self.use_keyboard_mapping = True
        else:
            try:
                self.midi_input = pygame.midi.Input(input_device_id)
                self.use_keyboard_mapping = False
            except pygame.midi.MidiException as e:
                raise ValueError(f"Failed to initialize MIDI input device: {e}")

        self.running = True

        # 如果使用键盘映射，则监听键盘事件
        if self.use_keyboard_mapping:
            self.listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
            self.listener.start()

    def on_key_press(self, key):
        try:
            key_char = key.char.upper()  # 获取按下的键并转为大写
            if key_char in self.key_mapping:
                note = self.key_mapping[key_char]
                velocity = 127  # 默认力度
                virtual_key = note - 36
                self.v_key_pressed.emit(virtual_key)
                print(f"键盘按键 '{key_char}' 映射到 MIDI 音符 {note}")
                on_midi_input(note, velocity)
        except AttributeError:
            pass  # 如果按下的是特殊键（如Shift等），忽略

    def on_key_release(self, key):
        try:
            key_char = key.char.upper()  # 获取释放的键并转为大写
            if key_char in self.key_mapping:
                note = self.key_mapping[key_char]
                virtual_key = note - 36
                self.v_key_released.emit(virtual_key)
                print(f"键盘按键 '{key_char}' 释放，MIDI 音符 {note}")
                on_midi_input(note, 0, False)
        except AttributeError:
            pass  # 如果释放的是特殊键，忽略

    def run(self):
        while self.running:
            if not self.use_keyboard_mapping and self.midi_input.poll():
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
                        on_midi_input(note, velocity)
                    elif (128 <= status <= 143) or (144 <= status <= 159 and velocity == 0):
                        # Note Off event
                        virtual_key = note - 36
                        self.v_key_released.emit(virtual_key)
                        print("MIDI按键释放事件" + str(virtual_key))
                        on_midi_input(note, velocity, False)

    def stop(self):
        self.running = False
        if not self.use_keyboard_mapping:
            self.midi_input.close()
            pygame.midi.quit()
        pygame.quit()


# 使用示例
if __name__ == '__main__':
    app = QApplication([])
    midi_input = MidiInput()
    midi_input.run()
