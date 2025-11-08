import cv2
import easyocr
from pathlib import Path
import re
from typing import List, Tuple
from spylls.hunspell import Dictionary


class VideoSpellChecker:
    def __init__(self, output_dir: str = "screenshots_with_errors",
                 custom_dict_path: str = "custom_dictionary.txt"):
        """
        Инициализация проверки орфографии в видео

        Args:
            output_dir: Директория для сохранения скриншотов с ошибками
            custom_dict_path: Путь к файлу с пользовательским словарем
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Загружаем пользовательский словарь
        self.custom_words = self._load_custom_dictionary(custom_dict_path)

        # Инициализируем EasyOCR для русского и английского
        print("Загрузка моделей OCR (это может занять время при первом запуске)...")
        self.reader = easyocr.Reader(['ru', 'en'], gpu=False)
        print("OK EasyOCR загружен")

        # Инициализируем Hunspell словари для проверки орфографии
        print("Загрузка словарей для проверки орфографии...")

        # Путь к словарям (относительно текущего файла для CLI версии)
        dict_path = Path(__file__).parent / "dictionaries"

        try:
            ru_path = str(dict_path / "ru_RU")
            self.spell_ru = Dictionary.from_files(ru_path)
            print("OK Русский словарь загружен")
        except Exception as e:
            print(f"WARNING Не удалось загрузить русский словарь: {e}")
            print(f"   Запустите: python -m src.download_dictionaries")
            self.spell_ru = None

        try:
            en_path = str(dict_path / "en_US")
            self.spell_en = Dictionary.from_files(en_path)
            print("OK Английский словарь загружен")
        except Exception as e:
            print(f"WARNING Не удалось загрузить английский словарь: {e}")
            print(f"   Запустите: python -m src.download_dictionaries")
            self.spell_en = None

        print("OK Словари для проверки орфографии загружены")

    def _load_custom_dictionary(self, dict_path: str) -> set:
        """
        Загружает пользовательский словарь из файла

        Args:
            dict_path: Путь к файлу словаря

        Returns:
            Множество слов в нижнем регистре
        """
        custom_words = set()
        dict_file = Path(dict_path)

        if not dict_file.exists():
            print(f"INFO Пользовательский словарь не найден: {dict_path}")
            print(f"     Создайте файл {dict_path} для добавления своих слов")
            return custom_words

        try:
            with open(dict_file, 'r', encoding='utf-8') as f:
                for line in f:
                    # Убираем пробелы и переносы строк
                    line = line.strip()

                    # Пропускаем комментарии и пустые строки
                    if not line or line.startswith('#'):
                        continue

                    # Добавляем слово в нижнем регистре
                    custom_words.add(line.lower())

            if custom_words:
                print(f"OK Загружено {len(custom_words)} слов из пользовательского словаря")
            else:
                print(f"INFO Пользовательский словарь пуст")

        except Exception as e:
            print(f"WARNING Ошибка при чтении пользовательского словаря: {e}")

        return custom_words

    def extract_frames(self, video_path: str, interval: int = 2,
                      start_time: float = 0.0, end_time: float = None) -> List[Tuple[int, any]]:
        """
        Извлекает кадры из видео с заданным интервалом

        Args:
            video_path: Путь к видеофайлу
            interval: Интервал в секундах между кадрами
            start_time: Начальное время в секундах (по умолчанию с начала)
            end_time: Конечное время в секундах (по умолчанию до конца)

        Returns:
            Список кортежей (номер_кадра, изображение)
        """
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
            print(f"WARNING Начальное время {start_time}s превышает длительность видео {duration:.1f}s")
            start_frame = 0

        if end_frame > total_frames:
            end_frame = total_frames

        if start_frame >= end_frame:
            raise ValueError(f"Начальное время ({start_time}s) должно быть меньше конечного ({end_time}s)")

        print(f"Анализ видео с {start_time}s до {end_time if end_time else duration:.1f}s")
        print(f"Кадры: {start_frame} - {end_frame} из {total_frames}")

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
        print(f"✓ Извлечено {len(frames)} кадров из видео")
        return frames

    def extract_text(self, frame) -> str:
        """
        Извлекает текст из кадра с помощью EasyOCR

        Args:
            frame: Изображение кадра (numpy array)

        Returns:
            Распознанный текст
        """
        # EasyOCR работает с изображениями в формате RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Распознаем текст с детальной информацией о координатах
        results = self.reader.readtext(frame_rgb, detail=1)

        if not results:
            return ""

        # Сортируем блоки текста по вертикальной позиции (сверху вниз)
        # и группируем в строки
        sorted_results = sorted(results, key=lambda x: x[0][0][1])  # Сортировка по Y-координате

        # Группируем текстовые блоки по строкам (близкие по Y)
        lines = []
        current_line = []
        current_y = None
        y_threshold = 20  # Порог для объединения в одну строку (пикселей)

        for bbox, text, _ in sorted_results:
            # bbox[0][1] - это Y-координата верхнего левого угла
            y_pos = bbox[0][1]

            if current_y is None or abs(y_pos - current_y) <= y_threshold:
                # Текст на той же строке
                current_line.append((bbox[0][0], text))  # Сохраняем X-координату и текст
                if current_y is None:
                    current_y = y_pos
            else:
                # Новая строка - сохраняем предыдущую
                if current_line:
                    # Сортируем по X-координате (слева направо)
                    current_line.sort(key=lambda x: x[0])
                    lines.append(' '.join([t[1] for t in current_line]))
                current_line = [(bbox[0][0], text)]
                current_y = y_pos

        # Добавляем последнюю строку
        if current_line:
            current_line.sort(key=lambda x: x[0])
            lines.append(' '.join([t[1] for t in current_line]))

        # Объединяем строки с переносами
        text = '\n'.join(lines)

        return text

    def check_spelling(self, text: str) -> List[str]:
        """
        Проверяет орфографию и возвращает список ошибок

        Args:
            text: Текст для проверки

        Returns:
            Список найденных ошибок с вариантами исправления
        """
        errors = []

        # Разделяем текст на строки
        lines = text.split('\n')

        for line in lines:
            if not line.strip():
                continue

            # Извлекаем слова из строки (только буквы)
            words = re.findall(r'[а-яёА-ЯЁa-zA-Z]+', line)

            for word in words:
                # Пропускаем короткие слова и одиночные символы
                if len(word) < 3:
                    continue

                # Определяем язык слова
                cyrillic_count = len(re.findall('[а-яёА-ЯЁ]', word))
                latin_count = len(re.findall('[a-zA-Z]', word))

                # Пропускаем смешанные слова
                if cyrillic_count > 0 and latin_count > 0:
                    continue

                # Выбираем соответствующий словарь
                if cyrillic_count > 0:
                    spell_checker = self.spell_ru
                elif latin_count > 0:
                    spell_checker = self.spell_en
                else:
                    continue

                # Если словарь не загружен, пропускаем
                if spell_checker is None:
                    continue

                # Проверяем, есть ли слово в пользовательском словаре
                word_lower = word.lower()
                if word_lower in self.custom_words:
                    continue  # Слово в whitelist, пропускаем

                # Проверяем слово в основном словаре (регистронезависимо)
                if not spell_checker.lookup(word) and not spell_checker.lookup(word.lower()):
                    # Получаем варианты исправления (suggest возвращает генератор)
                    suggestions = list(spell_checker.suggest(word))[:3]

                    if suggestions:
                        errors.append(f"{word} (возможно: {', '.join(suggestions)})")
                    else:
                        errors.append(f"{word} (варианты не найдены)")

        return errors

    def process_video(self, video_path: str, interval: int = 2,
                     start_time: float = 0.0, end_time: float = None):
        """
        Основной метод обработки видео

        Args:
            video_path: Путь к видеофайлу
            interval: Интервал в секундах между кадрами
            start_time: Начальное время в секундах (по умолчанию с начала)
            end_time: Конечное время в секундах (по умолчанию до конца)
        """
        print(f"\n{'='*60}")
        print(f"Обработка видео: {video_path}")
        print(f"{'='*60}\n")

        # Извлекаем кадры
        frames = self.extract_frames(video_path, interval, start_time, end_time)

        total_errors = 0
        frames_with_errors = 0

        # Обрабатываем каждый кадр
        for frame_num, frame in frames:
            print(f"\nОбработка кадра {frame_num}...")

            # Извлекаем текст
            text = self.extract_text(frame)

            if not text.strip():
                print("  ℹ Текст не обнаружен")
                continue

            print(f"  ℹ Распознанный текст: {text[:100]}...")

            # Проверяем орфографию
            errors = self.check_spelling(text)

            if errors:
                frames_with_errors += 1
                total_errors += len(errors)
                print(f"  ✗ Найдено ошибок: {len(errors)}")

                # Сохраняем скриншот с ошибками
                output_path = self.output_dir / f"frame_{frame_num}_errors.jpg"
                cv2.imwrite(str(output_path), frame)

                # Сохраняем список ошибок в текстовый файл
                error_file = self.output_dir / f"frame_{frame_num}_errors.txt"
                with open(error_file, 'w', encoding='utf-8') as f:
                    f.write(f"Кадр: {frame_num}\n")
                    # Примечание: точное время рассчитывается на основе FPS видео
                    f.write(f"Время: ~{frame_num / 30:.1f} сек (приблизительно)\n\n")
                    f.write(f"Полный текст:\n{text}\n\n")
                    f.write("Найденные ошибки:\n")
                    for error in errors:
                        f.write(f"  - {error}\n")

                print(f"  ✓ Сохранено: {output_path}")
            else:
                print("  ✓ Ошибок не найдено")

        print(f"\n{'='*60}")
        print(f"ОБРАБОТКА ЗАВЕРШЕНА!")
        print(f"{'='*60}")
        print(f"Всего обработано кадров: {len(frames)}")
        print(f"Кадров с ошибками: {frames_with_errors}")
        print(f"Всего найдено ошибок: {total_errors}")
        print(f"Результаты сохранены в: {self.output_dir.absolute()}")
        print(f"{'='*60}\n")


def main():
    """Пример использования"""
    import sys

    if len(sys.argv) < 2:
        print("Использование: python video_speller.py <путь_к_видео> [интервал_в_секундах]")
        print("Пример: python video_speller.py video.mp4 2")
        sys.exit(1)

    video_path = sys.argv[1]
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 2

    checker = VideoSpellChecker(output_dir="screenshots_with_errors")
    checker.process_video(video_path, interval=interval)


if __name__ == "__main__":
    main()
