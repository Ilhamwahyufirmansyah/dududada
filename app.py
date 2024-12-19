import streamlit as st
import pandas as pd
import plotly.express as px
import wbdata
from datetime import datetime
import geopandas as gpd
import pydeck as pdk
import openai
import altair as alt


st.write("# Dududada")
st.write("### Dynamic Update and Distribution of up-to-date DAta on DAshboard ")

# ricky 
# Tabs
tabs = st.tabs(["Home", "Data dan Analisis", "Referensi"])

# Load data
df_reshaped = pd.read_csv('USinData.csv')

# Clean and preprocess data
df_reshaped['Population'] = df_reshaped['Population'].str.replace(",", "").astype(float)

# Sidebar
with st.sidebar:
    st.title('US in Data')

    year_list = sorted(df_reshaped.Year.unique(), reverse=True)
    states_list = sorted(df_reshaped['States'].unique())
    columns_list = ['Population', 'GDP', 'Unemployment', 'Poverty']

    selected_year = st.selectbox('Select a year', year_list)
    selected_state = st.selectbox('Select a state', ['All'] + states_list)
    selected_column = st.selectbox('Select data to display', columns_list)

    df_filtered = df_reshaped[df_reshaped['Year'] == selected_year]
    if selected_state != 'All':
        df_filtered = df_filtered[df_filtered['States'] == selected_state]

    df_filtered_sorted = df_filtered.sort_values(by=selected_column, ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
    

#ilham
# Tab data dan analisis
with tabs[1]:
    # Heatmap
    def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
        heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
        return heatmap
    # Choropleth map
    def make_choropleth(input_df, input_id, input_column, input_color_theme):
        choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
                               color_continuous_scale=input_color_theme,
                               range_color=(0, max(df_filtered[selected_column])),
                               scope="usa",
                               labels={selected_column: selected_column}
                              )
        choropleth.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=350
        )
        return choropleth

    #######################

    # Dashboard Main Panel
    col = st.columns((1.5, 4.5, 2), gap='medium')
    with col[0]:
            st.markdown('#### Gains/Losses')

    # Display metrics for the top and bottom states
    if not df_filtered_sorted.empty:
        first_state_name = df_filtered_sorted.iloc[0]['States']
        first_state_value = df_filtered_sorted.iloc[0][selected_column]
        last_state_name = df_filtered_sorted.iloc[-1]['States']
        last_state_value = df_filtered_sorted.iloc[-1][selected_column]

        st.metric(label=first_state_name, value=f"{first_state_value:,}")
        st.metric(label=last_state_name, value=f"{last_state_value:,}")
        
    with col[1]:
        st.markdown(f'#### Total {selected_column}')
        
        choropleth = make_choropleth(df_filtered, 'States Code', selected_column, selected_color_theme)
        st.plotly_chart(choropleth, use_container_width=True)
        
        heatmap = make_heatmap(df_reshaped, 'Year', 'States', selected_column, selected_color_theme)
        st.altair_chart(heatmap, use_container_width=True)

    with col[2]:
        st.markdown(f'#### Top States by {selected_column}')

        st.dataframe(df_filtered_sorted,
                 column_order=("States", selected_column),
                 hide_index=True)


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






