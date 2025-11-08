# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ui/main_window.ui', 'ui'),
        ('ui/about_dialog.ui', 'ui'),
        ('assets/app.ico', 'assets'),
        ('custom_dictionary.txt', '.'),
        ('docs/README.txt', '.'),
        ('dictionaries', 'dictionaries'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.uic',
        'easyocr',
        'cv2',
        'numpy',
        'torch',
        'torchvision',
        'spylls',
        'PIL',
        'scipy._cyutility',
        'scipy.special._ufuncs_cxx',
        'scipy.special.cython_special',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PySide6', 'PySide2', 'tkinter', 'matplotlib'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Создаём splash-экран
splash = Splash(
    'assets/splash.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=(200, 260),
    text_size=10,
    text_color='white',
    text_default='Загрузка...',
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    splash,
    splash.binaries,
    [],
    name='VideoSpellChecker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Без консольного окна
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/app.ico',  # Иконка приложения
)
