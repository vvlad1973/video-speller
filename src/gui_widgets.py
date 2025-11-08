"""
Вспомогательные классы для GUI
"""
import sys
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal
from src.video_speller import VideoSpellChecker


def get_app_dir():
    """Получить директорию приложения (работает и для .py и для .exe)"""
    if getattr(sys, 'frozen', False):
        # Запущено из exe (PyInstaller)
        return Path(sys.executable).parent
    else:
        # Запущено из .py - возвращаем корень проекта (родитель src/)
        return Path(__file__).parent.parent


class WorkerThread(QThread):
    """Поток для обработки видео без блокировки GUI"""
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)
    frame_signal = pyqtSignal(object)  # Сигнал для передачи текущего кадра
    progress_signal = pyqtSignal(int)  # Сигнал для обновления прогресса (0-100)

    def __init__(self, video_path, interval, output_dir, start_time=0.0, end_time=None):
        super().__init__()
        self.video_path = video_path
        self.interval = interval
        self.output_dir = output_dir
        self.start_time = start_time
        self.end_time = end_time

    def run(self):
        """Запуск обработки видео"""
        try:
            # Создаем экземпляр проверки с перехватом вывода
            self.log_signal.emit("=" * 60)
            self.log_signal.emit(f"Обработка видео: {self.video_path}")
            self.log_signal.emit("=" * 60)

            checker = VideoSpellCheckerWithLogging(
                output_dir=self.output_dir,
                log_callback=self.log_signal.emit,
                frame_callback=self.frame_signal.emit,
                progress_callback=self.progress_signal.emit
            )

            result = checker.process_video_with_result(
                self.video_path,
                self.interval,
                self.start_time,
                self.end_time
            )

            self.finished_signal.emit(result)

        except Exception as e:
            self.error_signal.emit(f"Ошибка: {str(e)}")


