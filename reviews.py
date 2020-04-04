import requests
import json
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

def extract_reviews():

    api_key = '7K8GNIVUcB3xHw2iO2bmvRWfrE0WauXm9Rke_9F-vDYzeP4bj1yBSjZYjAm2V1OsnV-YGc5FL9aZVr81g8EWOQUscGx3et1yFuu-c7UGhjL_pAkcaR1fwzb2SPFyXnYx'

    headers = {'Authorization': 'Bearer %s' % api_key}

    conn = sqlite3.connect('businesses.db')
    cur = conn.cursor()


    cur.execute(''' Drop Table If Exists Review ''')
    cur.execute(''' Select business_id From Business''')
    # count = 0
    data = list()
    for row in cur:
        # if count == 10:
            # break
        # count +=1
        business_id = row[0]
        # print(count, business_id)
        # print(business_id)
        url = 'https://api.yelp.com/v3/businesses/' + business_id + '/reviews'
        # url = 'https://api.yelp.com/v3/businesses/sCC7-hSdCkNPExejZT9BAQ/reviews'
        req = requests.get(url, headers=headers)
        # print('The status code is {}'.format(req.status_code))
        js = json.loads(req.text)
        for item in js:
            # print(item)
            if item == 'reviews':
                review_item = js['reviews'][0]
                # count += 1
                # data.append(review_item)
                # print(count)
                # print(review_item)
        # for item in js['reviews']:
            # print(count)
            # print(item)
                # print('business id',business_id)
                # print('review item keys', review_item.keys())
                # print('user id', review_item['user']['id'])
                # print('time created', review_item['time_created'])
                # print('rating', review_item['rating'])
                # print('text', review_item['text'])
                data_dict = {'business_id':business_id,
                        'user_id':review_item['user']['id'], 'time_created':review_item['time_created'],
                        'rating':review_item['rating'], 'review':review_item['text']}
                data.append(data_dict)
                # cur.execute(''' Insert Into Review(business_id, user_id) Values(?,?) ''', (business_id, review_item['user']['id']))
                
                # cur.execute(''' Insert Into Review(business_id, user_id,
                        # time_created, rating, review) Values(?,?,?,?,?) ''',
                    # (business_id, review_item['user']['id'], review_item['time_created'], review_item['rating'], review_item['text']))


    df = pd.DataFrame(data)
    # print(df)
    conn.commit()

    return df


def insert_reviews():

    engine = create_engine('sqlite:///businesses.db', echo=False)
    df = extract_reviews()
    df.to_sql('Review', con=engine, if_exists='append')

if __name__ == '__main__':

    insert_reviews()
