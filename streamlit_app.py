import streamlit as st
import pandas as pd
import plotly.express as px
import requests, time
from st_supabase_connection import SupabaseConnection

# Title
st.set_page_config(page_title="Protocol Performance Test", page_icon="🚀")

# Connection management
if 'conn' not in st.session_state:
    st.session_state.conn = st.connection("supabase",type=SupabaseConnection)

conn = st.session_state.conn


# Save test results to the protocol_performance table
def save_test_results(protocol_name, time_seconds):
    # Get the protocol endpoint from the protocols table using the protocol name
    res = conn.table("protocols").select("endpoint").eq("name", protocol_name).execute()
    if res.data and len(res.data) > 0:
        endpoint_value = res.data[0]['endpoint']
        # Insert the test result into protocol_performance.
        insert_res = conn.table("protocol_performance").insert({
            "protocol_name": endpoint_value,
            "time_seconds": time_seconds
        }).execute()
        # Convert the Pydantic model to a dict using model_dump() (instead of dict())
        insert_res_dict = insert_res.model_dump()
        if insert_res_dict.get("error"):
            st.error(f"Error saving test results: {insert_res_dict['error'].message}")
        else:
            st.success("Test results saved successfully.")
    else:
        st.error("Protocol endpoint not found.")

# Load test results from protocol_performance
def load_test_results(protocol_name):
    # Get the endpoint for the protocol from the protocols table
    res = conn.table("protocols").select("endpoint").eq("name", protocol_name).execute()
    if res.data and len(res.data) > 0:
        endpoint_value = res.data[0]['endpoint']
        # Load the results from protocol_performance if they exist
        results = conn.table("protocol_performance") \
                      .select("time_seconds") \
                      .eq("protocol_name", endpoint_value) \
                      .order("created_at") \
                      .execute()
        if results.data:
            return [record["time_seconds"] for record in results.data]
        else:
            return []
    else:
        st.error("Protocol endpoint not found for loading test results.")
        return []
    
# Interactive chart generation
def plot_interactive_chart(data_frame):
    if not data_frame.empty:
        fig = px.line(data_frame, title="Protocol Performance Over Time 📈")
        fig.update_xaxes(title_text='Test Iterations')
        fig.update_yaxes(title_text='Response Time (seconds)', tickformat=".6f")
        st.plotly_chart(fig)
    else:
        st.write("Ooops...\n\nThere is no data available to plot, sorry 😢")
        
# Main function that handles the endpoint callouts for each protocol
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
                # Save the response data
                save_test_results(selected_protocol, response_time)
                return response_time, response_json
        else:
            if not simulate:
                st.error(f"Failed to test {endpoint}: Server responded with status code {response.status_code}")
                return None
    except requests.RequestException as e:
        if not simulate:
            st.error(f"Failed to test {endpoint}: {e}")
            return None

# Retrieve all protocols from the protocols table and convert to a DataFrame
protocols_result = conn.table("protocols").select("*").execute()
protocols_df = pd.DataFrame(protocols_result.data) if protocols_result.data else pd.DataFrame()

# Retrieval of complete protocol list
protocol_list = protocols_df['name'].tolist() if not protocols_df.empty else []

# Search functionality for different input boxes
st.text_input("Search Protocols 🔍", placeholder="Type name or description...", key="search_query")
search_query = st.session_state.get("search_query", "").strip()
if search_query and not protocols_df.empty:
    filtered_df = protocols_df[
        protocols_df['name'].str.contains(search_query, case=False, na=False) |
        protocols_df['description'].str.contains(search_query, case=False, na=False)
    ]
    protocol_list = filtered_df['name'].tolist() if not filtered_df.empty else []
else:
    filtered_df = protocols_df

# ---------------------------
# Sidebar: Protocol Selection & Details

st.sidebar.title("PROTOCOL LIST 🏃🏻‍♂️‍➡️")
selected_protocol = st.sidebar.selectbox("Select Protocol", protocol_list)

# Retrieve details for the selected protocol.
protocol_details_res = conn.table("protocols").select("*").eq("name", selected_protocol).execute()
protocol_details_df = pd.DataFrame(protocol_details_res.data) if protocol_details_res.data else pd.DataFrame()

