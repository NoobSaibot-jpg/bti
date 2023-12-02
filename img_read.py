import os
import re
import pytesseract
import PIL.Image
from rich.console import Console
from tkinter import filedialog
from tkinter import *
import mysql.connector

console = Console()
dir = os.getcwd()
console.print('Busines', style= 'bold black on white', justify='center')

root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()

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
        console.log(f"Ошибка подключения к базе данных: {err}", log_locals = True)
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
        console.log("Дані успішно оновленні в базі даних \n", style='white on green')
    except mysql.connector.Error as err:
        console.log(f"Помилка при оновленні даних: {err} :warning \n", style='white on red')
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
    database = input("Укажіть базу: ")
    return host, user, password, database

host, user, password, database = get_database_credentials()
mydb = connect_to_database(host, user, password, database)

def get_column_value(barcode, mydb):
    mycursor = mydb.cursor()
    try:
        mycursor.execute("SELECT case_box FROM cases WHERE case_barcode = %s", (barcode,))
        result = mycursor.fetchone()  # Получение одной строки результата
        if result:
            column_value = result[0]  # Значение столбца из первой строки
            return column_value
        else:
            return None
    except mysql.connector.Error as err:
        print({err})
        return None

for i in folders:
    try:
        if len(i) == 13 and len(os.listdir(os.path.join(folder_selected, i))) == 0:
            console.log(
                f'{i} - Порожня папка :warning: \n', style='white on red')
            output_file.write(f'Справа {i}: порожня папка\n')
        elif len(i) != 13 and os.path.isdir(os.path.join(folder_selected, i)):
            console.log(f'{i} - не справа \n')
        elif os.path.isfile(os.path.join(folder_selected, i)):
            console.log(f'{i} - не справа \n')
        elif len(i) == 13 and len(os.listdir(os.path.join(folder_selected, i))) > 0:
            if os.path.splitext(os.listdir(os.path.join(folder_selected, i))[0])[1] == exten:
                data = read_img(os.path.join(folder_selected, i, os.listdir(os.path.join(folder_selected, i))[0]))

                if len(data) == 0 or len(data[0]) == 0 or len(data[1]) == 0:
                    console.log(
                        f'{i}: не вдалося розпізнати зображення :warning: \n', style='white on red')
                    output_file.write(f'Справа {i}: не вдалося розпізнати\n')
                elif len(data) > 0:
                    column_value = get_column_value(i, mydb)
                    if column_value:
                        console.log(f"Справа {i} можливо дубль штрихкодів :warning: \n", style='white on red')
                        output_file.write(f'Справа {i}: можливо дубль\n')
                    else:
                        box = str(data[0])
                        b_index = box.find('.')
                        cut_box = box[b_index:-2].strip('.')
                        st = str(data[1])
                        st_index = st.find('.')
                        cut_str = str_type(st[2:st_index:].strip('.'))
                        console.log(
                            f'Справа {i}:  успішно ріспізнано {cut_box}, {cut_str} \n', style='white on green')
                        output_file.write(f'Справа {i}: {data}\n')
                        add_to_db(cut_box, i, cut_str, mydb)
            else:
                print(f'{i}')
    except Exception as e:
        console.log("Exception occurred:", e, style='white on red :warning: \n')
if mydb:
    mydb.close()
output_file.close()
input()

