"""
2. Зарегистрироваться на https://openweathermap.org/api и написать функцию, которая получает погоду в данный момент для города,
название которого получается через input. https://openweathermap.org/current
"""


import requests
import time
import json


api_key = "c81e5a656d51e706611fe46a7f0e6bfb"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = input("Enter city name : ")

complete_url = base_url + "appid=" + api_key + "&q=" + city_name

def get_data(base_url, api_key,city):
    while True:
        time.sleep(1)
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        if response.status_code == 200:
            print(complete_url)
            break
        else:
            print(" City Not Found ")
            break
    return response.json()
response = get_data(base_url, api_key, city_name)

print('Получен результат')
print(response)

with open('lesson_1_2_weather.json', 'w') as f:
    json_repo = json.dump(response, f, indent=4)
