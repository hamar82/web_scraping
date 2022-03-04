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
#lenta.ru

import requests
import datetime
from pymongo import MongoClient
from lxml.html import fromstring
from dateutil import parser


def lenta_news():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.110 Safari/537.36'
    }
    resp = requests.get("https://lenta.ru", headers=headers)
    text = fromstring(resp.text)
    top_news = text.xpath(".//div[@class='topnews']")
    news_columns = top_news[0].xpath("./div[@class='topnews__column']")
    with MongoClient() as client:
        db = client.news_parcer
        collection = db.lenta_ru
        for news in news_columns:
            news_column = news.xpath("./a | ./*/a")
            for item in news_column:
                item_info = {}
                if not item.get("href").startswith("https"):
                    link = "https://lenta.ru" + item.get("href")
                else:
                    link = item.get("href")
                title = item.xpath(".//h3 | .//span")
                publish_date = datetime.datetime.strptime(f"{datetime.date.today()} "
                                                          f"{item.xpath('.//time')[0].text}", "%Y-%m-%d %H:%M")
                item_info["source"] = "lenta.ru"
                item_info["title"] = title[0].text
                item_info["link"] = link
                item_info["publish_date"] = publish_date
                expired_news = datetime.datetime.now() - datetime.timedelta(hours=24)
                collection.update_one(
                    {
                        "link": link
                    },
                    {"$set": item_info},
                    upsert=True
                )
                collection.delete_many(
                    {
                        "publish_date": {"$lt": expired_news}
                    }
                )


def main():
    lenta_news()


if __name__ == "__main__":
    main()




#news.mail.ru

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.110 Safari/537.36'
    }


def mail_news():
    resp = requests.Session()
    resp.headers.update(headers)
    main_page = resp.get("https://news.mail.ru/")
    text = fromstring(main_page.text)
    news_block = text.xpath("//table[@class='daynews__inner']")
    news_list = text.xpath("//ul[contains(@class, 'list_half')]")
    news_links = []
    main_news = news_block[0].xpath(".//div[contains(@class, 'daynews__item')]/a")
    news_from_list = news_list[0].xpath("./li[@class='list__item']/a")

    for item in main_news:
        news_links.append(item.get("href"))

    for item in news_from_list:
        news_links.append(item.get("href"))

    with MongoClient() as client:
        db = client.news_parcer
        collection = db.mail_ru_news
        for link in news_links:
            news = {}
            news_page = resp.get(link)
            page_dom = fromstring(news_page.text)
            info_block = page_dom.xpath("//div[contains(@class, 'cols__inner')]/div[contains(@class, 'js-article')]")[0]
            publish_date = str(parser.parse(info_block.xpath(".//span[contains(@class, 'js-ago')]")[0].get("datetime")))
            source = info_block.xpath(".//span[@class='link__text']")[0].text
            title = info_block.xpath(".//h1[@class='hdr__inner']")[0].text
            news["title"] = title
            news["publish_date"] = publish_date
            news["source"] = source
            news["link"] = link
            expired_news = datetime.datetime.now() - datetime.timedelta(hours=24)

            collection.update_one(
                {
                    "link": link
                },
                {"$set": news},
                upsert=True
            )
            collection.delete_many(
                {
                    "publish_date": {"$lt": expired_news}
                }
            )


def main():
    mail_news()


if __name__ == "__main__":
    main()



#yandex news

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.110 Safari/537.36'
    }


def yandex_news():
    with MongoClient() as client:
        db = client.news_parcer
        collection = db.yandex_news
        resp = requests.Session()
        resp.headers.update(headers)
        main_page = resp.get("https://yandex.ru/news")
        text = fromstring(main_page.text)
        news_block = text.xpath("//section[@aria-labelledby='top-heading']")
        news_items = news_block[0].xpath(".//div[contains(@class, 'mg-grid__item')]")

        for item in news_items:
            news = {}
            link = item.xpath(".//a[@class='mg-card__link']")[0].get("href")
            title = item.xpath(".//a[@class='mg-card__link']")[0].text
            footer = item.xpath(".//div[contains(@class, 'mg-card-source')]")[0]
            source = footer.xpath("//a[@class='mg-card__source-link']")[0].text
            publish_date = datetime.datetime.strptime(f"{datetime.date.today()} "
                                                      f"{footer.xpath('span[@class=mg-card-source__time]')[0].text}",
                                                      "%Y-%m-%d %H:%M")
            news["link"] = link
            news["title"] = title
            news["source"] = source
            news["publish_date"] = publish_date

            expired_news = datetime.datetime.now() - datetime.timedelta(hours=24)

            collection.update_one(
                {
                    "link": link
                },
                {"$set": news},
                upsert=True
            )
            collection.delete_many(
                {
                    "publish_date": {"$lt": expired_news}
                }
            )


def main():
    yandex_news()


if __name__ == "__main__":
    main()

