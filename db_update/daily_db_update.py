from datetime import date 
import os
from datetime import datetime
from threading import Timer

import requests
import pymysql.cursors

#from app.app import db, eur_exchange_rates


def get_latest_exchange_rates(access_key, currencies):

    symbols = ",".join(currencies)
    api_link = "http://api.exchangeratesapi.io/v1/latest?"  
    request_parameters = f"access_key={access_key}&symbols={symbols}"

    get_exchange_rates_link = api_link + request_parameters
    response = requests.get(get_exchange_rates_link)

    return response.json()


def change_exchange_rates_base(base, to_base, exchange_rates):

    exchange_rates = exchange_rates.copy()
    change_base_ratio = exchange_rates[base] / exchange_rates[to_base]
    exchange_rates[base] = round(change_base_ratio, 6)
    exchange_rates[to_base] = 1

    lst_currencies = list(exchange_rates.keys())
    lst_currencies.remove(base)
    lst_currencies.remove(to_base)

    for cur in lst_currencies:
        exchange_rates[cur] = round(change_base_ratio/(1/exchange_rates[cur]), 6)

    return exchange_rates


"""def db_exchange_rate_insert(date, base, currency, currency_value):

    exchange_rate = eur_exchange_rates(date=date, base=base, currency=currency, 
        currency_value=currency_value)

    db.session.add(exchange_rate)
    db.session.commit()"""


def db_exchange_rate_insert(date, base, currency, currency_value):
    
    connection = pymysql.connect(host='0.0.0.0',
                            database=os.getenv('MYSQL_DATABASE'),
                            user=os.getenv('MYSQL_USER_NAME'),
                            password=os.getenv('MYSQL_ROOT_PASSWORD'),
                            cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `exchange_rates` (`date`, `base`, `currency`, `currency_value`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (date, base,currency, currency_value))

            sql = "UPDATE `events` SET date = %s WHERE event = 'last_update'"
            cursor.execute(sql, (date))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()



def update_exchangerates_db():

    access_key = os.getenv('API_ACCESS_TOKEN')
    currencies = ["USD", "EUR", "RUB", "CNY"]

    eur_exchange_rate = get_latest_exchange_rates(access_key, currencies)
    
    if not ('error' in eur_exchange_rate.keys()):

        eur_exchange_rate = eur_exchange_rate["rates"]        
        exchange_rates_dict = dict()
        exchange_rates_dict["EUR"] = eur_exchange_rate

        for i in eur_exchange_rate.keys():
            if i != "EUR":
                exchange_rates_dict[i] = change_exchange_rates_base("EUR", i, eur_exchange_rate)


        date_today = date.today() 
        for base in exchange_rates_dict.keys():

            for curr in exchange_rates_dict[base].items():

                db_exchange_rate_insert(date_today, base, curr[0], curr[1])
        



if __name__ == "__main__":

    update_exchangerates_db()
    x=datetime.today()
    y=x.replace(day=x.day+1, hour=9, minute=0, second=0, microsecond=0)
    delta_t=y-x

    secs=delta_t.seconds+1
    t = Timer(secs, update_exchangerates_db())
    try:
        
        t.start()
    except Exception as err:
        print(err)