import pandas as pd
import json
import sqlite3
from  sqlalchemy import create_engine

def get_text():

    filename =  'yelp_academic_dataset_review.json'

    with open(filename) as f:
        data = f.readlines()
        data = list(map(json.loads, data))

    df = pd.DataFrame(data)
        

    return df


def insert_text_from_json():

    engine = create_engine('sqlite:///yelp.db', echo=False)
    df = get_text()
    df.to_sql('Review', con=engine, index=False, if_exists='append')

if __name__ == '__main__':

    insert_text_from_json()
