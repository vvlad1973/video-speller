# Video Spell Checker

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green.svg)

Automatic spell checking in videos. The application extracts frames from videos, recognizes text, and finds spelling errors in Russian and English.

## Features

- ✅ **Graphical User Interface (GUI)** based on PyQt6
- ✅ Extract frames from video with customizable interval
- ✅ OCR text recognition in Russian and English (EasyOCR)
- ✅ Local spell checking without internet connection
- ✅ **Works WITHOUT installing external software** (everything via pip)
- ✅ **Custom dictionary** - add your own exception words
- ✅ Save only frames with errors
- ✅ Detailed reports with timecodes
- ✅ Automatic opening of results folder

## Installation

### Option 0A: Portable version for Windows (no Python installation required)

#### Option 0A: ONE FILE - Single EXE file (recommended)

**The easiest way!** One file, runs immediately:

1. Download the `dist/VideoSpellChecker.exe` file
2. Run it
3. Done!

**Size:** 239 MB (everything in one file)
**Requirements:** Windows 10/11 (64-bit), minimum 4GB RAM
**Details:** see file `dist/README_ONEFILE.txt`

#### Option 0B: ONE DIR - Folder with files

Faster startup, but need to copy the entire folder:

1. Copy the entire `dist/VideoSpellChecker/` folder to your computer
2. Run `VideoSpellChecker.exe` inside the folder
3. Done!

**Size:** ~1.5 GB (unpacked libraries)
**Requirements:** Windows 10/11 (64-bit), minimum 4GB RAM
**Details:** see file `dist/VideoSpellChecker/README_EXE.txt`

### Option 0B: Portable version for Linux (no Python installation required)

Portable application for Linux is built using PyInstaller:

```bash
# 1. Install dependencies (if not present)
sudo apt install libxcb-xinerama0 libxcb-cursor0 libgl1  # Ubuntu/Debian
# or
sudo dnf install libxcb xcb-util-cursor mesa-libGL       # Fedora

# 2. Build the application
./build_dir.sh    # ONE DIR version (recommended for Linux)
# or
./build_one_file.sh    # ONE FILE version

# 3. Run
cd dist/VideoSpellChecker
chmod +x VideoSpellChecker
./VideoSpellChecker
```

**Requirements:** Linux (Ubuntu 20.04+, Fedora 34+), 64-bit, minimum 4GB RAM
**Details:** see file `dist/VideoSpellChecker/README_LINUX.txt`

**System installation (optional):**

```bash
# Copy to /opt
sudo cp -r dist/VideoSpellChecker /opt/

# Edit paths in .desktop file
nano /opt/VideoSpellChecker/VideoSpellChecker.desktop
# Change Exec=/opt/VideoSpellChecker/VideoSpellChecker
#        Icon=/opt/VideoSpellChecker/app.ico

# Install .desktop file
sudo cp /opt/VideoSpellChecker/VideoSpellChecker.desktop /usr/share/applications/
sudo update-desktop-database
```

### Option 1: With virtual environment (recommended for developers)

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download dictionaries for spell checking
python -m src.download_dictionaries

# 5. Run the application
python main.py
```

### Option 2: Simple installation (Python libraries only)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download dictionaries for spell checking
python -m src.download_dictionaries
```

**That's it!** No additional software needs to be installed.

On first run:

- EasyOCR will automatically download models for text recognition (~100MB)
- The application will prompt to download dictionaries if they are missing

**Update:** The application uses Hunspell dictionaries (like LibreOffice) for quality spell checking without external dependencies and freezing.

### Transfer to another machine

To transfer the project to another computer:

1. **Copy the project** (without the `venv` folder):

   ```bash
   # Can be excluded from copying:
   # - venv/
   # - __pycache__/
   # - screenshots_*/
   ```

2. **On the new machine** perform installation:

   ```bash
   # Create new virtual environment
   python -m venv venv

   # Activate it
   venv\Scripts\activate  # Windows

   # Install dependencies
   pip install -r requirements.txt

   # Download dictionaries (if missing)
   python -m src.download_dictionaries
   ```

3. **Done!** Run `python main.py`

**Important:** Files that need to be copied:

- ✅ All `.py` files
- ✅ `requirements.txt`
- ✅ `main_window.ui` and `about_dialog.ui`
- ✅ `custom_dictionary.txt`
- ✅ `dictionaries/` (if dictionaries are already downloaded)
- ❌ DO NOT copy `venv/` (created anew on the new machine)

### What gets installed

- `opencv-python` - video and image processing
- `easyocr` - text recognition (without external dependencies!)
- `spylls` - Hunspell spell checking (complete LibreOffice dictionaries)
- `torch` and `torchvision` - engine for EasyOCR neural networks
- `PyQt6` - graphical user interface

## Usage

### GUI version (recommended)

```bash
python main.py
```

A graphical window will open where you can:

1. Select a video file
2. Configure the interval between frames
3. Start checking
4. Monitor the process in real-time
5. Get a report with timecodes
6. Automatically open the results folder

