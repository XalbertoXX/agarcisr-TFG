import streamlit as st
from utils.database import load_test_results
from utils.plotting import plot_interactive_chart
import pandas as pd

# Protocol comparison tab
def show_compare_protocols(conn, protocol_list):
    comparison_protocols = st.multiselect("Select protocols to compare", protocol_list)
    if comparison_protocols:
        comparison_data = {protocol: pd.Series(load_test_results(conn, protocol), dtype=float) for protocol in comparison_protocols}
        comparison_df = pd.DataFrame(comparison_data)
        plot_interactive_chart(comparison_df)
        st.write("The chart above shows the performance of the selected protocols over time. In general, the lower the response time, the better the performance of the protocol, but there are more thigns to take into consideration\n\n"
                 "The chart is interactive, so you can zoom in, zoom out, and hover over the data points to see the exact response time for each protocol. This is the main metric to determine the performance of the protocols, although not the only one as we will see scrolling down. \n ",
                 "It is also updated in real-time as new tests are performed, so you can keep an eye on the performance of the protocols as you test them 📊 while also seeing in real time which protocol is the best given the selected above, and while different. It could help visualice each one of them in an easy and clicky way.")
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