import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
sns.set_style('whitegrid')


def generate_data():

    ### Data collected from https://www.zillow.com/phoenix-az/home-values/  ###

    df = pd.read_excel('PHX_Housing.xls', sheet_name='All Homes', skiprows=[0, 1, 3], usecols=[0, 13])
    df.rename({'Region Name':'postal_code', 'Current.2':'Rent'}, axis=1, inplace=True)

    conn = sqlite3.connect('yelp.db')
    cur = conn.cursor()

    df1 = pd.read_sql_query("Select latitude, longitude, postal_code, Sentiment From Temp", conn)
    df1['postal_code'] = df1['postal_code'].replace('', np.nan)
    df1.dropna(inplace=True)
    df1['postal_code'] = np.int64(df1['postal_code'])
    df1['Sentiment'] = np.float64(df1['Sentiment'])


    df2 = df.merge(df1, on='postal_code', how='inner')
    df2.drop(columns=['postal_code'], axis=1, inplace=True)

    bins = 5
    lat_range = abs(df2['latitude'].max() - df2['latitude'].min())
    lon_range = abs(df2['longitude'].max() - df2['longitude'].min())

    lat_vals = [df2['latitude'].min() + i*lat_range/bins for i in range(0, bins)]
    lon_vals = [df2['longitude'].min() + i*lon_range/bins for i in range(0, bins)]
    
    lat_vals.append(df2['latitude'].max())
    lon_vals.append(df2['longitude'].max())
    lat_vals = sorted(lat_vals)
    lon_vals = sorted(lon_vals)

    lat_labels, lon_labels = list(), list()

    lat_labels = [str(x) for x in lat_vals[1:]]
    lon_labels = [str(x) for x in lon_vals[1:]]

    lat_region = pd.cut(df2['latitude'], bins=lat_vals, labels=lat_labels)
    df2.insert(2, 'lat_region', lat_region)

    lon_region = pd.cut(df2['longitude'], bins=lon_vals, labels=lon_labels)
    df2.insert(3, 'lon_region', lon_region)

    df2.drop(columns=['latitude', 'longitude'], axis=1, inplace=True)

    df3 = df2.groupby(['lat_region', 'lon_region']).agg({'Sentiment': 'mean', 'Rent':'mean'})
    df3.dropna(inplace=True)


    conn.commit()

    return df3



def clustering(df):

    rent =  df['Rent'].values
    sentiment = df['Sentiment'].values

    X = np.array((rent, sentiment)).T

    plt.figure(figsize=(8,8))
    plt.scatter(rent, sentiment, s=50, label='sentiment-stars')
    plt.legend()
    plt.xlabel('rent', fontsize=20)
    plt.ylabel('sentiment', fontsize=20)
    plt.title('Clustering of sentiment and rent data', fontsize=20)
    plt.savefig('Figures/sentiment-rent.png')
    plt.show()
    
    wcss = list()

    for i in range(1, 20):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10,
                random_state=0)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)
    

    plt.plot(range(1, 20), wcss)
    plt.xlabel('Number of Clusters', fontsize=20)
    plt.ylabel('WCSS', fontsize=20)
    plt.title('Elbow  Method', fontsize=20)
    plt.savefig('Figures/wcss.png')
    plt.show()


    kmeans =  KMeans(n_clusters=3, init='k-means++', max_iter=300, n_init=10,
            random_state=0)
    pred_y = kmeans.fit_predict(X)

    plt.figure(figsize=(10, 8))
    plt.scatter(rent, sentiment, c=pred_y, s=50, cmap='viridis')
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],  s=300, c='k')
    plt.xlabel('rent', fontsize=20)
    plt.ylabel('sentiment', fontsize=20)
    plt.title('Result of  KMeans clustering on Sentiment Analysis and  Housing Data', fontsize=20)
    plt.savefig('Figures/Clustering_Sentiment_Rent.png')
    plt.show()


if  __name__ == '__main__':

    df = generate_data()
    clustering(df)

