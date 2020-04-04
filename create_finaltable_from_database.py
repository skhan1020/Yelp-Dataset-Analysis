import sqlite3
import pandas as pd


conn = sqlite3.connect('businesses.db')
cur = conn.cursor()

cur.executescript('''
        Drop Table IF Exists Final;

        Create Table Final As
        Select B.business_id, B.name, B.latitude, B.longitude, R.user_id, R.time_created,
        B.review_count, R.rating,
        R.review From Business B Inner Join Review R On B.business_id =
        R.business_id
        ''')


# df_business = pd.read_sql_query("Select * From Business", conn)
# df_review = pd.read_sql_query("Select * From Review", conn)
# print(df_business.shape)
# print(df_review.shape)

df_temp = pd.read_sql_query("Select * From Final", conn)
print(df_temp.shape)

print("unique business ids", df_temp['business_id'].unique().shape)
print("unique user ids", df_temp['user_id'].unique().shape)

df_temp.set_index(['user_id', 'business_id'], inplace=True)

print(df_temp.head())

conn.commit()



