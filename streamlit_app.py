import streamlit as st

def home():
    st.title('Home Page')
    st.write('Welcome to the Home page mon amou!')
    st.write('Navigate to the About page using the sidebar.')

def about():
    st.title('About Page')
    st.write('This is the About page.')
    st.write('Feel free to learn more about us here!')

def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.radio("Go to", ["Home", "About"])

    if page == "Home":
        home()
    elif page == "About":
        about()

if __name__ == "__main__":
    main()
