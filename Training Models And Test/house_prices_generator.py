#Функция для генерации новых данных

import pandas as pd
import numpy as np
import configparser
from sqlalchemy import create_engine  
import datetime
import pickle
from sdv.single_table import GaussianCopulaSynthesizer


config = configparser.ConfigParser()
config.read('/home/aleksey/Notebooks_Projects/House-Prices-Airflow-Superset/Training Models And Test/config.ini')
conn_string = config.get('DATABASE', 'connection_url')


#Таблица с новыми данными которые генерируются

new_data_from_generator = 'house_prices_generator'

filepath = '/home/aleksey/Notebooks_Projects/House-Prices-Airflow-Superset/Training Models And Test/synthesizer.pkl'

synthesizer = GaussianCopulaSynthesizer.load(filepath)


def upload_generator_data(new_data_from_generator):

    #Генерация случайных данных

    
    synthetic_data = synthesizer.sample(num_rows=10)

    #Баг с обучением

    synthetic_data['3SsnPorch'] = 0

    #Убираем баг и подставляем дату

    synthetic_data['dt'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    
    engine = create_engine(conn_string) 
    
    with engine.connect() as conn:
        synthetic_data.to_sql(new_data_from_generator, con=conn, if_exists='replace',index=False) 
    
    return print(synthetic_data)

if __name__ == "__main__":
     upload_generator_data(new_data_from_generator)