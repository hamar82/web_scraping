"""
Урок 5. Scrapy

Написать программу, которая собирает посты из группы https://vk.com/tokyofashion
Будьте внимательны к сайту!
Делайте задержки, не делайте частых запросов!

1) В программе должен быть ввод, который передается в поисковую строку по постам группы
2) Соберите данные постов:
- Дата поста
- Текст поста
- Ссылка на пост(полная)
- Ссылки на изображения(если они есть; необязательно)
- Количество лайков, "поделиться" и просмотров поста
3) Сохраните собранные данные в MongoDB
4) Скролльте страницу, чтобы получить больше постов(хотя бы 2-3 раза)
5) (Дополнительно, необязательно) Придумайте как можно скроллить "до конца" до тех пор пока посты не перестанут добавляться

Чем пользоваться?
Selenium, можно пользоваться lxml, BeautifulSoup

Советы по дз
https://gb.ru/lessons/216633#!#comment-890162



"""



import time
import unicodedata

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from pymongo import MongoClient
from bs4 import BeautifulSoup

from datetime import datetime
from random import randint

from urllib.parse import urljoin




URL = "https://vk.com/tokyofashion"
DRIVER_PATH = "./selenium_drivers/chromedriver"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(DRIVER_PATH, options=options)
driver.get(URL)
driver.refresh()
# //button[@class='add-more-btn']


Mongo_host = "localhost"
Mongo_port = 27017
db_name = "VK"
collection_name = "posts"


def add_new(data_post):
    """
    Функция принимает список словарей, но может принять и один словарь, если нужно.
    Возвращает 1, если запись новая и была добавлена в базу
    """
    with MongoClient(Mongo_host, Mongo_port) as client:
        db = client[db_name]
        collection = db[collection_name]
        collection.update_one(
            {'id_post': data_post['id_post']},
            {'$set': data_post,
             '$currentDate': {'lastModified': True}},
            upsert=True,
        )
    return True


button = driver.find_element_by_xpath("//a[contains(@class, 'ui_tab_search')]")
button.click()
time.sleep(2)
text_search = 'tokyo'
search_input = driver.find_element_by_xpath('//input[@class="ui_search_field _field"]')
search_input.send_keys(text_search + '\n')

print(search_input)


def data_pars(post):

    try:
        result_dict = {}
        soup_post = BeautifulSoup(post, "lxml")

        element = soup_post.find('span', attrs={'class': 'rel_date'})
        result_dict['date_post'] = unicodedata.normalize("NFKD", element.text) if element else None

        element = soup_post.find('div', attrs={'class': 'wall_post_text'})
        result_dict['text_post'] = element.text if element else None

        element = soup_post.find('div')
        result_dict['id_post'] = element['data-post-id'] if element else None
        result_dict['link_post'] = urljoin(URL, '?w=wall' + element['data-post-id']) if element else None

        element = soup_post.find('div', attrs={'class': 'PostButtonReactions__title _counter_anim_container'})
        result_dict['likes_count'] = element.text if element else None

        element = soup_post.find('div', attrs={'class': 'PostBottomAction PostBottomAction--withBg share _share'})
        result_dict['reposts_count'] = element['data-count'] if element else None

        element = soup_post.find('div', attrs={'class': 'like_views like_views--inActionPanel'})
        result_dict['views_count'] = element['title'].split(' ')[0] if element else None

        return result_dict

    except Exception:

        return None



list_posts = []
start_post = 0
posts_counts = 0
last_height = 0

while True:
    posts = driver.find_elements_by_xpath("//div[contains(@id, 'post-')]")
    posts_counts = len(posts)
    for post in posts[start_post:posts_counts]:
        outer_html = post.get_attribute("outerHTML")
        post_data = data_pars(outer_html)
        if post_data:
            add_new(post_data)
        else:
            print("Error", outer_html[150])
    start_post = max(0, posts_counts - 30)

     id_last_post = post_data.get('id_post')
     print(id_last_post)
     last_post = driver.find_element_by_xpath(f'//a[@data-post-id="{id_last_post}"]')

print("Data collection completed")