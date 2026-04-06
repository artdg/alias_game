import PyInstaller.__main__
import os

# Параметры сборки
PyInstaller.__main__.run([
    'alias_game.py',
    '--onefile',           # Один exe файл
    '--windowed',          # Без консоли
    '--name=AliasGame',    # Имя файла
    '--icon=icon.ico',     # Иконка (если есть)
    '--add-data=words.txt;.', # Если есть дополнительные файлы
    '--hidden-import=tkinter',
    '--hidden-import=threading',
    '--clean',             # Очистка временных файлов
])