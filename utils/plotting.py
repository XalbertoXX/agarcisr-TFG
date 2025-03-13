import plotly.express as px
import streamlit as st

# Interactive chart showcase
def plot_interactive_chart(data_frame):
    if not data_frame.empty:
        fig = px.line(data_frame, title="Protocol Performance Over Time 📈")
        fig.update_xaxes(title_text='Test Iterations')
        fig.update_yaxes(title_text='Response Time (seconds)', tickformat=".6f")
        st.plotly_chart(fig)
    else:
        st.write("Ooops...\n\nThere is no data available to plot, sorry 😢")