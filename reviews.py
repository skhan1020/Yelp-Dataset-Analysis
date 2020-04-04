import requests
import json
import sqlite3
import pandas as pd
from sqlalchemy import create_engine
import config

def extract_reviews():

    api_key = config.yelp_api_key

    headers = {'Authorization': 'Bearer %s' % api_key}

    conn = sqlite3.connect('businesses.db')
    cur = conn.cursor()


    cur.execute(''' Drop Table If Exists Review ''')
    cur.execute(''' Select business_id From Business''')

    data = list()
    for row in cur:
        business_id = row[0]
        url = 'https://api.yelp.com/v3/businesses/' + business_id + '/reviews'
        req = requests.get(url, headers=headers)
        js = json.loads(req.text)
        for item in js:
            if item == 'reviews':
                review_item = js['reviews'][0]
                data_dict = {'business_id':business_id,
                        'user_id':review_item['user']['id'], 'time_created':review_item['time_created'],
                        'rating':review_item['rating'], 'review':review_item['text']}
                data.append(data_dict)
                

    df = pd.DataFrame(data)
    conn.commit()

    return df


def insert_reviews():

    engine = create_engine('sqlite:///businesses.db', echo=False)
    df = extract_reviews()
    df.to_sql('Review', con=engine, if_exists='append')

if __name__ == '__main__':

    insert_reviews()
