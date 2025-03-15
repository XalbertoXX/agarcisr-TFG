import streamlit as st
from utils.database import get_connection, get_protocols, get_protocol_details
from tabs.overview import show_overview
from tabs.test_protocols import show_test_protocols
from tabs.compare_protocols import show_compare_protocols
from tabs.ask_ai import show_ai

# Title
st.set_page_config(page_title="Protocol Performance Test", page_icon="🚀")

# Connection management
conn = get_connection()

# Retrieval of all protocols from the protocols table
protocols_df = get_protocols(conn)

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
with st.sidebar:
    st.markdown("# PROTOCOLS LIST 🔭")
    selected_protocol = st.sidebar.selectbox("Select Protocol", protocol_list)

    # Obtain the details for the selected protocol
    protocol_details_df = get_protocol_details(conn, selected_protocol)

    st.title("Protocol Details 🧐")
    if not protocol_details_df.empty:
        st.sidebar.info(protocol_details_df['description'].iloc[0])
        st.sidebar.write(protocol_details_df['description_long'].iloc[0])
    else:
        st.sidebar.warning("No protocol has been found :/ 404")

    st.sidebar.markdown("---") 
    # AI Chat Widget
    show_ai()  

# Tabs
tab1, tab2, tab3 = st.tabs(["Overview", "Test Protocols", "Compare Protocols"])

# Tab 1: Overview
with tab1:
    show_overview()

# Tab 2: Test Protocols
with tab2:
    show_test_protocols(conn, selected_protocol, protocol_details_df)

# Tab 3: Compare Protocols
with tab3:
    show_compare_protocols(conn, protocol_list)