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
    



def connect_to_database(host, user, password, database):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Ошибка подключения к базе данных: {err}")
        return None
    
def add_to_db(box, barcode, strtype, mydb):
    mycursor = mydb.cursor()
    try:
        mycursor.execute(
            "UPDATE `cases` SET case_box = %s WHERE case_barcode = %s",
            (box, barcode)
        )
        mycursor.execute(
            "UPDATE `cases` SET case_strtype = %s WHERE case_barcode = %s",
            (strtype, barcode)
        )
        mydb.commit()
        console.print("Дані успішно оновленні в базі даних \n", style='white on green')
    except mysql.connector.Error as err:
        console.print(f"Помилка при оновленні даних: {err} :warning \n", style='white on red')
    finally:
        mycursor.close()

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

def get_database_credentials():
    host = input("Укажіть хост: ")
    user = input("Укажіть користувача: ")
    password = input("Укажіть пароль: ")
    database = "bti"
    return host, user, password, database

host, user, password, database = get_database_credentials()
mydb = connect_to_database(host, user, password, database)

for i in folders:
    try:
        if len(i) == 13 and len(os.listdir(os.path.join(folder_selected, i))) == 0:
            console.print(
                f'{i} - Порожня папка', style='white on red')
        elif len(i) != 13 and os.path.isdir(os.path.join(folder_selected, i)):
            console.print(f'{i} - не справа')
        elif os.path.isfile(os.path.join(folder_selected, i)):
            console.print(f'{i} - не справа')
        elif len(i) == 13 and len(os.listdir(os.path.join(folder_selected, i))) > 0:
            if os.path.splitext(os.listdir(os.path.join(folder_selected, i))[0])[1] == exten:
                data = read_img(os.path.join(folder_selected, i, os.listdir(os.path.join(folder_selected, i))[0]))

                if len(data) == 0 or len(data[0]) == 0 or len(data[1]) == 0:
                    console.print(
                        f'{i}: не вдалося розпізнати зображення :warning:', style='white on red')
                elif len(data) > 0:
                    box = str(data[0])
                    b_index = box.find('.')
                    cut_box = box[b_index:-2].strip('.')
                    st = str(data[1])
                    st_index = st.find('.')
                    cut_str = str_type(st[2:st_index:].strip('.'))
                    console.print(
                        f'Справа {i}:  успішно ріспізнано {cut_box}, {cut_str}"', style='white on green')
                    output_file.write(f'Справа {i}: {data}\n')
                    add_to_db(cut_box, i, cut_str, mydb)
            else:
                print(f'{i}')
    except Exception as e:
        console.print("Exception occurred:", e, style='white on red')
if mydb:
    mydb.close()
output_file.close()
input()

