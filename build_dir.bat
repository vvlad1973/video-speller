@echo off
echo ============================================
echo Building ONE DIR version...
echo ============================================

pyinstaller --clean video_speller_dir.spec

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo Copying additional files to dist...
    echo ============================================

    REM Copy README
    if exist README_EXE.txt (
        copy /Y README_EXE.txt dist\VideoSpellChecker\README.txt
        echo [OK] README.txt copied
    )

    REM Copy app.ico
    if exist app.ico (
        copy /Y app.ico dist\VideoSpellChecker\app.ico
        echo [OK] app.ico copied
    )

    REM Copy dictionaries folder
    if exist dictionaries (
        xcopy /E /I /Y dictionaries dist\VideoSpellChecker\dictionaries
        echo [OK] dictionaries folder copied
    )

    echo.
    echo ============================================
    echo Build completed successfully!
    echo ============================================
    echo.
    echo Output: dist\VideoSpellChecker\
    echo Size: ~1.5 GB
    echo.
) else (
    echo.
    echo ============================================
    echo Build FAILED!
    echo ============================================
    exit /b 1
)
