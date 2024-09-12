import platform
import fluidsynth
from utils.filePath import filePath


class SoundNoise:
    fs = None

    def __init__(self):
        super().__init__()
        print('初始化 Fluidsynth 并加载 SoundFont')

        # 检测操作系统并选择合适的音频驱动
        system = platform.system()
        if system == "Darwin":
            driver = "coreaudio"  # macOS 使用 coreaudio
        elif system == "Windows":
            driver = "dsound"  # Windows 使用 DirectSound
        elif system == "Linux":
            driver = "alsa"  # Linux 使用 ALSA
        else:
            driver = "pulseaudio"  # 默认选择 pulseaudio

        print(f"Detected OS: {system}, 使用音频驱动: {driver}")

        # 初始化 Fluidsynth，并启动合适的音频驱动
        self.fs = fluidsynth.Synth()
        self.fs.start(driver=driver)

        # 加载 SoundFont
        path = filePath('sounds/FluidR3_GM/') + 'FluidR3_GM.sf2'
        sfid = self.fs.sfload(path)
        self.fs.program_select(0, sfid, 0, 0)  # 通道 0，选择钢琴音色

    def play_note_on(self, note, velocity=127):
        """播放音符"""
        self.fs.noteon(0, note, velocity)

    def play_note_off(self, note):
        """关闭音符"""
        self.fs.noteoff(0, note)

    # MIDI输入处理
    def on_midi_input(self, note, velocity, is_note_on=True):
        if is_note_on:
            self.play_note_on(note, velocity)
        else:
            self.play_note_off(note)
