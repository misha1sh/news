from flask import Flask,render_template,jsonify
import json
from datetime import datetime
from digester import get_digest
from importer import load

app = Flask(__name__)



digests = [
    {
        'id': 1,
        'profile': 'accounter',
        'title': u'Демобилизация',
        'description': u'Поезд к дому мчится полечу домой как птица',
        'date': u'12.10.2022',
        'url': 'www.facebook.com'
    },
    {
        'id': 2,
        'profile': 'ceo',
        'title': 'ставка ЦБ',
        'description': 'Кризис аларм',
        'date': '10.01.2021',
        'url': 'www.vk.com'
    }

]

trend = {'trends': ['мобилизация', 'Путин', 'Любовь', 'секс', 'наркотики']}
insight = {'insights': ['тренды', 'секс']}


# create digests for the accounter profile
def digest_accounter():
    digest = []
    for i in digests:
        if i['profile'] == 'accounter':
            digest = i
    return json.dumps(digest, ensure_ascii=False).encode('utf8')

def digest_ceo():
    digest = []
    for i in digests:
        if i['profile'] == 'ceo':
            digest = i
    return json.dumps(digest, ensure_ascii=False).encode('utf8')

def trends():
    return json.dumps(trend, ensure_ascii=False).encode('utf8')

def insights():
    return json.dumps(insight, ensure_ascii=False).encode('utf8')




@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/v0/digest/accounter', methods=['GET'])
def get_digest_accounter():
    digest = get_digest(load(), 'buh', 30, 3)
    response = []
    for news in digest:
        tmp = {
            'url': news['url'],
            'publication_date': datetime.fromtimestamp(news['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
            'title': news['title'],
            'description': news['description']
        }
        response.append(tmp)
    return json.dumps(response, ensure_ascii=False).encode('utf8')

@app.route('/api/v0/digest/ceo', methods=['GET'])
def get_digest_ceo():
    return digest_ceo()

@app.route('/api/v0/digest/trends', methods=['GET'])
def get_digest_trends():
    return trends()

@app.route('/api/v0/digest/insights', methods=['GET'])
def get_digest_insights():
    return insights()


if __name__ == '__main__':
    app.run(debug=False, port=8080) 