import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
day_df = pd.read_csv('dashboard/main_data.csv')

# Data Cleaning
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Add columns for season names and day names
season_mapping = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}
day_df["season_name"] = day_df["season"].map(season_mapping)
day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
day_df['day_name'] = day_df['weekday'].apply(lambda x: day_names[x])
day_df['is_weekend'] = day_df['weekday'].isin([0, 6])

# Sidebar for questions
st.sidebar.title("Bike Sharing Data Analysis")
question = st.sidebar.selectbox("Choose a question to analyze:", 
                                ["Season-wise User Analysis", 
                                 "Weekend vs Weekday Analysis", 
                                 "Manual Grouping: Working Day vs Holiday"])

# Plot for Question 1: Season-wise User Analysis
if question == "Season-wise User Analysis":
    st.title("Season-wise Analysis of Bike Sharing Users")

    # Grouping data by season
    season_summary = day_df.groupby(by="season").agg({
        'casual': 'sum',
        'registered': 'sum'
    })
    season_summary['total_users'] = season_summary['casual'] + season_summary['registered']
    season_summary['season_name'] = season_summary.index.map(season_mapping)

    labels = season_summary['season_name']
    casual_users = season_summary['casual']
    registered_users = season_summary['registered']

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    bar1 = ax.bar(x - width/2, casual_users, width, label='Casual Users', color='green')
    bar2 = ax.bar(x + width/2, registered_users, width, label='Registered Users', color='orange')

    ax.set_xlabel('Season')
    ax.set_ylabel('Number of Users')
    ax.set_title('Number of Casual and Registered Users by Season')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    st.pyplot(fig)

    # Conclusion
    st.write("**Conclusion**: Musim yang paling banyak pengguna baik casual maupun registered terjadi pada musim gugur (fall) dan yang paling sedikit terjadi pada musim dingin (winter).")

# Plot for Question 2: Weekend vs Weekday Analysis
elif question == "Weekend vs Weekday Analysis":
    st.title("Weekend vs Weekday User Analysis")

    mean_values = day_df.groupby(by=["is_weekend", "weekday"]).agg({
        "casual": "mean",
        "registered": "mean",
        "cnt": "mean"
    }).reset_index()

    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.barplot(data=mean_values, x='weekday', y='casual', hue='is_weekend', palette='viridis', ax=ax1)
    ax1.set_title('Average Casual Users by Day of the Week and Weekend')
    ax1.set_xlabel('Day of the Week')
    ax1.set_ylabel('Average Casual Rentals')
    ax1.set_xticks(range(7))
    ax1.set_xticklabels(day_names)

    st.pyplot(fig1)

    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.barplot(data=mean_values, x='weekday', y='registered', hue='is_weekend', palette='viridis', ax=ax2)
    ax2.set_title('Average Registered Users by Day of the Week and Weekend')
    ax2.set_xlabel('Day of the Week')
    ax2.set_ylabel('Average Registered Rentals')
    ax2.set_xticks(range(7))
    ax2.set_xticklabels(day_names)

    st.pyplot(fig2)

    # Conclusion
    st.write("**Conclusion**: pada hari kerja, penyewaan cenderung lebih tinggi dibandingkan dengan hari libur. Pengguna terdaftar lebih mendominasi pada hari kerja, sedangkan pengguna kasual lebih aktif pada akhir pekan.")

# Manual Grouping: Working Day vs Holiday
elif question == "Manual Grouping: Working Day vs Holiday":
    st.title("Analysis of Working Days vs Holidays")

    grouped_data = day_df.groupby(['workingday', 'holiday']).agg({
        'casual': ['mean', 'sum'],       # Rata-rata dan total penyewaan kasual
        'registered': ['mean', 'sum'],   # Rata-rata dan total penyewaan terdaftar
        'cnt': ['mean', 'sum']           # Rata-rata dan total penyewaan keseluruhan
    }).reset_index()

    # Rename columns
    grouped_data.columns = ['Working Day', 'Holiday', 
                             'Average Casual Rentals', 'Total Casual Rentals', 
                             'Average Registered Rentals', 'Total Registered Rentals',
                             'Average Total Rentals', 'Total Rentals']

    st.dataframe(grouped_data)

    # Plot for average rentals on working days vs holidays
    melted_data = grouped_data.melt(id_vars=['Working Day', 'Holiday'], 
                                    value_vars=['Average Casual Rentals', 'Average Registered Rentals', 'Average Total Rentals'],
                                    var_name='Rental Type', value_name='Average Rentals')

    fig3, ax3 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=melted_data, x='Rental Type', y='Average Rentals', hue='Working Day', palette='viridis', ax=ax3)
    ax3.set_title('Average Rentals on Working Days vs Holidays')
    ax3.set_xlabel('Rental Type')
    ax3.set_ylabel('Average Rentals')
    ax3.set_xticks(range(3))
    ax3.set_xticklabels(['Casual', 'Registered', 'Total'], rotation=45)

    st.pyplot(fig3)

    # Conclusion
    st.write("**Conclusion**: pola penyewaan sepeda antara hari kerja dan hari libur sangat berbeda. Pada hari kerja, jumlah pengguna terdaftar cenderung lebih tinggi dibandingkan dengan pengguna kasual, sedangkan pada hari libur, jumlah pengguna kasual meningkat secara signifikan.")
