import pandas as pd  # 导入Pandas数据分析库
import pygame  # 导入Pygame游戏开发库
from pygame.locals import *  # 导入Pygame游戏窗口相关模块
import random  # 导入Python随机数库
import numpy as np  # 导入NumPy科学计算库

# 从文件中加载已编码的和弦数据
chord_data = pd.read_csv('encoded_chords.csv', header=None)
chords = chord_data.values.tolist()

# 定义状态转移矩阵
matrix_size = len(set(chord_data.values.ravel()))
transition_matrix = np.zeros((matrix_size, matrix_size))
for i in range(len(chords)-1):
    transition_matrix[chords[i]][chords[i+1]] += 1
for i in range(matrix_size):
    transition_matrix[i] /= transition_matrix[i].sum()

# 定义和弦进程生成器函数
def generate_chord_progression(start_chord, num_chords):
    chord_sequence = []
    current_chord = start_chord
    for i in range(num_chords):
        chord_sequence.append(current_chord)
        current_chord = np.random.choice(matrix_size, p=transition_matrix[current_chord])
    return chord_sequence

# 定义用户界面
pygame.init()  # 初始化Pygame
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width,display_height))  # 设置游戏窗口大小
pygame.display.set_caption('Chord Progression Generator')  # 设置游戏窗口标题
clock = pygame.time.Clock()  # 设置游戏时钟

white = (255,255,255)  # 设置白色RGB值
black = (0,0,0)  # 设置黑色RGB值

font_small = pygame.font.SysFont(None, 25)  # 设置小字体
font_large = pygame.font.SysFont(None, 40)  # 设置大字体

def text_objects(text, font):
    textSurface = font.render(text, True, black)  # 渲染文本
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac, action=None):
    mouse = pygame.mouse.get_pos()  # 获取鼠标位置
    click = pygame.mouse.get_pressed()  # 获取鼠标按键状态
    if x+w > mouse[0] > x and y+h > mouse[1] > y:  # 判断鼠标是否在按钮上
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))  # 绘制活动状态下的按钮

        if click[0] == 1 and action != None:  # 判断鼠标左键是否按下
            action()  # 执行按钮对应的函数
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))  # 绘制非活动状态下的按钮

    smallText = pygame.font.SysFont(None, 20)  # 设置按钮文字字体
    textSurf, textRect = text_objects(msg, smallText)  # 渲染按钮文字
    textRect.center = ((x+(w/2)), (y+(h/2)))
    gameDisplay.blit(textSurf, textRect)  # 在窗口上显示按钮文本

def quit_game():
    pygame.quit()  # 关闭Pygame
    quit()  # 关闭Python程序

def generate_chord_progression_ui():
    gameDisplay.fill(white)  # 设置背景颜色为白色
    textSurf, textRect = text_objects("Choose a chord to start with:", font_large)  # 渲染窗口标题
    textRect.center = ((display_width/2), (display_height/2-50))
    gameDisplay.blit(textSurf, textRect)

    chords = list(set(chord_data.values.ravel()))  # 获取所有和弦种类
    num_chords = len(chords)
    button_width = 70
    button_height = 40
    button_gap = 20
    button_x = (display_width-button_width*num_chords-button_gap*(num_chords-1))/2
    button_y = display_height/2

    for i in range(num_chords):
        button_text = str(chords[i])
        button_color = (150,150,150)
        button(button_text, button_x, button_y, button_width, button_height, button_color, button_color, lambda i=i:generate_chord_sequence(chords[i]))

        button_x += button_width + button_gap

    pygame.display.update()

def generate_chord_sequence(start_chord):
    gameDisplay.fill(white)  # 设置背景颜色为白色
    textSurf, textRect = text_objects("Generating chord progression...", font_small)  # 渲染提示信息
    textRect.center = (display_width/2, display_height/2)
    gameDisplay.blit(textSurf, textRect)
    pygame.display.update()

    chord_sequence = generate_chord_progression(start_chord, 8)  # 生成和弦进程
    print(chord_sequence)

    gameDisplay.fill(white)  # 设置背景颜色为白色
    textSurf, textRect = text_objects("Chord progression:", font_large)  # 渲染窗口标题
    textRect.center = ((display_width/2), (display_height/2-50))
    gameDisplay.blit(textSurf, textRect)

    chord_text = ''
    for chord in chord_sequence:
        chord_text += str(chord) + '  '
    textSurf, textRect = text_objects(chord_text, font_large)  # 渲染和弦进程
    textRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(textSurf, textRect)

    button("Generate again", 150, 500, 200, 50, (0,200,0), (0,255,0), lambda:generate_chord_sequence(start_chord))  # 设置“再次生成”按钮
    button("Quit", 450, 500, 100, 50, (200,0,0), (255,0,0), quit_game)  # 设置“退出”按钮

    pygame.display.update()

generate_chord_progression_ui()  # 运行用户界面

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # 关闭Pygame
            quit()  # 关闭Python程序
        pygame.display.update()
        clock.tick(60)