#!/usr/bin/env python3
"""
Конвертирует app.ico в PNG файлы разных размеров для Linux
"""
from PIL import Image
import os

# Путь к исходному .ico файлу
ico_path = "assets/app.ico"
output_dir = "assets"

# Открываем .ico файл
img = Image.open(ico_path)

# Размеры для создания
sizes = [48, 128, 256]

for size in sizes:
    # Создаём копию изображения и изменяем размер
    resized = img.resize((size, size), Image.Resampling.LANCZOS)

    # Сохраняем как PNG
    output_path = os.path.join(output_dir, f"app_{size}.png")
    resized.save(output_path, "PNG")
    print(f"Created: {output_path}")

# Создаём основную иконку app.png (256x256)
main_icon = img.resize((256, 256), Image.Resampling.LANCZOS)
main_icon.save(os.path.join(output_dir, "app.png"), "PNG")
print(f"Created: {os.path.join(output_dir, 'app.png')}")

print("\nDone! PNG icons created successfully.")
