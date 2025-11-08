#!/bin/bash
echo "============================================"
echo "Building ONE DIR version..."
echo "============================================"
echo

pyinstaller --clean video_speller_dir.spec

if [ $? -eq 0 ]; then
    echo
    echo "============================================"
    echo "Copying additional files to dist..."
    echo "============================================"

    # Copy README (Linux version)
    if [ -f "README_LINUX.txt" ]; then
        cp -f README_LINUX.txt dist/VideoSpellChecker/README.txt
        echo "[OK] README.txt copied (Linux version)"
    elif [ -f "README_EXE.txt" ]; then
        cp -f README_EXE.txt dist/VideoSpellChecker/README.txt
        echo "[OK] README.txt copied"
    fi

    # Copy app.ico
    if [ -f "app.ico" ]; then
        cp -f app.ico dist/VideoSpellChecker/app.ico
        echo "[OK] app.ico copied"
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
