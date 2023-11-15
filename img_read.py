import shutil
import re
import pytesseract
from PIL import Image
import os
from rich.console import Console
from rich.progress import track

console = Console()

dir = os.getcwd()


def move_directory(fold, dist):
    shutil.move(fold, dist)


tess_path = f'{dir}\\tess\\tesseract.exe'

exten = '.jpg'

folders = os.listdir()

pattern_fl = r"кв\.?\s*\d+"

pattern_str = r'\b(бул|вул|ква|наб|площ|про|туп|уз|шос)\b'


def read_img(file_name):
    img = Image.open(file_name)
    pytesseract.pytesseract.tesseract_cmd = tess_path
    text = pytesseract.image_to_string(img, lang='ukr')
    list_text = list(text.split('\n'))
    fl = [item for item in list_text if re.search(pattern_fl, item)]
    st = [item for item in list_text if re.search(pattern_str, item)]
    return fl, st


output_file = open("output.txt", "w", encoding="utf-8")

for i in track(folders, description= f"Processing folder"):
    if len(i) == 13 and len(os.listdir(i)) == 0:
        move_directory(i, f'{dir}\\Проблемни')
        console.print(
            f'{i} is folder no content and move to problem directory', style='white on red')
    elif len(i) != 13 and os.path.isdir(i):
        console.print(f'{i} is folder but no bisness')
    elif os.path.isfile(i):
        console.print(f'{i} is file')
    elif len(i) == 13 and len(os.listdir(i)) > 0:
        if os.path.splitext(os.listdir(i)[0])[1] == exten:
            data = read_img(f'{dir}\\{i}\\{os.listdir(i)[0]}')
            if len(data) == 0 or len(data[0]) == 0 or len(data[1]) == 0:
                console.print(
                    f'{i}: cant read image and move to problem directory :warning:', style='white on red')
                move_directory(i, f'{dir}\\Проблемни')
            elif len(data) > 0:
                console.print(
                    f'Дело {i}:  ok! {data}    move to OkFoler', style='white on green')
                output_file.write(f'Дело {i}: {data}\n')
                move_directory(i, f'{dir}\\Подписаные')
        else:
            print(f'{i} is not an image')

output_file.close()


