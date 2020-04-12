from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions
from bokeh.plotting import gmap
import config
import sqlite3
import pandas as pd
import pdfkit

conn = sqlite3.connect("businesses.db")
cur = conn.cursor()

df = pd.read_sql_query(''' Select latitude, longitude, Sentiment  From Final ''', conn)
latitude_list = [float(x) for x in df['latitude'].values]
longitude_list = [float(x) for  x in df['longitude'].values]
sentiment = [int(x) for x in df['Sentiment'].values]
colors = ['green' if x == 1 else 'red' for x in sentiment]
legends = ['Positive' if x == 1 else 'Negative' for x in sentiment]


map_options = GMapOptions(lat=40.7128, lng=-74.0060, map_type="roadmap", zoom=10)
api_key = config.gmap_api_key 

bokeh_plot = gmap(api_key, map_options, title='Business Locations')

source = ColumnDataSource(data=dict(lat=latitude_list, lon=longitude_list, color=colors, legend=legends))

bokeh_plot.circle(x="lon", y="lat", size=2, color='color', legend_field='legend', fill_alpha=0.8, source=source)
output_file('bokehmap.html')
pdfkit.from_file('bokehmap.html', 'sentiment.pdf')
show(bokeh_plot)

conn.commit()

