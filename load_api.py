import configparser
import json
import logging

import requests

import pandas as pd

from logger import log_message

config =  configparser.ConfigParser()
config.read('api.cfg')

url_querry_init = 'https://content.guardianapis.com/search?' \
    + 'api-key=' + config['API']['KEY'] + '&' \
    + 'tag=' + 'world%2Fjustin-trudeau' + '&' \
    + 'order-by=' + 'oldest'

def get_stat(df_response):
    df_response['webPublicationDate'] = pd.to_datetime(df_response['webPublicationDate'])
    df_response['Date_YMD']=  pd.to_datetime(df_response['webPublicationDate'].apply(lambda x: x.strftime("%Y-%m-%d")))
    series = df_response.groupby(['Date_YMD']).size()
    df_response_stat = pd.DataFrame({'Date':series.index, 'No. of articles':series.values})
    return df_response_stat

def load_articles_about_justin_trudeau (from_date = '2018-01-01'):
    log_message('load_api',f"Creating response for loading from {from_date}...")
    url_querry = url_querry_init + '&' + 'from-date=' + from_date
    response = requests.get(url_querry)
    data_json = response.json()

    log_message('load_api',f"Geting data from api...")
    count_of_pages = data_json['response']['pages']
    log_message('load_api',f"Get next count of pages:  {count_of_pages}.")

    if count_of_pages == 0:
        log_message('load_api',f"Return 0 count for {from_date}.")
        df = pd.DataFrame(data = {'Date': [from_date], 'No. of articles': [0]})
        return df
    elif count_of_pages == 1:
        log_message('load_api',"Loading 1 page...")
        df_response = pd.DataFrame(data_json['response']['results'])
        df_response_stat = get_stat(df_response)
        log_message('load_api',"Loaded 1 page.")
        return df_response_stat
    else:
        log_message('load_api',f"Loading {count_of_pages} pages...")
        df_response = pd.DataFrame(data_json['response']['results'])
        for page in range(2,count_of_pages+1):
            response = requests.get(url_querry  + '&' + 'page=' + str(page))
            data_json = response.json()
            df_page = pd.DataFrame(data_json['response']['results'])
            frames = [df_response, df_page]
            result = pd.concat(frames)
            df_response = result
        df_response_stat = get_stat(df_response)
        log_message('load_api',"Loaded all pages.")
        return df_response_stat