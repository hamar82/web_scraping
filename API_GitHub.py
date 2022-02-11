"""
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.
"""
# https://api.github.com/users/hamar82/repos

import requests

import json

def get_data(url: str) -> dict:
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            break
    return response.json()

username = input('Введите username: ')
username = 'hamar82' if username == '' else username
url = 'https://api.github.com/users/'+username+'/repos'

response = get_data(url)
print('Получен результат')
print(response)

repo = []
for itm in response:
    repo.append(itm['name'])
print(f'Список репозиториев пользователя {username}')
print(repo)

with open('lesson_1_repo.json', 'w') as f:
    json_repo = json.dump(repo, f)