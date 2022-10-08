# tokenize stopwords lemmatizer/stemmer(snowball)

import nltk
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import RegexpTokenizer
import pymorphy2
import string

ru_stopwords = set(stopwords.words("russian") + list(string.punctuation + '»' + '—' +  '«') + ['п.','ст.', 'рф', "это"])
only_words_tokenizer = RegexpTokenizer(r'\w+')
snowball = SnowballStemmer(language="russian")
morph = pymorphy2.MorphAnalyzer()

def tokenize(text):
    # text = only_words_tokenizer.tokenize(text) 
    text = word_tokenize(text, language="russian")
    res = []
    for word in text:
        if word.lower() not in ru_stopwords and len(word) > 1:
            res.append(word)
    return res

def keywords_calc(text, filt=None):
    words = tokenize(text)
    res = {}
    for word in words:
        short = snowball.stem(word)
        if short not in res:
            normal = morph.parse(word)
            if len(normal) == 0:
                continue
            normal = normal[0]
            if normal.tag.POS == "INFN" or normal.tag.POS == "VERB" or normal.tag.POS == "ADJF":
                continue
            if filt and filt(normal):
                continue
            
            res[short] = { 
                "word": word, #normal.normal_form if normal.score > 0.5 else word,
                "short": short,
                "count": 0
            }
        res[short]["count"] += 1
            
    return res



from joblib import Parallel, delayed
def keywords_groups_calc(data, filt=None):
    keywords_groups = Parallel(n_jobs=16)(delayed(keywords_calc)(i['text'], filt) for i in data)
    return keywords_groups


# keywords_calc(tbl['text'][0][:200])
# keywords_calc("ходить думать тест это сообщает")