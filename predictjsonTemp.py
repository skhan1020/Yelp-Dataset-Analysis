import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import  LogisticRegression
from sklearn.metrics import roc_curve, auc

conn = sqlite3.connect('yelp.db')
cur = conn.cursor()

df = pd.read_sql_query("Select business_id, name, user_id, stars, useful, funny,  cool,  latitude,  longitude, Sentiment From Temp", conn)

df['Sentiment'] = np.float64(df['Sentiment'])

#### Logistic Regression Model #####

df1 = df.groupby(['business_id', 'name', 'latitude', 'longitude']).agg({'stars':'mean', 'useful':'mean', 'funny':'mean', 'cool':'mean', 'Sentiment':'mean'})
df1['Sentiment']  = np.where(df1['Sentiment'] > 0, 1, 0)

print(df1.shape)
# print(df.Sentiment.values)
# print(df.stars.values)
# print(df.useful.values)
# print(df.funny.values)
# print(df.cool.values)
# print(df1['stars'].describe())
# print(df1['useful'].describe())
# print(df1['funny'].describe())
# print(df1['cool'].describe())
# print(df1['Sentiment'].describe())
# df1['Sentiment'].hist(bins=100, range=[min(df['Sentiment'].values), max(df['Sentiment'].values)], figsize=(8,6))
# plt.show()

features  =  df1[['stars', 'useful', 'funny', 'cool']]
sentiment = df1['Sentiment']

X_train,  X_test, y_train, y_test =  train_test_split(features, sentiment, random_state=0)
scaler  = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.fit_transform(X_test)

for i, this_C in  enumerate([0.1, 1.0, 10.0]):
    clf = LogisticRegression(C=this_C).fit(X_train_scaled, y_train)
    y_predict = clf.predict(X_test_scaled)
    y_score_clf = clf.decision_function(X_test_scaled)

    print('Train Accuracy %.3f' %(clf.score(X_train_scaled, y_train)))
    print('Test Accuracy %.3f' %(clf.score(X_test_scaled, y_test)))

    fpr_clf, tpr_clf, _ = roc_curve(y_test, y_score_clf)
    roc_auc_clf  = auc(fpr_clf, tpr_clf)

    yval = [x for  x  in  fpr_clf]
    plt.figure(figsize=(10, 10))
    plt.plot(fpr_clf, yval, c='r', lw=1)
    plt.plot(fpr_clf, tpr_clf, lw=3,  label= "C = " + str(this_C) + " auc-roc = " + str(roc_auc_clf.round(2)))
    plt.legend(loc='best')
    plt.xlabel('FPR')
    plt.ylabel('TPR')
    plt.title(f'ROC curve using Logistic Regression (C={this_C})')
    plt.show()
conn.commit()



