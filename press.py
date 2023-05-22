import keyboard


def on_key_press(event):
    if event.name == 'q':
        print('You pressed the q key!')


keyboard.on_press(on_key_press)

# 程序会一直监听键盘的输入按键，直到用户按下 "Esc" 键
keyboard.wait('esc')