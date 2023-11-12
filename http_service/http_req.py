from django.shortcuts import render
from django.http import HttpResponse

import requests
import os

def index(request):
    return render(request, "index.html")
 
def postuser(request):    
    nam = request.POST.get("resp", "Undefined") # получаем из данных запроса POST отправленные через форму данные
    url = f'https://www.kaggle.com/datasets?search={nam}'
    responce = requests.get(url)
    return HttpResponse(f"<h3>Название файла: {responce}</h3>")

# def download(q: str):
#     datasets_list = os.system(f'kaggle datasets list -s {q}')
    
#     # print(datasets_list)
#     # qwe = str(datasets_list)
#     url = f'https://www.kaggle.com/datasets?search={q}'
#     responce = requests.get(url)
#     if responce.status_code == 200:
#         print(responce)
#     else:
#         print(responce.status_code)

#     # with open ('qwe.txt', 'w') as file:
#     #     file.write(str(os.system(f'kaggle datasets list -s {q}')))

#     # print(responce.status_code, 'status_code')
#     # print(responce.url, 'url')

# # принимает запрос и передаёт его в функцию download для скачивания
# def main() -> None:
#     q = input('Введите запрос: ')
#     download(q)

# main()

# kaggle datasets list -s [KEYWORD]
# datasets_list = os.system(f'kaggle datasets list -s {obj_adress}')