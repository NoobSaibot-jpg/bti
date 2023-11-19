import shutil
import re
import pytesseract
import PIL.Image

import os
from rich.console import Console
from tkinter import filedialog
from tkinter import *

console = Console()
dir = os.getcwd()

root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()

def move_directory(fold, dist):
    shutil.move(fold, dist)

tess_path = f'{dir}\\tess\\tesseract.exe'
exten = '.jpg'

folders = os.listdir(folder_selected)

pattern_fl = r"кв\.?\s*\d+"
pattern_str = r'\b(бул|вул|ква|наб|площ|про|туп|уз|шос)\b'

def read_img(file_name):
    img = PIL.Image.open(file_name)
    pytesseract.pytesseract.tesseract_cmd = tess_path
    text = pytesseract.image_to_string(img, lang='ukr')
    list_text = list(text.split('\n'))
    fl = [item for item in list_text if re.search(pattern_fl, item)]
    st = [item for item in list_text if re.search(pattern_str, item)]
    return fl, st

output_file = open("output.txt", "w", encoding="utf-8")

for i in folders:
    try:
        if len(i) == 13 and len(os.listdir(os.path.join(folder_selected, i))) == 0:
            move_directory(os.path.join(folder_selected, i), f'{folder_selected}\\Проблемни')
            console.print(
                f'{i} - папка пуста, перемещена в директорию с проблемами', style='white on red')
        elif len(i) != 13 and os.path.isdir(os.path.join(folder_selected, i)):
            console.print(f'{i} - это папка, но нет дела')
        elif os.path.isfile(os.path.join(folder_selected, i)):
            console.print(f'{i} - это файл')
        elif len(i) == 13 and len(os.listdir(os.path.join(folder_selected, i))) > 0:
            if os.path.splitext(os.listdir(os.path.join(folder_selected, i))[0])[1] == exten:
                data = read_img(os.path.join(folder_selected, i, os.listdir(os.path.join(folder_selected, i))[0]))
                if len(data) == 0 or len(data[0]) == 0 or len(data[1]) == 0:
                    console.print(
                        f'{i}: не удалось прочитать изображение, перемещено в директорию с проблемами :warning:', style='white on red')
                    move_directory(os.path.join(folder_selected, i), f'{folder_selected}\\Проблемни')
                elif len(data) > 0:
                    console.print(
                        f'Дело {i}:  успешно! {data}    перемещено в папку "Подписаные"', style='white on green')
                    output_file.write(f'Дело {i}: {data}\n')
                    move_directory(os.path.join(folder_selected, i), f'{folder_selected}\\Подписаные')
            else:
                print(f'{i} - это не изображение')
    except Exception as e:
        print("Exception occurred:", e)

output_file.close()

