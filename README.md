## ChordPrediction
[English](https://github.com/kinglegendzzh/chordPrediction/blob/master/README_EN.md) [中文](https://github.com/kinglegendzzh/chordPrediction/blob/master/README.md)

> 智能化音乐创作工具(基于马尔科夫链的和弦预测算法)
>
> 和弦预测是音乐生成领域的重要应用之一。该系统提出一种基于n阶马尔科夫链的和弦预测算法，并将其应用于实时和弦预测。该算法先根据历史和弦序列构建一个马尔科夫链，然后根据当前和弦序列的状态生成下一个和弦。在使用多个和弦序列进行训练的情况下，该算法可以更好地处理不同音乐风格之间的转换，从而提高生成结果的多样性。
>
> 本系统还提供一套应用该算法的交互式界面，用户可以通过简单的弹奏生成自己所需的和弦，还能对和弦进行标注、保存和预览，并自主训练模型的准确度。经过性能评估，该算法基于模型数据，能够预测出高质量的和弦，同时保证了预测速度和稳定性。

### 一、系统预览图

![DraggedImage](https://github.com/kinglegendzzh/chordPrediction/assets/33552269/9f731d4e-9f4b-4282-ae57-2c272437475f)

**界面元素：**

1. 当前和弦
2. 预测下一个和弦及匹配度
3. 实时记录和弦序列
4. 预选算法准确度
5. 预选音乐风格/标签
6. 保存当前和弦序列至历史记录
7. 标注当前和弦序列至模型数据
8. 对历史记录的预览
9. 对模型标注模型的预览
10. 实时监听的虚拟映射MIDI键盘

**目前适配的MIDI设备：**

- MIDI专业键盘49键及以上（最佳适配品牌：艾肯ICON iKeyBoard5 49键）

### 二、音乐创作背景

和弦是音乐创作三大要素的核心，相当于一栋房子的地基，因此和弦设计阶段是整个音乐制作周期最重要的部分，它奠定了整首音乐的风格、听感和情绪基调。

![DraggedImage-1](https://github.com/kinglegendzzh/chordPrediction/assets/33552269/224efee5-e24f-4583-aa7c-25eb38d5dafb)

和弦作为乐曲的地基，其种类繁多，其中最主要的几种类型为:大三和弦、小三和弦、增三和弦、减三和弦;大七和弦、小七和弦、属七和弦、减七和弦、半减七和弦;挂留和弦。这些不同类型的和弦为乐曲赋予了各自的色彩和韵味。然而，和弦之间的排列组合也十分重要。若组合得当，会产生和谐美妙的音感。

在音乐中，和弦是构建旋律和歌曲结构的基础元素之一。无论是专业编曲人，还是普通的音乐创作爱好者，在创作过程中，和弦设计是一个非常关键的环节，因为一个好的和弦能够为歌曲增加魅力、情感和深度。而和弦的选取不当则可能会导致歌曲听起来单调乏味，缺少变化和情感。

1. 需要扎实的音乐理论功底
2. 需要音乐创作的经验
3. 需要灵感和创造力

### 三、本系统对音乐创作的帮助

本系统作为一个基于马尔科夫链的和弦预测系统，它可以通过分析已有的和弦组合和模型数据，自动生成一些新的和弦预测结果，从而帮助创作出更加新颖、富有创意的音乐作品。

因此该系统主要支撑起了音乐创作流程中的和弦设计阶段，对于音乐制作人来说，通过这个系统可以缩短创作时间。制作人可以将系统生成的和弦进行结合嵌入到自己的作品之中，达到更好的效果和质量。此外，该系统还可作为乐曲创作的辅助工具，在需要作曲时，再加入自己的创意和想象，更好地满足自己的创意和要求。

### 四、开发编译的安装指南

本系统需要一些基础的环境配置来确保能够正常运行。以下是安装的详细步骤：

1. 下载并安装 Python 3.7 或更高版本。

2. 克隆本项目到本地：
   ```bash
   git clone https://github.com/kinglegendzzh/chordPrediction.git
3. 进入项目目录：
   ```bash
   cd chordPrediction
   ```
4. 安装并导入一些必要的外部依赖
   > 下载 FluidR3_GM Soundfont https://member.keymusician.com/Member/FluidR3_GM/index.html
   > 安装fluidsynth的C编译库 https://www.fluidsynth.org/
5. 安装相关依赖
   ```bash
   pip install -r requirements.txt
   ```
   > **部分参考**：
   > <p>安装<strong>musicpy</strong>库：<a href="https://github.com/Rainbow-Dreamer/musicpy">https://github.com/Rainbow-Dreamer/musicpy</a></p>
   > <p>安装<strong>pyqt5</strong>库： <a href="https://pypi.org/project/PyQt5/">https://pypi.org/project/PyQt5/</a></p>
   > <p>安装<strong>pygame</strong>库：<a href="https://www.pygame.org/download.shtml">https://www.pygame.org/download.shtml</a></p>


### 五、如何打包并生成可执行文件

打包本系统有两种方式：

#### 方式一（手动打包）

1. 下载 PyInstaller，并在项目路径下执行以下命令生成可执行文件，
```bash
pip install pyinstaller
```
2. 找到ChordCrafter.spec或ChordCrafter_win64.spec文件，根据注释提示修改相关Path路径；
3. 在终端进入项目路径，输入下列命令即可生成可执行文件；
 
   ```bash
   pyinstaller ChordCrafter.spec  # 适用于MacOS/Linux打包
   pyinstaller ChordCrafter_win64.spec  # 适用于Windows打包
   ```

#### 方式二（直接在 [Releases](https://github.com/kinglegendzzh/chordPrediction/releases/) 下载可执行文件，现已支持Windows）

### 六、如何使用

参见我在B站上发布的软件使用指南，【我开发了一个和弦创作工具（基于马尔科夫链的和弦预测算法）「开发的 KL」】 [链接](https://www.bilibili.com/video/BV1Ww4m1i7CN/?share_source=copy_web&vd_source=1243dee83a20c6e1d4c96e246dd5b026)

### 七、未来更新清单

❗️❗️❗️“最高优先级，最近很有可能更新”

❗️❗️“比较重要的功能”

❗️“在更新计划当中，但不那么重要”

```python
# TODO ❗️❗️ 对踏板的适配、预览和弦（全部播放、当前播放、预选音色和节拍）、播放时对当前序列的和弦的键位渲染、匹配比例阈值、预测和弦的序列化展示、对预测和弦的键位渲染
# TODO ❗️ 和弦的情绪属性、暂停记录
# TODO ❗️❗️❗️ 支持多预测结果的输出 ✔已完成
# TODO 和弦预测的初始化函数执行动作不再每秒刷新一次了，现在改成只会在标签改变事件发生时才会触发，极大地提升了系统性能
# TODO ❗️❗️ getChordAttr和弦输出测试
# TODO 预测来源
# TODO 更详细的分类
# TODO 日志系统/和弦翻译系统
# TODO ❗️❗️❗️ 基于转移概率矩阵的优化算法 ✔已完成
```

### 作者寄语

如果你喜欢我的项目，欢迎⭐️star！

我于2020年开始接触乐理，21年后逐渐对编曲创作原理初步形成了自己的理解，虽然我并非音乐班底出身，但抱着对音乐创作的兴趣我一直坚持自学编曲，我在我的哔哩哔哩账号中会经常发表音乐作品和相关技术性文章。自学期间踩过很多的坑，也吸取了很多经验。在2022年8月份左右，我在想能否开发一个辅助我音乐创作的工具，于是诞生起了这个项目的点子，调研期间我发现，python语言对音乐生成领域、机器学习领域有很大的优势，它有着生态丰富的开源社区；同时我发现了有不少音乐/编程双修的同行人也在对这个比较小众的交叉领域无私地奉献着，为我提供了许多宝贵的经验，我在此向这些先行者致敬🫡

本人对音乐创作和计算机领域的研究都有比较大的兴趣，即使这个项目无人问津未来我也将持续更新、自己自用。如果很有幸你能喜欢并使用我的程序，欢迎提出你的宝贵建议，你的支持是我最大的更新动力。个人邮箱：kinglegendzzh@163.com。个人微信：zzh13999325716