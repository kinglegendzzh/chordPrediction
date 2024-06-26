# -*- mode: python ; coding: utf-8 -*-
#pyinstaller打包程序，先根据下面的注释提示修改路径Path，在终端进入项目路径，输入'pyinstaller ChordCrafter.spec'生成可执行文件

block_cipher = None


a = Analysis(
    ['VirtualKeyboard.py',
    'service/markov.py',
    'service/MidiInput.py',
    'utils/filePath.py',
    'utils/musicUtils.py',
    'utils/QueueUtil.py',
    'utils/StringUtils.py'
    ],
    pathex=['E:\\apps\\pycharm\\project\\chordPrediction'], #输入你的项目绝对路径
    binaries=[],
    datas=[
    ('E:\\apps\\pycharm\\project\\chordPrediction\\labels','labels'),
    ('E:\\apps\\pycharm\\project\\chordPrediction\\records','records'),
    ('E:\\apps\\pycharm\\project\\chordPrediction\\labels\\dorian.model','labels'),
    ('E:\\apps\\pycharm\\project\\chordPrediction\\labels\\jazz.model','labels'),
    ('E:\\apps\\pycharm\\project\\chordPrediction\\labels\\pop.model','labels'),
    ('E:\\apps\\pycharm\\project\\chordPrediction\\labels\\rock.model','labels'),
    ('E:\\apps\\pycharm\\project\\chordPrediction\\labels\\五度圈模型.model','labels'),
    ('E:\\apps\\pycharm\\project\\chordPrediction\\labels\\常用终止式.model','labels'),
    ('E:\\apps\\pycharm\\project\\chordPrediction\\labels\\忧郁.model','labels'),
    ('E:\\apps\\pycharm\\project\\chordPrediction\\labels\\恢弘.model','labels'),
    ('E:\\apps\\pycharm\\project\\chordPrediction\\labels\\我的自制数据集.model','labels'),
    ('E:\\apps\\pycharm\\project\\chordPrediction\\records\\多利亚宇.model','records'),
    ('E:\\apps\\pycharm\\project\\chordPrediction\\records\\悲伤爵士.model','records'),
    ('E:\\apps\\pycharm\\project\\chordPrediction\\records\\我的自制和弦.model','records'),
    ('E:\\apps\\pycharm\\project\\chordPrediction\\records\\马里奥终止式.model','records')
    ], #输入你想要导入的资源文件（预测模板），（Windows系统需要将上述默认配置改成绝对路径，否则将导入失败）
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ChordCrafter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ChordCrafter',
)
