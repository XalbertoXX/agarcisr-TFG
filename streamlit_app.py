import streamlit as st
import requests
import time
import pandas as pd
import plotly.express as px
import json
import os

# Protocols Information
protocols = {
    'Protocol': {
        'description': 'description',
        'description_long': 'description_long',
        'endpoint': 'endpoint'
    },
    'Protocol': {
        'description': 'description',
        'description_long': 'description_long',
        'endpoint': 'endpoint'
    }
}

# Streamlit Page Configuration
st.set_page_config(page_title='Protocol Performance Comparison', layout='wide')

# Protocol Selection
st.sidebar.title("Protocol List 🌌")
selected_protocol = st.sidebar.selectbox("Select Protocol", list(protocols.keys()))

# Protocol Description
st.sidebar.info(protocols[selected_protocol]['description'])

def test_protocol(endpoint, simulate=False):
    response_time = None

    try:
        start_time = time.time()
        response = requests.get(f'http://localhost:5000/{endpoint}')

        end_time = time.time()
        response_time = end_time - start_time

        if response.status_code == 200:
            response_data = response.json()
            # Display the response data
            st.write(f"Response from server: {response_data}")

            # Save response data along with the time to JSON file
            response_data['response_time'] = response_time
            with open('dh_exchange_data.json', 'w') as file:
                json.dump(response_data, file)

        else:
            if not simulate:
                st.error(f"Failed to test {endpoint}: Server responded with status code {response.status_code}")

    except requests.RequestException as e:
        if not simulate:
            st.error(f"Failed to test {endpoint}: {e}")

    return response_time

# Function to Save Test Results to File
def save_test_results(data, filename='test_results.json'):
    with open(filename, 'w') as file:
        json.dump(data, file)

# Function to Load Test Results from File
def load_test_results(filename='test_results.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return None

# Initialize response times data structure with empty lists
response_times_data = {protocol: [] for protocol in protocols.keys()}
tests_count = {protocol: 0 for protocol in protocols.keys()}  # Tracks the number of tests for each protocol

# Function to Plot Interactive Chart
def plot_interactive_chart(data_frame):
    fig = px.line(data_frame, title="Protocol Performance Over Time")
    fig.update_xaxes(title_text='Test Iterations')
    fig.update_yaxes(title_text='Response Time (seconds)')
    st.plotly_chart(fig)

# Button to Test Protocol
if st.button(f'Test {selected_protocol}'):
    response_time = test_protocol(protocols[selected_protocol]['endpoint'])

    if response_time is not None:
        st.success(f"{selected_protocol} Response Time: {response_time:.3f} seconds")
        tests_count[selected_protocol] += 1

        # Create the DataFrame from the updated response times data
        df = pd.DataFrame(response_times_data)

        # Display the line chart using Plotly for better interactivity
        plot_interactive_chart(df)

# Protocol Comparison Feature
comparison_protocols = st.multiselect("Compare Protocols", list(protocols.keys()), default=None)
if comparison_protocols:
    comparison_df = pd.DataFrame({protocol: response_times_data[protocol] for protocol in comparison_protocols})
    plot_interactive_chart(comparison_df)

# Enhanced Sidebar for Protocol Information
with st.sidebar:
    st.title("Protocol Details")
    st.write(protocols[selected_protocol]['description_long'])

