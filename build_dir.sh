#!/bin/bash
echo "============================================"
echo "Building ONE DIR version..."
echo "============================================"
echo

# Используем Python из текущего окружения (venv)
python -m PyInstaller --clean video_speller_dir.spec

if [ $? -eq 0 ]; then
    echo
    echo "============================================"
    echo "Copying additional files to dist..."
    echo "============================================"

    # Copy README (Linux version)
    if [ -f "docs/README_LINUX.txt" ]; then
        cp -f docs/README_LINUX.txt dist/VideoSpellChecker/README.txt
        echo "[OK] README.txt copied (Linux version)"
    fi

    # Copy app.ico
    if [ -f "assets/app.ico" ]; then
        cp -f assets/app.ico dist/VideoSpellChecker/app.ico
        echo "[OK] app.ico copied"
    fi

    # Copy PNG icons for Linux
    if [ -f "assets/app.png" ]; then
        cp -f assets/app.png dist/VideoSpellChecker/app.png
        echo "[OK] app.png copied"
    fi
    if [ -f "assets/app-256px.png" ]; then
        cp -f assets/app-256px.png dist/VideoSpellChecker/app-256px.png
        echo "[OK] app-256px.png copied"
    fi

    # Copy dictionaries folder
    if [ -d "dictionaries" ]; then
        cp -rf dictionaries dist/VideoSpellChecker/
        echo "[OK] dictionaries folder copied"
    fi

    # Copy .desktop file (Linux)
    if [ -f "VideoSpellChecker.desktop" ]; then
        cp -f VideoSpellChecker.desktop dist/VideoSpellChecker/
        echo "[OK] VideoSpellChecker.desktop copied"
    fi

    # Copy installation script
    if [ -f "install_linux.sh" ]; then
        cp -f install_linux.sh dist/VideoSpellChecker/
        chmod +x dist/VideoSpellChecker/install_linux.sh
        echo "[OK] install_linux.sh copied"
    fi

    # Make the binary executable
    if [ -f "dist/VideoSpellChecker/VideoSpellChecker" ]; then
        chmod +x dist/VideoSpellChecker/VideoSpellChecker
        echo "[OK] VideoSpellChecker made executable"
    fi

    echo
    echo "============================================"
    echo "Build completed successfully!"
    echo "============================================"
    echo
    echo "Output: dist/VideoSpellChecker/"
    echo "Size: ~1.5 GB"
    echo
else
    echo
    echo "============================================"
    echo "Build FAILED!"
    echo "============================================"
    exit 1
fi
