import json
import re
    


def load_cfo():
    with open("cfo_news_365.json") as f:
        data_cfo = json.load(f)
        
    def clear(data_cfo):
        res = []
        for i in data_cfo:
            res.append(i)
            res[-1]["text"] = re.sub("Узнать больше.*", "", res[-1]["text"])
        return res
    
    data_cfo = clear(data_cfo)
    print("cfo", len(data_cfo))
    return data_cfo


def load_cons():
    with open("consultant_news.json") as f:
        data_cons = json.load(f)
    print("cons", len(data_cons))
    return data_cons


def load_klerk():
    with open("klerk_news_365.json") as f:
        data_klerk= json.load(f)

    def uniq(data_klerk):
        res = []
        seen = set()
        for i in data_klerk:
            if i["url"] in seen: continue
            seen.add(i["url"])
            res.append(i)
        return res

    data_klerk = uniq(data_klerk)
    print("klerk", len(data_klerk))
    return data_klerk

def load():
    return {
        "cfo": load_cfo(),
        "cons": load_cons(),
        "klerk": load_klerk()
    }
