import streamlit as st
import pandas as pd
import plotly.express as px
import wbdata
from datetime import datetime
import geopandas as gpd
import pydeck as pdk
import openai


# ricky 

# Streamlit setup
st.title("World Bank Data Viewer")

st.write("# Tugas Kelompok Dududada")

st.write("## Pendahuluan")
st.write("Tuliskan di bagian ini latar belakang data apa yang dipilih, mengapa kelompok memilih data ini, dsb.")

st.write("## Deskripsi Data")
st.write("Tuliskan di bagian ini deskripsi tentang data yang digunakan.")

st.write("## Visualisasi")
st.write("Buat visualisasi yang menurut kelompok kalian perlu ditampilkan.")
st.write("Gunakan juga elemen-elemen interaktif `streamlit`.")

st.markdown("Menampilkan data PDB (GDP) dari World Bank API menggunakan Streamlit.")

# Input dari pengguna untuk negara dan rentang tahun
countries = st.multiselect(
    "Pilih negara (kode ISO-3):",
    options=["ID", "US", "CN", "JP", "DE"],  # Indonesia, US, China, Japan, Germany
    default=["ID", "US"]
)
start_year = st.slider("Pilih tahun mulai:", 2000, 2023, 2010)
end_year = st.slider("Pilih tahun akhir:", 2000, 2023, 2020)

# Validasi input
if start_year > end_year:
    st.error("Tahun mulai tidak boleh lebih besar dari tahun akhir.")
else:
    # Ambil data World Bank
    indicator = {'NY.GDP.MKTP.CD': 'GDP'}  # Indikator GDP dalam USD
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)

    try:
        # Ambil data dan filter berdasarkan waktu
        data = wbdata.get_dataframe(indicator, country=countries)
        data = data.reset_index()  # Konversi MultiIndex ke DataFrame biasa
        data['date'] = pd.to_datetime(data['date'])
        data_filtered = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

        # Tampilkan data di Streamlit
        st.subheader("Hasil Data")
        if not data_filtered.empty:
            st.dataframe(data_filtered)
            st.write(f"Data mencakup dari {start_year} hingga {end_year}.")
        else:
            st.warning("Tidak ada data yang ditemukan untuk rentang waktu ini.")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")



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


