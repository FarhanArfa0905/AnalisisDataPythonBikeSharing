import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Memuat Data data yang diperlukan
all_df = pd.read_csv("dashboard/all_data.csv")
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

# Membuat Sidebar untuk pilihan rentang tanggal berapa yang diinginkan
with st.sidebar:
    min_date = all_df["dteday"].min()
    max_date = all_df["dteday"].max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Melakukan filter data berdasarkan rentang waktu yang dipilih
filtered_df = all_df[(all_df['dteday'] >= pd.to_datetime(start_date)) & (all_df['dteday'] <= pd.to_datetime(end_date))]

#Membuat Dataframe untuk dianalisis
def create_rentals_per_season_df(df):
    rentals_per_season = df.groupby('season').agg({'cnt': 'sum', 'casual': 'sum', 'registered': 'sum'}).reset_index()
    return rentals_per_season

def create_rentals_by_workingday_df(df):
    rentals_by_workingday = df.groupby('workingday').agg({'cnt': 'sum', 'casual': 'sum', 'registered': 'sum'}).reset_index()
    return rentals_by_workingday

def create_holiday_non_holiday_df(df):
    holiday_non_holiday = df.groupby('holiday').agg({'cnt': 'sum', 'casual': 'sum', 'registered': 'sum'}).reset_index()
    return holiday_non_holiday

def create_performance_per_year_df(df):
    performance_per_year = df.groupby('yr').agg({'cnt': 'sum', 'casual': 'sum', 'registered': 'sum'}).reset_index()
    return performance_per_year

# Buat DataFrames
rentals_per_season = create_rentals_per_season_df(filtered_df)
rentals_by_workingday = create_rentals_by_workingday_df(filtered_df)
holiday_non_holiday = create_holiday_non_holiday_df(filtered_df)
performance_per_year = create_performance_per_year_df(filtered_df)

# Main Dashboard
st.header('Bike Sharing Dashboard')
st.write("In this Dashboard we show history about number of rentals.")

# Hubungan Musim dengan Jumlah Pengguna Sepeda
st.subheader('Relationship between Season and Number of Rent Bcycle')

# Atur urutan musim sebagai kategori
season_order = ['springer', 'summer', 'fall', 'winter']
rentals_per_season['season'] = pd.Categorical(rentals_per_season['season'], categories=season_order, ordered=True)

# memisahkan casual, registered, dan total
rentals_per_season_melted = rentals_per_season.melt(id_vars='season', value_vars=['cnt', 'registered', 'casual'], var_name='User Type', value_name='Count')

# Mengatur urutan manual untuk User Type (cnt, registered, casual)
user_type_order = ['cnt', 'registered', 'casual']
rentals_per_season_melted['User Type'] = pd.Categorical(rentals_per_season_melted['User Type'], categories=user_type_order, ordered=True)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='season', y='Count', hue='User Type', data=rentals_per_season_melted, ax=ax)
plt.title("Number of Rent Bcycle per Season", loc="center", fontsize=15)
plt.ylabel("Number of Rent")
plt.xlabel("Season")
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
plt.xticks(rotation=45)
plt.legend(title='User Type')
st.pyplot(fig)

# Hubungan Jumlah Penyewa Sepeda pada Saat Holiday dan Weekend dengan Hari Kerja Buat Sub Judul
st.subheader('Relationship between the number of bicycle renters during holidays and weekends with weekdays')

#memisahkan casual, registered, dan cnt
rentals_by_workingday_melted = rentals_by_workingday.melt(id_vars='workingday', value_vars=['cnt', 'registered', 'casual'], var_name='User Type', value_name='Count')

# Mengatur urutan manual untuk User Type (cnt, registered, casual)
rentals_by_workingday_melted['User Type'] = pd.Categorical(rentals_by_workingday_melted['User Type'], categories=user_type_order, ordered=True)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='workingday', y='Count', hue='User Type', data=rentals_by_workingday_melted, ax=ax)
plt.title("Number of Rent per Weekday or Weekend + Holiday", loc="center", fontsize=15)
plt.ylabel("Number of Rent")
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
st.pyplot(fig)

# Hubungan Holiday dengan Tidak Holiday Terhadap Jumlah Penyewa
st.subheader('The Relationship between Holidays and Non-Holidays on the Number of Rent')

# memisahkan casual, registered, dan cnt
holiday_non_holiday_melted = holiday_non_holiday.melt(id_vars='holiday', value_vars=['cnt', 'registered', 'casual'],var_name='User Type', value_name='Count')

# Mengatur urutan manual untuk User Type (cnt, registered, casual)
holiday_non_holiday_melted['User Type'] = pd.Categorical(holiday_non_holiday_melted['User Type'], categories=user_type_order, ordered=True)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='holiday', y='Count', hue='User Type', data=holiday_non_holiday_melted, ax=ax)
plt.title("Number of Rent per Holiday or not holiday", loc="center", fontsize=15)
plt.ylabel("Number of Rent")
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
st.pyplot(fig)

# Performa Bike Sharing dari Tahun ke Tahun
st.subheader('Bike Sharing Performance from Year to Year')

# Reshape untuk memisahkan casual, registered, dan cnt
performance_per_year_melted = performance_per_year.melt(id_vars='yr', value_vars=['cnt', 'registered', 'casual'], var_name='User Type', value_name='Count')

# Mengatur urutan manual untuk User Type (cnt, registered, casual)
performance_per_year_melted['User Type'] = pd.Categorical(performance_per_year_melted['User Type'], categories=user_type_order, ordered=True)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='yr', y='Count', hue='User Type', data=performance_per_year_melted, ax=ax)
plt.title("Bike Sharing Performance from Year 2011 and 2012", loc="center", fontsize=15)
plt.ylabel("Number of Rent")
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
st.pyplot(fig)

# Footer
st.write("Copyright @Arfahanz31")
