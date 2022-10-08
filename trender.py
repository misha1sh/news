import time
import datetime


from keyworder import idf_precalc, tf_idf, keywords_sum, keywords_norm, keywords_mean, most_popular_keywords, keywords_diff
from tokenizer import keywords_groups_calc
from clusterizer import clusterize

def get_trends(data_from_parser, days):
    data = data_from_parser["cfo"] + data_from_parser["cons"] + data_from_parser["klerk"] + data_from_parser["rbc"] 
    def filt(normal):
        if normal.tag._POS in ["NUMB", "UNKN"] or normal.tag.POS in ["COMP", "PRTS", "PRTF"]:
            return True
        if normal.normal_form in ["октябрь", "сентябрь"]:
            return True
        return False

    idfs = idf_precalc([ keywords_groups_calc(data, filt=filt) ])

    time_begin = time.time() - datetime.timedelta(days=30).total_seconds()
    data_before = list(filter(lambda i: time_begin <= i["timestamp"], data))
    data_after = list(filter(lambda i: time_begin > i["timestamp"], data))

    keyword_groups_before = keywords_groups_calc(data_before, filt=filt)
    keyword_groups_after = keywords_groups_calc(data_after, filt=filt)

    keyword_groups_before = tf_idf(keyword_groups_before, idfs)
    keyword_groups_after = tf_idf(keyword_groups_after, idfs)

    keywords = most_popular_keywords(keywords_diff(keywords_mean(keyword_groups_before),
                                        keywords_mean(keyword_groups_after)), 20)

    import pymorphy2
    import string

    res = []
    morph = pymorphy2.MorphAnalyzer()

    for i in keywords:
        normal = morph.parse(i['word'])
        normal = normal[0]
        res.append(normal.normal_form)

    return res