with st.sidebar:
    st.title("Protocol Details 🧐")
    if not protocol_details_df.empty:
        st.sidebar.info(protocol_details_df['description'].iloc[0])
        st.sidebar.write("### Protocol Details")
        st.sidebar.write(protocol_details_df['description_long'].iloc[0])
    else:
        st.sidebar.warning("No protocol has been found :/ 404")

# Tabs
tab1, tab2, tab3 = st.tabs(["Overview", "Test Protocols", "Compare Protocols"])

# Tab 1: Overview
with tab1:
    st.title("Welcome to the Protocol Performance Testing App! 🚀")
    st.markdown("""
    ### Purpose
    This app allows users to test and compare the performance of various cryptographic protocols.  
    Cryptographic protocols are crucial for secure communication, especially in the age of quantum computing and cyber threats.
    These reasons are what inspire the creation of this website, as it is important to understand the performance characteristics 
    of these protocols to make informed decisions when implementing secure systems.

    ### Usage
    Here we will be testing some of the most popular protocols, and some of the most secure ones, to see how they perform in real time.
    - **Search for a Protocol**: Use the search bar on the right to quickly find protocols of interest by name or description.
    - **Test Protocols**: You can get in depth explanations of the protocols and test them by clicking the button below, where 
    you can also see the response time of the server alongside some other metrics.
    - **Compare Protocols**: Thanks to the usage of different visualizations, you can compare the performance of different protocols 
    in real time, and see which one is the best in terms of performance while also seeing the average response time and the standard deviation of each protocol.

    ### History of Protocols
    Cryptographic protocols have evolved significantly over time. At its core, protocols are sets of rules that govern the secure exchange of information.
    This allowerd the creation of secure communication channels, and the ability to encrypt and decrypt messages, ensuring the privacy and integrity of the data,
    evolving into the protocols we know today. These are able to secure not just the data, but also the communication channels, and the identities of the parties involved,
    ensuring the sessions that run daily communications, transactions, and more.
    
    To get a wider scope of the different resources we wanted to provide, here is a brief history of some of the most popular protocols:
    - **Good old days**: Diffie-Hellman and RSA were some of the first protocols to be developed, and are still widely used today, although they differ in the way they encrypt and decrypt messages
    and in the way they are used. While Diffie-Hellman is used to establish secure communication channels through key exchange by using prime numbers to generate the keys, RSA is used to encrypt and decrypt messages
    using the public and private keys of the parties involved. They were pioneers in the field of cryptography, and are still used today, although they are not as secure as they used to be. This gets us to the next point.
                
    - **Evolving to the future**: Elliptic Curve Cryptography (ECC) is a more modern protocol that is used to secure communication channels and encrypt messages, it is based on the mathematical properties of elliptic curves          
    and we have the perfect example to showcase this, the Elliptic Curve Diffie-Hellman (ECDH) protocol, which is used to establish secure communication channels through key exchange, and is considered to be more secure 
    than the traditional Diffie-Hellman protocol. This is because it uses smaller key sizes to achieve the same level of security, which makes it more efficient and faster while aiming for quantum resistance.
                
    - **Quantum Computing**: The advent of quantum computing has posed new challenges to traditional cryptographic systems. Quantum computers leverage quantum bits (qubits) to perform computations,
    which can solve certain problems much faster than classical computers can, setting a new paradigm in the way we understand security.
    This is why it is important to test and compare the performance of these protocols, as they are the ones that will be used in the future to secure the data and the communication channels
    and can showcase the viability of the current solutions we have in place.
    - Quantum computers can break widely-used protocols like RSA and Diffie-Hellman, due to their ability to factor large numbers efficiently.
    In order to fight this, alongside the usage of elliptic curve cryptography, there are other proposals such as lattice-based cryptography and learning with errors (LWE), and we chose two contenders to fend off the quantum threat:
    - **Cristal Kyber**: A lattice-based cryptography protocol that uses the hardness of the learning with errors (LWE) which revolves around the hardness of finding the error in a noisy system of equations to secure the data and the communication channels.
    - **NTRU**: A lattice-based cryptography protocol that uses the hardness of the shortest vector problem (SVP) to secure the data and the communication channels. This one differs from the previous one as it uses the 
    hardness of finding the shortest vector in a lattice to secure the data and the communication channels.
                

    ### Why This App?
    This application is designed to provide an intuitive way to test, compare and learn what are otherwise considered to be "opace" and complex algorithms that secure everyday technology.
    Mixing usability and complexity isn´t easy, but trying to get close to the user and having graphs and real time data can help to understand them a bit better 🤓!
    """)

