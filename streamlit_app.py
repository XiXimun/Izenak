import streamlit as st

from sources.utils import get_names, get_df, get_departments, build_fig, get_year_range


# ----------------- general parameters -----------------

names_file = './data/insee.fr/dpt2022.csv'

# ------------------------------------------------------


def home():
    st.title(':baby: Tout savoir sur les prénoms !')
    st.write("Vous trouverez ici toutes les statistiques des prénoms donnés en France recensés par l'INSEE.")

    df = get_df(names_file)

    sexes = st.multiselect(label='Fille ou garçon ?', options=['Fille', 'Garçon'])
    sexes = [2 if x == 'Fille' else 1 for x in sexes]
    df = df[df['sexe'].isin(sexes)]

    names_list = get_names(df)
    names_list = st.multiselect('Choisis des prénoms', names_list)
    df = df[df['prénom'].isin(names_list)]

    if names_list:
        departments_list = get_departments(df)
        departments_list = st.multiselect('Choisis une zone géographique', departments_list)
        if departments_list:
            df = df[df['département'].isin(departments_list)]

        year_min, year_max = get_year_range(df)
        year_min, year_max = st.slider('Choisis une période', year_min, year_max, (year_min, year_max))
        df = df[df['année'].isin(range(year_min, year_max + 1))]

        fig = build_fig(df)
        st.plotly_chart(fig, use_container_width=True)

    # st.dataframe(df.reset_index(drop=True))


def about():
    st.title('À propos')
    st.write("Les statistiques proviennent des données fournies par l'INSEE.")
    st.write("Vous retrouverez les prénoms donnés en France entre 1900 et 2022. Les prénoms donnés moins de 3 fois par an et par département ne sont pas reportés.")
    st.markdown('Toutes suggestions, remarques, bugs ou encouragements peuvent être transmis au webmaster: <a href="mailto:web.xilo@gmail.com">web.xilo@gmail.com</a>', unsafe_allow_html=True)



def main():
    st.set_page_config(page_title='Prénoms', page_icon=':baby:')
    page = st.sidebar.radio(" ", ["Accueil", "À propos"])

    if page == "Accueil":
        home()
    elif page == "À propos":
        about()


if __name__ == "__main__":
    main()
