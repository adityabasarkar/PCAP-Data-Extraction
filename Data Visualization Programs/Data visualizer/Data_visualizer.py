import pyshark
import os
import csv
import socket
import ipapi
import geoip2.webservice
import ipaddress
import json
import urllib
import urllib3
import plotly.graph_objects as go
import pandas as pd

csvreader = csv.reader(open("C:/Users/adity_724nfxg/OneDrive/Documents/aditya docs/Mentorship NCSSM materials/generated CSVs/GeneratedCSV4.csv", 'r'))
rowAccum = []
ip2domain = {}
ip2Lat = {}
ip2Long = {}
unable = {}

for row in csvreader:
    rowAccum.append(row)

rowAccum.remove(["Source", "Destination IP", "Volume", "Destination Domain", "Destination Latitude", "Destination Longitude"])

fig = go.Figure()
for row in rowAccum:
    wid = 1
    if int(row[2]) > 1000:
        wid = 1
    if int(row[2]) > 10000:
        wid = 2
    if int(row[2]) > 100000:
        wid = 3
    if int(row[2]) > 1000000:
        wid = 4
    if int(row[2]) > 10000000:
        wid = 5

    col = ''
    ColorDict = {
        'Echo plus 2nd gen':"red",
        'Desktop (server)':"blue",
        'Echo Look':"orange",
        'Nestcam':"yellow",
        'Motog Phone':"green",
        'Google onHub':"purple",
        'Ring Door bell':"black",
        'Samsung Smartthings hub2':"brown",
        'Smartwifiplug':"cyan",
        'LG smart TV':"tan",
        'Router':"white"
    }
    fig.add_trace(
        go.Scattergeo(
            locationmode = 'USA-states',
            lon = [-78.6821, row[5]],
            lat = [35.7847, row[4]],
            mode = 'lines',
            line = dict(width = wid,color = ColorDict[row[0]]),
            opacity = 1,
            legendgroup = row[0],
            showlegend = True,
            legendgrouptitle = dict(text = row[0]),
            hovertext = 'Domain: ' + row[3] + ', ' + 'Volume (Bits): ' + row[2]
        )
    )

fig.update_layout(
    title_text = 'Source to Destination IP visualization',
    showlegend = True,
    geo = dict(
        resolution = 50,
        showland = True,
        showlakes = True,
        landcolor = 'rgb(204, 204, 204)',
        countrycolor = 'rgb(204, 204, 204)',
        lakecolor = 'rgb(255, 255, 255)',
        projection_type = "equirectangular",
        coastlinewidth = 1,
        lataxis = dict(
            range = [20, 60],
            showgrid = True,
            dtick = 10
        ),
        lonaxis = dict(
            range = [-100, 20],
            showgrid = True,
            dtick = 20
        ),
    )
)

fig.write_html('first_figure.html', auto_open=True)