import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
day_df = pd.read_csv('dashboard/main_data.csv')

# Mengubah tipe data kolom dteday menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Menambahkan kolom season_text dan weather_condition
weather_labels = {1: 'Cerah', 2: 'Kabut', 3: 'Hujan Ringan', 4: 'Hujan Berat'}
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['weather_condition'] = day_df['weathersit'].map(weather_labels)
day_df['season_text'] = day_df['season'].map(season_mapping)

# Menambahkan kolom is_weekend
day_df['is_weekend'] = day_df['weekday'].apply(lambda x: True if x == 0 or x == 6 else False)

# Set up the Streamlit app layout
st.title('Analisis Data Bike Sharing Dataset')
st.sidebar.title('Navigasi')

# Sidebar untuk memilih pertanyaan
question = st.sidebar.selectbox('Pilih Pertanyaan:', [
    'Pengaruh Kombinasi Hari Kerja, Musim, dan Kondisi Cuaca',
    'Hubungan antara Temperatur, Kecepatan Angin, dan Kelembaban',
    'Pola Penyewaan pada Hari Kerja vs. Hari Libur'
])

# Fungsi untuk pertanyaan 1
if question == 'Pengaruh Kombinasi Hari Kerja, Musim, dan Kondisi Cuaca':
    st.header('Pengaruh Kombinasi Hari Kerja, Musim, dan Kondisi Cuaca terhadap Penyewaan Sepeda')
    
    # Visualisasi boxplot pengaruh musim
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='season_text', y='cnt', data=day_df)
    plt.title("Pengaruh Musim terhadap Total Rental Sepeda")
    st.pyplot(plt)

    # Visualisasi pengaruh musim dan akhir pekan
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='season_text', y='cnt', hue='is_weekend', data=day_df)
    plt.title("Pengaruh Musim dan Akhir Pekan terhadap Rental Sepeda")
    st.pyplot(plt)

    # Visualisasi tren bulanan
    day_df['year_month'] = day_df['dteday'].dt.to_period('M').astype(str)
    monthly_trend = day_df.groupby('year_month')['cnt'].mean().reset_index()
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='year_month', y='cnt', data=monthly_trend)
    plt.xticks(rotation=45)
    plt.title("Tren Penggunaan Sepeda per Bulan")
    plt.xlabel("Bulan")
    plt.ylabel("Rata-rata Penyewaan Sepeda")
    st.pyplot(plt)

# Fungsi untuk pertanyaan 2
elif question == 'Hubungan antara Temperatur, Kecepatan Angin, dan Kelembaban':
    st.header('Hubungan antara Temperatur, Kecepatan Angin, dan Kelembaban terhadap Penyewaan Sepeda')

    # Filter data hanya untuk hari kerja
    workingday_df = day_df[day_df['workingday'] == 1]

    # Visualisasi pairplot
    sns.pairplot(workingday_df, x_vars=['temp', 'windspeed', 'hum'], y_vars='cnt', height=4)
    plt.suptitle("Hubungan Temperatur, Kecepatan Angin, Kelembaban dengan Rental Sepeda pada Hari Kerja", y=1.02)
    st.pyplot(plt)

    # Visualisasi pengaruh cuaca terhadap pengguna kasual
    sns.lmplot(x='temp', y='casual', data=workingday_df, line_kws={'color': 'red'})
    plt.title("Pengaruh Temperatur terhadap Pengguna Kasual")
    st.pyplot(plt)

    # Visualisasi pengaruh cuaca terhadap pengguna terdaftar
    sns.lmplot(x='temp', y='registered', data=workingday_df, line_kws={'color': 'blue'})
    plt.title("Pengaruh Temperatur terhadap Pengguna Terdaftar")
    st.pyplot(plt)

# Fungsi untuk pertanyaan 3
elif question == 'Pola Penyewaan pada Hari Kerja vs. Hari Libur':
    st.header('Pola Penyewaan pada Hari Kerja vs. Hari Libur')

    # Mengelompokkan data berdasarkan 'is_weekend' dan 'holiday'
    grouped_data = day_df.groupby(['is_weekend', 'holiday']).agg({
        'casual': ['mean', 'sum'],
        'registered': ['mean', 'sum'],
        'cnt': ['mean', 'sum']
    }).reset_index()

    # Rename columns
    grouped_data.columns = ['Working Day', 'Holiday',
                             'Average Casual Rentals', 'Total Casual Rentals',
                             'Average Registered Rentals', 'Total Registered Rentals',
                             'Average Total Rentals', 'Total Rentals']

    # Membuat group untuk memudahkan plotting
    melted_data = grouped_data.melt(id_vars=['Working Day', 'Holiday'],
                                     value_vars=['Average Casual Rentals', 'Average Registered Rentals', 'Average Total Rentals'],
                                     var_name='Rental Type', value_name='Average Rentals')

    # Membuat plot chart
    plt.figure(figsize=(12, 6))
    sns.barplot(data=melted_data, x='Rental Type', y='Average Rentals', hue='Working Day', palette='viridis', ci=None)
    plt.title('Average Rentals on Working Days vs Holidays')
    plt.xlabel('Rental Type')
    plt.ylabel('Average Rentals')
    plt.xticks(rotation=45)
    st.pyplot(plt)
