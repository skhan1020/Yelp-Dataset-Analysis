import requests
import json
import sqlite3

conn = sqlite3.connect('businesses.db')
cur = conn.cursor()

cur.executescript('''
            Drop Table If Exists Business;

            CREATE TABLE Business( 
            business_id TEXT Not Null Primary Key, 
            name TEXT Unique, 
            latitude TEXT, 
            longitude TEXT, 
            review_count INTEGER, 
            image_url TEXT) 
            ''')

api_key = '7K8GNIVUcB3xHw2iO2bmvRWfrE0WauXm9Rke_9F-vDYzeP4bj1yBSjZYjAm2V1OsnV-YGc5FL9aZVr81g8EWOQUscGx3et1yFuu-c7UGhjL_pAkcaR1fwzb2SPFyXnYx'

headers = {'Authorization': 'Bearer %s' % api_key}

url = 'https://api.yelp.com/v3/businesses/search'
# params = {'limit':50, 'offset':50, 'term': 'bars', 'location': 'new york city'}

for offset in range(0, 1000, 50):
    params = {'limit': 50,
            'offset': offset,
            'term': 'restaurants',
            'location': 'new york city'
            }

    response = requests.get(url, params=params, headers=headers)

    print('The status code is {}'.format(response.status_code))
    if response.status_code == 200:
        js = json.loads(response.text)
    else:
        print('400 Bad Request')
        break


    for item in js['businesses']:
        cur.execute(''' Insert or Ignore Into Business(business_id, name, latitude, 
                longitude, review_count, image_url) Values(?,?,?,?,?,?) ''',
                (item['id'],item['name'], item['coordinates']['latitude'], 
                item['coordinates']['longitude'], item['review_count'],
                item['image_url']))

    # # print(item['id'])
    # # print(item['name'])
    # print(item['coordinates'])
    # print(item['review_count'])
    # print(item['image_url'])
    # print(item.keys())
    # print()
    # print()

conn.commit()



# json_file = 'yelp_academic_dataset_business.json'
# with open('yelp_academic_dataset_business.json') as f:
    # js = json.loads(f.read())
