import streamlit as st

# Load chosen css into pageimport streamlit as st
def load_css():
    with open("visuals/styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)