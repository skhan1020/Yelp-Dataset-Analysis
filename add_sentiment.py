import sqlite3
import pandas as pd
import flair

conn = sqlite3.connect('businesses.db')
cur = conn.cursor()

cur.execute(''' Alter Table Final Add Column Sentiment Int  ''')
df = pd.read_sql_query("Select review From Final", conn)

data  =  df['review'].values


flair_sentiment = flair.models.TextClassifier.load('en-sentiment')

for item in data:
    s = flair.data.Sentence(item)
    flair_sentiment.predict(s)
    sentiment = str(s.labels[0]).split(' ')[0]
    if sentiment == 'POSITIVE':
        cur.execute(''' Update Final Set Sentiment = ?  Where review = ?''', (1, item))
    else:
        cur.execute(''' Update Final Set Sentiment = ?  Where review = ?''', (0, item))

conn.commit()



