import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import  LogisticRegression
from sklearn.metrics import roc_curve, auc

def LogRegModel():

    conn = sqlite3.connect('yelp.db')
    cur = conn.cursor()

    df = pd.read_sql_query("Select business_id, name, user_id, stars, useful, funny,  cool,  latitude,  longitude, Sentiment From Temp", conn)

    df['Sentiment'] = np.float64(df['Sentiment'])

    #### Logistic Regression Model #####

    df1 = df.groupby(['business_id', 'name', 'latitude', 'longitude']).agg({'stars':'mean', 'useful':'mean', 'funny':'mean', 'cool':'mean', 'Sentiment':'mean'})
    
    df1['Sentiment']  = np.where(df1['Sentiment'] > 0, 1, 0)

    pearson_corr_coeff = df1.corr(method='pearson').loc['stars', 'Sentiment']
    print("Stars and Sentiment Correlation Coefficient :", pearson_corr_coeff)

    df1['stars'].hist(bins=100, range=[min(df['stars'].values), max(df['stars'].values)], figsize=(8,6))
    plt.show()

    pearson_corr_coeff = df1.corr(method='pearson').loc['useful', 'Sentiment']
    print("Useful and Sentiment Correlation Coefficient :", pearson_corr_coeff)

    df1['useful'].hist(bins=100, range=[min(df['useful'].values), max(df['useful'].values)], figsize=(8,6))
    plt.show()

    df1['funny'].hist(bins=100, range=[min(df['funny'].values), max(df['funny'].values)], figsize=(8,6))
    plt.show()

    pearson_corr_coeff = df1.corr(method='pearson').loc['cool', 'Sentiment']
    print("Cool and Sentiment Correlation Coefficient :", pearson_corr_coeff)

    df1['cool'].hist(bins=100, range=[min(df['cool'].values), max(df['cool'].values)], figsize=(8,6))
    plt.show()


    df1['Sentiment'].hist(bins=100, range=[min(df['Sentiment'].values), max(df['Sentiment'].values)], figsize=(8,6))
    plt.show()

    features  =  df1[['stars']]
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

if __name__ == '__main__':

    LogRegModel()

