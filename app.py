import streamlit as st
import pandas as pd
<<<<<<< HEAD
import plotly.express as py

st.title("dududada")


=======
import plotly.express as px
import wbdata
from datetime import datetime
>>>>>>> 695a12010702dbc201b6471e088724e17da9713b


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





# dwi







# fatim

st.write("## Analisis")
st.write("Buat analisis sederhana dari visualisasi data yang muncul di bagian sebelumnya.")

st.write("## Kesimpulan")
st.write("Tuliskan butir-butir kesimpulan dari analisis.")

st.write("## Referensi / Daftar Pustaka")
st.write("Tuliskan di bagian ini referensi yang digunakan dalam proyek kelompok ini, misalnya sumber data, makalah ilmiah, dsb.")


