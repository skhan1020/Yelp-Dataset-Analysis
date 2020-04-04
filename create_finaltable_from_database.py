import sqlite3

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


conn.commit()



