# Быстрый старт - Video Spell Checker

## Установка (5 минут)

```bash
# 1. Установите зависимости
pip install -r requirements.txt

# 2. Скачайте словари
python download_dictionaries.py
```

## Использование

### Графический интерфейс (рекомендуется)

```bash
python gui.py
```

1. Нажмите "Обзор" и выберите видео
2. Установите интервал между кадрами (по умолчанию 2 секунды)
3. Нажмите "Начать проверку"
4. Дождитесь завершения
5. Результаты откроются автоматически

### Консольная версия

```bash
python video_speller.py video.mp4
```

## Добавление своих слов

Отредактируйте `custom_dictionary.txt`:

```bash
# Технические термины
PyTorch
TensorFlow
AdaptON

# Ваши специфические слова
знакомиться
информационные
```

Сохраните и перезапустите программу.

## Результаты

Программа создаст папку `screenshots_<имя_видео>_errors` с:

- Скриншотами кадров где найдены ошибки (`frame_XXX_errors.png`)
- Текстовыми файлами с деталями ошибок и тайм-кодами (`frame_XXX_errors.txt`)
- Итоговым отчётом о проверке (`report-YYYYMMDD-HHMMSS.txt`)

## Решение проблем

### Ошибка DLL при запуске

```bash
pip uninstall torch torchvision -y
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Слишком много ложных срабатываний

Добавьте правильные слова в `custom_dictionary.txt`

### Программа зависает

Проверьте, что используется версия с Hunspell (не LanguageTool)

## Создание portable версии (для разработчиков)

### Windows

```bash
# 1. Установите PyInstaller
pip install pyinstaller

# 2. Запустите сборку
build_one_file.bat    # Один exe файл (239 MB)
# или
build_dir.bat         # Папка с файлами (~1.5 GB)
```

### Linux

```bash
# 1. Установите PyInstaller
pip install pyinstaller

# 2. Запустите сборку
./build_one_file.sh   # Один файл (239 MB)
# или
./build_dir.sh        # Папка с файлами (~1.5 GB)

# 3. Запустите приложение
cd dist/VideoSpellChecker
./VideoSpellChecker
```

**Установка в систему (Linux):**

```bash
sudo cp -r dist/VideoSpellChecker /opt/
sudo cp /opt/VideoSpellChecker/VideoSpellChecker.desktop /usr/share/applications/
```

## Документация

- [README.md](README.md) - Полная документация
- [CUSTOM_DICTIONARY.md](CUSTOM_DICTIONARY.md) - Подробно о пользовательском словаре
- [QT_DESIGNER.md](QT_DESIGNER.md) - Редактирование интерфейса
- [example.py](example.py) - Примеры программного использования

## Поддержка

Если возникли проблемы - проверьте полную документацию в [README.md](README.md)
