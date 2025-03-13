import requests
import time
import streamlit as st

# Funtion to call server endpoints and test functionalities of protocols
def test_protocol(endpoint, user_message):
    simulate = False
    try:
        start_time = time.time()
        if endpoint == 'rsa' and user_message:
            response = requests.post(f'http://localhost:5000/{endpoint}', json={'message': user_message})
        else:
            response = requests.get(f'http://localhost:5000/{endpoint}')
        end_time = time.time()
        response_time = end_time - start_time
        
        response_json = response.json()
        st.write(response_json)
        
        if response.status_code == 200 and response_json.get('success', True):
            if not simulate:
                return response_time, response_json
        else:
            if not simulate:
                st.error(f"Failed to test {endpoint}: Server responded with status code {response.status_code}")
                return None
    except requests.RequestException as e:
        if not simulate:
            st.error(f"Failed to test {endpoint}: {e}")
            return None