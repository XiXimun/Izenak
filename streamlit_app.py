import streamlit as st
import plotly.express as px

from sources.utils import get_names, get_df


#---------------------------------- general parameters

names_file = './data/insee.fr/dpt2022.csv'


def home():
    st.title('Prénoms')
    st.write('Welcome to the Home page mon amou!')

    df = get_df(names_file)


    sexes = st.multiselect(label='Fille ou garçon ?', options=['Fille', 'Garçon'])
    sexes = [2 if x == 'Fille' else 1 for x in sexes]
    df = df[df['sexe'].isin(sexes)]

    names_list = get_names(df)
    names_list = st.multiselect('Choisis des prénoms', names_list)
    df = df[df['prénom'].isin(names_list)]

    if names_list:
        df = df.groupby(by=['prénom', 'année']).agg(nombre=("nombre", "sum")).reset_index()
        fig = px.line(df, x="année", y="nombre", title=f'Naissances en France', color='prénom', markers=True)
        fig.update_yaxes(rangemode="tozero")
        st.plotly_chart(fig, use_container_width=True)

    # st.dataframe(df.reset_index(drop=True))





def about():
    st.title('A propos ...')
    st.write('Données provenant de https://www.insee.fr')
    

    





def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.radio("Go to", ["Accueil", "A propos"])

    if page == "Accueil":
        home()
    elif page == "A propos":
        about()


if __name__ == "__main__":
    main()
