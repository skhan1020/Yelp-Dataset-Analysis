from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions 
from bokeh.plotting import gmap
import config
import sqlite3
import pandas as pd


conn = sqlite3.connect("businesses.db")
cur = conn.cursor()

df = pd.read_sql_query(''' Select latitude, longitude, Sentiment From Final ''', conn)
latitude_list = [float(x) for x in df['latitude'].values]
longitude_list = [float(x) for  x in df['longitude'].values]

map_options = GMapOptions(lat=40.7128, lng=-74.0060, map_type="roadmap", zoom=4)
api_key = config.api_key 

bokeh_plot = gmap(api_key, map_options, title='Business Locations')

source = ColumnDataSource(data=dict(lat=latitude_list, lon=longitude_list))

bokeh_plot.circle(x="lon", y="lat", size=30, fill_alpha=0.8, source=source)
output_file('bokehmap.html')
show(bokeh_plot)
conn.commit()


