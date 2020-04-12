import sqlite3
from sqlalchemy import create_engine
import pandas as pd
import dask.dataframe as dd

def generate_final_dataframe():

    conn = sqlite3.connect('yelp.db')
    cur = conn.cursor()


    df_review = pd.read_sql_query("Select * From Review", conn)
    df_business = pd.read_sql_query("Select * From Business", conn)

    print(df_review.head())
    print(df_business.head())

    dd_review = dd.from_pandas(df_review, npartitions=3)
    dd_business = dd.from_pandas(df_business, npartitions=3)

    dd_merged = dd_review.merge(dd_business, on='business_id', how='inner')
    df_merged = dd_merged.compute()
    print(df_merged.head())

    conn.commit()
    return df_merged

def create_table():

    engine = create_engine('sqlite:///yelp.db', echo=False)
    df = generate_final_dataframe()
    df.to_sql('BusinessReview', con=engine, index=False, if_exists='append')

if __name__ == '__main__':

    create_table()

