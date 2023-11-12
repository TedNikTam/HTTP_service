# скачивание таблицы с kaggle по полученной ссылке со страницы
import os
import zipfile
import pandas as pd
from pd_sql import upload_table_to_db


def dwnld_kag_tab(kaggle_table_link: str):
    os.system(f'kaggle datasets download -d {kaggle_table_link}') # скачивание файла
    file = (str(kaggle_table_link.split('/')[1]) +'.zip') # формирование названия zip-файла
    f_zip = zipfile.ZipFile(file, 'r') # zip-файл открывается на чтение
    f_zip.extractall('./') # извлекается содержимое zip-файла
    for file_info in f_zip.infolist(): # запускается цикл по чтению содержимого zip-файла
        p = file_info.filename
        # передаем файл в функцию для загрузки в базу
        upload_table_to_db(p)
        data = pd.read_csv(p, encoding='latin-1')
        os.remove(p) # после получения информации файл удаляется
        # формируется информация о фале и помещаеттся в перемменную
        a = (
            f"<h3>Название файла: <br>{file_info.filename} <br><br> "
            f"\nИнформация о колонках в файле: <br> {data.columns} <br><br>" 
            f"\nКол-во строк и столбцов:  <br>{data.shape} </h3>"
            )
        print(
            "\nНазвание файла: ", file_info.filename,
            "\nИнформация о колонках в файле: ", data.columns,
            "\nКол-во строк и столбцов: ", data.shape,
            )
    f_zip.close() # zip-файл закрывается
    os.remove(file) # zip-файл удаляется
    print(f"-"*20 + "\nФайлы удалены!")
    
    # переменная с информацией о файле возвращается в основную функцию
    return(a)