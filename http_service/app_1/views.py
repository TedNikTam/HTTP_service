from django.shortcuts import render
from django.http import HttpResponse
import requests
import os
import pandas as pd
import zipfile
import sqlite3
from dwnld_kag_tab import dwnld_kag_tab
 
def index(request):
    return render(request, "index.html")

#===========================================
# принемает ссылку на скачиваение таблицы с kaggle и отправляет ответ
def kaggle_table(request):
    kaggle_table_link = request.POST.get("dwnld", "Undefined") 
    # запрос отправляется для скачивания и формирования ответа 
    a = dwnld_kag_tab(kaggle_table_link)
    # ответ отправляется на страницу
    return HttpResponse(a)
   


def post_tables(request):
    # Подключаемся к базе данных   
    connection = sqlite3.connect('db.sqlite3') 
    cursor = connection.cursor()

    # получаем спиксок всех таблиц
    all_tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all_tables_list = []
    for table in all_tables:
        all_tables_list.append(table[0])

    # получение запроса со страницы
    table_name = request.POST.get("resp", "Undefined") 
    print(type(table_name))
    cursor = connection.execute(f'SELECT * FROM {table_name}')
    table_content = cursor.fetchall()
 
    # получаем названия столцов в таблице
    connection.row_factory = sqlite3.Row
    cursor = connection.execute(f'SELECT * FROM {table_name}')
    column_names = cursor.fetchone()
    # names = column_names.keys() # .keys - вытаскивает имена
    
    # закрываем соединение с базой
    connection.commit()
    connection.close()

    # отправляем полученные данные на страницу
    return HttpResponse(f"<h3>Все таблицы: <br>{all_tables_list} <br><br> Название столбцов: <br> {column_names.keys()} <br><br> Содержимое таблицы: <br>{table_content} </h3>")
#===========================================

# def postuser(request):   
#     # Подключаемся к базе данных 
#     conn = sqlite3.connect('db.sqlite3')
#     # получение запроса со страницы
#     nam = request.POST.get("resp", "Undefined") 
#     # скачивание файла
#     os.system(f'kaggle datasets download -d {nam}') 
#     # формирование названия zip-файла
#     file = (str(nam.split('/')[1]) +'.zip') 
#     # zip-файл открывается на чтение
#     f_zip = zipfile.ZipFile(file, 'r') 
#     # извлекается содержимое zip-файла
#     f_zip.extractall('./') 
#     # запускается цикл по чтению содержимого zip-файла
#     for file_info in f_zip.infolist(): 
#         # читаем файл
#         data = pd.read_csv(file_info.filename, encoding='latin-1')
#         # Читаем файл CSV и создаем таблицу в базе данных
#         data.to_sql(file_info.filename, conn, if_exists='replace', index=False)
#         print(
#             "\nНазвание файла: ", file_info.filename,
#             "\nИнформация о колонках в файле: ", data.columns,
#             "\nКол-во строк и столбцов: ", data.shape,
#             )

#     # zip-файл закрывается   
#     f_zip.close() 
#     # после получения информации zip-файл удаляется
#     os.remove(file)
#     # после получения информации файл удаляется 
#     os.remove(file_info.filename) 
#     # Сохраняем изменения и закрываем соединение
#     conn.commit()
#     conn.close()
#     # отправляем полученные данные на страницу
#     return HttpResponse(f"<h3>Название файла: <br> {file_info.filename} <br><br> Информация о колонках в файле: <br>{list(data.columns)} <br><br> Кол-во строк и столбцов: <br>{data.shape}</h3>")
#===========================================
# def index(request):
#     return render(request, "index.html")

# def postuser(request):    
#     nam = request.POST.get("resp", "Undefined") # получаем из данных запроса POST отправленные через форму данные
#     url = f'https://www.kaggle.com/datasets?search={nam}'
#     # datasets_list = os.system(f'kaggle datasets list -s {nam}')
#     responce = requests.get(url)
#     print(responce.url, 'url')
#     return HttpResponse(f"<h3>Название файла: {responce.url} <br> {os.system(f'kaggle datasets list -s {nam}')} </h3>")
