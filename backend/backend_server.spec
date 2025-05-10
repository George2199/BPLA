# -*- mode: python ; coding: utf-8 -*-

import os
block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[os.path.abspath('.')],  # Добавлено!
    binaries=[],
    datas=[
        ('seed.py', '.'), 
        ('config.py', '.'), 
        ('models.py', '.'), 
    ],
    hiddenimports=['seed'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='backend_server',
    debug=False,
    strip=False,
    upx=True,
    console=True,
)
