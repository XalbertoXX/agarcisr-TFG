import streamlit as st
from utils.database import get_connection, get_protocols, get_protocol_details
from utils.style_loader import load_css
from tabs.overview import show_overview
from tabs.test_protocols import show_test_protocols
from tabs.compare_protocols import show_compare_protocols
from tabs.ask_ai import show_ai
from tabs.questions import show_questions

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

# Sidebar: Protocol Selection & Details
with st.sidebar:
    load_css()

    st.markdown('<div class="protocol-header">PROTOCOLS LIST</div>', unsafe_allow_html=True)
    selected_protocol = st.sidebar.selectbox("Select your favorite 📍", protocol_list)

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
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Test Protocols", "Compare Protocols", "FAQs"])

# Tab 1 Main page overview
with tab1:
    show_overview(conn)

# Tab 2 Test protocols 
with tab2:
    show_test_protocols(conn, selected_protocol, protocol_details_df)

# Tab 3 Full comparison of protocols
with tab3:
    show_compare_protocols(conn, protocol_list)

# Tab 3 Frequently asked questions
with tab4:
    show_questions()
st.markdown('<div class="wrapper">', unsafe_allow_html=True)
# Footer
st.markdown(
    """<div class="footer">
        <p>Made with ❤️ by... Me?</p>
    </div>""",unsafe_allow_html=True,
)

st.markdown('</div>', unsafe_allow_html=True)