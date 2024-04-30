import requests, time, json, os
import pandas as pd
import plotly.express as px
import streamlit as st

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

st.set_page_config(page_title='Protocol Performance Comparison', layout='wide')

def save_test_results(data, filename='test_results.json'):
    with open(filename, 'w') as file:
        json.dump(data, file)

def load_test_results(filename='test_results.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return None

def plot_interactive_chart(data_frame, title="Protocol Performance Over Time"):
    fig = px.line(data_frame, title=title)
    fig.update_xaxes(title_text='Test Iterations')
    fig.update_yaxes(title_text='Response Time (seconds)')
    st.plotly_chart(fig)

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

# Load or initialize test results
response_times_data = load_test_results()

# Protocol Selection
st.sidebar.title("Protocol List 🌌")
selected_protocol = st.sidebar.selectbox("Select Protocol", list(protocols.keys()))

# Protocol Description
st.sidebar.info(protocols[selected_protocol]['description'])

# Enhanced Sidebar for Protocol Information
with st.sidebar:
    st.title("Protocol Details")
    st.write(protocols[selected_protocol]['description_long'])

tab1, tab2 = st.tabs(["Test Protocols", "Compare Protocols"])

# Tab 1: Test Protocols
with tab1:
    # Display a textbox for custom message input when RSA is selected
    user_message = ""
    if selected_protocol == 'RSA 🛡️':
        user_message = st.text_area("Enter your message for RSA encryption:")

    if st.button(f'Test {selected_protocol}'):
        response_time = test_protocol(protocols[selected_protocol]['endpoint'], user_message=user_message)
        if response_time:
            st.success(f"{selected_protocol} Response Time: {response_time:.3f} seconds")
            response_times_data[selected_protocol].append(response_time)
            save_test_results(response_times_data)

# Tab 2: Compare Protocols
with tab2:
    comparison_protocols = st.multiselect("Select protocols to compare", list(protocols.keys()), default=list(protocols.keys()))
    if comparison_protocols:
        comparison_df = pd.DataFrame({protocol: response_times_data[protocol] for protocol in comparison_protocols})
        plot_interactive_chart(comparison_df)
