import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 🌟 Customizing Dashboard Title
st.set_page_config(page_title="Smart Energy Dashboard", layout="wide")

# 🎯 Title & Description
st.title("⚡ Smart Energy Consumption Dashboard")
st.markdown("""
Welcome to the *Electricity Usage Analysis Dashboard*!  
📌 Upload your *electricity usage data* and gain insights into your energy consumption.  
📌 Discover *trends, peak hours, and ways to optimize your energy usage*.  
""")

# 📂 File Upload Section
st.sidebar.header("📂 Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Upload Electricity Usage CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ✅ Convert Date Column
    df['DATE'] = pd.to_datetime(df['DATE'], format='mixed', dayfirst=True, errors='coerce')

    # ✅ Handle missing values
    df.ffill(inplace=True)

    # ✅ Create DateTime Index
    df['DateTime'] = df['DATE'].astype(str) + ' ' + df['START TIME']
    df['DateTime'] = pd.to_datetime(df['DateTime'], errors='coerce')
    df.set_index('DateTime', inplace=True)

    # ✅ Drop unnecessary columns
    df.drop(columns=['DATE', 'START TIME', 'END TIME', 'UNITS', 'NOTES'], inplace=True)

    # 📅 Sidebar Date Filters
    st.sidebar.header("📅 Filter Data")
    start_date = st.sidebar.date_input("Start Date", df.index.min().date())
    end_date = st.sidebar.date_input("End Date", df.index.max().date())

    df_filtered = df.loc[start_date:end_date]

    # 🔹 Create Two Columns
    col1, col2 = st.columns(2)

    # 📊 Daily Electricity Usage Trend
    with col1:
        st.subheader("📈 Daily Electricity Usage")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df_filtered.index, df_filtered['USAGE'], color='blue', linewidth=2)
        ax.set_xlabel("Date")
        ax.set_ylabel("Electricity Usage (kWh)")
        ax.set_title("📊 Daily Electricity Usage Over Time")
        ax.grid(True)
        st.pyplot(fig)

    # 📊 Weekday vs. Weekend Comparison
    with col2:
        st.subheader("📊 Weekday vs. Weekend Consumption")
        df_filtered['Day_of_Week'] = df_filtered.index.dayofweek
        df_filtered['Weekend'] = df_filtered['Day_of_Week'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')

        fig2, ax2 = plt.subplots(figsize=(7, 5))
        sns.boxplot(x='Weekend', y='USAGE', data=df_filtered, ax=ax2)
        ax2.set_xlabel("Day Type")
        ax2.set_ylabel("Electricity Usage (kWh)")
        ax2.set_title("📊 Weekday vs. Weekend Energy Consumption")
        st.pyplot(fig2)

    # 📉 Monthly Trend Analysis
    st.subheader("📆 Monthly Electricity Usage Trends")
    df_filtered['Month'] = df_filtered.index.month
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.boxplot(x='Month', y='USAGE', data=df_filtered, ax=ax3, palette="coolwarm")
    ax3.set_xlabel("Month")
    ax3.set_ylabel("Electricity Usage (kWh)")
    ax3.set_title("📆 Electricity Usage Across Different Months")
    ax3.grid(True)
    st.pyplot(fig3)

    # 📊 Peak Usage Hours
    st.subheader("⏳ Peak Usage Hours")
    df_filtered['Hour'] = df_filtered.index.hour
    peak_hours = df_filtered.groupby('Hour')['USAGE'].mean().reset_index()

    fig4, ax4 = plt.subplots(figsize=(8, 4))
    sns.barplot(x='Hour', y='USAGE', data=peak_hours, ax=ax4, palette="magma")
    ax4.set_xlabel("Hour of the Day")
    ax4.set_ylabel("Average Usage (kWh)")
    ax4.set_title("⏳ Peak Energy Consumption Hours")
    st.pyplot(fig4)

    # ✅ Download Cleaned Dataset
    st.subheader("💾 Download Cleaned Dataset")
    csv = df_filtered.to_csv(index=True).encode('utf-8')
    st.download_button("Download CSV", data=csv, file_name="cleaned_electricity_usage.csv", mime="text/csv")

else:
    st.warning("⚠ Please upload a CSV file to analyze!")