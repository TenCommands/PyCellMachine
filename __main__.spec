# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('D:\\GitHub\\PyCellMachine\\pycellmachine\\*', 'pycellmachine'), ('D:\\GitHub\\PyCellMachine\\pycellmachine\\_internal\\*', 'pycellmachine\\_internal'), ('D:\\GitHub\\PyCellMachine\\pycellmachine\\texturepacks\\*', 'pycellmachine\\texturepacks'), ('D:\\GitHub\\PyCellMachine\\pycellmachine\\mods\\*', 'pycellmachine\\mods')]
binaries = []
hiddenimports = ['pygame', 'pycellmachine._internal']
tmp_ret = collect_all('pygame')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['pycellmachine\\__main__.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='__main__',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['pycellmachine\\_internal\\assets\\logo.png'],
)
