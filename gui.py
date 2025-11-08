"""
GUI версия с использованием Qt Designer (.ui файл)
Для редактирования интерфейса используйте Qt Designer с файлом main_window.ui
"""

import sys
import os
import subprocess
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor, QPixmap, QImage, QIcon
from gui_widgets import WorkerThread
from PyQt6.QtWidgets import QTimeEdit
from PyQt6.QtCore import QTime


class SmartTimeEdit(QTimeEdit):
    """QTimeEdit с автоматическим переключением разрядов при достижении предела"""

    def stepBy(self, steps):
        """Переопределяем поведение спиннеров для переключения разрядов"""
        from PyQt6.QtWidgets import QDateTimeEdit

        current = self.time()
        section = self.currentSection()

        # Конвертируем в секунды
        total_seconds = current.hour() * 3600 + current.minute() * 60 + current.second()

        # Определяем шаг в зависимости от текущей секции
        if section == QDateTimeEdit.Section.SecondSection:
            step_seconds = steps
        elif section == QDateTimeEdit.Section.MinuteSection:
            step_seconds = steps * 60
        elif section == QDateTimeEdit.Section.HourSection:
            step_seconds = steps * 3600
        else:
            step_seconds = steps

        # Добавляем шаг
        total_seconds += step_seconds

        # Ограничиваем минимумом и максимумом
        min_time = self.minimumTime()
        max_time = self.maximumTime()

        min_seconds = min_time.hour() * 3600 + min_time.minute() * 60 + min_time.second()
        max_seconds = max_time.hour() * 3600 + max_time.minute() * 60 + max_time.second()

        if total_seconds < min_seconds:
            total_seconds = min_seconds
        elif total_seconds > max_seconds:
            total_seconds = max_seconds

        # Конвертируем обратно
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        self.setTime(QTime(hours, minutes, seconds))


def get_app_dir():
    """Получить директорию приложения (работает и для .py и для .exe)"""
    if getattr(sys, "frozen", False):
        # Запущено из exe (PyInstaller)
        return Path(sys.executable).parent
    else:
        # Запущено из .py
        return Path(__file__).parent


def get_resource_path(relative_path):
    """Получить абсолютный путь к ресурсу (UI файлы, иконки)
    Работает как для dev режима, так и для PyInstaller"""
    if getattr(sys, "frozen", False):
        # PyInstaller создает временную папку _MEIPASS для ресурсов
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent

    return base_path / relative_path


