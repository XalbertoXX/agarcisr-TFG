import streamlit as st
import requests
import time
import pandas as pd
import plotly.express as px
import json
import os

# Protocols Information
protocols = {
    'Diffie-Hellman 🤝': {
        'description': 'A method of securely exchanging cryptographic keys over a public channel.',
        'description_long': 'The Diffie-Hellman protocol is a method for securely exchanging cryptographic keys over a public channel. It allows two parties to agree upon a shared secret key, which can then be used for secure communication or encryption. The protocol relies on the mathematical properties of modular exponentiation to ensure that even if an eavesdropper intercepts the exchanged information, they cannot easily determine the shared secret key without solving a computationally difficult problem.',
        'endpoint': 'diffie_hellman'
    },
    'RSA 🛡️': {
        'description': 'A form of public-key cryptography using a pair of keys for encryption and decryption.',
        'description_long': 'RSA uses a pair of keys, a public key for encryption and a private key for decryption. It is widely used for secure data transmission and involves complex computations that ensure security even with public disclosure of the encryption key.',
        'endpoint': 'rsa'
    }
}

# Streamlit Page Configuration
st.set_page_config(page_title='Protocol Performance Comparison', layout='wide')

# Protocol Selection
st.sidebar.title("Protocol List 🌌")
selected_protocol = st.sidebar.selectbox("Select Protocol", list(protocols.keys()))

# Protocol Description
st.sidebar.info(protocols[selected_protocol]['description'])

# Display a textbox for custom message input when RSA is selected
user_message = ""
if selected_protocol == 'RSA 🛡️':
    user_message = st.text_area("Enter your message for RSA encryption:")

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

                # Save response data along with the time to JSON file
                response_data['response_time'] = response_time
                with open('protocol_test_data.json', 'w') as file:
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

# Load previous test results, if available
loaded_data = load_test_results()
if loaded_data:
    response_times_data = loaded_data
else:
    # Pre-populate data with simulated tests
    for _ in range(10):  # Number of simulations
        for protocol in protocols.keys():
            response_time = test_protocol(protocols[protocol]['endpoint'], simulate=True)
            if response_time is not None:
                response_times_data[protocol].append(response_time)
                tests_count[protocol] += 1
    save_test_results(response_times_data)


# Function to Plot Interactive Chart
def plot_interactive_chart(data_frame):
    fig = px.line(data_frame, title="Protocol Performance Over Time")
    fig.update_xaxes(title_text='Test Iterations')
    fig.update_yaxes(title_text='Response Time (seconds)')
    st.plotly_chart(fig)

# Button to Test Protocol
if st.button(f'Test {selected_protocol}'):
    if selected_protocol == 'RSA 🛡️':
        response_time = test_protocol(protocols[selected_protocol]['endpoint'], user_message=user_message)
    else:
        response_time = test_protocol(protocols[selected_protocol]['endpoint'])

    if response_time is not None:
        st.success(f"{selected_protocol} Response Time: {response_time:.3f} seconds")
        tests_count[selected_protocol] += 1

        # Update response_times_data after testing a protocol
        for protocol in response_times_data.keys():
            if protocol == selected_protocol:
                response_times_data[protocol].append(response_time)
            else:
                # Use the last known value for protocols not tested in this iteration
                last_value = response_times_data[protocol][-1] if response_times_data[protocol] else 0
                response_times_data[protocol].append(last_value)

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