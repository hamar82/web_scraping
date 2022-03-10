"""
Урок 4. Парсинг HTML. XPath

Написать приложение(используя lxml, нельзя использовать BeautifulSoup), которое собирает основные новости с сайтов
news.mail.ru, lenta.ru, yandex news Для парсинга использовать xpath. Структура данных должна содержать:
название источника(mail и яндекс не источники, а аггрегаторы, см. страницу новости),
наименование новости,
ссылку на новость,
дата публикации

Сложить все новости в БД, новости должны обновляться, т.е. используйте update

"""


 #'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'



from lxml import html
from pprint import pprint
import requests

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

response = requests.get('https://lenta.ru/')
dom = html.fromstring(response.text)
lenta_News = []
all_news = []


def __init__(self):
    global item
    client = MongoClient('localhost', 27017)
    self.mongobase = client.lenta

    items = dom.xpath("//div[@class = 'span4']/div[@class = 'item' or @class = 'first-item']")
    for item in items:
        news = {}
        news['time'] = item.xpath(".//time[@class = 'g-time']/text()")
        news['date'] = item.xpath(".//time/@title")
        news_l = item.xpath(".//a/@href")
        news['link'] = f'https://lenta.ru{news_l[0]}'
        news['news'] = item.xpath(".//a[contains (@href, '/news/')]/text()")
        news['resource'] = "lenta.ru"
        all_news.append(news)

        strings = []
        for key, item in news.items():
            strings.append("{}: {}".format(key.capitalize(), item))
        result = "; ".join(strings)
        new_result = result.replace(u"\\xa0", u" ").replace(u", 'Отменить'", u"")
        lenta_News.append(new_result)

    all_lenta_News = []
    for x in lenta_News:
        if x not in all_lenta_News:
            all_lenta_News.append(x)

    pprint(all_lenta_News)

    collection.insert_one(item)
    return item




def __init__(self):
    global item
    client = MongoClient('localhost', 27017)
    self.mongobase = client.mail


    header = {'User_Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    responce = requests.get('https://news.mail.ru/')
    dom = html.fromstring(responce.text)

    mail_News = []
    mail_ru_News = dom.xpath("//div[contains(@class, 'layout')]//text()")

    for news in mail_ru_News:
        NMR = {}
        NMR['source'] = news.xpath("//span[@class= 'newsitem__param']//text()|//div/span[@class = 'newsitem__param js-ago']/text()")
        NMR['name_link'] = news.xpath("//li[@class= 'list__item']//@href|//span[@class= 'link__text']//text() | //div/span[@class = 'newsitem__param js-ago']/text()")
        NMR['day_news_link'] = news.xpath("//a[@class= 'newsitem__title link-holder']//@href|//a[@class= 'newsitem__title link-holder']//text()|//div/span[@class = 'newsitem__param js-ago']/text()")
        all_NMR.append(NMR)

        strings = []
        for key, item in NMR.items():
            strings.append("{}: {}".format(key.capitalize(), item))
        result = "; ".join(strings)
        new_result = result.replace(u"\\xa0", u" ").replace(u", 'Отменить'", u"")
        mail_News.append(new_result)

    all_mail_News = []
    for x in mail_News:
        if x not in all_mail_News:
            all_mail_News.append(x)

    print(all_mail_News)

    collection.insert_one(item)
    return item




def __init__(self):
    global item
    client = MongoClient('localhost', 27017)
    self.mongobase = client.yandex

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

    response = requests.get('https://yandex.ru/news/')
    dom = html.fromstring(response.text)
    yandex_News = []
    all_news = []

    items = dom.xpath("//div[contains(@class, 'rubric')]")

    for item in items:
        news = {'link_sourse_title_time': item.xpath(
            "//a[contains(@class,'mg-card__source-link')]/text() | //a[contains(@class,'mg-card__source-link')]/@href | //h2[contains(@class ,'mg-card__title')]/text() | //span[contains(@class,'mg-card-source__time')]/text()")}
        # news['headers'] = item.xpath(")
        # news['link'] = item.xpath("//a[contains(@class,'mg-card__source-link')]/text()")
        # news['sourse'] = item.xpath("//a[contains(@class,'mg-card__source-link')]/@href")
        # news['title'] = item.xpath("//h2[contains(@class ,'mg-card__title')]/text()")
        # news['time'] = item.xpath("//span[contains(@class,'mg-card-source__time')]/text()")
        all_news.append(news)

        strings = []
        for key, item in news.items():
            strings.append("{}: {}".format(key.capitalize(), item))
        result = "; ".join(strings)
        new_result = result.replace(u"\\xa0", u" ").replace(u", 'Отменить'", u"")
        yandex_News.append(new_result)

    all_yandex_News = []
    for x in yandex_News:
        if x not in all_yandex_News:
            all_yandex_News.append(x)

    print(all_yandex_News, end="______________________________________________________")

    collection.insert_one(item)
    return item