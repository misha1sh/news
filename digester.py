import importer
from keyworder import idf_precalc, tf_idf, keywords_sum, keywords_norm, keywords_mean, most_popular_keywords, keywords_diff
from tokenizer import keywords_groups_calc
from clusterizer import clusterize


import time
import datetime

def get_data_before(data, days):
    time_begin = time.time() - datetime.timedelta(days=days).total_seconds()
    # data_news = list(filter(lambda i: time_begin <= i["timestap"], data))
    data_news = list(filter(lambda i: time_begin <= i["timestamp"], data))
    return data_news



def get_popular_keywords(data, idfs):
    keyword_groups = keywords_groups_calc(data)
    # idfs = idf_precalc([keyword_groups])

    # keyword_groups = tf_idf(keyword_groups, idfs)
    keyword_groups = tf_idf(keyword_groups, idfs)
    mmean = keywords_mean(keyword_groups)

    popular_keywords = []
    for document in keyword_groups:
        p = most_popular_keywords(keywords_diff(document, mmean), 30)
        popular_keywords.append({
            "short": set([i['short'] for i in p]), 
            "long": {
                i['short']: i for i in p
            }
        })
    return popular_keywords

# person_type = ceo or buh
# days = digest days count
# count = articles count
def get_digest(data_from_parser, person_type, days, count):
    data = get_data_for_person(data_from_parser, "buh")
    idfs = idf_precalc([ keywords_groups_calc(data) ])

    data = get_data_before(data, days=days)
    popular_keywords = get_popular_keywords(data, idfs)
    res = clusterize(data, popular_keywords, count=count, debug=False)
    return res

def get_data_for_person(data_from_parser, person_type):
    if person_type == "ceo":
        return data_from_parser["cfo"]
    elif person_type == "buh":
        return data_from_parser["cons"] + data_from_parser["klerk"]