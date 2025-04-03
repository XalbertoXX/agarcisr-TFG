import streamlit as st
from utils.carousel import display_carousel
from utils.database import get_page_content

# Main page
def show_overview(conn):
    st.title("Welcome to the Protocol Performance Test Site 🧪!")
    content = get_page_content(conn,"overview_text")
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("Failed to load content")

    display_carousel()