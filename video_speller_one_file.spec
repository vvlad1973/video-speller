# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None
IS_WINDOWS = sys.platform == 'win32'

# Собираем все файлы opencv-python для Linux
cv2_datas = []
cv2_binaries = []
cv2_hiddenimports = []
if not IS_WINDOWS:
    # Находим путь к cv2 в активном окружении
    import site
    import sysconfig

    # Пробуем разные места, где может быть cv2
    possible_paths = []

    # 1. Через sysconfig (работает в venv)
    scheme_names = sysconfig.get_scheme_names()
    for scheme in scheme_names:
        try:
            purelib = sysconfig.get_path('purelib', scheme)
            platlib = sysconfig.get_path('platlib', scheme)
            if purelib:
                possible_paths.append(purelib)
            if platlib and platlib != purelib:
                possible_paths.append(platlib)
        except:
            pass

    # 2. Через site.getsitepackages()
    possible_paths.extend(site.getsitepackages())

    # 3. Через sys.path
    import sys
    possible_paths.extend([p for p in sys.path if 'site-packages' in p])

    # Ищем cv2
    cv2_path = None
    for path in possible_paths:
        test_path = os.path.join(path, 'cv2')
        if os.path.exists(test_path):
            cv2_path = test_path
            break

    if cv2_path:
        # Копируем всю папку cv2 как datas (не Tree напрямую)
        cv2_datas = [(cv2_path, 'cv2')]
        print(f"[INFO] Found cv2 at: {cv2_path}")
    else:
        print(f"[WARNING] cv2 not found! Searched in: {possible_paths}")

    # Также добавляем hiddenimports
    cv2_hiddenimports = ['cv2', 'cv2.cv2']

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=cv2_binaries,
    datas=[
        ('ui/main_window.ui', 'ui'),
        ('ui/about_dialog.ui', 'ui'),
        ('assets/app.ico', 'assets'),
        ('custom_dictionary.txt', '.'),
        ('docs/README.txt', '.'),
        ('dictionaries', 'dictionaries'),
    ] + cv2_datas,
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.uic',
        'PyQt6.sip',
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
    ] + cv2_hiddenimports,
    # Включаем Qt плагины и OpenCV для Linux
    collect_all=['PyQt6'] if not IS_WINDOWS else [],
    collect_submodules=['cv2'] if not IS_WINDOWS else [],
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

# Создаём splash-экран только для Windows (Linux не поддерживает tkinter в venv)
if IS_WINDOWS:
    splash = Splash(
        'assets/splash.png',
        binaries=a.binaries,
        datas=a.datas,
        text_pos=(200, 260),
        text_size=10,
        text_color='white',
        text_default='Загрузка...',
    )
    exe_args = [
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        splash,
        splash.binaries,
        [],
    ]
else:
    # Linux: без splash-экрана
    exe_args = [
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
    ]

exe = EXE(
    *exe_args,
    name='VideoSpellChecker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=IS_WINDOWS,  # UPX только для Windows (на Linux может зависать)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=not IS_WINDOWS,  # На Linux нужна консоль для отладки, на Windows скрываем
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/app.ico',  # Иконка приложения
)
