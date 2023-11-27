#=================== СОРТИРОВКА ПО СТОЛБЦАМ ===================
import sqlite3
import pandas as pd


def sort_by_column(table_name: str):
    # Подключаемся к базе данных   
    connection = sqlite3.connect('db.sqlite3') 

    ddd = pd.read_sql(f'SELECT * FROM {table_name}', connection)
    # выводит на печать всю таблицу
    # print(df)
    # ddd = df
    # all_colums = df.columns
    # print(all_colums)
   
    print(ddd)

    # sort_by = input('Введите азвание столбца: ')
    # ascending_by = input('Как сортировать? ↑ или ↓ ')
    # if ascending_by == '↑':
    #     ddd = df.sort_values(by=f'{sort_by}', ascending=True)
    # else:
    #     ddd = df.sort_values(by=f'{sort_by}', ascending=False)
    # print(ddd)

    print('>>>>>>>>>>=========================================<<<<<<<<<')
    # закрываем соединение с базой
    connection.commit()
    connection.close()
    return(ddd)

# sort_by_column()
