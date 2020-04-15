from bokeh.io import output_file, show, export_png
from bokeh.models import (ColumnDataSource, GMapOptions, HoverTool, PanTool, WheelZoomTool, BoxSelectTool, BoxZoomTool)
from bokeh.plotting import gmap
import config
import sqlite3
import pandas as pd
import numpy as np


def makeplot():

    conn = sqlite3.connect("yelp.db")
    cur = conn.cursor()

    df = pd.read_sql_query(''' Select latitude, longitude, name, Sentiment  From Temp ''', conn)
    df['Sentiment'] = np.float64(df['Sentiment'])
    df1 = df.groupby(['name', 'latitude', 'longitude']).agg({'Sentiment':'mean'})
    df1['Sentiment'] = np.where(df1['Sentiment'] > 0, 1, 0)
    df1.reset_index(inplace=True)

    names = [x  for x in df1['name'].values]
    latitude_list = [float(x) for x in df1['latitude'].values]
    longitude_list = [float(x) for  x in df1['longitude'].values]
    sentiment = [x for x in df1['Sentiment'].values]
    colors = ['green' if x == 1 else 'red' for x in sentiment]
    legends = ['Positive' if x == 1 else 'Negative' for x in sentiment]


    map_options = GMapOptions(lat=33.4484, lng=-112.0740, map_type="roadmap", zoom=12)
    api_key = config.gmap_api_key 


    source = ColumnDataSource(data=dict(lat=latitude_list, lon=longitude_list, label = names, color=colors, legend=legends))

    hover = HoverTool(tooltips=[("Name", "@label")])

    bokeh_plot = gmap(api_key, map_options, tools=[hover, WheelZoomTool(), PanTool(), BoxZoomTool()], title='Business Locations')

    bokeh_plot.circle(x="lon", y="lat", size=4, color='color', legend_field='legend', fill_alpha=0.8, source=source)
    output_file('sentimentmap.html')
    export_png(bokeh_plot, filename="Figures/sentimentmap.png")
    show(bokeh_plot)

    conn.commit()


if __name__ == '__main__':
    makeplot()

