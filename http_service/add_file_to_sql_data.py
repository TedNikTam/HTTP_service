#=================== ДОБАВЛЕНИЯ ТАБЛИЦЫ И СОДЕРЖИМОГО ФАЙЛА В БАЗУ ===================
import sqlite3
import pandas as pd
from pd_sql import upload_table_to_db_2


def add_file_to_sql_data():
    # Подключаемся к базе данных
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    # делаем запрос в базу к таблице app_1_file куда сохранились название и адрес файла
    cursor.execute('SELECT * FROM app_1_file')
    app_1_file = cursor.fetchall()
    for i in app_1_file:
        # формируется полный адресс файла
        p = f"C:/Users/NickT/Desktop/PY_code/qwe/HTTP_service/http_service/{i[2]}"
        # файл читается
        df = pd.read_csv(p, encoding='latin-1')
        # отправляется для полноценного создания таблицы, с содержимым файла, в базе
        upload_table_to_db_2(p)
    # закрываем соединение с базой
    connection.close()