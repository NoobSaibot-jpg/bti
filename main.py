from database_operations import connect_to_database, add_to_db, get_column_value
from image_processing import read_img
import os
from rich.console import Console
from tkinter import filedialog
from tkinter import *

console = Console()
dir = os.getcwd()
exten = '.jpg'

root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()
output_file = open("output.txt", "w", encoding="utf-8")

def get_database_credentials():
    host = input("Укажите хост: ")
    user = input("Укажите пользователя: ")
    password = input("Укажите пароль: ")
    database = input("Укажите базу данных: ")
    return host, user, password, database

host, user, password, database = get_database_credentials()
mydb = connect_to_database(host, user, password, database)

# Функция для обработки папок и изображений
def process_folders(folder_selected, mydb):
    folders = os.listdir(folder_selected)
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
                    cut_box, cut_str = read_img(os.path.join(folder_selected, i, os.listdir(os.path.join(folder_selected, i))[0]))
                    if cut_box == None:
                        console.log(
                            f'{i}: не вдалося розпізнати зображення :warning: \n', style='white on red')
                        output_file.write(f'Справа {i}: не вдалося розпізнати\n')
                    elif cut_box:
                        column_value = get_column_value(i, mydb)
                        if column_value:
                            console.log(f"Справа {i} можливо дубль штрихкодів :warning: \n", style='white on red')
                            output_file.write(f'Справа {i}: можливо дубль\n')
                    else:
                        
                        console.log(
                            f'Справа {i}:  успішно ріспізнано кв:{cut_box} \n', style='white on green')
                        output_file.write(f'Справа {i}: кв: {cut_box}, тип вулиці: {cut_str}\n')
                        add_to_db(barcode= i, mydb= mydb, box= cut_box, strtype= cut_str)
            else:
                print(f'{i}')
        except Exception as e:
            console.print(f"Произошла ошибка: {e} :warning: ", style='white on red')

process_folders(folder_selected, mydb)
if mydb:
    mydb.close()
output_file.close()
input()