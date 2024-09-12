# -*- mode: python ; coding: utf-8 -*-
#pyinstaller打包程序，先根据下面的注释提示修改路径Path，在终端进入项目路径，输入'pyinstaller ChordCrafter.spec'生成可执行文件

block_cipher = None


a = Analysis(
    ['VirtualKeyboard.py',
    'service/markov.py',
    'service/MidiInput.py',
    'service/numpyMarkov.py',
    'service/soundNoise.py',
    'utils/filePath.py',
    'utils/musicUtils.py',
    'utils/QueueUtil.py',
    'utils/StringUtils.py'
    ],
    pathex=['/Users/apple/Desktop/pythonProject/chordPrediction'], #输入你的项目绝对路径
    binaries=[],
    datas=[
    ('/Users/apple/Desktop/pythonProject/chordPrediction/labels','labels'),
    ('/Users/apple/Desktop/pythonProject/chordPrediction/records','records'),
    ('/Users/apple/Desktop/pythonProject/chordPrediction/sounds','sounds'),
    ('/Users/apple/Desktop/pythonProject/chordPrediction/sounds/FluidR3_GM','sounds/FluidR3_GM/')
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
