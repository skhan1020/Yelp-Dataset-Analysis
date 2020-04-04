import sqlite3
import pandas as pd
import flair

conn = sqlite3.connect('businesses.db')
cur = conn.cursor()

# cur.execute(''' Alter Table Final Drop Column If Exists Sentiment ''')
cur.execute(''' Alter Table Final Add Column Sentiment Int  ''')
df = pd.read_sql_query("Select review From Final", conn)

data  =  df['review'].values

# data  =  data[:2]
# print(data.shape)

flair_sentiment = flair.models.TextClassifier.load('en-sentiment')

# cur.execute('''Select Sentiment From Final''')
count = 0
# for row in cur:
    # if count == 2:
        # break
for item in data:
    print(count)
    # item = data[count]
    s = flair.data.Sentence(item)
    flair_sentiment.predict(s)
    sentiment = str(s.labels[0]).split(' ')[0]
    print(sentiment)
    if sentiment == 'POSITIVE':
        # # sentiment.append(1) 
        # cur.execute('''Insert Into Final(Sentiment) Values(?) ''', (1,))
        cur.execute(''' Update Final Set Sentiment = ?  Where review = ?''', (1, item))
    else:
        # # sentiment.append(0)
        # cur.execute('''Insert Into Final(Sentiment) Values(?) ''', (0,))
        cur.execute(''' Update Final Set Sentiment = ?  Where review = ?''', (0, item))
    count += 1

# df['sentiment'] = sentiment

# print(df.head())

# print("unique business ids", df_temp['business_id'].unique().shape)
# print("unique user ids", df_temp['user_id'].unique().shape)

# df_temp.set_index(['user_id', 'business_id'], inplace=True)

# print(df_temp.head())

conn.commit()



