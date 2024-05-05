import streamlit as st
import requests, time, json, os
import pandas as pd
import plotly.express as px
from sqlalchemy import text 

# Set the page title and favicon
st.set_page_config(page_title="Protocol Performance Test", page_icon="🚀")

# Connection management
if 'conn' not in st.session_state:
    st.session_state.conn = st.connection("postgresql", type="sql")

conn = st.session_state.conn

# Save the results for  test results
def save_test_results(protocol_name, time_seconds):
    query = text("""
        INSERT INTO protocol_performance (protocol_name, time_seconds, created_at)
        VALUES ((SELECT endpoint FROM protocols WHERE name = :protocol_name), :time_seconds, CURRENT_TIMESTAMP);
    """)
    
    with conn.session as c:
        try:
            # Execute the query with parameters
            c.execute(query, {'protocol_name': protocol_name, 'time_seconds': time_seconds})
            c.commit() # Commit the transaction
        except Exception as e:
            st.error(f"An error occurred: {e}")
            c.rollback()  # Roll back the transaction on error

# Load or initialize test results
def load_test_results(protocol_name):
    query = """
        SELECT time_seconds FROM protocol_performance
        WHERE protocol_name = (SELECT endpoint FROM protocols WHERE name = :protocol_name)
        ORDER BY created_at ASC;
    """
    try:
        df = conn.query(query, params={'protocol_name': protocol_name}, ttl="5s")
        return df['time_seconds'].tolist() if not df.empty else []
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []

# Plot the interactive chart
def plot_interactive_chart(data_frame):
    if not data_frame.empty:
        fig = px.line(data_frame, title="Protocol Performance Over Time 📈")
        fig.update_xaxes(title_text='Test Iterations')
        fig.update_yaxes(title_text='Response Time (seconds)')
        st.plotly_chart(fig)
    else:
        st.write("Ooops...\n\nThere is no data available to plot, sorry 😢")
        
# Test the protocol
def test_protocol(endpoint, simulate=False, user_message=None):
    response_time = None
    try:
        start_time = time.time()
        if endpoint == 'rsa' and user_message:
            response = requests.post(f'http://localhost:5000/{endpoint}', json={'message': user_message})
        else:
            response = requests.get(f'http://localhost:5000/{endpoint}')
        end_time = time.time()
        response_time = end_time - start_time

        if response.status_code == 200:
            response_data = response.json()
            if not simulate:
                st.write(f"Response from server: {response_data}")
                # Save response data
                save_test_results(selected_protocol, response_time)
        else:
            if not simulate:
                st.error(f"Failed to test {endpoint}: Server responded with status code {response.status_code}")
    except requests.RequestException as e:
        if not simulate:
            st.error(f"Failed to test {endpoint}: {e}")

    return response_time


# Perform query.
df = conn.query('SELECT * FROM protocols;', ttl="10m")

# Frontend main title, sidebar and tabs definition
protocol_list = df['name'].tolist()

# Sidebar
st.sidebar.title("Protocol List 🌌")
selected_protocol = st.sidebar.selectbox("Select Protocol", list(protocol_list))

# Perform query to get the protocol data of the selected protocol
df1 = conn.query(f""" SELECT * FROM protocols WHERE name = '{selected_protocol}';""", ttl="10m")

# Protocol Description
st.sidebar.info(df1['description'].iloc[0])

# Enhanced Sidebar for Protocol Information
with st.sidebar:
    st.title("Protocol Details 🧐")
    st.write(df1['description_long'].iloc[0])

# Tabs
tab1, tab2 = st.tabs(["Test Protocols", "Compare Protocols"])

# Tab 1: Test Protocols
with tab1:
    user_message = ""
    if selected_protocol == 'RSA 📜':
        user_message = st.text_area("Enter your message for RSA encryption:")

    if st.button(f'Test {selected_protocol}'):
        response_time = test_protocol(df1['endpoint'].iloc[0], user_message=user_message)
        if response_time:
            st.success(f"{selected_protocol} Response Time: {response_time:.3f} seconds")
            save_test_results(selected_protocol, response_time)

# Tab 2: Compare Protocols
with tab2:
    comparison_protocols = st.multiselect("Select protocols to compare", protocol_list)
    if comparison_protocols:
        comparison_data = {protocol: pd.Series(load_test_results(protocol), dtype=float) for protocol in comparison_protocols}
        comparison_df = pd.DataFrame(comparison_data)
        plot_interactive_chart(comparison_df)