#!/bin/bash
echo "============================================"
echo "Building ONE FILE version..."
echo "============================================"
echo

pyinstaller --clean video_speller_one_file.spec

if [ $? -eq 0 ]; then
    echo
    echo "============================================"
    echo "Copying additional files to dist..."
    echo "============================================"

    # Copy README (Linux version)
    if [ -f "docs/README_LINUX.txt" ]; then
        cp -f docs/README_LINUX.txt dist/README.txt
        echo "[OK] README.txt copied (Linux version)"
    fi

    # Copy app.ico
    if [ -f "assets/app.ico" ]; then
        cp -f assets/app.ico dist/app.ico
        echo "[OK] app.ico copied"
    fi

    # Copy dictionaries folder
    if [ -d "dictionaries" ]; then
        cp -rf dictionaries dist/
        echo "[OK] dictionaries folder copied"
    fi

    # Copy .desktop file (Linux)
    if [ -f "VideoSpellChecker.desktop" ]; then
        cp -f VideoSpellChecker.desktop dist/
        echo "[OK] VideoSpellChecker.desktop copied"
    fi

    # Make the binary executable
    if [ -f "dist/VideoSpellChecker" ]; then
        chmod +x dist/VideoSpellChecker
        echo "[OK] VideoSpellChecker made executable"
    fi

    echo
    echo "============================================"
    echo "Build completed successfully!"
    echo "============================================"
    echo
    echo "Output: dist/VideoSpellChecker"
    echo "Size: ~239 MB"
    echo
else
    echo
    echo "============================================"
    echo "Build FAILED!"
    echo "============================================"
    exit 1
fi
