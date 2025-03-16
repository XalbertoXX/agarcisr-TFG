import requests
import time
import json
import streamlit as st

def test_protocol(endpoint, user_message):
    simulate = False
    try:
        start_time = time.time()
        
        # Track request size (for POST requests)
        request_size = 0
        if endpoint == 'rsa' and user_message:
            # For POST requests (e.g., RSA), calculate request size
            request_body = json.dumps({'message': user_message})
            request_size = len(request_body.encode('utf-8'))
            response = requests.post(f'http://localhost:5000/{endpoint}', json={'message': user_message})
        else:
            # For GET requests, assume no request body
            response = requests.get(f'http://localhost:5000/{endpoint}')
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Calculate response size
        response_size = len(response.content)
        
        # Calculate bandwidth (Mbps)
        bandwidth = (request_size + response_size) * 8 / (response_time * 1e6) if response_time > 0 else 0
        
        # Calculate encryption overhead (for RSA only)
        encryption_overhead = None
        if endpoint == 'rsa' and user_message:
            # Assume the response includes encrypted data (modify based on your API)
            encrypted_message = response.json().get('encrypted_message', '')
            original_size = len(user_message.encode('utf-8'))
            encrypted_size = len(encrypted_message.encode('utf-8'))
            encryption_overhead = encrypted_size - original_size
        
        response_json = response.json()
        st.write(response_json)
        
        if response.status_code == 200 and response_json.get('success', True):
            if not simulate:
                return {
                    "response_time": response_time,
                    "bandwidth": bandwidth,
                    "encryption_overhead": encryption_overhead,
                    "response_json": response_json
                }
        else:
            if not simulate:
                st.error(f"Failed to test {endpoint}: Server responded with status code {response.status_code}")
                return None
    except Exception as e:
        if not simulate:
            st.error(f"Failed to test {endpoint}: {e}")
            return None