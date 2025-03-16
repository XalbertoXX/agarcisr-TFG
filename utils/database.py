import streamlit as st
from st_supabase_connection import SupabaseConnection
import pandas as pd

# Supobase connection
def get_connection():
    if 'conn' not in st.session_state:
        st.session_state.conn = st.connection("supabase", type=SupabaseConnection)
    return st.session_state.conn

# Obtain protocol data
def get_protocols(conn):
    protocols_result = conn.table("protocols").select("*").execute()
    return pd.DataFrame(protocols_result.data) if protocols_result.data else pd.DataFrame()

# Obtain protocol details
def get_protocol_details(conn, protocol_name):
    protocol_details_res = conn.table("protocols").select("*").eq("name", protocol_name).execute()
    return pd.DataFrame(protocol_details_res.data) if protocol_details_res.data else pd.DataFrame()

# Save test results of test conducted into DB
def save_test_results(conn, protocol_name, time_seconds, bandwidth, encryption_overhead):
    res = conn.table("protocols").select("endpoint").eq("name", protocol_name).execute()
    if res.data and len(res.data) > 0:
        endpoint_value = res.data[0]['endpoint']
        insert_res = conn.table("protocol_performance").insert({
            "protocol_name": endpoint_value,
            "time_seconds": time_seconds,
            "bandwidth": bandwidth,
            "encryption_overhead": encryption_overhead
        }).execute()
        insert_res_dict = insert_res.model_dump()
        if insert_res_dict.get("error"):
            st.error(f"Error saving test results: {insert_res_dict['error'].message}")
        else:
            st.success("Test results saved successfully.")
    else:
        st.error("Protocol endpoint not found.")

# Load test results from DB
def load_test_results(conn, protocol_name):
    res = conn.table("protocols").select("endpoint").eq("name", protocol_name).execute()
    if res.data and len(res.data) > 0:
        endpoint_value = res.data[0]['endpoint']
        results = conn.table("protocol_performance") \
                     .select("time_seconds", "bandwidth", "encryption_overhead") \
                     .eq("protocol_name", endpoint_value) \
                     .order("created_at") \
                     .execute()
        return results.data if results.data else []
    else:
        st.error("Protocol endpoint not found for loading test results.")
        return []