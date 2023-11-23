from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import sqlite3
from .forms import FileUploadForm
from dwnld_kag_tab import dwnld_kag_tab
from creat_table_info import creat_table_info
from add_file_to_sql_data import add_file_to_sql_data


#=====================================================================================
# получаем запрос со страницы
def index(request):
    return render(request, "index.html")
#=====================================================================================
# принемает назание таблицы и отправляет названия столбцов и содержимое   
def post_tables(request):
    # получение запроса со страницы
    table_name = request.POST.get("resp", "Undefined")
    # запрос отправляется для формирования данных о таблице
    sss = creat_table_info(table_name)
    # отправляем полученные данные обратно на страницу
    return HttpResponse(sss)
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
            add_file_to_sql_data()
    else:
        form = FileUploadForm()
    return render(request, 'upload_file.html', {'form': form})

# после загрузки формируется адрес файла для создания таблицы, с его содержимым, в базе
# работает строго с CSV

#=====================================================================================