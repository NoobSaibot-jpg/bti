import shutil
import re
import pytesseract
import PIL.Image

import os
from rich.console import Console
from tkinter import filedialog
from tkinter import *
import mysql.connector

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
pattern_str = r'\b(бул|вул|кв|наб|пл|пров|туп|уз|шос|пр-кт)\b'

def str_type(str):
    if str == 'бул':
        return 8
    elif str == 'вул':
        return 1
    elif str == 'кв':
        return 9
    elif str == 'наб':
        return 10
    elif str == 'пл':
        return 4
    elif str == 'пров':
        return 2
    elif str == 'туп':
        return 7
    elif str == 'уз':
        return 6
    elif str == 'шос':
        return 11
    elif str == 'пр-кт':
        return 3
    elif str == 'проїзд':
        return 5
    



def add_to_db(box, barcode, strtype):
    # db_host = input("Укажіть хост: ")
    # db_user = input("укажіть користувача: ")
    # db_password = input("Укажіть пароль: ")
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bti"
    )

    mycursor = mydb.cursor()
    mycursor.execute(f'''
                 UPDATE `cases` 
                 SET case_box = {box}
                  WHERE case_barcode = {barcode}
                 ''')
    mycursor.execute(f'''
                 UPDATE `cases` 
                 SET case_strtype = {strtype}
                  WHERE case_barcode = {barcode}
                 ''')
    mydb.commit()
    mydb.close()

def read_img(file_name):
    img = PIL.Image.open(file_name)
    pytesseract.pytesseract.tesseract_cmd = tess_path
    text = pytesseract.image_to_string(img, lang='ukr')
    list_text = list(text.split('\n'))
    fl = [item for item in list_text if re.search(pattern_fl, item)]
    st = [item for item in list_text if re.search(pattern_str, item)]
    if st != [] and fl != []:
        return fl, st
    else:
        return []

output_file = open("output.txt", "w", encoding="utf-8")

for i in folders:
    try:
        if len(i) == 13 and len(os.listdir(os.path.join(folder_selected, i))) == 0:
            # move_directory(os.path.join(folder_selected, i), f'{folder_selected}\\Проблемни')
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
                    # move_directory(os.path.join(folder_selected, i), f'{folder_selected}\\Проблемни')
                elif len(data) > 0:
                    box = str(data[0])
                    b_index = box.find('.')
                    cut_box = box[b_index:-2].strip('.')
                    st = str(data[1])
                    st_index = st.find('.')
                    cut_str = str_type(st[2:st_index:].strip('.'))
                    console.print(
                        f'Дело {i}:  успешно! {cut_box}, {cut_str}    перемещено в папку "Подписаные"', style='white on green')
                    output_file.write(f'Дело {i}: {data}\n')
                    add_to_db(box = cut_box, barcode = i, strtype=cut_str)
                    # move_directory(os.path.join(folder_selected, i), f'{folder_selected}\\Подписаные')
            else:
                print(f'{i} - это не изображение')
    except Exception as e:
        print("Exception occurred:", e)

output_file.close()
root.mainloop()

