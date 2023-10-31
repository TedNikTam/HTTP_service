from django.shortcuts import render
from django.http import HttpResponse
import os
import pandas as pd
import zipfile

 
def index(request):
    return render(request, "index.html")
 
def postuser(request):    
    nam = request.POST.get("resp", "Undefined") # получаем из данных запроса POST отправленные через форму данные
    # datasets_list = str(os.system(f'kaggle datasets list -s {nam}'))
    # obj_adress = ("sahityasetu/crime-data-in-los-angeles-2020-to-present") # адрес для скачивания 
    os.system(f'kaggle datasets download -d {nam}') # скачивание файла
    file = (str(nam.split('/')[1]) +'.zip') # формирование названия zip-файла
    f_zip = zipfile.ZipFile(file, 'r') # zip-файл открывается на чтение
    f_zip.extractall('./') # извлекается содержимое zip-файла
    for file_info in f_zip.infolist(): # запускается цикл по чтению содержимого zip-файла
        data = pd.read_csv(file_info.filename, encoding='latin-1')
        print(
            "\nНазвание файла: ", file_info.filename,
            "\nИнформация о колонках в файле: ", data.columns,
            "\nКол-во строк и столбцов: ", data.shape,
            )
       
    f_zip.close() # zip-файл закрывается
    os.remove(file) # после получения информации zip-файл удаляется
    os.remove(file_info.filename) # после получения информации файл удаляется
    return HttpResponse(f"<h3>Название файла: {file_info.filename} <br> Информация о колонках в файле: {data.columns} <br> Кол-во строк и столбцов: {data.shape}</h3>")
