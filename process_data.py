import logging

import pandas as pd

from logger import log_message

'''
df - dataframe that should contains fields:
    Date - datetume
    No. of articles - integer or float
'''

def save_time_series(df):
    # Save data to csv
    df.to_csv('number of articles about Justin Trudeau.csv',index=False)
    log_message('process_data',"Data saved to 'number of articles about Justin Trudeau.csv'")

    # Calculate a statistic of number of articles per month
    df['Year-Month'] = df['Date'].apply(lambda x: x.strftime("%Y-%m"))
    df_year_month = df.groupby(['Year-Month']).sum('No. of articles')

    # Create and save plot with articles about Justin Trudeau at month
    plot = df_year_month.plot(kind='bar',
                              title='Articles about Justin Trudeau at month',
                              xlabel='Date, Year and Month',
                              ylabel='Number of articles',
                              legend=None,
                              figsize=(20,10)
                            )
    fig = plot.get_figure()
    fig.savefig("Articles about Justin Trudeau at month.png",bbox_inches = 'tight')
    log_message('process_data',"Articles about Justin Trudeau at month saved as graph to 'Articles about Justin Trudeau at month.csv'")