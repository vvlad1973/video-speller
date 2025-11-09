# Video Spell Checker

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green.svg)

Автоматическая проверка орфографии в видео. Программа извлекает кадры из видео, распознает текст и находит орфографические ошибки на русском и английском языках.

## Возможности

- ✅ **Графический интерфейс (GUI)** на базе PyQt6
- ✅ Извлечение кадров из видео с настраиваемым интервалом
- ✅ OCR распознавание текста на русском и английском языках (EasyOCR)
- ✅ Локальная проверка орфографии без интернета
- ✅ **Работает БЕЗ установки внешнего ПО** (всё через pip)
- ✅ **Пользовательский словарь** - добавляйте свои слова-исключения
- ✅ Сохранение только кадров с ошибками
- ✅ Подробные отчеты с тайм-кодами
- ✅ Автоматическое открытие папки с результатами

## Установка

### Вариант 0A: Portable версия для Windows (без установки Python)

#### Вариант 0A: ONE FILE - Один EXE файл (рекомендуется)

**Самый простой способ!** Один файл, запускается сразу:

1. Скачайте файл `dist/VideoSpellChecker.exe`
2. Запустите его
3. Готово!

**Размер:** 239 MB (всё в одном файле)
**Требования:** Windows 10/11 (64-bit), минимум 4GB RAM
**Подробности:** см. файл `dist/README_ONEFILE.txt`

#### Вариант 0B: ONE DIR - Папка с файлами

Более быстрый запуск, но нужно копировать всю папку:

1. Скопируйте всю папку `dist/VideoSpellChecker/` на ваш компьютер
2. Запустите `VideoSpellChecker.exe` внутри папки
3. Готово!

**Размер:** ~1.5 GB (распакованные библиотеки)
**Требования:** Windows 10/11 (64-bit), минимум 4GB RAM
**Подробности:** см. файл `dist/VideoSpellChecker/README_EXE.txt`

### Вариант 0B: Portable версия для Linux (без установки Python)

Portable приложение для Linux собирается с помощью PyInstaller:

```bash
# 1. Установите зависимости (если их нет)
sudo apt install libxcb-xinerama0 libxcb-cursor0 libgl1  # Ubuntu/Debian
# или
sudo dnf install libxcb xcb-util-cursor mesa-libGL       # Fedora

# 2. Соберите приложение
./build_dir.sh    # ONE DIR версия (рекомендуется для Linux)
# или
./build_one_file.sh    # ONE FILE версия

# 3. Запустите
cd dist/VideoSpellChecker
chmod +x VideoSpellChecker
./VideoSpellChecker
```

**Требования:** Linux (Ubuntu 20.04+, Fedora 34+), 64-bit, минимум 4GB RAM
**Подробности:** см. файл `dist/VideoSpellChecker/README_LINUX.txt`

**Установка в систему (опционально):**

```bash
# Копируем в /opt
sudo cp -r dist/VideoSpellChecker /opt/

# Редактируем пути в .desktop файле
nano /opt/VideoSpellChecker/VideoSpellChecker.desktop
# Измените Exec=/opt/VideoSpellChecker/VideoSpellChecker
#          Icon=/opt/VideoSpellChecker/app.ico

# Устанавливаем .desktop файл
sudo cp /opt/VideoSpellChecker/VideoSpellChecker.desktop /usr/share/applications/
sudo update-desktop-database
```

### Вариант 1: С виртуальным окружением (рекомендуется для разработчиков)

```bash
# 1. Создайте виртуальное окружение
python -m venv venv

# 2. Активируйте его
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Скачайте словари для проверки орфографии
python -m src.download_dictionaries

# 5. Запустите приложение
python main.py
```

### Вариант 2: Простая установка (только Python библиотеки)

```bash
# 1. Установите зависимости
pip install -r requirements.txt

# 2. Скачайте словари для проверки орфографии
python -m src.download_dictionaries
```

**Вот и всё!** Никаких дополнительных программ устанавливать не нужно.

При первом запуске:

- EasyOCR автоматически скачает модели для распознавания текста (~100MB)
- Программа предложит скачать словари, если они отсутствуют

**Обновление:** Программа использует Hunspell словари (как в LibreOffice) для качественной проверки орфографии без внешних зависимостей и зависаний.

### Перенос на другую машину

Для переноса проекта на другой компьютер:

