import requests
import json
import sqlite3
import config

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

api_key =  config.yelp_api_key

headers = {'Authorization': 'Bearer %s' % api_key}

url = 'https://api.yelp.com/v3/businesses/search'

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


conn.commit()

