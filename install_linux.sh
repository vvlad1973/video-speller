#!/bin/bash
# Скрипт установки VideoSpellChecker для Linux
# Устанавливает приложение, иконку и .desktop файл

echo "=========================================="
echo "Installing VideoSpellChecker for Linux"
echo "=========================================="
echo

# Проверяем, запущен ли скрипт из директории dist
if [ ! -f "VideoSpellChecker" ]; then
    echo "ERROR: VideoSpellChecker binary not found!"
    echo "Please run this script from the dist directory after building."
    exit 1
fi

# Определяем директорию установки
INSTALL_DIR="$HOME/.local/bin/VideoSpellChecker"
ICON_DIR="$HOME/.local/share/icons/hicolor"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "Installation paths:"
echo "  Binary: $INSTALL_DIR"
echo "  Icon: $ICON_DIR/256x256/apps/VideoSpellChecker.png"
echo "  Desktop file: $DESKTOP_DIR/VideoSpellChecker.desktop"
echo

# Создаём директории
mkdir -p "$INSTALL_DIR"
mkdir -p "$ICON_DIR/256x256/apps"
mkdir -p "$ICON_DIR/128x128/apps"
mkdir -p "$ICON_DIR/48x48/apps"
mkdir -p "$DESKTOP_DIR"

# Копируем приложение
echo "Copying application files..."
cp -r * "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/VideoSpellChecker"
echo "[OK] Application files copied"

# Копируем иконки
if [ -f "app.png" ] || [ -f "app-256px.png" ]; then
    # Основная иконка 256x256
    if [ -f "app-256px.png" ]; then
        cp app-256px.png "$ICON_DIR/256x256/apps/VideoSpellChecker.png"
    elif [ -f "app.png" ]; then
        cp app.png "$ICON_DIR/256x256/apps/VideoSpellChecker.png"
    fi
    echo "[OK] 256x256 icon installed"

    # Дополнительные размеры если есть
    if [ -f "app-128px.png" ]; then
        mkdir -p "$ICON_DIR/128x128/apps"
        cp app-128px.png "$ICON_DIR/128x128/apps/VideoSpellChecker.png"
        echo "[OK] 128x128 icon installed"
    fi

    if [ -f "app-48px.png" ]; then
        mkdir -p "$ICON_DIR/48x48/apps"
        cp app-48px.png "$ICON_DIR/48x48/apps/VideoSpellChecker.png"
        echo "[OK] 48x48 icon installed"
    fi
else
    echo "[WARNING] PNG icons not found, skipping icon installation"
fi

# Создаём .desktop файл
echo "Creating desktop entry..."
cat > "$DESKTOP_DIR/VideoSpellChecker.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Video Spell Checker
Comment=Автоматическая проверка орфографии в видео
Comment[en]=Automatic spell checking in videos
Exec=$INSTALL_DIR/VideoSpellChecker
Icon=VideoSpellChecker
Terminal=false
Categories=AudioVideo;Video;Utility;
Keywords=video;spell;checker;ocr;subtitle;
StartupNotify=true
MimeType=video/mp4;video/x-msvideo;video/quicktime;video/x-matroska;
EOF

chmod +x "$DESKTOP_DIR/VideoSpellChecker.desktop"
echo "[OK] Desktop entry created"

# Обновляем кэш иконок
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f -t "$ICON_DIR" 2>/dev/null
    echo "[OK] Icon cache updated"
fi

# Обновляем базу .desktop файлов
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null
    echo "[OK] Desktop database updated"
fi

echo
echo "=========================================="
echo "Installation completed successfully!"
echo "=========================================="
echo
echo "You can now:"
echo "  1. Run from terminal: $INSTALL_DIR/VideoSpellChecker"
echo "  2. Find 'Video Spell Checker' in your application menu"
echo
echo "To uninstall, run:"
echo "  rm -rf $INSTALL_DIR"
echo "  rm -f $DESKTOP_DIR/VideoSpellChecker.desktop"
echo "  rm -f $ICON_DIR/*/apps/VideoSpellChecker.png"
echo