1. **Скопируйте проект** (без папки `venv`):

   ```bash
   # Можно исключить из копирования:
   # - venv/
   # - __pycache__/
   # - screenshots_*/
   ```

2. **На новой машине** выполните установку:

   ```bash
   # Создайте новое виртуальное окружение
   python -m venv venv

   # Активируйте его
   venv\Scripts\activate  # Windows

   # Установите зависимости
   pip install -r requirements.txt

   # Скачайте словари (если их нет)
   python -m src.download_dictionaries
   ```

3. **Готово!** Запускайте `python main.py`

**Важно:** Файлы которые нужно скопировать:

- ✅ Все `.py` файлы
- ✅ `requirements.txt`
- ✅ `main_window.ui` и `about_dialog.ui`
- ✅ `custom_dictionary.txt`
- ✅ `dictionaries/` (если словари уже скачаны)
- ❌ НЕ копируйте `venv/` (создается заново на новой машине)

### Что устанавливается

- `opencv-python` - обработка видео и изображений
- `easyocr` - распознавание текста (без внешних зависимостей!)
- `spylls` - проверка орфографии Hunspell (полные словари LibreOffice)
- `torch` и `torchvision` - движок для нейросетей EasyOCR
- `PyQt6` - графический интерфейс

## Использование

### GUI версия (рекомендуется)

```bash
python main.py
```

Откроется графическое окно где вы можете:

1. Выбрать видео файл
2. Настроить интервал между кадрами
3. Запустить проверку
4. Наблюдать за процессом в реальном времени
5. Получить отчет с тайм-кодами
6. Автоматически открыть папку с результатами

### Консольная версия

```bash
python video_speller.py video.mp4
```

### С настраиваемым интервалом

```bash
python video_speller.py video.mp4 3
```

(извлечет кадры каждые 3 секунды)

### Программное использование

```python
from video_speller import VideoSpellChecker

# Создаем экземпляр проверки
checker = VideoSpellChecker(output_dir="my_results")

# Обрабатываем видео
checker.process_video("path/to/video.mp4", interval=2)
```

## Пользовательский словарь

Вы можете добавить свои слова, которые не должны помечаться как ошибки. Это полезно для:

- Технических терминов (AdaptON, PyTorch, EasyOCR)
- Названий брендов (YouTube, GitHub)
- Специфических слов вашего проекта

Отредактируйте файл `custom_dictionary.txt`:

```bash
# Добавьте свои слова (по одному на строку)
AdaptON
PyTorch
знакомиться
информационные
```

**Подробная документация:** [CUSTOM_DICTIONARY.md](CUSTOM_DICTIONARY.md)

## Результаты

После обработки будет создана папка `screenshots_<имя_видео>_errors` в той же директории, где находится программа. В ней будут:

- `frame_XXX_errors.png` - скриншоты кадров с ошибками
- `frame_XXX_errors.txt` - текстовые файлы с деталями:
  - Номер кадра и точное время (тайм-код)
  - Полный распознанный текст
  - Список найденных ошибок
- `report-YYYYMMDD-HHMMSS.txt` - **итоговый отчёт** о проверке:
  - Дата и время проверки
  - Параметры обработки (интервал, временной диапазон)
  - Статистика по всем обработанным кадрам
  - Детальная информация по каждому кадру с ошибками
  - Тайм-коды всех найденных ошибок

## Пример вывода

```bash
⏳ Загрузка моделей OCR (это может занять время при первом запуске)...
✓ EasyOCR загружен
✓ Словари для проверки орфографии загружены

==============================================================
Обработка видео: presentation.mp4
==============================================================

✓ Извлечено 150 кадров из видео

Обработка кадра 0...
  ℹ Распознанный текст: Привет мир! Это тестовое видео...
  ✗ Найдено ошибок: 2
  ✓ Сохранено: screenshots_with_errors\frame_0_errors.jpg

...

==============================================================
ОБРАБОТКА ЗАВЕРШЕНА!
==============================================================
Всего обработано кадров: 150
Кадров с ошибками: 5
Всего найдено ошибок: 12
Результаты сохранены в: C:\Repositories\video-speller\screenshots_presentation_errors
==============================================================
```

## Устранение неполадок

### Медленная первая загрузка

- При первом запуске EasyOCR скачивает модели (~100MB)
- Это происходит один раз, последующие запуски будут быстрее

### Ошибка "Numpy is not available" или проблемы с NumPy

