# -*- mode: python ; coding: utf-8 -*-

import platform

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],  # Project root
    binaries=[],
    datas=[
        ('locales', 'locales'),
        ('assets', 'assets'),
        ('assets/icons/compressor.icns', 'assets/icons'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinterdnd2',
        'PIL',
        'PIL._tkinter_finder',
        'pillow_heif',
        'docx2pdf',
        'zipfile',
        'tempfile',
        'shutil',
        'subprocess',
        'json',
        'locale',
        'threading',
        'os',
        'sys',
        'pathlib',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=['generativemodels'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FileCompressor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icons/compressor.icns'
)

app = BUNDLE(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='FileCompressor.app',
    icon='assets/icons/compressor.icns',
    bundle_identifier='com.filecompressor.app',
    info_plist={
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13.0',
        'CFBundleDisplayName': 'FileCompressor',
        'NSPrincipalClass': 'NSApplication',
    }
)