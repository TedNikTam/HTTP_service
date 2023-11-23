#=================== НАЗВАНЯ СТОЛБЦОВ И СОДЕРЖИМОЕ ТАБЛИЦЫ ===================
import sqlite3


def creat_table_info(table_name: str):    
    # Подключаемся к базе данных   
    connection = sqlite3.connect('db.sqlite3') 
    cursor = connection.cursor()
    cursor = connection.execute(f'SELECT * FROM {table_name}')
    
    # содержимое таблицы - получется (список из кортежей)
    table_content = cursor.fetchall()
    # содержимое таблицы преобразуется в строку
    string = ''
    for el in table_content:
        string += str(el)
    table_content_list = ')<br>('.join(string.split(')('))


    # получаем названия столцов
    connection.row_factory = sqlite3.Row
    cursor = connection.execute(f'SELECT * FROM {table_name}')
    # получаем первую запись - названия столбцов
    column_names = cursor.fetchone()
    # названия столбцов (тип - список) преобразуется в строку и выводится списком
    column_names_list ="<br>".join(column_names.keys())

    # формируется ответ на страницу
    sss = (
        f"<h3>Название столбцов: </h3> {column_names_list} <br><br>" 
        f"<h3>Содержимое таблицы: </h3> {table_content_list}" 
    )

    # закрываем соединение с базой
    connection.commit()
    connection.close()
    # отправляем полученные данные обратно в функцию post_tables
    return(sss)