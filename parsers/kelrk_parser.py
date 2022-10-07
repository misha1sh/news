from hashlib import new
from types import new_class
import requests as rq
from bs4 import BeautifulSoup as bs
import re
import datetime as dt
import time

KLERK_NEWS_URL='https://www.klerk.ru/news/page/'


def parse_klerk_news(days=1):
    page_number = 1
    ress = []
    while (True):
        response = rq.get(KLERK_NEWS_URL + str(page_number))
        page_number += 1
        if (response.status_code == 200):
            news_urls = re.findall('klerk\.ru/buh/news/[\d]*/\"', response.text)[:-5]
            for news_url in news_urls:
                res = {}
                url = 'https://www.' + news_url[:-1]
                res['url']= url
                news = rq.get(url).text
                soup = bs(news, 'html.parser')
                res['site'] = 'klerk'
                res['title'] = soup.body.find("h1").text
                res['description'] = soup.body.find(class_="article__resume").text            
                res['text'] = soup.body.find(class_="article__content").text
                date_raw = re.findall('\d{4}-\d+-\d+ \d+:\d+:\d+', str(soup.body.find(class_="status__block")))[0]
                date, time = date_raw.split()
                date = date.split('-')
                time = time.split(':')
                res['timestap'] = dt.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2])).timestamp() * 1000
                if (days * 86400000 + res['timestap'] < dt.datetime.now().timestamp() * 1000):
                    return ress
                ress.append(res)
            
            

if __name__ == "__main__":
    parse_klerk_news(30)