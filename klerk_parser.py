from hashlib import new
from types import new_class
import requests as rq
from bs4 import BeautifulSoup as bs
import re
import datetime as dt
import json

KLERK_NEWS_URL='https://www.klerk.ru/news/page/'


def parse_klerk_news(days=1):
    page_number = 1
    ress = []
    while (True):
        response = rq.get(KLERK_NEWS_URL + str(page_number))
        page_number += 1
        error_count = 0
        if (response.status_code == 200):
            news_urls = re.findall('klerk\.ru/buh/news/[\d]*/\"', response.text)[:-5]
            for news_url in news_urls:
                try:
                    res = {}
                    url = 'https://www.' + news_url[:-1]
                    res['url']= url
                    news = rq.get(url).text
                    soup = bs(news, 'html.parser')
                    res['site'] = 'klerk'
                    res['title'] = soup.body.find("h1").text.replace("\xa0", " ").replace("\t", " ")
                    res['text'] = soup.body.find(class_="article__content").text.replace("\xa0", " ").replace("\t", " ")
                    try:
                        res['description'] = soup.body.find(class_="article__resume").text.replace("\xa0", " ").replace("\t", " ")
                    except:
                        if (len(res['text']) > 100):
                            res['description'] = res['text'][:100] + '...'
                        else:
                            res['description'] = res['text']
                    date_raw = re.findall('\d{4}-\d+-\d+ \d+:\d+:\d+', str(soup.body.find(class_="status__block")))[0]
                    date, time = date_raw.split()
                    date = date.split('-')
                    time = time.split(':')
                    res['timestamp'] = dt.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2])).timestamp()
                    if (days * 86400 + res['timestamp'] < dt.datetime.now().timestamp()):
                        return ress
                    ress.append(res)
                except Exception as e:
                    error_count += 1
                    print(e, url)
                    if (error_count > 0):
                        return ress
            
            

if __name__ == "__main__":
    res = parse_klerk_news(365)
    with open('klerk_news_365.json', 'w') as outfile:
        json.dump(res, outfile)
