"""
Скрипт для загрузки словарей Hunspell
"""
import urllib.request
import os
from pathlib import Path

def download_file(url, destination):
    """Загрузить файл по URL"""
    print(f"Загрузка {destination}...")
    try:
        urllib.request.urlretrieve(url, destination)
        size_kb = os.path.getsize(destination) / 1024
        print(f"OK {destination} загружен ({size_kb:.1f} KB)")
        return True
    except Exception as e:
        print(f"ERROR {destination}: {e}")
        return False

def main():
    # Создаем папку для словарей
    dict_dir = Path("dictionaries")
    dict_dir.mkdir(exist_ok=True)

    print("Загрузка словарей Hunspell...")
    print("="*60)

    # URLs для словарей (используем репозиторий с актуальными словарями)
    dictionaries = [
        {
            'name': 'Русский (ru_RU)',
            'files': [
                ('https://raw.githubusercontent.com/LibreOffice/dictionaries/master/ru_RU/ru_RU.aff',
                 'dictionaries/ru_RU.aff'),
                ('https://raw.githubusercontent.com/LibreOffice/dictionaries/master/ru_RU/ru_RU.dic',
                 'dictionaries/ru_RU.dic'),
            ]
        },
        {
            'name': 'Английский (en_US)',
            'files': [
                ('https://raw.githubusercontent.com/LibreOffice/dictionaries/master/en/en_US.aff',
                 'dictionaries/en_US.aff'),
                ('https://raw.githubusercontent.com/LibreOffice/dictionaries/master/en/en_US.dic',
                 'dictionaries/en_US.dic'),
            ]
        }
    ]

    for dict_info in dictionaries:
        print(f"\n{dict_info['name']}:")
        for url, dest in dict_info['files']:
            download_file(url, dest)

    print("\n" + "="*60)
    print("Загрузка завершена!")
    print("\nПроверка словарей...")

    # Проверяем, что файлы загружены
    required_files = [
        'dictionaries/ru_RU.aff',
        'dictionaries/ru_RU.dic',
        'dictionaries/en_US.aff',
        'dictionaries/en_US.dic'
    ]

    all_ok = True
    for file_path in required_files:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 100:
            print(f"OK {file_path}")
        else:
            print(f"ERROR {file_path} - отсутствует или поврежден")
            all_ok = False

    if all_ok:
        print("\nOK Все словари успешно загружены!")
        return 0
    else:
        print("\nERROR Некоторые словари не загружены")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
