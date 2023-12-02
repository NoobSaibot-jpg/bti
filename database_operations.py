import mysql.connector
from rich.console import Console

console = Console()

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
        console.log(f"Ошибка подключения к базе данных: {err}", style='white on red')
        return None

def add_to_db(box, strtype, barcode, mydb):
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
        console.log("Данные успешно обновлены в базе данных", style='white on green')
    except mysql.connector.Error as err:
        console.log(f"Ошибка при обновлении данных: {err}", style='white on red')
    finally:
        mycursor.close()

def get_column_value(barcode, mydb):
    mycursor = mydb.cursor()
    try:
        mycursor.execute("SELECT case_box FROM cases WHERE case_barcode = %s", (barcode,))
        result = mycursor.fetchone()
        if result:
            column_value = result[0]
            return column_value
        else:
            return None
    except mysql.connector.Error as err:
        console.log(f"Ошибка запроса данных: {err}", style='white on red')
        return None