class VideoSpellCheckerWithLogging(VideoSpellChecker):
    """Расширенный класс с поддержкой логирования в GUI"""

    def __init__(self, output_dir="screenshots_with_errors", log_callback=None, frame_callback=None,
                 progress_callback=None, custom_dict_path=None):
        self.log_callback = log_callback
        self.frame_callback = frame_callback
        self.progress_callback = progress_callback
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Определяем путь к пользовательскому словарю
        if custom_dict_path is None:
            app_dir = get_app_dir()
            custom_dict_path = app_dir / "custom_dictionary.txt"

        # Загружаем пользовательский словарь
        self.custom_words = self._load_custom_dictionary(custom_dict_path)

        # Инициализируем EasyOCR
        self.log("⏳ Загрузка моделей OCR (это может занять время при первом запуске)...")
        import easyocr
        self.reader = easyocr.Reader(['ru', 'en'], gpu=False)
        self.log("✓ Модели OCR загружены")

        # Инициализируем проверку орфографии
        self.log("⏳ Загрузка словарей...")
        from spylls.hunspell import Dictionary

        # Загружаем словари
        self.spell_ru = self._load_dictionary('ru_RU', 'Русский')
        self.spell_en = self._load_dictionary('en_US', 'Английский')

    def _load_dictionary(self, dict_name, display_name):
        """Загружает словарь Hunspell из папки dictionaries

        Для GUI версии пути определяются через get_app_dir() для работы с PyInstaller
        """
        from spylls.hunspell import Dictionary

        app_dir = get_app_dir()
        dict_dir = app_dir / 'dictionaries'
        dict_path = dict_dir / dict_name
        aff_file = dict_dir / f'{dict_name}.aff'
        dic_file = dict_dir / f'{dict_name}.dic'

        # Проверяем наличие файлов словаря
        if aff_file.exists() and dic_file.exists():
            try:
                dictionary = Dictionary.from_files(str(dict_path))
                self.log(f"✓ {display_name} словарь загружен")
                return dictionary
            except Exception as e:
                self.log(f"⚠ Ошибка загрузки {display_name.lower()} словаря: {e}")
                return None
        else:
            # Словарь не найден - GUI предложит загрузить через диалог
            self.log(f"⚠ {display_name} словарь не найден")
            self.log(f"ℹ Для автоматической загрузки словарей используйте: python -m src.download_dictionaries")
            return None

    def _load_custom_dictionary(self, dict_path):
        """Загружает пользовательский словарь из файла"""
        custom_words = set()

        try:
            if Path(dict_path).exists():
                with open(dict_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            custom_words.add(line.lower())

                self.log(f"✓ Загружено слов из пользовательского словаря: {len(custom_words)}")
            else:
                self.log(f"ℹ Пользовательский словарь пуст")

        except Exception as e:
            self.log(f"⚠ Ошибка при чтении пользовательского словаря: {e}")

        return custom_words

    def log(self, message):
        """Вывод сообщения в лог"""
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)

    def send_frame(self, frame):
        """Отправить кадр для превью"""
        if self.frame_callback:
            self.frame_callback(frame)

    def send_progress(self, progress):
        """Отправить прогресс обработки (0-100)"""
        if self.progress_callback:
            self.progress_callback(progress)

    def _cleanup_old_results(self):
        """Очищает старые скриншоты и текстовые файлы с ошибками, сохраняя итоговые отчеты"""
        import glob
        import os

        # Удаляем старые PNG скриншоты (frame_*_errors.png)
        for png_file in glob.glob(str(self.output_dir / "frame_*_errors.png")):
            try:
                os.remove(png_file)
            except Exception as e:
                self.log(f"⚠ Не удалось удалить {png_file}: {e}")

        # Удаляем старые TXT файлы с ошибками (frame_*_errors.txt)
        for txt_file in glob.glob(str(self.output_dir / "frame_*_errors.txt")):
            try:
                os.remove(txt_file)
            except Exception as e:
                self.log(f"⚠ Не удалось удалить {txt_file}: {e}")

        # Отчеты report-*.txt НЕ удаляем

    def process_video_with_result(self, video_path, interval=2, start_time=0.0, end_time=None):
        """Обработка видео с возвратом результата"""
        import cv2
        import re
        import glob

        self.log("")

        # Очищаем старые результаты (кроме отчетов)
        self._cleanup_old_results()

        # Извлекаем кадры
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Не удалось открыть видео: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0

        frame_interval = int(fps * interval)

        # Вычисляем начальный и конечный кадры
        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps) if end_time is not None else total_frames

        # Проверяем корректность временных границ
        if start_frame >= total_frames:
            self.log(f"⚠ Начальное время {start_time}s превышает длительность видео {duration:.1f}s")
            start_frame = 0

        if end_frame > total_frames:
            end_frame = total_frames

        if start_frame >= end_frame:
            raise ValueError(f"Начальное время ({start_time}s) должно быть меньше конечного ({end_time}s)")

        # Форматируем время для отображения
        start_min, start_sec = divmod(int(start_time), 60)
        if end_time is not None:
            end_min, end_sec = divmod(int(end_time), 60)
            self.log(f"ℹ Анализ видео с {start_min}:{start_sec:02d} до {end_min}:{end_sec:02d}")
        else:
            dur_min, dur_sec = divmod(int(duration), 60)
            self.log(f"ℹ Анализ видео с {start_min}:{start_sec:02d} до {dur_min}:{dur_sec:02d} (конец)")

        self.log(f"ℹ Кадры: {start_frame} - {end_frame} из {total_frames}")

        # Перемещаемся к начальному кадру
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        frames = []
        frame_count = start_frame

        while frame_count < end_frame:
            ret, frame = cap.read()
            if not ret:
                break

            if (frame_count - start_frame) % frame_interval == 0:
                frames.append((frame_count, frame))

            frame_count += 1

        cap.release()
        self.log(f"✓ Извлечено {len(frames)} кадров из видео")

        # Результаты обработки
        total_errors = 0
        frames_with_errors = []

        # Обрабатываем каждый кадр
        for idx, (frame_num, frame) in enumerate(frames):
            self.log(f"\nОбработка кадра {idx + 1}/{len(frames)} (кадр #{frame_num})...")

            # Отправляем кадр для превью и обновляем прогресс
            self.send_frame(frame)
            progress = int((idx + 1) / len(frames) * 100)
            self.send_progress(progress)

            # Извлекаем текст
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Распознаем текст с детальной информацией о координатах
            results = self.reader.readtext(frame_rgb, detail=1)

            if not results:
                self.log("  ℹ Текст не обнаружен")
                continue

            # Извлекаем текст из результатов OCR
            text_parts = []
            for result in results:
                text_parts.append(result[1])  # result[1] содержит распознанный текст

            full_text = '\n'.join(text_parts)

            # Проверяем орфографию
            errors = self.check_spelling(full_text)

            if errors:
                total_errors += len(errors)

                self.log(f"  ⚠ Найдено ошибок: {len(errors)}")
                for error in errors[:5]:
                    self.log(f"     • {error}")
                if len(errors) > 5:
                    self.log(f"     ... и еще {len(errors) - 5} ошибок")

                # Собираем весь текст
                text = ' '.join([result[1] for result in results])

                # Сохраняем кадр с ошибками (используем imencode для поддержки кириллицы в пути)
                output_path = self.output_dir / f"frame_{frame_num}_errors.png"
                is_success, buffer = cv2.imencode('.png', frame)
                if is_success:
                    buffer.tofile(str(output_path))
                else:
                    self.log(f"  ⚠ Не удалось сохранить изображение: {output_path}")

                # Вычисляем тайм-код
                timecode = frame_num / fps

                # Сохраняем список ошибок
                error_file = self.output_dir / f"frame_{frame_num}_errors.txt"
                with open(error_file, 'w', encoding='utf-8') as f:
                    f.write(f"Кадр: {frame_num}\n")
                    f.write(f"Время: {timecode:.2f} сек ({int(timecode // 60)}:{int(timecode % 60):02d})\n\n")
                    f.write(f"Полный текст:\n{text}\n\n")
                    f.write("Найденные ошибки:\n")
                    for error in errors:
                        f.write(f"  - {error}\n")

                frames_with_errors.append({
                    'frame_num': frame_num,
                    'timecode': timecode,
                    'errors_count': len(errors),
                    'errors': errors,
                    'text': text
                })

                self.log(f"  ✓ Сохранено: {output_path}")
            else:
                self.log("  ✓ Ошибок не найдено")

        self.log("\n" + "=" * 60)
        self.log("ОБРАБОТКА ЗАВЕРШЕНА!")
        self.log("=" * 60)
        self.log(f"Всего обработано кадров: {len(frames)}")
        self.log(f"Кадров с ошибками: {len(frames_with_errors)}")
        self.log(f"Всего найдено ошибок: {total_errors}")
        self.log(f"Результаты сохранены в: {self.output_dir.absolute()}")
        self.log("=" * 60)

        # Сохраняем итоговый отчёт
        from datetime import datetime
        report_filename = f"report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
        report_path = self.output_dir / report_filename

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("ИТОГОВЫЙ ОТЧЁТ ПРОВЕРКИ ОРФОГРАФИИ\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Видео файл: {video_path}\n")
            f.write(f"Интервал кадров: {interval} сек\n")
            f.write(f"Временной диапазон: {start_time:.2f}s - {end_time if end_time else duration:.2f}s\n\n")

            f.write("=" * 60 + "\n")
            f.write("СТАТИСТИКА\n")
            f.write("=" * 60 + "\n")
            f.write(f"Всего обработано кадров: {len(frames)}\n")
            f.write(f"Кадров с ошибками: {len(frames_with_errors)}\n")
            f.write(f"Всего найдено ошибок: {total_errors}\n\n")

            if frames_with_errors:
                f.write("=" * 60 + "\n")
                f.write("ДЕТАЛЬНАЯ ИНФОРМАЦИЯ ПО ОШИБКАМ\n")
                f.write("=" * 60 + "\n\n")

                for idx, frame_info in enumerate(frames_with_errors, 1):
                    timecode = frame_info['timecode']
                    minutes = int(timecode // 60)
                    seconds = int(timecode % 60)

                    f.write(f"{idx}. КАДР #{frame_info['frame_num']}\n")
                    f.write(f"   Время: {timecode:.2f}s ({minutes}:{seconds:02d})\n")
                    f.write(f"   Количество ошибок: {frame_info['errors_count']}\n")
                    f.write(f"   Распознанный текст: {frame_info['text']}\n")
                    f.write(f"   Ошибки:\n")
                    for error in frame_info['errors']:
                        f.write(f"      - {error}\n")
                    f.write("\n")

            f.write("=" * 60 + "\n")
            f.write(f"Результаты сохранены в: {self.output_dir.absolute()}\n")
            f.write("=" * 60 + "\n")

        self.log(f"\n✓ Итоговый отчёт сохранён: {report_path}")

        return {
            'total_frames': len(frames),
            'frames_with_errors': len(frames_with_errors),
            'total_errors': total_errors,
            'output_dir': str(self.output_dir.absolute()),
            'errors_details': frames_with_errors,
            'fps': fps,
            'report_file': str(report_path)
        }
