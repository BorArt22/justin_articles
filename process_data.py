'''
Process and save data from dataframe

input:
df - dataframe that should contains fields:
    Date - datetume. 
    No. of articles - integer or float.

output:
    'number_of_articles_about_justin_trudeau.csv'
    'number_of_articles_about_justin_trudeau_per_month.png'
'''

import logging

import pandas as pd

from logger import log_message

def save_time_series(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].apply(lambda x: x.strftime("%Y-%m-%d"))
    df['No. of articles'] = df['No. of articles'].astype('int')
    # Save data to csv
    df.to_csv('number_of_articles_about_justin_trudeau.csv',index=False)
    log_message('process_data',"Data saved to 'number_of_articles_about_justin_trudeau.csv'")

    # Calculate a statistic of number of articles per month
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year-Month'] = df['Date'].apply(lambda x: x.strftime("%Y-%m"))
    df_year_month = df.groupby(['Year-Month']).sum('No. of articles')

    # Create and save plot with articles about Justin Trudeau per month
    plot = df_year_month.plot(kind='bar',
                              title='Number of articles about Justin Trudeau per month',
                              xlabel='Date, Year and Month',
                              ylabel='Number of articles',
                              legend=None,
                              figsize=(20,10)
                            )
    fig = plot.get_figure()
    fig.savefig("number_of_articles_about_Justin_Trudeau_per_month.png",bbox_inches = 'tight')
    log_message('process_data',"Number of articles about Justin Trudeau per month saved as graph to 'number_of_articles_about_Justin_Trudeau_per_month.png'")