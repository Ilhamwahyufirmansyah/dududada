import streamlit as st
import pandas as pd
import plotly.express as px
import wbdata
from datetime import datetime
import geopandas as gpd
import pydeck as pdk
import openai

st.write("# Dududada")
st.write("### Dynamic Update and Distribution of up-to-date DAta on DAshboard ")

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
st.sidebar.header("Silakan Memilih Data")
selected_indicator = st.sidebar.selectbox("Pilih Indikator", list(indicators.keys()))

selected_countries = st.sidebar.multiselect("Pilih Negara", options=country_list.keys(), default=["Indonesia", "Malaysia", "Singapore"])

selected_years = st.sidebar.slider("Pilih Tahun", 2000, 2023, (2010, 2020))

# Tabs
tabs = st.tabs(["Home", "Data dan Analisis", "Referensi"])

# Tab Data dan Analisis
with tabs[1]:
    st.title("Menampilkan Data yang Anda Pilih")
    st.write(f"**Indikator yang Dipilih :** {selected_indicator}")
    st.write(f"**Negara yang Dipilih    :** {', '.join(selected_countries)}")
    st.write(f"**Periode Tahun          :** {selected_years[0]} - {selected_years[1]}")

    st.caption("Data yang anda pilih akan diambil dari World Bank Data kemudian ditampilkan dan dianalisis dibawah ini")

    st.write("## 2. Data")
    st.write("Anda dapat menampilkan data dalam tabel.")

    # Mengonversi nama negara menjadi kode negara
    selected_country_codes = [country_list[country] for country in selected_countries]

    # Fetch data
    if selected_country_codes:
        data = fetch_data(indicators[selected_indicator], selected_country_codes, selected_years[0], selected_years[1])
        if data is not None and not data.empty:
            show_dataframe = st.toggle("Tampilkan Tabel", value=True)

            if show_dataframe:
                st.write("### Tabel Data")
                st.dataframe(data)

                # Tambahkan tombol unduh data
                csv = data.to_csv(index=False)
                st.download_button(
                    label="Unduh Data sebagai CSV",
                    data=csv,
                    file_name="data.csv",
                    mime="text/csv"
                )

            st.write("## 3. Visualisasi")
            st.write("Anda dapat melihat visualisasi data yang anda pilih untuk lebih memahaminya")

            chart = data.pivot(index="Year", columns="Country", values="Value")

            show_line_chart = st.toggle("Tampilkan Line Chart", value=True)
            if show_line_chart:
                st.write("### Line Chart")
                st.line_chart(chart)

            show_bar_chart = st.toggle("Tampilkan Bar Chart", value=True)
            if show_bar_chart:
                st.write("### Bar Chart")
                st.bar_chart(chart)

            show_scatter_plot = st.toggle("Tampilkan Scatter Plot", value=False)
            if show_scatter_plot:
                st.write("### Scatter Plot")
                fig = px.scatter(data, x="Year", y="Value", color="Country", title="Scatter Plot")
                st.plotly_chart(fig)

#ilham
            st.write("### Deck.gl Map Visualization")
        
            show_map = st.toggle("Tampilkan Deck.gl Map", value=False)
            if show_map:
                # Contoh Data
                map_data = pd.DataFrame({
                    "lat": [37.7749, -23.5505, 28.6139, 39.9042, 55.7558, -25.2744],
                    "lon": [-122.4194, -46.6333, 77.2090, 116.4074, 37.6173, 133.7751],
                    "Country": ["United States", "Brazil", "India", "China", "Russia", "Australia"],
                    "Value": [10, 20, 30, 40, 50, 60]
                })

            # Konfigurasi Layer
            layer = pdk.Layer(
                "ScatterplotLayer",
                map_data,
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
            st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))            
            
            st.write("## 4. Analisis")
            st.write("Berikut ini analisis atas data yang anda pilih")

            # Menambahkan analisis statistik
            st.write("### Statistik Deskriptif")
            st.write(data.groupby("Country")["Value"].describe())

            # Analisis otomatis menggunakan API OpenAI versi terbaru
            st.write("### Analisis Otomatis")
            with st.spinner("Menghasilkan analisis..."):
                import openai

                # Menyiapkan prompt untuk analisis otomatis
                prompt = f"Buat analisis terhadap data berikut:\n\n{data.head(10).to_string()}\n\nTampilkan pola, tren, atau insight menarik dari data ini."

                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Anda adalah asisten analisis data yang ahli."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    analysis = response["choices"][0]["message"]["content"].strip()
                    st.write(analysis)
                except Exception as e:
                    st.error(f"Gagal menghasilkan analisis otomatis: {e}")

        else:
            st.warning("Data tidak ditemukan untuk pilihan ini.")
    else:
        st.warning("Silakan pilih setidaknya satu negara.")

    st.write("## 5. Kesimpulan")
    st.write("Kesimpulan dari analisis.")


# Tab Referensi
with tabs[2]:
    st.title("Referensi")
    st.caption("""
        Data yang digunakan dalam analisis ini diambil dari **World Bank** melalui library **wbdata**.
        Informasi lebih lanjut tentang data dapat ditemukan di: [https://data.worldbank.org](https://data.worldbank.org)
    """)
    
    st.write("Tuliskan di bagian ini referensi yang digunakan dalam proyek kelompok ini, misalnya sumber data, makalah ilmiah, dsb.")




# dwi
with tabs[0]:
    st.write("### Selamat Datang di Almanac!")
    st.write("Almanac merupakan halaman yang menyediakan data dan analisis ekonomi dari berbagai negara pada berbagai rentang tahun.",
        "Data tersebut meliputi beberapa indikator penting, seperti tingkat inflasi, kemiskinan, pengangguran, pertumbuhan ekonomi, dan jumlah populasi yang bersumber dari World Bank.")
    st.write("##### 1. Inflasi")
    st.write('Inflasi, yang diukur dengan Indeks Harga Konsumen (IHK), mencerminkan perubahan persentase tahunan dalam biaya yang dikeluarkan oleh konsumen untuk memperoleh barang dan jasa.')
    st.write("##### 2. Kemiskinan")
    st.write("Tingkat kemiskinan direpresentasikan oleh penduduk yang hidup dengan pengeluaran kurang dari $2,15 per hari yang dihitung berdasarkan harga yang disesuaikan dengan daya beli pada tahun 2017.",
    "Indikator ini menghitung jumlah penduduk miskin menurut standar internasional yang telah disesuaikan dengan perubahan harga dan nilai tukar antar negara pada tahun 2017.")
    st.write("##### 3. Pengangguran")
    st.write("Tingkat pengangguran merupakan persentase dari angkatan kerja yang tidak memiliki pekerjaan tetapi sedang dalam proses mencari pekerjaan.")
    st.write("##### 4. Pertumbuhan Ekonomi")
    st.write("Pertumbuhan ekonomi merupakan kenaikan produksi barang dan jasa di suatu negara dalam periode waktu tertentu yang diukur dengan perubahan Produk Domestik Bruto (PDB)")
    st.write("##### 5. Jumlah Populasi")
    st.write("Jumlah populasi suatu negara meruapakn jumlah individu yang tinggal di negara tersebut pada suatu waktu tertentu. Nilai jumlah populasi yang ditampilkan merupakan perkiraan pada pertengahan tahun")
    st.write("")
    st.write("Untuk melihat data-data tersebut, pilih filter data di Sidebar dan buka tab Data dan Analisis.")









# fatim






