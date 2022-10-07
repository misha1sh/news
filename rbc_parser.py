# Импорт библиотек
import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from IPython import display




class rbc_parser:
    def __init__(self):
        pass
    
    
    def _get_url(self, param_dict: dict) -> str:
        """
        Возвращает URL для запроса json таблицы со статьями
        """
        url = 'https://www.rbc.ru/v10/search/ajax/?project={0}&category={1}&dateFrom={2}&dateTo={3}&offset={4}&limit={5}&query={6}&material={7}'.format(param_dict['project'],
                            param_dict['category'],
                            param_dict['dateFrom'],
                            param_dict['dateTo'],
                            param_dict['offset'],
                            param_dict['limit'],
                            param_dict['query'],
                            param_dict['material'])
        print(url)
        
        return url
    
    
    def _get_search_table(self, param_dict: dict,
                          includeText: bool = True) -> pd.DataFrame:
        """
        Возвращает pd.DataFrame со списком статей
        
        includeText: bool
        ### Если True, статьи возвращаются с текстами
        """
        url = self._get_url(param_dict)
        r = rq.get(url)
        search_table = pd.DataFrame(r.json()['items'])
        if includeText and not search_table.empty:
            get_text = lambda x: self._get_article_data(x['fronturl'])
            search_table[['overview', 'text']] = search_table.apply(get_text,
                                                                    axis=1).tolist()
            
        return search_table.sort_values('publish_date_t', ignore_index=True)
    
    
    def _get_article_data(self, url: str):
        """
        Возвращает описание и текст статьи по ссылке
        """
        r = rq.get(url)
        soup = bs(r.text, features="lxml") # features="lxml" чтобы не было warning
        div_overview = soup.find('div', {'class': 'article__text__overview'})
        if div_overview:
            overview = div_overview.text.replace('<br />','\n').strip()
        else:
            overview = None
        p_text = soup.find_all('p')
        if p_text:
            text = ' '.join(map(lambda x:
                                x.text.replace('<br />','\n').strip(),
                                p_text))
        else:
            text = None
        
        return overview, text 
    
    def get_articles2(self,
                     param_dict,
                     count=100) -> pd.DataFrame:
        """
        Функция для скачивания статей интервалами через каждые time_step дней
        Делает сохранение таблицы через каждые save_every * time_step дней

        param_dict: dict
        ### Параметры запроса 
        ###### project - раздел поиска, например, rbcnews
        ###### category - категория поиска, например, TopRbcRu_economics
        ###### dateFrom - с даты
        ###### dateTo - по дату
        ###### offset - смещение поисковой выдачи
        ###### limit - лимит статей, максимум 100
        ###### query - поисковой запрос (ключевое слово), например, РБК

        """
        param_copy = param_dict.copy()
        
        out = pd.DataFrame()
        cur_count = 0
        
        while cur_count <= count:
            param_copy["offset"] = cur_count
            print('Parsing articles from ', cur_count)
            new_arcticles = self._get_search_table(param_copy)
            out = out.append(new_arcticles, ignore_index=True)
            cur_count += len(new_arcticles)
        print('Finish')
        
        return out
    
    def get_articles(self,
                     param_dict,
                     time_step = 7,
                     save_every = 5,
                     save_excel = True) -> pd.DataFrame:
        """
        Функция для скачивания статей интервалами через каждые time_step дней
        Делает сохранение таблицы через каждые save_every * time_step дней

        param_dict: dict
        ### Параметры запроса 
        ###### project - раздел поиска, например, rbcnews
        ###### category - категория поиска, например, TopRbcRu_economics
        ###### dateFrom - с даты
        ###### dateTo - по дату
        ###### offset - смещение поисковой выдачи
        ###### limit - лимит статей, максимум 100
        ###### query - поисковой запрос (ключевое слово), например, РБК

        """
        param_copy = param_dict.copy()
        time_step = timedelta(days=time_step)
        dateFrom = datetime.strptime(param_copy['dateFrom'], '%d.%m.%Y')
        dateTo = datetime.strptime(param_copy['dateTo'], '%d.%m.%Y')
        if dateFrom > dateTo:
            raise ValueError('dateFrom should be less than dateTo')
        
        out = pd.DataFrame()
        save_counter = 0

        while dateFrom <= dateTo:
            param_copy['dateTo'] = (dateFrom + time_step).strftime("%d.%m.%Y")
            if dateFrom + time_step > dateTo:
                param_copy['dateTo'] = dateTo.strftime("%d.%m.%Y")
            print('Parsing articles from ' + param_copy['dateFrom'] +  ' to ' + param_copy['dateTo'])
            out = out.append(self._get_search_table(param_copy), ignore_index=True)
            dateFrom += time_step + timedelta(days=1)
            param_copy['dateFrom'] = dateFrom.strftime("%d.%m.%Y")
            save_counter += 1
            if save_counter == save_every:
                display.clear_output(wait=True)
                out.to_excel("/tmp/checkpoint_table.xlsx")
                print('Checkpoint saved!')
                save_counter = 0
        
        if save_excel:
            out.to_excel("rbc_{}_{}.xlsx".format(
                param_dict['dateFrom'],
                param_dict['dateTo']))
        print('Finish')
        
        return out
    
    