import streamlit as st
from utils.database import load_test_results
from utils.plotting import plot_interactive_chart
import pandas as pd

# Protocol comparison tab
def show_compare_protocols(conn, protocol_list):
    comparison_protocols = st.multiselect("Select protocols to compare", protocol_list)
    if comparison_protocols:
        comparison_data = {
            protocol: {
                "response_times": [r["time_seconds"] for r in load_test_results(conn, protocol)],
                "bandwidth": [r["bandwidth"] for r in load_test_results(conn, protocol)],
                "encryption_overhead": [r["encryption_overhead"] for r in load_test_results(conn, protocol)]
            } for protocol in comparison_protocols
        }

        # Create DataFrames for each metric
        response_df = pd.DataFrame({
            protocol: pd.Series(data["response_times"]) for protocol, data in comparison_data.items()
        })
        bandwidth_df = pd.DataFrame({
            protocol: pd.Series(data["bandwidth"]) for protocol, data in comparison_data.items()
        })
        encryption_df = pd.DataFrame({
            protocol: pd.Series(data["encryption_overhead"]) for protocol, data in comparison_data.items()
        })

        # Response time chart
        st.write("# Performance Over Time 📈")
        plot_interactive_chart(response_df)
        st.write("The chart above shows the performance of the selected protocols over time. In general, the lower the response time, the better the performance of the protocol, but there are more thigns to take into consideration\n\n"
            "ℹ️ All charts are interactive, so zoom, hover, and click to explore data! Move over the data points to see the exact response time for each protocol. These are the main metrics to determine the performance of the protocols, although not the only ones as we will see. \n ",
            "It is also updated in real-time as new tests are performed, so you can keep an eye on the performance of the protocols as you test them 📊 while also seeing in real time which protocol is the best given the selected above, and while different. It could help visualice each one of them in an easy and clicky way.")
        
        # Average Response Time
        st.write("## Protocol Analysis 🔍")
        st.write("### Average Response Time")
        st.write("🔶 The average response for each protocol is calculated as the sum of all response times divided by the number of tests performed:")
        st.write(response_df.mean())

        # Standard Deviation
        st.write("### Standard Deviation")
        st.write("🔶 The standard deviation for each protocol is a metric that indicates how much the response times vary from the average."
        "Higher deviation values indicate more variability in the response times, which isn't ideal for establishing a protocol that might need to secure many sessions at the same time or encrypt large amounts of data:")
        st.write(response_df.std())

        # Bandwidth
        st.write("---")
        st.write("## Bandwidth Usage 📶")
        st.metric(label="Bandwidth measured in Mbps", value="Mbps")
        st.line_chart(bandwidth_df)
        st.write("Bandwidth indicates how much data is transferred per second. 🧳 Lower values are better for network efficiency, meaning that the protocol is not requiring that many resources from the actual servers, "
        "giving us a great insight on hown different mathematical implementations can make different approaches work in an environment like this. It showcases how far we have come if protocols created 40 years ago match security"
        "and speed with newer ones, and on the contrary, it can show how efficient, newer protocols that are able to withdstand the quantum threat, can be 😵")

        # Average Bandwidth Usage
        st.write("## Average Bandwidth Usage")
        avg_bandwidth = bandwidth_df.mean()
        st.write("🔶 The average bandwidth usage for each protocol is calculated as the sum of all bandwidth values divided by the number of tests performed:")
        st.write(avg_bandwidth)
        st.write("---")
        
        # Encryption Overhead
        if "RSA 📜" in comparison_protocols:
            
            st.write("## Encryption Overhead 🔐")

            # Filter encryption_df for RSA (ensure the name matches exactly)
            rsa_encryption_df = encryption_df[["RSA 📜"]].dropna()
            if not rsa_encryption_df.empty:

                # Calculate the average encryption overhead for RSA
                rsa_avg_overhead = rsa_encryption_df.mean().iloc[0]

                st.metric(label="Average Encryption Overhead for RSA protocol is", value=f"{rsa_avg_overhead:.2f} bytes")

                # Display the bar chart for RSA
                st.line_chart(rsa_encryption_df)
                st.write("Encryption overhead shows how much extra data is added by encryption. Lower values mean more efficient/shorter messages, where bigger values affect timing and deviatons which can be observed in the executions and timings."
                "That's why relying on plain numbers can be tricky 🔢 and incorrect, we need numbers and context to form our opinions.")
            else:
                st.write("No encryption overhead data available for RSA")
        else:
            st.write("⚠️ **To see metrics like encryption overhead, checkout the rsa protocol** Sorry 😓")

        st.write("---")    
        st.write("🔶The best protocol in terms of performance is determined by the protocol with the lowest average response time in correlation with the lowest standard deviation:")
        avg_series = response_df.mean().dropna()
        std_series = response_df.std().dropna()
        if avg_series.empty:
            st.write("No valid data available to determine the best protocol.")
        else:
            best_protocol = avg_series.idxmin()
            best_avg = avg_series.loc[best_protocol]
            best_std = std_series.get(best_protocol, float('nan'))
            st.write(f"**🏆 Best Protocol**: {best_protocol}, with an average response time of {best_avg:.3f} seconds and standard deviation of {best_std:.3f} seconds.")