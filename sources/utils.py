import pandas as pd
import streamlit as st
import plotly.express as px
import json
# from urllib.request import urlopen


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
    year_min = df['année'].min()
    year_max = df['année'].max()
    if year_min == year_max:
        return year_min, year_max + 1
    else:
        return year_min, year_max


@st.cache_data
def get_names_stats(names_list, df_allnames):
    df_allnames_grp = df_allnames.groupby(['prénom', 'année']).agg(nombre=('nombre', 'sum')).reset_index()

    df = pd.DataFrame()
    for _, df_allnames_iyear in df_allnames_grp.groupby('année'):
        df_allnames_iyear['popularité (rang)'] = df_allnames_iyear['nombre'].rank(method='max', ascending=False).astype('int')
        df_allnames_iyear['popularité (%)'] = (1. - df_allnames_iyear['nombre'].rank(method='max', ascending=False, pct=True))
        df_iyear = df_allnames_iyear[df_allnames_iyear['prénom'].isin(names_list)]
        df = pd.concat([df, df_iyear])
    return df


@st.cache_data
def get_nombre_naissance_fig(df):
    fig = px.line(df, x='année', y='nombre', title='Nombre de naissances', color='prénom', markers=True)
    fig.update_yaxes(rangemode="tozero")
    return fig


@st.cache_data
def get_popularite_fig(df, type_pop):
    fig = px.line(df, x="année", y=f"popularité ({type_pop})", title='Popularité', color='prénom', markers=True)
    if type_pop == 'rang':
        fig.update_yaxes(rangemode="tozero", autorange="reversed")
    elif type_pop == '%':
        fig.update_layout(yaxis_range=[0, 1], yaxis_tickformat=".0%")

    return fig


@st.cache_data
def get_all_stats(df_allnames):
    df_allnames_grp = df_allnames.groupby(['prénom']).agg(nombre=('nombre', 'sum')).reset_index()
    df_allnames_grp['popularité (rang)'] = df_allnames_grp['nombre'].rank(method='max', ascending=False).astype('int')
    df_allnames_grp['popularité (%)'] = 100*(1. - df_allnames_grp['nombre'].rank(method='max', ascending=False, pct=True))
    df_allnames_grp = df_allnames_grp.sort_values(['nombre', 'prénom'], ascending=[False, True]).reset_index(drop=True)

    return df_allnames_grp

@st.cache_data
def get_departement_stats(names_list, df_allnames):
    print(df_allnames)
    df_allnames_grp = df_allnames.groupby('département').agg(nombre=('nombre', 'sum')).reset_index()
    print(df_allnames_grp)
    return df_allnames


@st.cache_data
def build_map(df, type_map):
    df = df.groupby(['département']).agg(nombre=('nombre', 'sum')).reset_index()

    # with urlopen('https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson') as f:
    with open('./data/carte-de-france-et-outre-mers-new.geojson') as f:
        geojson = json.load(f)

    full_df = pd.DataFrame({
        'nom': [feature['properties']['Département'] for feature in geojson['features'] if 'code' in feature['properties']],
        'département': [feature['properties']['code'] for feature in geojson['features'] if 'code' in feature['properties']]
    })
    full_df['nombre'] = 0

    for _, r in df.iterrows():
        full_df.loc[full_df['département'] == r['département'], 'nombre'] = r['nombre']

    color_continuous_scale = ['#ffffff', '#FF4B4B']

    fig = px.choropleth_mapbox(
        full_df,
        geojson=geojson,
        featureidkey='properties.code',
        locations='département',
        color='nombre',
        center={"lat": 46.5, "lon": 2.4},
        zoom=4.4,
        mapbox_style="white-bg",
        hover_name='nom',
        opacity=1.,
        color_continuous_scale=color_continuous_scale
    )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

    return fig
