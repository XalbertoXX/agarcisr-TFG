import streamlit as st

# Load css
def load_css():
    with open("visuals/styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
# Injects bare css for dynamic frames
def load_bare_css():
    with open("visuals/styles.css", "r") as f:
        css_content = f.read()
        return css_content