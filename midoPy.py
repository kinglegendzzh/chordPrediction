import os
import mido
rtmidi = mido.Backend('mido.backends.rtmidi')
portmidi = mido.Backend('mido.backends.portmidi')
input_names = rtmidi.get_input_names()
print(f"Available MIDI inputs: {input_names}")

# 打开输入设备
if input_names:
    with rtmidi.open_input(input_names[0]) as inport:
        print(f"Using input device: {inport.name}")

        # 开始监听输入设备
        for msg in inport:
            # 处理MIDI消息
            print(msg)
else:
    print("No MIDI input devices available.")

