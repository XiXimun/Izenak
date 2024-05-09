import streamlit as st
import pandas as pd
import plotly.express as px

from sources.utils import get_names, get_df, get_departments, get_year_range, build_map, get_stats


# ----------------- general parameters -----------------

names_file = './data/insee.fr/dpt2022.csv'

# ------------------------------------------------------


def un_prenom():
    st.title(':baby: Tout savoir sur un prénom !')
    st.write("Vous trouverez ici toutes les statistiques des prénoms donnés en France recensés par l'INSEE.")

    df_allnames = get_df(names_file)

    sexes = st.multiselect(label='Fille ou garçon ?', options=['Fille', 'Garçon'])
    sexes = [2 if x == 'Fille' else 1 for x in sexes]
    df_allnames = df_allnames[df_allnames['sexe'].isin(sexes)]

    names_list = get_names(df_allnames)
    names_list = st.multiselect('Choisis des prénoms', names_list)
    df_selnames = df_allnames[df_allnames['prénom'].isin(names_list)]

    if names_list:

        departments_list = get_departments(df_selnames)
        departments_list = st.multiselect('Choisis une zone géographique', departments_list)
        if departments_list:
            df_selnames = df_selnames[df_selnames['département'].isin(departments_list)]
            df_allnames = df_allnames[df_allnames['département'].isin(departments_list)]

        year_min, year_max = get_year_range(df_selnames)
        year_min, year_max = st.slider('Choisis une période', year_min, year_max, (year_min, year_max))
        df_selnames = df_selnames[df_selnames['année'].isin(range(year_min, year_max + 1))]
        df_allnames = df_allnames[df_allnames['année'].isin(range(year_min, year_max + 1))]

        df = get_stats(names_list, df_allnames)

        fig = px.line(df, x='année', y='nombre', title='Nombre de naissances', color='prénom', markers=True)
        fig.update_yaxes(rangemode="tozero")
        st.plotly_chart(fig, use_container_width=True)

        type_pop = st.radio('Popularité :', ['rang', '%'], horizontal=True, captions=['Classement absolu', 'Classement relatif'])

        fig = px.line(df, x="année", y=f"popularité ({type_pop})", title='Popularité', color='prénom', markers=True)
        if type_pop == 'rang':
            fig.update_yaxes(rangemode="tozero")
            fig.update_yaxes(autorange="reversed")
        elif type_pop == '%':
            fig.update_layout(yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

        # fig = build_map(df_selnames)
        # st.plotly_chart(fig, use_container_width=True)

    # st.dataframe(df_selnames.reset_index(drop=True))


def prenoms_populaires():

    st.title(':star2: Les prénoms populaires !')
    st.write("Vous trouverez ici toutes les statistiques des prénoms donnés en France recensés par l'INSEE.")

    df = get_df(names_file)

    sexes = st.multiselect(label='Fille ou garçon ?', options=['Fille', 'Garçon'])
    sexes = [2 if x == 'Fille' else 1 for x in sexes]
    df = df[df['sexe'].isin(sexes)]

    departments_list = get_departments(df)
    departments_list = st.multiselect('Choisis une zone géographique', departments_list)
    if departments_list:
        df = df[df['département'].isin(departments_list)]

    year_min, year_max = get_year_range(df)
    year_min, year_max = st.slider('Choisis une période', year_min, year_max, (year_min, year_max))
    df = df[df['année'].isin(range(year_min, year_max + 1))]

    st.dataframe(df.reset_index(drop=True))


def a_propos():
    st.title('À propos')
    st.write("Les statistiques proviennent des données fournies par l'INSEE.")
    st.write("Vous retrouverez les prénoms donnés en France entre 1900 et 2022. Les prénoms donnés moins de 3 fois par an et par département ne sont pas reportés.")
    st.markdown('Toutes suggestions, remarques, bugs ou encouragements peuvent être transmis au webmaster: <a href="mailto:web.xilo@gmail.com">web.xilo@gmail.com</a>', unsafe_allow_html=True)


def main():
    st.set_page_config(page_title='Prénoms', page_icon=':baby:')
    # page = st.sidebar.radio(' ', ['Un prénom', 'Prénoms populaires', 'À propos'])
    page = st.sidebar.radio(' ', ['Un prénom', 'À propos'])

    if page == "Un prénom":
        un_prenom()
    if page == "Prénoms populaires":
        prenoms_populaires()
    elif page == "À propos":
        a_propos()


if __name__ == "__main__":
    main()
