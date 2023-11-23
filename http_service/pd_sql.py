#=================== С ПОМОЩЬЮ PANDAS ДОБАВЛЯЕТСЯ ФАЙЛ В SQL ===================
import pandas as pd
import sqlite3
from creat_table_info import creat_table_info



# применяется при скачивания и добавления в базу файла со страницы kaggle
def upload_table_to_db(p: str):
    # Подключаемся к базе данных
    connection = sqlite3.connect('db.sqlite3')

    # Читаем файл CSV и загружаем его в базу данных
    df = pd.read_csv(p, encoding='latin-1')
    # отделяем расширение файла
    file = (str(p.split('.')[0])) 
    # меняем тире(минус) на подчерк
    new_name = file.replace('-', "_") 
    # загружаем файл в базу
    df.to_sql(new_name, connection, if_exists='replace', index=False) 
    
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()

# применяется при загрузке в базу файла со страницы
def upload_table_to_db_2(p: str):
    # Подключаемся к базе данных
    connection = sqlite3.connect('db.sqlite3')

    # Читаем файл CSV и загружаем его в базу данных
    df = pd.read_csv(p, encoding='latin-1')
    # отделяем расширение файла
    file = (str(p.split('.')[0]))
    # отделяем часть указанного пути до последнего слеша(/)
    file_2 = (str(file.split('/')[-1])) 
    # меняем тире(минус) на подчерк
    table_name = file_2.replace('-', "_") 
    # загружаем файл в базу
    df.to_sql(table_name, connection, if_exists='replace', index=False) 
    
    creat_table_info(table_name) 
    
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()


