# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import sys
from PyInstaller.utils.hooks import collect_submodules


hiddenimports = collect_submodules('rich') + ['ctypes', '_ctypes']

binaries = []
python_dll_dir = Path.cwd() / '.venv' / 'Scripts'
if python_dll_dir.exists():
    binaries.extend([(str(dll), '.') for dll in python_dll_dir.glob('libffi*.dll')])

base_prefix = Path(sys.base_prefix)
ffi_candidates = [
    base_prefix / 'Library' / 'bin' / 'ffi.dll',
    base_prefix / 'DLLs' / 'ffi.dll',
]
for ffi_dll in ffi_candidates:
    if ffi_dll.exists():
        binaries.append((str(ffi_dll), '.'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=[('VERSION', '.')],
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
    name='EDJS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
