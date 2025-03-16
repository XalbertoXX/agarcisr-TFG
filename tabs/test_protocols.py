import streamlit as st
from utils.protocol_testing import test_protocol
from utils.database import save_test_results

# Testing protocol tab
def show_test_protocols(conn, selected_protocol, protocol_details_df):
    st.write("⬇️ Here is the magic button 🔥")
    user_message = ""
    # RSA test for input
    if selected_protocol.lower().startswith('rsa'):
        user_message = st.text_area("Enter a message for the fun...", value="Hello, World!", placeholder="Hello, World!")
    # Other protocol test
    if st.button(f'Test {selected_protocol}'):
        if not protocol_details_df.empty:
            endpoint = protocol_details_df['endpoint'].iloc[0]
            result = test_protocol(endpoint, user_message)
            # If retrieval from operation is performed correctly then proceeds
            if result is not None:
                response_time = result["response_time"]
                bandwidth = result["bandwidth"]
                encryption_overhead = result["encryption_overhead"]
                response_json = result["response_json"]
                # Save results
                save_test_results(conn, selected_protocol, response_time, bandwidth, encryption_overhead)
                
                # Display information
                st.markdown(f"## 🎉 The protocol {selected_protocol} was tested successfully!\n\n"
                        "During this time the program sent a request to the server A in order to begin with the cryptographic operations. Afterwards it sent the correct petition to the endpoint of server B "
                        "and the server processed the request back after running through all the needed steps for the selected procedure.")
                
                st.markdown(f"### ⏳ Response Time: {response_time:.3f} seconds")
                st.markdown(f"### 📶 Bandwidth Usage: {bandwidth:.2f} Mbps")
                if encryption_overhead is not None:
                    st.markdown(f"### 🔐 Encryption Overhead: {encryption_overhead} bytes")
                                               
                # Retrieve the explanation template from protocols table
                explanation_template = protocol_details_df['protocol_explanation'].iloc[0]
                explanation = explanation_template.format(**response_json)
                formatted_explanation = f'<div style="max-width:800px; margin: 0 auto; text-align:left;">{explanation}</div>'
                st.markdown(formatted_explanation, unsafe_allow_html=True)
                st.write("The lower the response time, the better the performance of the protocol. 🚀\n"
                        "For more information, check the interactive charts on the 'Compare Protocols' tab. 📈\n\nTchau! 👋🏽")
            else:
                st.error("Test did not complete successfully.")
        else:
            st.error("Protocol details not found.")