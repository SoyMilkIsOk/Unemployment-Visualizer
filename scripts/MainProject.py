#!/usr/local/bin/python3

import json
import urllib.request
from urllib.request import urlopen
from pathlib import Path

import plotly
import plotly.express as px
import plotly.graph_objs as go


import csv

import pandas as pd
import numpy as np
from numpy import genfromtxt

def graph():

    path = Path(__file__).parent.parent / "data/unemployment_data_us.csv" #Found this helpful trick with pathlib on stackoverflow: https://stackoverflow.com/questions/40416072/reading-file-using-relative-path-in-python-project

    with path.open() as csv_file:

        listColumns = [2,4,5,6,7,8,9,10,11,12]
        file = csv.reader(csv_file, delimiter=',')

        data = [row for row in file]
        headers = data[0]
        headers = [headers[i] for i in listColumns]
        data = np.asarray(data[1:])
        data = data[:, listColumns]

    srs = pd.date_range("2010", freq="M", periods=132)
    df = pd.DataFrame(data, index = srs)

    df.columns = headers #set the header row as the df header
    # print(df.columns)

    fig = px.line(df, x=df.index, y=df.columns,
        markers=True
        )
    fig.update_yaxes(type='linear',title="Unemployment Rate (%)")
    fig.update_xaxes(title="Year (2010-2020)")

    # fig.write_html('first_figure.html', auto_open=True)
    fig.show()


def graph2(yearOrMonth):
    if (yearOrMonth == "year"):
        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            counties = json.load(response)

        df = pd.read_csv("../data/counties_unemployment2000-2020.csv",
            dtype={"fips": str})
        # print(df)

        df = df.melt(id_vars=['fips'], var_name='year', value_name='unemp')
        # print(df)

        fig = px.choropleth(df, geojson=counties, locations='fips', color='unemp',
            color_continuous_scale="YlOrRd",
            range_color=(2, 12),
            labels={'unemp':'Unemployment Rate (%)'},
            title = 'Yearly County Unemployment Rates - (2010-2020)',
            scope = 'usa',
            animation_frame="year"
            )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.show()

    elif (yearOrMonth == "month2020"):

        with open('../data/States.json') as response:
            states = json.load(response)

        df = pd.read_csv("../data/StatesMonthlyData.csv",
            dtype={"fips": str})

        # print(df['state'])
        for state in df['state']:
            for row in states:
                if (row['state'] == state):
                    df.loc[(df.state == state),'state']= row['abbreviation'].upper()

        # print(df)

        df = df.melt(id_vars=['state'], var_name='month', value_name='unemp')
        # print(df)

        fig = px.choropleth(df, locationmode='USA-states', locations='state', color='unemp',
            color_continuous_scale="YlOrRd",
            range_color=(2, 15),
            labels={'unemp':'Unemployment Rate (%)'},
            title = 'Monthly State Unemployment Rate - 2020',
            scope = 'usa',
            animation_frame="month"
            )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.show()

    elif (yearOrMonth == "month2021"):

        with open('../data/States.json') as response:
            states = json.load(response)

        df = pd.read_csv("../data/StatesMonthlyData-2021.csv",
            dtype={"fips": str})

        # print(df['state'])
        for state in df['state']:
            for row in states:
                if (row['state'] == state):
                    df.loc[(df.state == state),'state']= row['abbreviation'].upper()

        # print(df)

        df = df.melt(id_vars=['state'], var_name='month', value_name='unemp')
        # print(df)

        fig = px.choropleth(df, locationmode='USA-states', locations='state', color='unemp',
            color_continuous_scale="YlOrRd",
            range_color=(2, 15),
            title = 'Monthly State Unemployment Rate - 2021',
            labels={'unemp':'Unemployment Rate (%)'},
            scope = 'usa',
            animation_frame="month"
            )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.show()