Если при обработке видео возникает ошибка "Numpy is not available" или проблемы совместимости:

**Решение:** Установите совместимые версии библиотек:

```bash
pip install "numpy<2" "opencv-python<4.10" "opencv-python-headless<4.10"
pip install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cpu
```

Эти версии полностью совместимы друг с другом и работают из коробки.

### Ошибки установки PyTorch

- Если `pip install -r requirements.txt` не работает, установите PyTorch отдельно:

  ```bash
  pip install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cpu
  pip install -r requirements.txt
  ```

### Текст не распознается или плохо распознается

- Проверьте качество и разрешение видео
- EasyOCR работает лучше с четким, контрастным текстом
- Попробуйте увеличить размер шрифта в видео

### Слишком много ложных срабатываний

- OCR может некорректно распознавать некоторые символы
- В [video_speller.py:105](video_speller.py#L105) можно изменить минимальную длину слова (сейчас 3 символа)
- Можно добавить свои слова в словарь исключений

### Программа использует много памяти

- EasyOCR загружает модели в память (~500MB)
- Это нормально для нейросетевых моделей OCR

## Создание EXE сборки (для разработчиков)

### Сборка на Windows

Чтобы создать portable EXE версию приложения:

```bash
# 1. Установите PyInstaller
pip install pyinstaller

# 2. Выберите режим сборки:

# Вариант A: ONE FILE (монолитная сборка)
build_one_file.bat
# или вручную:
pyinstaller --clean video_speller_one_file.spec

# Вариант B: ONE DIR (немонолитная сборка)
build_dir.bat
# или вручную:
pyinstaller --clean video_speller_dir.spec
```

### Сборка на Linux

Чтобы создать portable версию для Linux:

```bash
# 1. Установите PyInstaller и системные зависимости
pip install pyinstaller

# Примечание: Splash-экран недоступен на Linux из-за ограничений tkinter в venv
# Сборка будет выполнена без splash-экрана

# 2. Выберите режим сборки:

# Вариант A: ONE FILE (монолитная сборка)
./build_one_file.sh
# или вручную:
pyinstaller --clean video_speller_one_file.spec

# Вариант B: ONE DIR (немонолитная сборка) - рекомендуется для Linux
./build_dir.sh
# или вручную:
pyinstaller --clean video_speller_dir.spec
```

**Примечание:** На Linux splash-экран отключен автоматически из-за проблем совместимости tkinter с виртуальными окружениями.

### Установка на Linux (после сборки)

После сборки на Linux вы можете установить приложение в систему для удобного запуска:

```bash
cd dist/  # или dist/VideoSpellChecker/ для ONE DIR версии
./install_linux.sh
```

Скрипт установки автоматически:
- Установит приложение в `~/.local/bin/VideoSpellChecker/`
- Установит PNG иконки в системную директорию `~/.local/share/icons/`
- Создаст .desktop файл для меню приложений
- Обновит кэш иконок и базу приложений

После установки приложение можно запустить:
- Из меню приложений (Video Spell Checker)
- Из терминала: `~/.local/bin/VideoSpellChecker/VideoSpellChecker`

**Удаление:**
```bash
rm -rf ~/.local/bin/VideoSpellChecker
rm -f ~/.local/share/applications/VideoSpellChecker.desktop
rm -f ~/.local/share/icons/hicolor/*/apps/VideoSpellChecker.png
```

### Готовые bat-файлы для сборки

Проект включает удобные bat-файлы для быстрой сборки на Windows:

- **`build_one_file.bat`** - создаёт ONE FILE версию (один exe файл)
- **`build_dir.bat`** - создаёт ONE DIR версию (папка с файлами)

Эти скрипты автоматически:

1. Запускают PyInstaller с соответствующим spec-файлом
2. Копируют дополнительные файлы в dist:
   - `README.txt` (инструкция для пользователей exe-версии)
   - `app.ico` (иконка приложения)
   - `dictionaries/` (словари для проверки орфографии)

Spec-файлы уже настроены и включают:

- Иконку приложения (`app.ico`)
- **Splash-экран** (`splash.png`) - показывается во время распаковки (только Windows)
- UI файлы (`.ui`)
- Пользовательский словарь
- Все необходимые библиотеки
- Автоматическое определение платформы (Windows/Linux)

### Выбор режима сборки

Проект включает два готовых spec-файла:

**ONE FILE (монолитная сборка):**

```bash
pyinstaller --clean video_speller_one_file.spec
```

- Всё упаковано в один EXE файл
- Проще распространять
- Медленнее первый запуск (распаковка во временную папку)
- Размер: ~239 MB (Windows), ~500-700 MB (Linux)
- Результат: `dist/VideoSpellChecker.exe` или `dist/VideoSpellChecker`

**ONE DIR (немонолитная сборка):**

```bash
pyinstaller --clean video_speller_dir.spec
```

- EXE + папка с библиотеками
- Быстрее запускается
- Меньше использует RAM
- Проще обновлять отдельные компоненты
- Размер: ~1.5 GB (распакованные библиотеки)
- Результат: `dist/VideoSpellChecker/` (директория)

**Примечание:**

- Размер итоговой сборки большой из-за PyTorch и других ML библиотек
- Linux-сборки больше Windows из-за необходимости упаковывать системные библиотеки для портативности

### Структура dist после сборки

**ONE FILE версия** (`dist/`):

```text
dist/
├── VideoSpellChecker[.exe]     # Основное приложение (239 MB Windows / 500-700 MB Linux)
├── README.txt                  # Инструкция для пользователей
├── app.ico                     # Иконка приложения (Windows)
├── app.png                     # Иконка приложения (Linux, 256x256)
├── app-256px.png              # Дополнительная иконка (Linux)
├── install_linux.sh           # Скрипт установки (Linux)
├── VideoSpellChecker.desktop  # Desktop entry файл (Linux)
└── dictionaries/              # Словари для проверки орфографии
    ├── ru_RU.aff
    ├── ru_RU.dic
    ├── en_US.aff
    └── en_US.dic
```

**ONE DIR версия** (`dist/VideoSpellChecker/`):

```text
dist/VideoSpellChecker/
├── VideoSpellChecker[.exe]     # Основное приложение
├── README.txt                  # Инструкция для пользователей
├── app.ico                     # Иконка приложения (Windows)
├── app.png                     # Иконка приложения (Linux, 256x256)
├── app-256px.png              # Дополнительная иконка (Linux)
├── install_linux.sh           # Скрипт установки (Linux)
├── VideoSpellChecker.desktop  # Desktop entry файл (Linux)
├── dictionaries/           # Словари для проверки орфографии
├── _internal/              # Библиотеки и зависимости
└── ... (множество DLL и файлов библиотек)
```

### Настройка splash-экрана

Приложение использует splash-экран (`splash.png`), который отображается во время распаковки ONEFILE версии.

Чтобы создать свой splash-экран:

1. Создайте изображение `splash.png` (рекомендуемый размер: 400x300 пикселей)
2. Поместите его в корневую папку проекта
3. Пересоберите приложение

Или используйте Python для генерации:

```python
from PIL import Image, ImageDraw, ImageFont

width, height = 400, 300
img = Image.new('RGB', (width, height), color='#2c3e50')
draw = ImageDraw.Draw(img)

# Добавьте свой текст и графику
font = ImageFont.truetype('arial.ttf', 32)
draw.text((100, 100), 'Ваш текст', fill='white', font=font)

img.save('splash.png')
```

Splash-экран автоматически закрывается после полной загрузки приложения.

### Создание иконок для Linux

Проект включает скрипт для конвертации `.ico` иконки в PNG форматы для Linux:

```bash
python convert_icon.py
```

Этот скрипт создаст:
- `assets/app.png` (256x256) - основная иконка
- `assets/app_256.png` (256x256)
- `assets/app_128.png` (128x128)
- `assets/app_48.png` (48x48)

PNG иконки автоматически копируются в dist при сборке на Linux и используются скриптом установки `install_linux.sh`.

**Создание собственных иконок:**

Если вы хотите использовать свою иконку:

1. Создайте PNG изображения нужных размеров (48x48, 128x128, 256x256)
2. Сохраните их в папку `assets/` с именами `app-48px.png`, `app-128px.png`, `app-256px.png`
3. Создайте основную иконку `assets/app.png` (256x256)
4. Пересоберите приложение

Иконки будут автоматически включены в сборку и установлены при запуске `install_linux.sh`.

## Лицензия

MIT License with Commercial Use

Для коммерческого использования требуется согласование условий с автором.
Подробности см. в файле [LICENSE](LICENSE).
