# -*- coding: utf-8 -*-
"""
@author: Sander van der Plas
"""

import cityroute
import osmnx as ox
import networkx as nx
from matplotlib.collections import LineCollection
import pandas as pd
import numpy as np
from shapely.geometry import LineString, Polygon, box
import geopandas as gpd
import folium
from folium.map import Marker
from folium.plugins import MarkerCluster
import json
import loadWFS as lw
from owslib.wfs import WebFeatureService

### GATHERING STARTING DATA
city = 'Utrecht, Netherlands'
origin_location = "Stationshal 12 Utrecht"
dest_location = "Parijsboulevard 143 Utrecht"
network_type = 'bike'
shortest_path, roads_graph, short_nodes, edges = cityroute.cityroute(city, origin_location, dest_location, network_type, weight='lenght').get_shortest_path()
# fastest_path, roads_graph, short_nodes, edges = cityroute.cityroute(city, origin_location, dest_location, network_type, weight='time').get_shortest_path()

route_nodes = [roads_graph.nodes[n] for n in shortest_path]
route_coords = [(n['x'], n['y']) for n in route_nodes]
route_geom = LineString(route_coords)
route_df = gpd.GeoDataFrame(geometry=[route_geom])
route_df = route_df.set_crs('epsg:4326')

# Then filter and get data based on routes
route_wfs = route_df.to_crs('epsg:28992')
xmin, ymin, xmax, ymax = route_wfs.total_bounds

# use following WFS services
wfsUrl_bag = 'https://service.pdok.nl/lv/bag/wfs/v2_0?request=GetCapabilities&service=WFS&typename=bag:ligplaats'
wfsUrl_wijk = 'https://service.pdok.nl/cbs/wijkenbuurten/2022/wfs/v1_0?request=GetFeature&service=WFS'

wfs_wijk = (lw.loadWFS(wfsUrl_wijk, xmin, ymin, xmax, ymax)).create_gdf()
gdf_wijk = wfs_wijk.set_crs('epsg:28992') # set coordinate to 
gdf_wijk = gdf_wijk.to_crs('epsg:4326')

# Intersect neighbourhoods and use the result to filter the buildings
route_polygon = route_df.geometry.buffer(0.0001).unary_union
gdf_wijk_intersection = gdf_wijk[gdf_wijk.intersects(route_polygon)]

# Get data based on neighbourhood
response_wfs = gdf_wijk_intersection.to_crs('epsg:28992')
xmin, ymin, xmax, ymax = response_wfs.total_bounds

# Gather and filter buildings based on neighbourhoods
wfs_bag = (lw.loadWFS(wfsUrl_bag, xmin, ymin, xmax, ymax)).create_gdf()
gdf_bag = wfs_bag.set_crs('epsg:28992')
gdf_bag = gdf_bag.to_crs("epsg:4326")
gdf_bag = gdf_bag[gdf_bag['oppervlakte_min'] >= 40]
# gdf_bag = gdf_bag[gdf_bag.geometry.within(gdf_wijk.iloc[0].geometry)]

gdf_bag = gpd.sjoin(gdf_bag, gdf_wijk_intersection, op='within')

buildings_before_1992 = gdf_bag[gdf_bag['bouwjaar'] < 1992]
buildings_after_1992 = gdf_bag[gdf_bag['bouwjaar'] >= 1992]

### BUILD OUR FOLIUM MAP
valconMap = folium.Map(location=[52.0901461, 5.1111027], zoom_start=11)

# Add different openstreetMaps
folium.TileLayer('openstreetmap').add_to(valconMap)
folium.TileLayer('Stamen Terrain').add_to(valconMap)
folium.TileLayer('Stamen Toner').add_to(valconMap)
folium.TileLayer('Stamen Water Color').add_to(valconMap)
folium.TileLayer('cartodbpositron').add_to(valconMap)
folium.TileLayer('cartodbdark_matter').add_to(valconMap)

# Add route to the map
route = folium.GeoJson(
    data=route_df["geometry"],
    name="shortest",
    style_function=lambda x: {
        'color': 'blue',
        'linewidth': 3,
        'weight': 2
    }
).add_to(valconMap)

# Create an overview of residents per neigbourhood
data_inwoners = pd.DataFrame(gdf_wijk_intersection[["buurtnaam", "aantalInwoners"]])
wijkpleth = folium.Choropleth(
    geo_data=gdf_wijk_intersection,
    name="Aantal inwoners per buurt",
    data=data_inwoners,
    columns=["buurtnaam", "aantalInwoners"],
    key_on='feature.properties.buurtnaam',
    fill_color="BuPu",
    fill_opacity=0.5,
    line_opacity=.1,
    legend_name="Residents",
).add_to(valconMap)

# Bring wijkpleth layer to the back
wijkpleth.layer_name = 'Residents'
valconMap.add_child(wijkpleth, name='Wijkpleth', index=0)

# Add polygons for buildings constructed before 1992
build_before_1992 = folium.GeoJson(
    data=buildings_before_1992["geometry"],
    name="Buildings before 1992",
    style_function=lambda x: {
        'fillColor': '#fd7f6f',
        'color': '#ed5151',
        'fillOpacity': 0.8,
        'weight': 1,
        'bringToBack': False,
    }
).add_to(valconMap)

# Add polygons for buildings constructed after 1992
build_after_1992 = folium.GeoJson(
    data=buildings_after_1992["geometry"],
    name="Buildings after 1992",
    style_function=lambda x: {
        'fillColor': '#b2e061',
        'color': '#a7c636',
        'fillOpacity': 0.8,
        'weight': 1,
        'bringToBack': False,
    }
).add_to(valconMap)

# Add markers for train station and building
folium.Marker(
    [52.0901461, 5.1111027],
    icon=folium.Icon(color='red', icon='train', prefix='fa')
).add_to(valconMap)

folium.Marker(
    [52.0972596, 5.0646437],
    icon=folium.Icon(color='green', icon='building', prefix='fa')
).add_to(valconMap)

# Add the layers to the LayerControl
folium.LayerControl().add_to(valconMap)

valconMap.save('valconMap.html')