class VideoSpellCheckerGUI(QMainWindow):
    """Главное окно приложения загружаемое из .ui файла"""

    def __init__(self):
        super().__init__()
        self.worker = None
        self.video_duration_seconds = None  # Длительность загруженного видео
        self.config_file = get_app_dir() / "config.ini"  # Путь к файлу конфигурации

        # Устанавливаем иконку приложения
        icon_path = get_resource_path("app.ico")
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        # Загружаем UI из файла
        ui_file = get_resource_path("main_window.ui")
        uic.loadUi(ui_file, self)

        # Инициализируем кастомные виджеты для времени
        self.setup_time_widgets()

        # Загружаем настройки
        self.load_settings()

        # Подключаем сигналы
        self.setup_connections()

        # Закрываем splash-экран если он есть (PyInstaller)
        try:
            import pyi_splash  # type: ignore

            pyi_splash.close()
        except:
            pass

    def setup_time_widgets(self):
        """Настраиваем виджеты времени (заменяем на SmartTimeEdit)"""
        from PyQt6.QtWidgets import QTimeEdit

        # Находим оригинальные QTimeEdit виджеты
        old_start = self.findChild(QTimeEdit, "startTimeInput")
        old_end = self.findChild(QTimeEdit, "endTimeInput")

        if not old_start or not old_end:
            print("ERROR: Не найдены виджеты startTimeInput или endTimeInput")
            return

        # Получаем layout, в котором находятся виджеты (они в одном layout)
        parent_layout = old_start.parent().layout()

        # Копируем настройки из .ui файла
        start_settings = {
            'time': old_start.time(),
            'displayFormat': old_start.displayFormat(),
            'enabled': old_start.isEnabled(),
            'minimumSize': old_start.minimumSize(),
            'maximumSize': old_start.maximumSize(),
            'alignment': old_start.alignment(),
            'buttonSymbols': old_start.buttonSymbols()
        }

        end_settings = {
            'time': old_end.time(),
            'displayFormat': old_end.displayFormat(),
            'enabled': old_end.isEnabled(),
            'minimumSize': old_end.minimumSize(),
            'maximumSize': old_end.maximumSize(),
            'alignment': old_end.alignment(),
            'buttonSymbols': old_end.buttonSymbols()
        }

        # Создаем новые SmartTimeEdit виджеты
        self.start_time_input = SmartTimeEdit()
        self.end_time_input = SmartTimeEdit()

        # Применяем настройки
        for widget, settings in [(self.start_time_input, start_settings), (self.end_time_input, end_settings)]:
            widget.setTime(settings['time'])
            widget.setDisplayFormat(settings['displayFormat'])
            widget.setEnabled(settings['enabled'])
            widget.setMinimumSize(settings['minimumSize'])
            widget.setMaximumSize(settings['maximumSize'])
            widget.setAlignment(settings['alignment'])
            widget.setButtonSymbols(settings['buttonSymbols'])

        # Устанавливаем objectName для доступа к виджетам
        self.start_time_input.setObjectName("startTimeInput")
        self.end_time_input.setObjectName("endTimeInput")

        # Включаем wrapping для автоматического переключения разрядов
        self.start_time_input.setWrapping(True)
        self.end_time_input.setWrapping(True)

        # Заменяем виджеты: сначала удаляем старые и вставляем новые
        parent_layout.replaceWidget(old_start, self.start_time_input)
        parent_layout.replaceWidget(old_end, self.end_time_input)

        # Удаляем старые виджеты
        old_start.deleteLater()
        old_end.deleteLater()

        # Добавляем подсказки
        self.start_time_input.setToolTip("Начальное время анализа [час:мин:сек]")
        self.end_time_input.setToolTip("Конечное время анализа [час:мин:сек]")

    def setup_connections(self):
        """Подключаем сигналы к слотам"""
        self.browseButton.clicked.connect(self.browse_file)
        self.browseOutputButton.clicked.connect(self.browse_output_dir)
        self.startButton.clicked.connect(self.start_processing)

        # Подключаем валидацию времени (визуальная индикация)
        self.start_time_input.timeChanged.connect(self.update_start_time_validation)
        self.end_time_input.timeChanged.connect(self.update_end_time_validation)

        # Сохраняем настройки при изменении папки вывода
        self.outputDirInput.textChanged.connect(self.save_settings)

        # Подключаем действия меню
        self.actionOpenDictionary.triggered.connect(self.open_custom_dictionary)
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.show_about_dialog)

    def update_start_time_validation(self):
        """Проверяет установленное время начала, обновляет ограничение для конечного времени"""

        start_time = self.start_time_input.time()
        end_time = self.end_time_input.time()
        max_end_time = self.end_time_input.maximumTime()

        self.end_time_input.blockSignals(True)

        # Вычисляем минимально допустимое значение для end_time
        min_end_time = start_time.addSecs(1)

        # Если минимум превышает максимум, используем максимум
        if min_end_time > max_end_time:
            min_end_time = max_end_time

        # Устанавливаем новый минимум
        self.end_time_input.setMinimumTime(min_end_time)

        # Если текущее значение меньше нового минимума, корректируем
        if end_time < min_end_time:
            self.end_time_input.setTime(min_end_time)

        self.end_time_input.blockSignals(False)

    def update_end_time_validation(self):
        """Проверяет и корректирует время если оно некорректное"""
        pass

    def load_settings(self):
        """Загружает сохраненные настройки"""
        from PyQt6.QtCore import QSettings

        settings = QSettings(str(self.config_file), QSettings.Format.IniFormat)

        # Загружаем папку вывода (по умолчанию: <каталог приложения>/out)
        default_output_dir = str(get_app_dir() / "out")
        output_dir = settings.value("output_dir", default_output_dir)
        self.outputDirInput.setText(output_dir)

    def save_settings(self):
        """Сохраняет настройки"""
        from PyQt6.QtCore import QSettings

        settings = QSettings(str(self.config_file), QSettings.Format.IniFormat)
        settings.setValue("output_dir", self.outputDirInput.text())
        settings.sync()

    def browse_output_dir(self):
        """Открыть диалог выбора папки для результатов"""
        current_dir = self.outputDirInput.text()
        if not current_dir:
            current_dir = str(get_app_dir() / "out")

        dir_name = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку для результатов",
            current_dir,
            QFileDialog.Option.ShowDirsOnly
        )

        if dir_name:
            self.outputDirInput.setText(dir_name)

    def browse_file(self):
        """Открыть диалог выбора файла"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите видео файл",
            "",
            "Video Files (*.mp4 *.avi *.mov *.mkv *.flv *.wmv);;All Files (*.*)",
        )

        if file_name:
            self.fileInput.setText(file_name)

            # Сбрасываем прогресс и очищаем лог
            self.progressBar.setValue(0)
            self.logOutput.clear()

            # Устанавливаем конечное время на длительность видео
            self.set_end_time_from_video(file_name)
            self.start_time_input.setEnabled(True)
            self.end_time_input.setEnabled(True)

    def set_end_time_from_video(self, video_path):
        """Устанавливает конечное время равным длительности видео"""
        try:
            import cv2
            from PyQt6.QtCore import QTime

            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return

            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()

            if fps > 0 and total_frames > 0:
                duration_seconds = int(total_frames / fps)

                # Сохраняем длительность видео
                self.video_duration_seconds = duration_seconds

                hours = duration_seconds // 3600
                minutes = (duration_seconds % 3600) // 60
                seconds = duration_seconds % 60

                # Устанавливаем время конца на длительность видео
                end_time = QTime(hours, minutes, seconds)
                self.end_time_input.setTime(end_time)

                self.start_time_input.setMaximumTime(end_time.addSecs(-1))
                self.end_time_input.setMaximumTime(end_time)

        except Exception as e:
            print(f"Не удалось определить длительность видео: {e}")

    def check_dictionaries(self):
        """Проверяет наличие словарей и предлагает скачать при необходимости"""
        app_dir = get_app_dir()
        dict_dir = app_dir / "dictionaries"
        ru_aff = dict_dir / "ru_RU.aff"
        ru_dic = dict_dir / "ru_RU.dic"
        en_aff = dict_dir / "en_US.aff"
        en_dic = dict_dir / "en_US.dic"

        missing_dicts = []
        if not (os.path.exists(ru_aff) and os.path.exists(ru_dic)):
            missing_dicts.append("Русский (ru_RU)")
        if not (os.path.exists(en_aff) and os.path.exists(en_dic)):
            missing_dicts.append("Английский (en_US)")

        if missing_dicts:
            msg = f"Не найдены словари:\n" + "\n".join(f"• {d}" for d in missing_dicts)
            msg += "\n\nСкачать словари автоматически?"

            reply = QMessageBox.question(
                self,
                "Словари не найдены",
                msg,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes,
            )

            if reply == QMessageBox.StandardButton.Yes:
                return self.download_dictionaries()
            else:
                QMessageBox.information(
                    self,
                    "Информация",
                    "Обработка продолжится без проверки орфографии.\n"
                    "Для загрузки словарей используйте download_dictionaries.py",
                )
                return True

        return True

    def download_dictionaries(self):
        """Загружает словари"""
        import urllib.request

        try:
            # Создаем папку для словарей
            app_dir = get_app_dir()
            dict_dir = app_dir / "dictionaries"
            dict_dir.mkdir(exist_ok=True)

            # URLs для словарей (используем репозиторий с актуальными словарями)
            dictionaries_to_download = [
                {
                    "name": "Русский (ru_RU)",
                    "files": [
                        (
                            "https://raw.githubusercontent.com/LibreOffice/dictionaries/master/ru_RU/ru_RU.aff",
                            dict_dir / "ru_RU.aff",
                        ),
                        (
                            "https://raw.githubusercontent.com/LibreOffice/dictionaries/master/ru_RU/ru_RU.dic",
                            dict_dir / "ru_RU.dic",
                        ),
                    ],
                },
                {
                    "name": "Английский (en_US)",
                    "files": [
                        (
                            "https://raw.githubusercontent.com/LibreOffice/dictionaries/master/en/en_US.aff",
                            dict_dir / "en_US.aff",
                        ),
                        (
                            "https://raw.githubusercontent.com/LibreOffice/dictionaries/master/en/en_US.dic",
                            dict_dir / "en_US.dic",
                        ),
                    ],
                },
            ]

            # Загружаем словари
            all_ok = True
            for dict_info in dictionaries_to_download:
                for url, dest in dict_info["files"]:
                    try:
                        urllib.request.urlretrieve(url, str(dest))
                        if not (dest.exists() and dest.stat().st_size > 100):
                            all_ok = False
                    except Exception as e:
                        all_ok = False
                        break

            if all_ok:
                QMessageBox.information(self, "Успех", "Словари успешно загружены!")
                return True
            else:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Ошибка при загрузке словарей.\n\n"
                    "Проверьте подключение к интернету или используйте download_dictionaries.py вручную",
                )
                return False

        except Exception as e:
            QMessageBox.warning(
                self,
                "Ошибка",
                f"Не удалось загрузить словари:\n{str(e)}\n\n"
                "Используйте download_dictionaries.py вручную",
            )
            return False

    def start_processing(self):
        """Начать обработку видео"""
        # Проверяем наличие словарей
        if not self.check_dictionaries():
            return

        video_path = self.fileInput.text()

        if not video_path:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите видео файл")
            return

        if not os.path.exists(video_path):
            QMessageBox.warning(self, "Ошибка", "Выбранный файл не существует")
            return

        interval = self.intervalInput.value()

        # Получаем время из QTimeEdit и конвертируем в секунды
        from PyQt6.QtCore import QTime

        start_time = self.start_time_input.time()
        start_time_seconds = (
            start_time.hour() * 3600 + start_time.minute() * 60 + start_time.second()
        )

        end_time = self.end_time_input.time()
        # Если время 00:00:00, значит до конца
        if end_time == QTime(0, 0, 0):
            end_time_seconds = None
        else:
            end_time_seconds = (
                end_time.hour() * 3600 + end_time.minute() * 60 + end_time.second()
            )

        # Валидация времени
        if end_time_seconds is not None and end_time_seconds <= start_time_seconds:
            QMessageBox.warning(
                self, "Ошибка", "Конечное время должно быть больше начального"
            )
            return

        # Очищаем лог и сбрасываем прогресс
        self.logOutput.clear()
        self.progressBar.setValue(0)

        # Блокируем кнопки и поля ввода
        self.startButton.setEnabled(False)
        self.browseButton.setEnabled(False)
        self.browseOutputButton.setEnabled(False)
        self.outputDirInput.setEnabled(False)
        self.intervalInput.setEnabled(False)
        self.start_time_input.setEnabled(False)
        self.end_time_input.setEnabled(False)
        self.startButton.setText("Обработка...")

        # Получаем базовую папку вывода из настроек
        base_output_dir = self.outputDirInput.text()
        if not base_output_dir:
            base_output_dir = str(get_app_dir() / "out")

        # Создаем подпапку с именем видео
        video_name = Path(video_path).stem
        output_dir = Path(base_output_dir) / f"screenshots_{video_name}_errors"
        output_dir = str(output_dir)

        # Создаем директорию если не существует
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Запускаем обработку в отдельном потоке
        self.worker = WorkerThread(
            video_path, interval, output_dir, start_time_seconds, end_time_seconds
        )
        self.worker.log_signal.connect(self.append_log)
        self.worker.frame_signal.connect(self.update_frame_preview)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.processing_finished)
        self.worker.error_signal.connect(self.processing_error)
        self.worker.start()

    def append_log(self, message):
        """Добавить сообщение в лог"""
        self.logOutput.append(message)
        self.logOutput.moveCursor(QTextCursor.MoveOperation.End)

    def update_frame_preview(self, frame):
        """Обновить превью текущего кадра"""
        import cv2

        if frame is None:
            return

        # Конвертируем BGR в RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Получаем размеры
        height, width, _ = frame_rgb.shape
        bytes_per_line = 3 * width

        # Создаем QImage
        q_image = QImage(
            frame_rgb.data, width, height, bytes_per_line, QImage.Format.Format_RGB888
        )

        # Масштабируем изображение с сохранением пропорций
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(
            self.framePreview.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        # Устанавливаем в label
        self.framePreview.setPixmap(scaled_pixmap)

    def update_progress(self, value):
        """Обновить прогресс-бар"""
        self.progressBar.setValue(value)

    def open_custom_dictionary(self):
        """Открыть файл пользовательского словаря"""
        import subprocess
        from PyQt6.QtWidgets import QMessageBox

        # Путь к файлу словаря
        app_dir = get_app_dir()
        dict_file = app_dir / "custom_dictionary.txt"

        # Создаём файл, если его нет
        if not dict_file.exists():
            try:
                with open(dict_file, "w", encoding="utf-8") as f:
                    f.write("# Пользовательский словарь\n")
                    f.write("# Добавьте свои слова (по одному на строку)\n")
                    f.write("# Строки, начинающиеся с #, игнорируются\n\n")

                QMessageBox.information(
                    self,
                    "Словарь создан",
                    f"Создан новый файл словаря:\n{dict_file}\n\nДобавьте в него свои слова-исключения.",
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "Ошибка", f"Не удалось создать файл словаря:\n{e}"
                )
                return

        # Открываем файл в системном редакторе
        try:
            if os.name == "nt":  # Windows
                os.startfile(dict_file)
            elif os.name == "posix":  # Linux/Mac
                if (
                    subprocess.call(["which", "xdg-open"], stdout=subprocess.DEVNULL)
                    == 0
                ):
                    subprocess.call(["xdg-open", dict_file])
                else:
                    subprocess.call(["open", dict_file])  # macOS
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось открыть файл:\n{e}\n\nПуть к файлу:\n{dict_file}",
            )

    def show_about_dialog(self):
        """Показать диалог 'О программе'"""
        from PyQt6.QtWidgets import QDialog

        # Создаем диалог и загружаем UI
        dialog = QDialog(self)
        about_ui_file = get_resource_path("about_dialog.ui")
        uic.loadUi(about_ui_file, dialog)

        # Показываем диалог
        dialog.exec()

    def processing_finished(self, result):
        """Обработка завершена успешно"""
        self.startButton.setEnabled(True)
        self.browseButton.setEnabled(True)
        self.browseOutputButton.setEnabled(True)
        self.outputDirInput.setEnabled(True)
        self.intervalInput.setEnabled(True)
        self.start_time_input.setEnabled(True)
        self.end_time_input.setEnabled(True)
        self.startButton.setText("Начать проверку")

        self.show_report(result)
        self.open_results_folder(result["output_dir"])

    def processing_error(self, error_message):
        """Обработка завершена с ошибкой"""
        self.startButton.setEnabled(True)
        self.browseButton.setEnabled(True)
        self.browseOutputButton.setEnabled(True)
        self.outputDirInput.setEnabled(True)
        self.intervalInput.setEnabled(True)
        self.start_time_input.setEnabled(True)
        self.end_time_input.setEnabled(True)
        self.startButton.setText("Начать проверку")

        self.append_log(f"\n❌ {error_message}")
        QMessageBox.critical(self, "Ошибка", error_message)

    def show_report(self, result):
        """Показать отчет о результатах"""
        report = "\n\n" + "=" * 60 + "\n"
        report += "ОТЧЕТ О ПРОВЕРКЕ\n"
        report += "=" * 60 + "\n\n"

        if result["frames_with_errors"] == 0:
            report += "✓ Ошибок не найдено!\n"
        else:
            report += f"Найдено кадров с ошибками: {result['frames_with_errors']}\n"
            report += f"Всего ошибок: {result['total_errors']}\n\n"
            report += "Тайм-коды кадров с ошибками:\n"
            report += "-" * 60 + "\n"

            for detail in result["errors_details"]:
                timecode = detail["timecode"]
                minutes = int(timecode // 60)
                seconds = int(timecode % 60)
                milliseconds = int((timecode % 1) * 1000)

                report += f"\n🕐 {minutes:02d}:{seconds:02d}.{milliseconds:03d} "
                report += f"(кадр #{detail['frame_num']}) - "
                report += f"{detail['errors_count']} ошибок\n"

                for _, error in enumerate(detail["errors"][:3]):
                    report += f"   • {error}\n"

                if len(detail["errors"]) > 3:
                    report += f"   ... и еще {len(detail['errors']) - 3} ошибок\n"

        report += "\n" + "=" * 60 + "\n"
        self.append_log(report)

    def open_results_folder(self, folder_path):
        """Открыть папку с результатами в проводнике"""
        if os.path.exists(folder_path):
            if sys.platform == "win32":
                os.startfile(folder_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", folder_path])
            else:
                subprocess.run(["xdg-open", folder_path])


def main():
    """Запуск приложения"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Устанавливаем иконку для всего приложения
    icon_path = get_resource_path("app.ico")
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    window = VideoSpellCheckerGUI()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
