'''
Loading data from articles about Justin Trudeau from the Guardian Media Group API 
(documentation http://open-platform.theguardian.com/documentation/)
and then processing it. Refresh data everyday.
    
    - Initialize numbers of article about Justin Trudeau from 2018-01-01
        - Create 'Number of articles about Justin Trudeau.csv' with number of articles per day.
        - Create 'Number of articles about Justin Trudeau per month.png' with barchart graph with number of articles per month.
    - Everyday at 00:00 loading new data for yesterday and refresh output files.
'''

import logging
from datetime import datetime, timedelta, date
import time

import pandas as pd

import schedule

from logger import log_message
from load_api import load_articles_about_justin_trudeau
from process_data import save_time_series

def load_data_for_yesterday_day():
    # Calculate yesterday date
    previous_date = (date.today() - timedelta(days = 1)).strftime("%Y-%m-%d")
    log_message('main',f"Run everyday loading new articles for previous day ({previous_date}).")

    # load previous data fron csv file
    df_prev = pd.read_csv('number of articles about Justin Trudeau.csv')
    last_date = df_prev['Date'].max()
    last_date_p1 = (datetime.strptime(last_date, '%Y-%m-%d') + timedelta(days = 1)).strftime("%Y-%m-%d")

    log_message('main',f"Last date from previously loaded data is {last_date}")

    # check that last date from previously loaded data is different from yesterday date
    if last_date >= previous_date:
        log_message('main',"Now load all needed data. Everyday scheduler works correctly.")
        return
    elif previous_date > last_date_p1:
        log_message('main',f"Loading data from {last_date_p1}.")

        df_new = load_articles_about_justin_trudeau(last_date_p1)
        r = pd.date_range(start=pd.to_datetime(last_date_p1), end = date.today() - timedelta(days = 1))
        df_new = df_new[df_new['Date'] <= previous_date].set_index('Date').reindex(r).fillna(0).rename_axis('Date').reset_index()

        frames = [df_prev, df_new]
        save_time_series(pd.concat(frames))
        log_message('main',"New data was loaded. Everyday scheduler works correctly.")

        return 
    else:
        log_message('main',f"Loading data from {previous_date}.")

        df_new = load_articles_about_justin_trudeau(previous_date)
        df_new = df_new[df_new['Date'] <= previous_date]

        frames = [df_prev, df_new]
        save_time_series(pd.concat(frames))
        log_message('main',"New data was loaded. Everyday scheduler works correctly.")

        return 

# initialize loading
log_message('main',"Initializing data from 2018-01-01...")
r = pd.date_range(start=pd.to_datetime('2018-01-01'), end = date.today() - timedelta(days = 1))
df_response_stat = load_articles_about_justin_trudeau('2018-01-01')
previous_date = (date.today() - timedelta(days = 1)).strftime("%Y-%m-%d")
df_response_stat = df_response_stat[df_response_stat['Date'] <= previous_date].set_index('Date').reindex(r).fillna(0).rename_axis('Date').reset_index()
save_time_series(df_response_stat)
log_message('main',"Data initialized.")

# create everyday scheduling
log_message('main',"Creating everyday scheduling...")
schedule.every().day.at("01:00").do(load_data_for_yesterday_day)
#schedule.every(1).minutes.do(load_data_for_yesterday_day) #test
log_message('main',"Created everyday scheduling.")

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute