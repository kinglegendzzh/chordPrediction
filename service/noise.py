import fluidsynth
from utils.filePath import filePath

# 初始化 Fluidsynth 并加载 SoundFont
fs = fluidsynth.Synth()
path = filePath('sounds/FluidR3_GM/') + 'FluidR3_GM.sf2'
sfid = fs.sfload(path)
fs.program_select(0, sfid, 0, 0)  # 通道 0，选择钢琴音色


def play_note_on(note, velocity=127):
    """播放音符"""
    fs.noteon(0, note, velocity)


def play_note_off(note):
    """关闭音符"""
    fs.noteoff(0, note)


# MIDI输入处理
def on_midi_input(note, velocity, is_note_on=True):
    if is_note_on:
        play_note_on(note, velocity)
    else:
        play_note_off(note)