# Tab 2: Test Protocols
with tab2:
    user_message = ""
    # For RSA, allow entering a message.
    if selected_protocol.lower().startswith('rsa'):
        user_message = st.text_area("Enter a message for the fun...", value="Hello, World!", placeholder="Hello, World!")
    if st.button(f'Test {selected_protocol}'):
        if not protocol_details_df.empty:
            endpoint = protocol_details_df['endpoint'].iloc[0]
            result = test_protocol(endpoint, user_message)
            if result is not None:
                response_time, response_json = result
                st.success(f"Response Time: {response_time:.3f} seconds")
                st.write(f"The protocol {selected_protocol} was tested successfully! 🎉\n\n"
                        "During this time the program sent a request to the server, "
                        "and the server processed the request and sent a response back. ")
                
                # Retrieve the explanation template from the protocols table.
                explanation_template = protocol_details_df['protocol_explanation'].iloc[0]
                explanation = explanation_template.format(**response_json)
                formatted_explanation = f'<div style="max-width:800px; margin: 0 auto; text-align:left;">{explanation}</div>'
                st.markdown(formatted_explanation, unsafe_allow_html=True)
                st.write("The lower the response time, the better the performance of the protocol. 🚀\n"
                "For more information, check the interactive chart on the 'Compare Protocols' tab. 📈\n\nTchau! 👋🏽")
            else:
                st.error("Test did not complete successfully.")
        else:
            st.error("Protocol details not found.")
            
# Tab 3: Compare Protocols
with tab3:
    comparison_protocols = st.multiselect("Select protocols to compare", protocol_list)
    if comparison_protocols:
        comparison_data = {protocol: pd.Series(load_test_results(protocol), dtype=float) for protocol in comparison_protocols}
        comparison_df = pd.DataFrame(comparison_data)
        plot_interactive_chart(comparison_df)
        st.write("The chart above shows the performance of the selected protocols over time. In general, the lower the response time, the better the performance of the protocol, but there are more thigns to take into consideration\n\n"
                 "The chart is interactive, so you can zoom in, zoom out, and hover over the data points to see the exact response time for each protocol. This is the main metric to determine the performance of the protocols, although not the only one as we will see scrolling down. \n ",
                 "It is also updated in real-time as new tests are performed, so you can keep an eye on the performance of the protocols as you test them 📊 while also seeing in real time which protocol is the best given the selected above, and while different. it could help visualice each of them in an easy and clicky way.")
        # Calculation of the average response time for each protocol, the desviations and the best protocol in therms of performance
        st.write("🔶The average response for each protocol is calculated as the sum of all response times divided by the number of tests performed:")
        st.write(comparison_df.mean())
        st.write("🔶The standard deviation for each protocol is a metric that indicates how much the response times vary from the average. Higher deviation values indicate more variability in the response times, which isn't ideal for establishing a protocol that might need to secure many sessions at the same time or encrypt large amounts of data:")
        st.write(comparison_df.std())
        st.write("🔶The best protocol in terms of performance is determined by the protocol with the lowest average response time in correlation with the lowest standard deviation:")
        avg_series = comparison_df.mean().dropna()
        std_series = comparison_df.std().dropna()
        if avg_series.empty:
            st.write("No valid data available to determine the best protocol.")
        else:
            best_protocol = avg_series.idxmin()
            best_avg = avg_series.loc[best_protocol]
            best_std = std_series.get(best_protocol, float('nan'))
            st.write(f"{best_protocol}, is the best protocol in terms of performance, with an average response time of {best_avg:.3f} seconds and a standard deviation of {best_std:.3f} seconds.")
