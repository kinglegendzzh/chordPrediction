import pygame
import pygame.midi
from PyQt5.QtCore import *
from service.soundNoise import SoundNoise
from pynput import keyboard  # 用于监听键盘输入


class MidiInput(QObject):
    """处理MIDI输入和键盘映射的类"""
    v_key_pressed = pyqtSignal(int)
    v_key_released = pyqtSignal(int)

    # 键盘到MIDI音符的映射
    key_mapping = {
        'A': 48, 'W': 49, 'S': 50, 'E': 51, 'D': 52, 'F': 53, 'T': 54,
        'G': 55, 'Y': 56, 'H': 57, 'U': 58, 'J': 59, 'K': 60, 'O': 61,
        'L': 62, 'P': 63, ';': 64, '；': 64, '\'': 65,
    }

    def __init__(self):
        super().__init__()
        self.sn = SoundNoise()
        self.active_keys = set()  # 用于跟踪按下的键
        self.use_keyboard_mapping = False
        self.running = True

        pygame.init()
        pygame.midi.init()

        self._initialize_midi_input()

    def _initialize_midi_input(self):
        """初始化MIDI设备或键盘映射"""
        print("读取所有MIDI输入设备：")
        self._print_midi_devices()

        input_device_id = self._choose_device()

        if input_device_id is None:
            self._enable_keyboard_mapping()
        else:
            self._initialize_midi_device(input_device_id)

    def _print_midi_devices(self):
        """打印所有可用的MIDI设备"""
        for i in range(pygame.midi.get_count()):
            device_info = pygame.midi.get_device_info(i)
            print(f'MIDI device {i}: {device_info}')

    def _choose_device(self):
        """手动选择MIDI设备"""
        choose = input("手动指定一个设备id（回车跳过使用键盘映射）：")
        return int(choose) if choose.strip() else None

    def _enable_keyboard_mapping(self):
        """启用键盘映射模式"""
        print("使用键盘映射模式")
        self.use_keyboard_mapping = True
        self._start_keyboard_listener()

    def _start_keyboard_listener(self):
        """开始监听键盘事件"""
        listener = keyboard.Listener(on_press=self._on_key_press, on_release=self._on_key_release)
        listener.start()

    def _initialize_midi_device(self, device_id):
        """初始化MIDI设备"""
        try:
            self.midi_input = pygame.midi.Input(device_id)
            self.use_keyboard_mapping = False
        except pygame.midi.MidiException as e:
            raise ValueError(f"无法初始化MIDI输入设备: {e}")

    def _on_key_press(self, key):
        """处理键盘按下事件"""
        try:
            key_char = key.char.upper()
            if key_char in self.key_mapping:
                self._handle_note_press(self.key_mapping[key_char])
        except AttributeError:
            pass  # 忽略特殊键（如Shift等）

    def _on_key_release(self, key):
        """处理键盘释放事件"""
        try:
            key_char = key.char.upper()
            if key_char in self.key_mapping:
                self._handle_note_release(self.key_mapping[key_char])
        except AttributeError:
            pass

    def _handle_note_press(self, note):
        """处理按下音符"""
        if note not in self.active_keys:
            self.active_keys.add(note)
            self._emit_key_press(note)

    def _handle_note_release(self, note):
        """处理释放音符"""
        if note in self.active_keys:
            self.active_keys.remove(note)
            self._emit_key_release(note)

    def _emit_key_press(self, note):
        """触发按键按下事件"""
        virtual_key = note - 36
        self.v_key_pressed.emit(virtual_key)
        print(f"MIDI音符 {note} 按下")
        self.sn.on_midi_input(note, 127)

    def _emit_key_release(self, note):
        """触发按键释放事件"""
        virtual_key = note - 36
        self.v_key_released.emit(virtual_key)
        print(f"MIDI音符 {note} 释放")
        self.sn.on_midi_input(note, 0, False)

    def run(self):
        """持续监听MIDI输入事件"""
        while self.running:
            if not self.use_keyboard_mapping and self.midi_input.poll():
                events = self.midi_input.read(10)
                self._process_midi_events(events)

    def _process_midi_events(self, events):
        """处理MIDI事件"""
        for event in events:
            status, note, velocity = event[0][0], event[0][1], event[0][2]
            print(f"status:{status}, note:{note}, velocity:{velocity}")

            if 144 <= status <= 159 and velocity > 0:
                self._handle_note_press(note)
            elif (128 <= status <= 143) or (144 <= status <= 159 and velocity == 0):
                self._handle_note_release(note)

    def stop(self):
        """停止MIDI输入"""
        self.running = False
        if not self.use_keyboard_mapping:
            self.midi_input.close()
            pygame.midi.quit()
        pygame.quit()
