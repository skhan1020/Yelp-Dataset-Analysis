import pandas as pd
import  sqlite3
import sqlalchemy
import numpy as np
from bokeh.io import output_file, show
from bokeh.models import (ColumnDataSource, GMapOptions, HoverTool, PanTool, WheelZoomTool, BoxSelectTool, BoxZoomTool)
from bokeh.plotting import gmap
from  bokeh.palettes import brewer
import config

def generate_data():

    ### Data collected from https://www.zillow.com/phoenix-az/home-values/  ###

    df = pd.read_excel('PHX_Housing.xls', sheet_name='All Homes', skiprows=[0, 1, 3], usecols=[0, 13])
    df.rename({'Region Name':'postal_code', 'Current.2':'Rent'}, axis=1, inplace=True)


    conn = sqlite3.connect('yelp.db')
    cur = conn.cursor()

    df1 = pd.read_sql_query("Select latitude, longitude, postal_code From Temp", conn) 
    df1['postal_code'] = df1['postal_code'].replace('', np.nan)
    df1.dropna(inplace=True)
    df1['postal_code'] = np.int64(df1['postal_code'])


    df2 = df.merge(df1, on='postal_code', how='inner')

    df3 = df2.groupby('postal_code').agg({'latitude':'mean', 'longitude':'mean',   'Rent': 'mean'}).reset_index()


    df3.drop_duplicates(subset=['postal_code'], inplace=True)

    conn.commit()
    return df3

def plot(df, palette, filename):

    df['latitude'] = np.float64(df['latitude'])
    df['longitude'] = np.float64(df['longitude'])
    latitude_list = [x for x in df['latitude'].values]
    longitude_list = [x for x in df['longitude'].values]
    rent = ['$' + str(x) for  x in df['Rent'].values]
    scale = np.array(df['Rent'].values)/max(df['Rent'].values)
    new_scale = [int(i*10) for i  in scale]
    scale_drop_duplicates =  list(set(new_scale))


    radius = [x*100 for x in new_scale]

    colors =   brewer[palette][9]
    colors = colors[::-1]

    colormap = dict(zip(scale_drop_duplicates, colors))
    colors = [colormap[x] for x  in new_scale]  

    map_options = GMapOptions(lat=33.4484, lng=-112.0740, map_type="roadmap", zoom=12)
    api_key = config.gmap_api_key

    source = ColumnDataSource(data=dict(lat=latitude_list, lon=longitude_list, radius=radius, colors=colors, alpha=scale, label = rent))

    hover = HoverTool(tooltips=[("Rent", "@label")])

    bokeh_plot = gmap(api_key, map_options, tools=[hover, WheelZoomTool(), PanTool(), BoxZoomTool()], title='Phoenix Housing Data (Rent per Sq. Ft.)')

    bokeh_plot.circle(x="lon", y="lat", radius="radius", fill_color="colors",
            line_color="colors", line_width=2, line_alpha=0.3, 
            fill_alpha=0.8, source=source)
    output_file(filename)
    show(bokeh_plot)


if __name__ ==  '__main__':

    df = generate_data()
    plot(df, 'Spectral', 'housingmap1_phoenix.html')
    plot(df, 'BuGn', 'housingmap2_phoenix.html')

