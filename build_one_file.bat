@echo off
echo ============================================
echo Building ONE FILE version...
echo ============================================

pyinstaller --clean video_speller_one_file.spec

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo Copying additional files to dist...
    echo ============================================

    REM Copy README
    if exist docs\README.txt (
        copy /Y docs\README.txt dist\README.txt
        echo [OK] README.txt copied
    )

    REM Copy dictionaries folder
    if exist dictionaries (
        xcopy /E /I /Y dictionaries dist\dictionaries
        echo [OK] dictionaries folder copied
    )

    echo.
    echo ============================================
    echo Build completed successfully!
    echo ============================================
    echo.
    echo Output: dist\VideoSpellChecker.exe
    echo Size: ~239 MB
    echo.
) else (
    echo.
    echo ============================================
    echo Build FAILED!
    echo ============================================
    exit /b 1
)
