# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import copy_metadata
import os
import platform
import sys

venv_path = os.popen('poetry env info --path').read().rstrip()
python_version = str(sys.version_info[0]) + '.' + str(sys.version_info[1])
arch = str('osx_' + platform.uname().machine)

datas = [
    (venv_path + '/lib/python' + python_version + '/site-packages/fido2/public_suffix_list.dat', 'fido2'),
    (venv_path + '/lib/python' + python_version + '/site-packages/pynitrokey/VERSION', 'pynitrokey'),
    ('../../../nitrokeyapp/ui', 'nitrokeyapp/ui'),
    ('../../../LICENSE', '.')
]
datas += copy_metadata('ecdsa')
datas += copy_metadata('fido2')
datas += copy_metadata('nitrokeyapp')
datas += copy_metadata('pynitrokey')
datas += copy_metadata('pyusb')
datas += copy_metadata('spsdk')

a = Analysis(
    ['../../../nitrokeyapp/__main__.py'],
    pathex=[],
    binaries=[
        (venv_path + '/lib/python' + python_version + '/site-packages/libusbsio/bin/' + arch + '/libusbsio.dylib', 'libusbsio')
    ],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter'],
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
    name='nitrokey-app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='arm64',
    codesign_identity=None,
    entitlements_file=None,
    contents_directory='.',
)
app = BUNDLE(
    exe,
    name='nitrokey-app2.app',
    icon='nitrokey-app.icns',
    bundle_identifier=None,
)

