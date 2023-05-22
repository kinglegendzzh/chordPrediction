import pygame
import pygame.midi

pygame.init()
pygame.midi.init()

# 遍历所有MIDI设备并输出信息
device_count = pygame.midi.get_count()
for i in range(device_count):
    device_info = pygame.midi.get_device_info(i)
    print('MIDI device {}: {}'.format(i, device_info))

# 打开MIDI输入设备
input_device_id = None
for i in range(device_count):
    device_info = pygame.midi.get_device_info(i)
    if device_info[1] == 'your midi device name':
        input_device_id = i
        break
input_device_id = 1
if input_device_id is None:
    print('Cannot find MIDI device {}'.format('your midi device name'))
    exit()
else:
    print('Found MIDI device {}'.format('your midi device name'))
midi_input = pygame.midi.Input(input_device_id)

# 监听键盘输入
while True:
    if midi_input.poll():
        # 处理MIDI输入事件
        events = midi_input.read(10)
        for event in events:
            print(event)

# 关闭MIDI输入设备和Pygame
midi_input.close()
pygame.midi.quit()
pygame.quit()