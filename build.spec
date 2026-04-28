# -*- mode: python ; coding: utf-8 -*-

import os
project_root = os.path.abspath('.')

a = Analysis(
    ['main.py'],
    pathex=[project_root],
    binaries=[],
    datas=[
        (os.path.join(project_root, 'assets'), 'assets'),
        (os.path.join(project_root, 'config'), 'config'),
        (os.path.join(project_root, 'ui'), 'ui'),
        (os.path.join(project_root, 'core'), 'core'),
    ],
    hiddenimports=[
        'ui',
        'ui.styles',
        'ui.widgets',
        'ui.main_window',
        'ui.config_window',
        'core',
        'core.scanner',
        'core.file_manager',
        'core.config_manager',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FileStructureReader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=os.path.join(project_root, 'assets', 'icon.ico'),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='FileStructureReader',
)
