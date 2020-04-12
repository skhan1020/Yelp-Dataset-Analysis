import sqlite3
from sqlalchemy import create_engine
import pandas as pd
import dask.dataframe as dd

def generate_final_dataframe():

    conn = sqlite3.connect('yelp.db')
    cur = conn.cursor()


    df_BR = pd.read_sql_query("Select * From BusinessReview", conn)
    df_API = pd.read_sql_query("Select * From Business_API", conn)

    df_BR.drop({'stars_y', 'review_count', 'is_open', 'attributes', 'categories'}, axis=1, inplace=True)


    dd_BR = dd.from_pandas(df_BR, npartitions=3)
    dd_API = dd.from_pandas(df_API, npartitions=3)

    dd_merged = dd_BR.merge(dd_API, on=['business_id', 'name'], how='inner')
    df_merged = dd_merged.compute()


    conn.commit()

    return df_merged

def create_table():

    engine = create_engine('sqlite:///yelp.db', echo=False)
    df = generate_final_dataframe()
    df.to_sql('Final', con=engine, index=False, if_exists='append')

if __name__ == '__main__':

    create_table()
