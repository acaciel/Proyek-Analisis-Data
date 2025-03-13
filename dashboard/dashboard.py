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
    }).reset_index()

    weather_rent_df['count'] = weather_rent_df['count'].astype(int)
    return weather_rent_df
    
# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season').agg({
        'count': 'sum'
    })
    return season_rent_df

# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count':'sum'
    }).reset_index()
    return weekday_rent_df

# Menyiapkan workingday_rent_df
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    })
    return workingday_rent_df

# Menyiapkan holiday_rent_df
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    })
    return holiday_rent_df

# Load cleaned data
day_df = pd.read_csv("dashboard/day_data.csv")
day_df['date'] = pd.to_datetime(day_df['date'])


# Membuat komponen filter
min_date = day_df['date'].min()
max_date = day_df['date'].max()
 
with st.sidebar:
    st.image("dashboard/logo bike rental.png")

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

sns.barplot(x='weather_situation', y='count', data=weather_rent_df, palette=nude_palette, ax=ax)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=12)

ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax.get_yaxis().get_major_formatter().set_scientific(False)
st.pyplot(fig)

# Season Rentals
st.subheader('Seasonly Rentals')

# Menyiapkan total penyewaan per musim

fig, ax = plt.subplots(figsize=(12, 6))

sns.barplot(x='season', y='count', data=season_rent_df, palette=nude_palette, ax=ax)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=14)
ax.tick_params(axis='y', labelsize=12)

ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax.get_yaxis().get_major_formatter().set_scientific(False)
st.pyplot(fig)

# Membuat jumlah penyewaan berdasarkan weekday, working dan holiday
st.subheader('Weekday, Workingday, and Holiday Rentals')
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(14,12))

# Berdasarkan weekday
sns.barplot(x='weekday', y='count', data=weekday_rent_df, palette=nude_palette, ax=axes[0])

axes[0].set_title('Number of Rents based on Weekday')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=14)
axes[0].tick_params(axis='y', labelsize=12)

# Berdasarkan workingday
sns.barplot(x='workingday', y='count', data=workingday_rent_df, palette=nude_palette[:2], ax=axes[1])

axes[1].set_title('Number of Rents based on Working Day')
axes[1].set_ylabel(None)
axes[1].tick_params(axis='x', labelsize=14)
axes[1].tick_params(axis='y', labelsize=12)
axes[1].yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
axes[1].get_yaxis().get_major_formatter().set_scientific(False)

# Berdasarkan holiday
sns.barplot(x='holiday', y='count', data=holiday_rent_df, palette=nude_palette[:2], ax=axes[2])

axes[2].set_title('Number of Rents based on Holiday')
axes[2].set_ylabel(None)
axes[2].tick_params(axis='x', labelsize=14)
axes[2].tick_params(axis='y', labelsize=12)
axes[2].yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
axes[2].get_yaxis().get_major_formatter().set_scientific(False)

plt.tight_layout()
st.pyplot(fig)
