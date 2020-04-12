import sqlite3
from sqlalchemy import create_engine
import pandas as pd
import flair

def generate_dataframe():
    conn = sqlite3.connect('yelp.db')
    cur = conn.cursor()

    df = pd.read_sql_query("Select * From Final", conn)
    df.drop(['latitude_y', 'longitude_y', 'review_count'], axis=1, inplace=True)
    df.rename({'stars_x':'stars', 'latitude_x':'latitude', 'longitude_x':'longitude'}, axis=1, inplace=True)
    # print(df.shape)
    df = df.groupby('business_id').head(5).reset_index(drop=True)
    # print(df.shape)
    # unique_businesses = df['name'].unique()
    # print(len(unique_businesses))

    conn.commit()
    return df

def create_table():

    engine = create_engine('sqlite:///yelp.db', echo=False)
    df = generate_dataframe()
    df.to_sql('Temp', con=engine, index=False, if_exists='append')

def add_sentiment():

    conn = sqlite3.connect('yelp.db')
    cur = conn.cursor()

    df = pd.read_sql_query("Select * From Temp", conn)

    data  =  df['text'].values


    flair_sentiment = flair.models.TextClassifier.load('en-sentiment')

    count = 0
    for item in data:
        # if count == 2:
            # break
        print(count)
        s = flair.data.Sentence(item)
        flair_sentiment.predict(s)
        sentiment = str(s.labels[0]).split(' ')[0]
        val = str(s.labels[0]).split(' ')[1]
        val = float(val[val.find('(')+1:val.find(')')])
        if sentiment == 'POSITIVE':
            print(s.labels[0], val)
            cur.execute(''' Update Temp Set Sentiment = ?  Where text = ?''', (val, item))
        else:
            print(s.labels[0], -val)
            cur.execute(''' Update Temp Set Sentiment = ?  Where text = ?''', (-val, item))
        count += 1


        conn.commit()

if __name__ == '__main__':

    create_table()
    add_sentiment()
