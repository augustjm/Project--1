import streamlit as st
import geopandas as gpd
import plotly.express as px
from xml.etree import ElementTree as ET
import pandas as pd

def read_kml_revised(kml_path):
    tree = ET.parse(kml_path)
    root = tree.getroot()
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    data = []
    for placemark in root.findall('.//kml:Placemark', ns):
        name = placemark.find('kml:name', ns).text if placemark.find('kml:name', ns) is not None else None
        locality = placemark.find('.//kml:ExtendedData/kml:SchemaData/kml:SimpleData[@name="LOCALITY"]', ns).text if placemark.find('.//kml:ExtendedData/kml:SchemaData/kml:SimpleData[@name="LOCALITY"]', ns) is not None else None
        case_size = placemark.find('.//kml:ExtendedData/kml:SchemaData/kml:SimpleData[@name="CASE_SIZE"]', ns).text if placemark.find('.//kml:ExtendedData/kml:SchemaData/kml:SimpleData[@name="CASE_SIZE"]', ns) is not None else None
        data.append({'Name': name, 'LOCALITY': locality, 'CASE_SIZE': case_size})
    return pd.DataFrame(data)

@st.cache_data
def load_data():
    geo_df = gpd.read_file(r"C:\Users\marcu\user\project_1\data\DengueClustersGEOJSON.geojson")
    kml_df = read_kml_revised(r"C:\Users\marcu\user\project_1\data\DengueClustersKML.kml")
    merged_df = pd.merge(geo_df, kml_df, on='Name', how='outer')
    return merged_df

# Load data
df = load_data()

# Debugging lines
st.write("Available columns:", df.columns.tolist())
st.write("First few rows:", df.head())

# Create the map plot
fig = px.choropleth_mapbox(df,
                           geojson=df.geometry,
                           locations=df.index,
                           color='CASE_SIZE',
                           hover_name='LOCALITY',
                           color_continuous_scale='Viridis',
                           mapbox_style='carto-positron',
                           center={'lat': df.geometry.centroid.y.mean(), 'lon': df.geometry.centroid.x.mean()},
                           zoom=10)

# Show the plot
st.write(fig)
