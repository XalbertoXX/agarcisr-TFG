import streamlit as st
import pandas as pd
import plotly.express as px
import requests, time
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
def test_protocol(endpoint, user_message):
    simulate = False
    response_time = None
    try:
        start_time = time.time()
        if endpoint == 'rsa' and user_message:
            response = requests.post(f'http://localhost:5000/{endpoint}', json={'message': user_message})
        else:
            response = requests.get(f'http://localhost:5000/{endpoint}')
        end_time = time.time()
        response_time = end_time - start_time
        st.write(response.json())
        if response.status_code == 200 and response.json().get('success', True):
            if not simulate:
                # Save response data
                save_test_results(selected_protocol, response_time)
                return response_time
        else:
            if not simulate:
                st.error(f"Failed to test {endpoint}: Server responded with status code {response.status_code}")
                return None
    except requests.RequestException as e:
        if not simulate:
            st.error(f"Failed to test {endpoint}: {e}")
            return None

df = conn.query('SELECT * FROM protocols;', ttl="10m")

# Frontend main title, sidebar and tabs definition
protocol_list = df['name'].tolist()

# Sidebar
st.sidebar.title("PROTOCOL LIST 🌌")
selected_protocol = st.sidebar.selectbox("Select Protocol", list(protocol_list))

# Query to get the protocol data of the selected protocol
df1 = conn.query(f""" SELECT * FROM protocols WHERE name = '{selected_protocol}';""", ttl="10m")

# Protocol Description
st.sidebar.info(df1['description'].iloc[0])

# Sidebar for Protocol Information
with st.sidebar:
    st.title("Protocol Details 🧐")
    st.write(df1['description_long'].iloc[0])

# Tabs
tab1, tab2 = st.tabs(["Test Protocols", "Compare Protocols"])

# Tab 1: Test Protocols
with tab1:
    user_message = ""
    if selected_protocol == 'RSA 📜':
        user_message = st.text_area("Enter a message for the fun... Hello, World? 🌍👀")

    if st.button(f'Test {selected_protocol}'):
        response_time = test_protocol(df1['endpoint'].iloc[0], user_message=user_message)

        if response_time is not None:
            st.success(f"Response Time: {response_time:.3f} seconds")

            st.write(f"The protocol {selected_protocol} was tested successfully! 🎉 \n\n"
                    "During this time the program was sending a request to the server,"
                    " and the server was processing the request sending a response back."
                    "The time it took for the server to respond is the response time.")
            
            st.write(f"The lower the response time, the better the performance of the protocol. 🚀\n"
                    "For more information, check the interactive chart on the 'Compare Protocols' tab. 📈 \n\nTchau! 👋🏽.")
            
# Tab 2: Compare Protocols
with tab2:
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
        st.write(f"{comparison_df.mean().idxmin()}, is the best protocol in terms of performance, with an average response time of {comparison_df.mean().min():.3f} seconds and a standard deviation of {comparison_df.std().min():.3f} seconds.")