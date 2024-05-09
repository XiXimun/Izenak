import pandas as pd
import streamlit as st
import plotly.express as px


@st.cache_data
def read_file(names_file):
    df = pd.read_csv(names_file, sep=';')
    return df


@st.cache_data
def get_df(names_file):

    df_raw = read_file(names_file)
    df_raw.columns = ['sexe', 'prénom', 'année', 'département', 'nombre']

    # Drop rows based on values
    df = df_raw[~(
        (df_raw['prénom'] == '_PRENOMS_RARES') |
        (df_raw['année'] == 'XXXX') |
        (df_raw['département'] == 'XX')
      )].copy()

    df['année'] = df['année'].astype(int)
    df['nombre'] = df['nombre'].astype(int)
    return df


@st.cache_data
def get_names(df):
    names_list = df['prénom'].unique().tolist()
    names_list.sort()
    return names_list


@st.cache_data
def get_departments(df):
    departments_list = df['département'].unique().tolist()
    departments_list.sort()
    return departments_list


@st.cache_data
def get_year_range(df):
    return df['année'].min(), df['année'].max()


@st.cache_data
def get_stats(names_list, df_allnames):
    df_allnames_grp = df_allnames.groupby(['prénom', 'année']).agg(nombre=('nombre', 'sum')).reset_index()

    df = pd.DataFrame()
    for i, df_allnames_iyear in df_allnames_grp.groupby('année'):
        df_allnames_iyear['popularité (rang)'] = df_allnames_iyear['nombre'].rank(method='max', ascending=False).astype('int')
        df_allnames_iyear['popularité (%)'] = 100*(1. - df_allnames_iyear['nombre'].rank(method='max', ascending=False, pct=True))
        # dft = dft.sort_values(['nombre', 'prénom'], ascending=[False, True]).reset_index(drop=True)

        df_iyear = df_allnames_iyear[df_allnames_iyear['prénom'].isin(names_list)]
        df = pd.concat([df, df_iyear])
    return df


@st.cache_data
def build_map(df):
    france_departments = px.data.gapminder().query("country == 'France'")
    fig = px.choropleth_mapbox(
        france_departments,
        geojson='https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson',
        locations='iso_alpha',
        featureidkey='properties.code',
        color='lifeExp',
        hover_name='country',
        hover_data=['iso_alpha', 'lifeExp'],
        color_continuous_scale="Viridis",
        mapbox_style="carto-positron",
        zoom=4,
        center={"lat": 46.603354, "lon": 1.888334}
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})



    from urllib.request import urlopen
    import json
    import numpy as np

    with urlopen('https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson') as response:
        geojson = json.load(response)
    df = pd.DataFrame([x['properties'] for x in geojson['features']])
    df['randNumCol'] = np.random.randint(0, 10, df.shape[0]).astype('str')

    fig = px.choropleth_mapbox(df, geojson=geojson, featureidkey='properties.code', locations='code', 
                            color="randNumCol", center = {"lat":47, "lon":2}, zoom=4.3, mapbox_style="carto-positron",
                            opacity=0.5)

    fig.update_layout(mapbox_style="open-street-map",
                    showlegend=False,
                    margin={"r":0,"t":0,"l":0,"b":0}, 
                    width=600, 
                    height=500
                    )

    return fig
