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
def build_fig(df):
    df = df.groupby(by=['prénom', 'année']).agg(nombre=("nombre", "sum")).reset_index()
    fig = px.line(df, x="année", y="nombre", title='Naissances en France', color='prénom', markers=True)
    fig.update_yaxes(rangemode="tozero")
    return fig
