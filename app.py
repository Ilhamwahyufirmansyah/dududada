import streamlit as st
import pandas as pd
import plotly.express as px
import wbdata
from datetime import datetime
import geopandas as gpd
import pydeck as pdk
import openai

st.write("# Dududada")

# ricky 

# Daftar manual negara dan kode ISO 3
country_list = {
    "Indonesia": "ID",
    "Malaysia": "MY",
    "Singapore": "SG",
    "Thailand": "TH",
    "Philippines": "PH",
    "Vietnam": "VN",
    "Brunei Darussalam": "BN",
    "Cambodia": "KH",
    "Lao PDR": "LA",
    "Myanmar": "MM",
}

# Fungsi untuk menarik data dari wbdata
def fetch_data(indicator, countries, start_year, end_year):
    # Mengambil data untuk rentang tahun tertentu
    data = wbdata.get_dataframe({indicator: 'value'}, country=countries)
    
    # Memfilter berdasarkan tahun
    data.reset_index(inplace=True)
    data['Year'] = data['date'].apply(lambda x: int(x[:4]))  # Mengambil tahun dari string tanggal
    data = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]
    data.rename(columns={'value': 'Value', 'country': 'Country'}, inplace=True)
    data = data[['Year', 'Country', 'Value']]
    
    return data

# Daftar indikator dan mapping ke kode wbdata
indicators = {
    "Inflasi": "FP.CPI.TOTL.ZG",
    "Kemiskinan": "SI.POV.DDAY",
    "Pengangguran": "SL.UEM.TOTL.ZS",
    "Pertumbuhan ekonomi": "NY.GDP.MKTP.KD.ZG",
    "Jumlah populasi": "SP.POP.TOTL",
}

# Sidebar
st.sidebar.header("Pilihan Data")
selected_indicator = st.sidebar.selectbox("Pilih Indikator", list(indicators.keys()))

selected_countries = st.sidebar.multiselect("Pilih Negara", options=country_list.keys(), default=["Indonesia", "Malaysia", "Singapore"])

selected_years = st.sidebar.slider("Pilih Tahun", 2000, 2023, (2010, 2020))

# Tabs
tabs = st.tabs(["Home", "Data dan Analisis", "Referensi"])

# Tab Home
with tabs[0]:
    st.title("Home")
    st.write("""
        Halaman ini bertujuan untuk memberikan analisis data ekonomi dari berbagai negara. 
        Data diambil dari **World Bank** menggunakan library **wbdata**. 
        Anda dapat memilih indikator, negara, dan rentang tahun pada sidebar.
    """)

# Tab Data dan Analisis
with tabs[1]:
    st.title("Data dan Analisis")
    st.write(f"**Indikator yang Dipilih:** {selected_indicator}")
    st.write(f"**Negara yang Dipilih:** {', '.join(selected_countries)}")
    st.write(f"**Periode Tahun:** {selected_years[0]} - {selected_years[1]}")

    # Mengonversi nama negara menjadi kode negara
    selected_country_codes = [country_list[country] for country in selected_countries]

    # Fetch data
    if selected_country_codes:
        data = fetch_data(indicators[selected_indicator], selected_country_codes, selected_years[0], selected_years[1])
        if data is not None and not data.empty:
            st.write("### Tabel Data")
            st.dataframe(data)

            st.write("### Visualisasi Data")
            chart = data.pivot(index="Year", columns="Country", values="Value")
            st.line_chart(chart)
        else:
            st.warning("Data tidak ditemukan untuk pilihan ini.")
    else:
        st.warning("Silakan pilih setidaknya satu negara.")

# Tab Referensi
with tabs[2]:
    st.title("Referensi")
    st.write("""
        Data yang digunakan dalam analisis ini diambil dari **World Bank** melalui library **wbdata**.
        Informasi lebih lanjut tentang data dapat ditemukan di: [https://data.worldbank.org](https://data.worldbank.org)
    """)


# Streamlit setup

st.write("## Pendahuluan")
st.write("Tuliskan di bagian ini latar belakang data apa yang dipilih, mengapa kelompok memilih data ini, dsb.")

st.write("## Deskripsi Data")
st.write("Tuliskan di bagian ini deskripsi tentang data yang digunakan.")

st.write("## Visualisasi")
st.write("Buat visualisasi yang menurut kelompok kalian perlu ditampilkan.")
st.write("Gunakan juga elemen-elemen interaktif `streamlit`.")



# ilham 
# Contoh Data
data = pd.DataFrame({
    "lat": [37.7749, -23.5505, 28.6139, 39.9042, 55.7558, -25.2744],
    "lon": [-122.4194, -46.6333, 77.2090, 116.4074, 37.6173, 133.7751],
    "Country": ["United States", "Brazil", "India", "China", "Russia", "Australia"],
    "Value": [10, 20, 30, 40, 50, 60]
})

# Konfigurasi Layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data,
    get_position="[lon, lat]",
    get_fill_color="[Value * 10, 100, 200]",
    get_radius="Value * 10000",
    pickable=True
)

# Viewport Awal
view_state = pdk.ViewState(
    latitude=20,
    longitude=0,
    zoom=1,
    pitch=40,
)

# Tampilkan Map
st.title("🌍 Deck.gl Map Visualization")
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))




# dwi







# fatim

st.write("## Analisis")
st.write("Buat analisis sederhana dari visualisasi data yang muncul di bagian sebelumnya.")

st.write("## Kesimpulan")
st.write("Tuliskan butir-butir kesimpulan dari analisis.")

st.write("## Referensi / Daftar Pustaka")
st.write("Tuliskan di bagian ini referensi yang digunakan dalam proyek kelompok ini, misalnya sumber data, makalah ilmiah, dsb.")


