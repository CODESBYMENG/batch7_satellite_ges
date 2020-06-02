# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/WIP_OCO2_Map.ipynb (unless otherwise specified).

__all__ = ['inventory_map_only', 'peaks_capture_map']

# Cell
import pandas as pd
import geopandas as gpd
import numpy as np
from numpy import exp, loadtxt, pi, sqrt, log
import math
import matplotlib
import matplotlib.pyplot as plt
import swiftclient
import json
from io import StringIO
import folium
from folium import plugins
import geopy
from shapely.geometry import Polygon
from shapely.wkt import loads
from geopy.distance import VincentyDistance

# Cell
def inventory_map_only(invent):
    """
    Create map with inventory only
    :param invent: GeoDataFrame, Dataframe containing all inventory.
    :return:
    """
    # Initialize Map
    inventory_map = folium.Map([43, 0], zoom_start=4)
    folium.TileLayer("CartoDB dark_matter", name="Dark mode").add_to(inventory_map)

    d={}
    invent_types = invent['CO2/CO2e emissions source'].unique()
    for cl in invent_types:
        d["{0}".format(cl)]=folium.FeatureGroup(name=cl).add_to(inventory_map)

    for index, row in invent.iterrows():
        radius = row['CO2/CO2e emissions (in tonnes per year)']/10000000
        color="#368534" # green

        tooltip =  "["+str(round(row['latitude'],2))+" ; "+str(round(row['longitude'],2))+"]"
        pop = str(round(row['CO2/CO2e emissions (in tonnes per year)'],0))
        title = "" + str(round(row['CO2/CO2e emissions (in tonnes per year)'],0)) + " T/y " + row['CO2 or CO2e']
        popup_html = """<h4>"""+title+"""</h4><p>"""+tooltip+"""</p>""" + """<p>"""+ str(row['CO2/CO2e emissions source']) + ", from " + str(row['Data source']) + """</p>"""
        popup=folium.Popup(popup_html, max_width=450)

        d[row['CO2/CO2e emissions source']].add_child(folium.CircleMarker(location=(row["latitude"],
                                      row["longitude"]),
                            radius=radius,
                            color=color,
                            popup=popup,
                            tooltip= str(row['CO2/CO2e emissions source']),
                            fill=True))

    folium.map.LayerControl(collapsed=False).add_to(inventory_map)

    plugins.Fullscreen(
        position='topright',
        title='Expand me',
        title_cancel='Exit me',
        force_separate_button=True
    ).add_to(inventory_map)

    #inventory_map.save("inventory_map.html")
    return inventory_map



def peaks_capture_map(peaks, invent):
    """
    Create map with peaks (marker + capture zone) and inventory
    :param peaks: GeoDataFrame, Dataframe containing the peaks we want to display.
    :param plants: GeoDataFrame, Dataframe containing all registered plants.
    :param plants_coal: GeoDataFrame, Dataframe containing all registered coal plants.
    :param cities: GeoDataFrame, Dataframe containing all registered big cities.
    :return:
    """
    # Initialize Map
    peaks_capture = folium.Map([40, -100], zoom_start=4)
    folium.TileLayer("CartoDB dark_matter", name="Dark mode").add_to(peaks_capture)

    # Adding detected peaks
    peaks_group = folium.FeatureGroup(name="Peaks").add_to(peaks_capture)
    peaks_group_capture = folium.FeatureGroup(name=" - 50km Capture Zone", show=False).add_to(peaks_capture)
    for index, row in peaks.iterrows():
        radius = row["amplitude"]/20
        tooltip =  "["+str(round(row['latitude'],2))+" ; "+str(round(row['longitude'],2))+"]"
        color="#FF3333" # red
        sounding = str(row['sounding_id'])
        date = str(row['date'])
        orbit = str(row['orbit'])

        popup_html="""<h4>"""+tooltip+"""</h4>"""+date+"""<p>sounding_id: """+sounding+"""</br>orbit: """+orbit+"""</p>"""
        popup_html+='<p><input type="button" value="Show plot"'
        # Injecting JavaScript in popup to fire the Dash Callback
        popup_html+='onclick="\
            let bco_input = parent.document.getElementById(\'input_sounding\'); \
            let lastValue = bco_input.value;'
        popup_html+=f'bco_input.value = \'{sounding}\';'
        popup_html+="let bco_event = new Event('input', { bubbles: true });\
            bco_event.simulated = true;\
            let tracker = bco_input._valueTracker;\
            if (tracker) {\
            tracker.setValue(lastValue);\
            }\
            bco_input.dispatchEvent(bco_event);\
            elt.dispatchEvent(new Event('change'));\
            \"/></p>"

        popup=folium.Popup(popup_html, max_width=450)

        peaks_group_capture.add_child(folium.GeoJson(row['geometry'], name=" - Capture Zone", tooltip=sounding, popup=popup))

        peaks_group.add_child(folium.CircleMarker(location=(row["latitude"],
                                      row["longitude"]),
                            radius=radius,
                            color=color,
                            tooltip=sounding,
                            popup=popup,
                            fill=True))


    d={}
    invent_types = invent['CO2/CO2e emissions source'].unique()
    for cl in invent_types:
        d["{0}".format(cl)]=folium.FeatureGroup(name=cl).add_to(peaks_capture)

    for index, row in invent.iterrows():
        radius = row['CO2/CO2e emissions (in tonnes per year)']/10000000
        color="#368534" # green

        tooltip =  "["+str(round(row['latitude'],2))+" ; "+str(round(row['longitude'],2))+"]"
        pop = str(round(row['CO2/CO2e emissions (in tonnes per year)'],0))
        title = "" + str(round(row['CO2/CO2e emissions (in tonnes per year)'],0)) + " T/y " + row['CO2 or CO2e']
        popup_html = """<h4>"""+title+"""</h4><p>"""+tooltip+"""</p>""" + """<p>"""+ str(row['CO2/CO2e emissions source']) + ", from " + str(row['Data source']) + """</p>"""
        popup=folium.Popup(popup_html, max_width=450)

        d[row['CO2/CO2e emissions source']].add_child(folium.CircleMarker(location=(row["latitude"],
                                      row["longitude"]),
                            radius=radius,
                            color=color,
                            tooltip= str(row['CO2/CO2e emissions source']),
                            fill=True))

    peaks_capture.keep_in_front(peaks_group)

    folium.map.LayerControl(collapsed=False).add_to(peaks_capture)

    plugins.Fullscreen(
        position='topright',
        title='Expand me',
        title_cancel='Exit me',
        force_separate_button=True
    ).add_to(peaks_capture)

    minimap = plugins.MiniMap()
    peaks_capture.add_child(minimap)

    #peaks_capture.save("peaks_capture_map.html")
    return peaks_capture