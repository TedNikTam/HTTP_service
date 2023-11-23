from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import sqlite3
from dwnld_kag_tab import dwnld_kag_tab
from pd_sql import upload_table_to_db_2
from .forms import FileUploadForm


#=====================================================================================
# получаем запрос со страницы
def index(request):
    return render(request, "index.html")
#=====================================================================================
# принемает назание таблицы и отправляет названия столбцов и содержимое   
def post_tables(request):
    # Подключаемся к базе данных   
    connection = sqlite3.connect('db.sqlite3') 
    cursor = connection.cursor()
    # получение запроса со страницы
    table_name = request.POST.get("resp", "Undefined")
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
    
    # закрываем соединение с базой
    connection.commit()
    connection.close()
    # отправляем полученные данные на страницу
    return HttpResponse(f"<h3>Название столбцов: <br> {column_names_list} <br><br> Содержимое таблицы: <br>{table_content_list} </h3>")
#=====================================================================================
# принемает назание таблицы и удаляет её
def del_tables(request):
    # Подключаемся к базе данных   
    connection = sqlite3.connect('db.sqlite3') 
    cursor = connection.cursor()
    # получение запроса со страницы
    table_name = request.POST.get("delete_table", "Undefined")
    # формирование запроса на удаление таблицы из базы
    del_table = f'DROP TABLE IF EXISTS {table_name};'
    # удаление таблицы
    cursor.execute(del_table)
    # закрываем соединение с базой
    connection.commit()
    connection.close()
    # отправляем ответ на страницу
    return HttpResponse(f"<h3>Таблица удалена</h3>")
#===================================================================================== 
# принемает ссылку на скачиваение таблицы с kaggle и отправляет ответ
def kaggle_table(request):
    kaggle_table_link = request.POST.get("dwnld", "Undefined") 
    # запрос отправляется для скачивания и формирования ответа 
    a = dwnld_kag_tab(kaggle_table_link)
    # ответ отправляется на страницу
    return HttpResponse(a)
#=====================================================================================
# по нажатию кнопки отправляет список таблиц
def all_tables(request):
    # Подключаемся к базе данных   
    connection = sqlite3.connect('db.sqlite3') 
    cursor = connection.cursor()
    # получат и отправляет спиксок всех таблиц
    all_tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all_tables_listik = []
    for table in all_tables:
        all_tables_listik.append(table[0])
    all_tables_list ="<br>".join(all_tables_listik)
    # ответ отправляется на страницу
    return HttpResponse(f"<h3>Все таблицы: <br> {all_tables_list} </h3>")
#=====================================================================================
# загружается файл в папку uplads и в таблице app_1_file сохраняется информация об адресе 
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            find_file()
    else:
        form = FileUploadForm()
    return render(request, 'upload_file.html', {'form': form})

# после загрузки формируется адрес файла для создания таблицы, с его содержимым, в базе
# работает строго с CSV
def find_file():
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
#=====================================================================================