### Console version

```bash
python video_speller.py video.mp4
```

### With customizable interval

```bash
python video_speller.py video.mp4 3
```

(will extract frames every 3 seconds)

### Programmatic usage

```python
from video_speller import VideoSpellChecker

# Create checker instance
checker = VideoSpellChecker(output_dir="my_results")

# Process video
checker.process_video("path/to/video.mp4", interval=2)
```

## Custom Dictionary

You can add your own words that should not be marked as errors. This is useful for:

- Technical terms (AdaptON, PyTorch, EasyOCR)
- Brand names (YouTube, GitHub)
- Specific words of your project

Edit the `custom_dictionary.txt` file:

```bash
# Add your words (one per line)
AdaptON
PyTorch
знакомиться
информационные
```

**Detailed documentation:** [CUSTOM_DICTIONARY.md](CUSTOM_DICTIONARY.md)

## Results

After processing, a folder `screenshots_<video_name>_errors` will be created in the same directory where the program is located. It will contain:

- `frame_XXX_errors.png` - screenshots of frames with errors
- `frame_XXX_errors.txt` - text files with details:
  - Frame number and exact time (timecode)
  - Full recognized text
  - List of found errors
- `report-YYYYMMDD-HHMMSS.txt` - **final report** on the check:
  - Date and time of check
  - Processing parameters (interval, time range)
  - Statistics for all processed frames
  - Detailed information for each frame with errors
  - Timecodes of all found errors

## Example Output

```bash
⏳ Loading OCR models (this may take time on first run)...
✓ EasyOCR loaded
✓ Spell checking dictionaries loaded

==============================================================
Processing video: presentation.mp4
==============================================================

✓ Extracted 150 frames from video

Processing frame 0...
  ℹ Recognized text: Hello world! This is a test video...
  ✗ Errors found: 2
  ✓ Saved: screenshots_with_errors\frame_0_errors.jpg

...

==============================================================
PROCESSING COMPLETED!
==============================================================
Total frames processed: 150
Frames with errors: 5
Total errors found: 12
Results saved in: C:\Repositories\video-speller\screenshots_presentation_errors
==============================================================
```

## Troubleshooting

### Slow first loading

- On first run, EasyOCR downloads models (~100MB)
- This happens once, subsequent runs will be faster

### Error "Numpy is not available" or NumPy compatibility issues

If during video processing you get "Numpy is not available" error or compatibility issues:

**Solution:** Install compatible library versions:

```bash
pip install "numpy<2" "opencv-python<4.10" "opencv-python-headless<4.10"
pip install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cpu
```

These versions are fully compatible with each other and work out of the box.

### PyTorch installation errors

- If `pip install -r requirements.txt` doesn't work, install PyTorch separately:

  ```bash
  pip install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cpu
  pip install -r requirements.txt
  ```

### Text is not recognized or poorly recognized

- Check the quality and resolution of the video
- EasyOCR works better with clear, high-contrast text
- Try increasing the font size in the video

### Too many false positives

