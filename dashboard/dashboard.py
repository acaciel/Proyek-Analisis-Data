import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.ticker as ticker

# Set style seaborn
sns.set(style='whitegrid')

# Menyiapkan weather_rent_df
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather_situation').agg({
        'count': 'sum'
    })
    return weather_rent_df
    
# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# Menyiapkan workingday_rent_df
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

# Menyiapkan holiday_rent_df
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

# Load cleaned data
day_df = pd.read_csv("dashboard\day_data.csv")

# Membuat komponen filter
min_date = day_df['date'].min()
max_date = day_df['date'].max()
 
with st.sidebar:
    st.image(r"C:\Users\aniss\OneDrive\Dokumen\SMT.6\Proyek Analisis Data Bike Sharing\dashboard\logo bike rental.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df['date'] >= str(start_date)) & 
                (day_df['date'] <= str(end_date))]

# Menyiapkan berbagai dataframe
weather_rent_df = create_weather_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)

# Membuat Dashboard 
st.header('Bike Rental Dashboard 🚲')

# Membuah jumlah penyewaan berdasarkan kondisi cuaca
st.subheader('Weatherly Rentals')
nude_palette = ["#F4E1D2", "#E6B8A2", "#D99B84", "#C2856D", "#A86A50"]

fig, ax = plt.subplots(figsize=(12, 6))

sns.barplot(x=weather_rent_df.index, y=weather_rent_df['count'], palette=nude_palette, ax=ax)

ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))

for index, row in enumerate(weather_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=12)
st.pyplot(fig)

# Season Rentals
st.subheader('Seasonly Rentals')

# Menyiapkan total penyewaan per musim
season_rent_df['total'] = season_rent_df['registered'] + season_rent_df['casual']

fig, ax = plt.subplots(figsize=(12, 6))

sns.barplot(x='season', y='total', data=season_rent_df, palette=nude_palette, ax=ax)

ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))

# Menambahkan label angka di atas batang
for index, row in enumerate(season_rent_df['total']):
    ax.text(index, row + 5000, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=14)
ax.tick_params(axis='y', labelsize=12)
st.pyplot(fig)

# Membuat jumlah penyewaan berdasarkan weekday, working dan holiday
st.subheader('Weekday, Workingday, and Holiday Rentals')
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(14,12))

# Berdasarkan weekday
sns.barplot(x='weekday', y='count', data=weekday_rent_df, palette=nude_palette, ax=axes[0])

for index, row in enumerate(weekday_rent_df['count']):
    axes[0].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[0].set_title('Number of Rents based on Weekday')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=14)
axes[0].tick_params(axis='y', labelsize=12)

# Berdasarkan workingday
sns.barplot(x='workingday', y='count', data=workingday_rent_df, palette=nude_palette[:2], ax=axes[1])

for index, row in enumerate(workingday_rent_df['count']):
    axes[1].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[1].set_title('Number of Rents based on Working Day')
axes[1].set_ylabel(None)
axes[1].tick_params(axis='x', labelsize=14)
axes[1].tick_params(axis='y', labelsize=12)

# Berdasarkan holiday
sns.barplot(x='holiday', y='count', data=holiday_rent_df, palette=nude_palette[:2], ax=axes[2])

for index, row in enumerate(holiday_rent_df['count']):
    axes[2].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[2].set_title('Number of Rents based on Holiday')
axes[2].set_ylabel(None)
axes[2].tick_params(axis='x', labelsize=14)
axes[2].tick_params(axis='y', labelsize=12)

for ax in axes:
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))

plt.tight_layout()
st.pyplot(fig)
