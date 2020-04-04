import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import  LogisticRegression
from sklearn.metrics import roc_curve, auc

conn = sqlite3.connect('businesses.db')
cur = conn.cursor()

df = pd.read_sql_query("Select review_count, rating, Sentiment From Final", conn)

print(df['rating'].value_counts())
print(df['review_count'].describe())
print(df['Sentiment'].value_counts())

df['review_count'].hist(bins=100, range=[min(df['review_count'].values), max(df['review_count'].values)], figsize=(8,6))
plt.show()

features  =  df[['review_count', 'rating']]
sentiment = df['Sentiment']

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
    plt.plot(fpr_clf, tpr_clf, lw=3,  label=str(this_C))
    plt.legend(loc='best')
    plt.xlabel('FPR')
    plt.ylabel('TPR')
    plt.title(f'ROC curve using Logistic Regression (C={this_C})')
    plt.show()

conn.commit()



