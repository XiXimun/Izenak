import pandas as pd
import streamlit as st




@st.cache_data
def read_file(names_file):
    df = pd.read_csv(names_file, sep=';')
    return df


@st.cache_data
def get_df(names_file):

    df_raw = read_file(names_file)
    df_raw.columns=['sexe', 'prénom', 'année', 'département', 'nombre']

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
