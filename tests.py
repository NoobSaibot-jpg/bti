# import shutil
# import re
import pytesseract
from PIL import Image, ImageEnhance
import os
from tkinter import filedialog
from tkinter import *

import mysql.connector

import PIL.Image

import os
from rich.console import Console
from tkinter import filedialog
from tkinter import *


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bti"
)

# Создаем курсор для выполнения запросов
mycursor = mydb.cursor()



# def get_column_value(barcode, mydb):
#     mycursor = mydb.cursor()
#     try:
#         mycursor.execute("SELECT case_box FROM cases WHERE case_barcode = %s", (barcode,))
#         result = mycursor.fetchone()  # Получение одной строки результата
#         if result:
#             column_value = result[0]  # Значение столбца из первой строки
#             return column_value
#         else:
#             return None
#     except mysql.connector.Error as err:
#         print({err})
#         return None

# Использование функции для получения значения столбца
# barcode = '2800003547831'
# column_value = get_column_value(barcode, mydb)
# if column_value:
#     print(f"Значение столбца: {column_value}")
# else:
#     print("Данные не найдены или произошла ошибка")

# ... (ваш код после этого)
# UPDATE название_таблицы
# SET имя_поля = 'новое_значение'
# WHERE условие;

# def value():
#     a = mycursor.execute('''
#              SELECT case_box FROM `cases` WHERE case_id =37029394
#              ''')
#     return a

# print(value())



mycursor.execute('''
             UPDATE `cases` 
             SET case_box = ""
             ''')

mycursor.execute('''
             UPDATE `cases` 
             SET case_strtype = ""
             ''')

mydb.commit()
mydb.close()

# Получаем результаты запроса
# myresult = mycursor.fetchall()
# for row in myresult:
#     print(row)

# console = Console()
# dir = os.getcwd()

# root = Tk()
# root.withdraw()
# folder_selected = filedialog.askdirectory()

# def move_directory(fold, dist):
#     shutil.move(fold, dist)

# tess_path = f'{dir}\\tess\\tesseract.exe'
# exten = '.jpg'

# folders = os.listdir(folder_selected)


# for folder in folders:
#     if len(folder) == 13:
#        mycursor.execute(f'''
#                  INSERT INTO cases (case_barcode)
#                  VALUES ({folder})
#                  ''')
#     else:
#         print(f'{folder} - это не изображение')



# pattern_fl = r"кв\.?\s*\d+"
# pattern_str = r'\b(бул|вул|ква|наб|площ|про|туп|уз|шос)\b'

# def read_img(file_name):
#     img = PIL.Image.open(file_name)
#     pytesseract.pytesseract.tesseract_cmd = tess_path
#     text = pytesseract.image_to_string(img, lang='ukr')
#     return text


# print(read_img('IMG_4912.jpg'))
# output_file = open("output.txt", "w", encoding="utf-8")

# for i in folders:
#     try:
#         if len(i) == 13 and len(os.listdir(os.path.join(folder_selected, i))) == 0:
#             move_directory(os.path.join(folder_selected, i), f'{folder_selected}\\Проблемни')
#             console.print(
#                 f'{i} - папка пуста, перемещена в директорию с проблемами', style='white on red')
#         elif len(i) != 13 and os.path.isdir(os.path.join(folder_selected, i)):
#             console.print(f'{i} - это папка, но нет дела')
#         elif os.path.isfile(os.path.join(folder_selected, i)):
#             console.print(f'{i} - это файл')
#         elif len(i) == 13 and len(os.listdir(os.path.join(folder_selected, i))) > 0:
#             if os.path.splitext(os.listdir(os.path.join(folder_selected, i))[0])[1] == exten:
#                 data = read_img(os.path.join(folder_selected, i, os.listdir(os.path.join(folder_selected, i))[0]))
#                 if len(data) == 0 or len(data[0]) == 0 or len(data[1]) == 0:
#                     console.print(
#                         f'{i}: не удалось прочитать изображение, перемещено в директорию с проблемами :warning:', style='white on red')
#                     move_directory(os.path.join(folder_selected, i), f'{folder_selected}\\Проблемни')
#                 elif len(data) > 0:
#                     console.print(
#                         f'Дело {i}:  успешно! {data}    перемещено в папку "Подписаные"', style='white on green')
#                     output_file.write(f'Дело {i}: {data}\n')
#                     move_directory(os.path.join(folder_selected, i), f'{folder_selected}\\Подписаные')
#             else:
#                 print(f'{i} - это не изображение')
#     except Exception as e:
#         print("Exception occurred:", e)

# output_file.close()

# # print (read_img("photo_1.jpg"))
# # root = Tk()
# # root.withdraw()
# # folder_selected = filedialog.askdirectory()
# # folders = list(os.listdir(folder_selected))
# # for i in folders:
# #     print(i)