- OCR may incorrectly recognize some characters
- In [video_speller.py:105](video_speller.py#L105) you can change the minimum word length (currently 3 characters)
- You can add your own words to the exception dictionary

### Program uses a lot of memory

- EasyOCR loads models into memory (~500MB)
- This is normal for neural network OCR models

## Creating EXE build (for developers)

### Building on Windows

To create a portable EXE version of the application:

```bash
# 1. Install PyInstaller
pip install pyinstaller

# 2. Choose build mode:

# Option A: ONE FILE (monolithic build)
build_one_file.bat
# or manually:
pyinstaller --clean video_speller_one_file.spec

# Option B: ONE DIR (non-monolithic build)
build_dir.bat
# or manually:
pyinstaller --clean video_speller_dir.spec
```

### Building on Linux

To create a portable Linux version:

```bash
# 1. Install PyInstaller and system dependencies
pip install pyinstaller

# Note: Splash screen is not available on Linux due to tkinter limitations in venv
# Build will proceed without splash screen

# 2. Choose build mode:

# Option A: ONE FILE (monolithic build)
./build_one_file.sh
# or manually:
pyinstaller --clean video_speller_one_file.spec

# Option B: ONE DIR (non-monolithic build) - recommended for Linux
./build_dir.sh
# or manually:
pyinstaller --clean video_speller_dir.spec
```

**Note:** On Linux, the splash screen is automatically disabled due to tkinter compatibility issues with virtual environments.

### Installing on Linux (after build)

After building on Linux, you can install the application into your system for convenient launching:

```bash
cd dist/  # or dist/VideoSpellChecker/ for ONE DIR version
./install_linux.sh
```

The installation script automatically:
- Installs the application to `~/.local/bin/VideoSpellChecker/`
- Installs PNG icons to system directory `~/.local/share/icons/`
- Creates a .desktop file for application menu
- Updates icon cache and application database

After installation, the application can be launched:
- From application menu (Video Spell Checker)
- From terminal: `~/.local/bin/VideoSpellChecker/VideoSpellChecker`

**Uninstall:**
```bash
rm -rf ~/.local/bin/VideoSpellChecker
rm -f ~/.local/share/applications/VideoSpellChecker.desktop
rm -f ~/.local/share/icons/hicolor/*/apps/VideoSpellChecker.png
```

### Ready-made bat files for building

The project includes convenient bat files for quick building on Windows:

- **`build_one_file.bat`** - creates ONE FILE version (single exe file)
- **`build_dir.bat`** - creates ONE DIR version (folder with files)

These scripts automatically:

1. Run PyInstaller with the corresponding spec file
2. Copy additional files to dist:
   - `README.txt` (instructions for exe version users)
   - `app.ico` (application icon)
   - `dictionaries/` (dictionaries for spell checking)

Spec files are already configured and include:

- Application icon (`app.ico`)
- **Splash screen** (`splash.png`) - shown during unpacking (Windows only)
- UI files (`.ui`)
- Custom dictionary
- All necessary libraries
- Automatic platform detection (Windows/Linux)

### Choosing build mode

The project includes two ready-made spec files:

**ONE FILE (monolithic build):**

```bash
pyinstaller --clean video_speller_one_file.spec
```

- Everything packed into one EXE file
- Easier to distribute
- Slower first launch (unpacking to temporary folder)
- Size: ~239 MB (Windows), ~500-700 MB (Linux)
- Result: `dist/VideoSpellChecker.exe` or `dist/VideoSpellChecker`

**ONE DIR (non-monolithic build):**

```bash
pyinstaller --clean video_speller_dir.spec
```

- EXE + folder with libraries
- Faster startup
- Uses less RAM
- Easier to update individual components
- Size: ~1.5 GB (unpacked libraries)
- Result: `dist/VideoSpellChecker/` (directory)

**Note:**

- The size of the final build is large due to PyTorch and other ML libraries
- Linux builds are larger than Windows builds due to the need to package system libraries for portability

### Dist structure after building

**ONE FILE version** (`dist/`):

```text
dist/
├── VideoSpellChecker[.exe]     # Main application (239 MB Windows / 500-700 MB Linux)
├── README.txt                  # User instructions
├── app.ico                     # Application icon (Windows)
├── app.png                     # Application icon (Linux, 256x256)
├── app-256px.png              # Additional icon (Linux)
├── install_linux.sh           # Installation script (Linux)
├── VideoSpellChecker.desktop  # Desktop entry file (Linux)
└── dictionaries/           # Spell checking dictionaries
    ├── ru_RU.aff
    ├── ru_RU.dic
    ├── en_US.aff
    └── en_US.dic
```

**ONE DIR version** (`dist/VideoSpellChecker/`):

```text
dist/VideoSpellChecker/
├── VideoSpellChecker[.exe]     # Main application
├── README.txt                  # User instructions
├── app.ico                     # Application icon (Windows)
├── app.png                     # Application icon (Linux, 256x256)
├── app-256px.png              # Additional icon (Linux)
├── install_linux.sh           # Installation script (Linux)
├── VideoSpellChecker.desktop  # Desktop entry file (Linux)
├── dictionaries/              # Spell checking dictionaries
├── _internal/                 # Libraries and dependencies
└── ... (many DLLs and library files)
```

### Configuring splash screen

The application uses a splash screen (`splash.png`) that is displayed during ONEFILE version unpacking.

To create your own splash screen:

1. Create an image `splash.png` (recommended size: 400x300 pixels)
2. Place it in the project root folder
3. Rebuild the application

Or use Python to generate:

```python
from PIL import Image, ImageDraw, ImageFont

width, height = 400, 300
img = Image.new('RGB', (width, height), color='#2c3e50')
draw = ImageDraw.Draw(img)

# Add your text and graphics
font = ImageFont.truetype('arial.ttf', 32)
draw.text((100, 100), 'Your text', fill='white', font=font)

img.save('splash.png')
```

The splash screen automatically closes after the application is fully loaded.

### Creating icons for Linux

The project includes a script to convert `.ico` icon to PNG formats for Linux:

```bash
python convert_icon.py
```

This script will create:
- `assets/app.png` (256x256) - main icon
- `assets/app_256.png` (256x256)
- `assets/app_128.png` (128x128)
- `assets/app_48.png` (48x48)

PNG icons are automatically copied to dist during Linux builds and used by the `install_linux.sh` installation script.

**Creating custom icons:**

If you want to use your own icon:

1. Create PNG images of required sizes (48x48, 128x128, 256x256)
2. Save them to `assets/` folder with names `app-48px.png`, `app-128px.png`, `app-256px.png`
3. Create main icon `assets/app.png` (256x256)
4. Rebuild the application

Icons will be automatically included in the build and installed when running `install_linux.sh`.

## License

MIT License with Commercial Use

For commercial use, terms must be agreed upon with the author.
See [LICENSE](LICENSE) file for details.
