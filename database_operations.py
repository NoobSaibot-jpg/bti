import mysql.connector

class DB:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connect()

    def connect(self):
        try:
            self.mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Подключение к базе данных успешно!")
        except mysql.connector.Error as err:
            print(f"Ошибка подключения к базе данных: {err}")
            self.mydb = None

    def add_to_db(self, box, barcode, strtype):
        if self.mydb:
            mycursor = self.mydb.cursor()
            try:
                mycursor.execute(
                    "UPDATE `cases` SET case_box = %s WHERE case_barcode = %s",
                    (box, barcode)
                )
                mycursor.execute(
                    "UPDATE `cases` SET case_strtype = %s WHERE case_barcode = %s",
                    (strtype, barcode)
                )
                self.mydb.commit()
                print("Данные успешно обновлены в базе данных")
            except mysql.connector.Error as err:
                print(f"Ошибка при обновлении данных: {err}")
            finally:
                mycursor.close()
        else:
            print("Нет подключения к базе данных.")

    def get_column_value(self, barcode):
        if self.mydb:
            mycursor = self.mydb.cursor()
            try:
                mycursor.execute("SELECT case_box FROM cases WHERE case_barcode = %s", (barcode,))
                result = mycursor.fetchone()  # Получение одной строки результата
                if result:
                    column_value = result[0]  # Значение столбца из первой строки
                    return column_value
                else:
                    return None
            except mysql.connector.Error as err:
                print(f"Ошибка при выполнении запроса: {err}")
                return None
            finally:
                mycursor.close()
        else:
            print("Нет подключения к базе данных.")

db = DB("localhost", "root", "", "bti")
# db.add_to_db("666", "2800000553212", "4")
print(db.get_column_value("2800000553212"))
