# Редактирование интерфейса в Qt Designer

Проект использует Qt Designer для редактирования GUI.

## Установка Qt Designer

### Windows

```bash
pip install pyqt6-tools
```

После установки Qt Designer будет доступен по пути:

```bash
Python\Lib\site-packages\qt6_applications\Qt\bin\designer.exe
```

### Linux/Mac

```bash
# Ubuntu/Debian
sudo apt-get install qt6-tools

# Mac
brew install qt-creator
```

## Редактирование интерфейса

### 1. Открыть Qt Designer

Запустите Qt Designer и откройте файл:

```bash
main_window.ui
```

### 2. Редактировать интерфейс

В Qt Designer вы можете:

- Изменять расположение элементов
- Менять размеры виджетов
- Изменять стили (CSS)
- Добавлять новые виджеты
- Настраивать свойства элементов

### 3. Сохранить изменения

После редактирования:

1. Сохраните файл `main_window.ui` (Ctrl+S)
2. Закройте Qt Designer
3. Запустите приложение: `python gui.py`

## Структура проекта

```bash
video-speller/
├── gui.py                  # Основной файл GUI (использует Qt Designer)
├── gui_widgets.py          # Вспомогательные виджеты и классы
├── main_window.ui          # UI файл для Qt Designer
└── video_speller.py        # Основная логика проверки орфографии
```

## Важные замечания

### Кастомные виджеты

В файле `.ui` определены стандартные QTimeEdit виджеты:

- `startTimeInput` - QTimeEdit для начального времени анализа
- `endTimeInput` - QTimeEdit для конечного времени анализа

При запуске приложения эти виджеты **автоматически заменяются** на `SmartTimeEdit` (наследник QTimeEdit с поддержкой автоматического переключения разрядов времени) в методе `setup_time_widgets()` файла [gui.py](gui.py).

**Важно:** Не меняйте тип этих виджетов в Qt Designer - оставляйте их как `QTimeEdit`. Замена происходит программно.

### Именование виджетов

Важно сохранять правильные имена виджетов в Qt Designer:

| Виджет | Имя в .ui файле | Тип | Описание |
|--------|----------------|------|----------|
| Поле файла | `fileInput` | QLineEdit | Путь к видео файлу |
| Кнопка обзора | `browseButton` | QPushButton | Выбор видео файла |
| Интервал | `intervalInput` | QSpinBox | Интервал между кадрами (сек) |
| Начало времени | `startTimeInput` | QTimeEdit | Начальное время анализа |
| Конец времени | `endTimeInput` | QTimeEdit | Конечное время анализа |
| Кнопка запуска | `startButton` | QPushButton | Запуск проверки |
| Прогресс-бар | `progressBar` | QProgressBar | Прогресс обработки |
| Лог | `logOutput` | QTextEdit | Вывод логов |
| Превью | `framePreview` | QLabel | Превью текущего кадра |

### Стили (CSS)

Стили можно редактировать в Qt Designer в свойстве `styleSheet`:

**Кнопка запуска:**

```css
QPushButton {
    background-color: #4CAF50;
    color: white;
    font-size: 14px;
    font-weight: bold;
    border-radius: 5px;
}
QPushButton:hover {
    background-color: #45a049;
}
QPushButton:disabled {
    background-color: #cccccc;
}
```

**Лог вывода:**

```css
QTextEdit {
    background-color: #2b2b2b;
    color: #f0f0f0;
    border: 1px solid #444;
    border-radius: 5px;
    padding: 10px;
}
```

**Превью кадра:**

```css
QLabel {
    background-color: #1a1a1a;
    border: 1px solid #444;
    border-radius: 5px;
}
```

## Запуск

```bash
python gui.py
```

GUI использует Qt Designer для визуального редактирования интерфейса.

## Конвертация .ui в .py (опционально)

Если вы хотите преобразовать `.ui` файл в Python код:

```bash
pyuic6 main_window.ui -o ui_main_window.py
```

Однако рекомендуется использовать прямую загрузку `.ui` файла через `uic.loadUi()`, так как это позволяет редактировать интерфейс без перегенерации кода.
