import time
import fluidsynth
from utils.filePath import filePath

print('初始化 Fluidsynth 并加载 SoundFont')

# 启动 Fluidsynth 并指定音频驱动
fs = fluidsynth.Synth()
fs.start(driver="coreaudio")  # macOS 使用 coreaudio
# fs.start(driver="dsound")  # Windows: "dsound" 或 "winmm"
# fs.start(driver="alsa")  # Linux: "alsa" 或 "pulseaudio"

# 加载 SoundFont
path = filePath('sounds/FluidR3_GM/') + 'FluidR3_GM.sf2'
print(f'path: {str(path)}')
sfid = fs.sfload(path)
fs.program_select(0, sfid, 0, 0)

# 播放音符
fs.noteon(0, 60, 127)  # 播放 C4 音符
time.sleep(1)               # 等待 1 秒
fs.noteoff(0, 60)      # 关闭音符
