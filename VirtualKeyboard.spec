# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['view/VirtualKeyboard.py',
    'service/markov.py',
    'service/MidiInput.py',
    'utils/markovUtils.py',
    'utils/musicUtils.py',
    'utils/QueueUtil.py',
    'utils/StringUtils.py'
    ],
    pathex=['/Users/apple/Desktop/pythonProject/chordPrediction'],
    binaries=[],
    datas=[
    ('labels/dorian.model','labels'),
    ('labels/jazz.model','labels'),
    ('labels/pop.model','labels'),
    ('labels/rock.model','labels'),
    ('labels/test.model','labels'),
    ('labels/五度圈模型.model','labels'),
    ('labels/常用终止式.model','labels'),
    ('labels/忧郁.model','labels'),
    ('labels/恢弘.model','labels'),
    ('labels/我的自制训练集.model','labels'),
    ('records/test.model','records'),
    ('records/test1.model','records'),
    ('records/test2.model','records'),
    ('records/test3.model','records'),
    ('records/test4.model','records'),
    ('records/多利亚宇.model','records'),
    ('records/悲伤爵士.model','records'),
    ('records/我的自制和弦.model','records'),
    ('records/马里奥终止式.model','records')
    ],
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
    name='VirtualKeyboard',
)
