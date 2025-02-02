import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.set_page_config(
    page_title="US Population Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.write("### Dynamic Update and Distribution of Up-to-date Data on Dashboard")
st.markdown("---")

# Tabs
tabs = st.tabs(["Home", "Data dan Analisis", "Referensi"])

# Load data
df_reshaped = pd.read_csv('USinData.csv')

# Clean and preprocess data
df_reshaped['Population'] = df_reshaped['Population'].str.replace(",", "").astype(float)

# Sidebar
with st.sidebar:
    st.title('US Data')

    year_list = sorted(df_reshaped.Year.unique(), reverse=True)
    states_list = sorted(df_reshaped['States'].unique())
    columns_list = ['Population', 'GDP', 'Unemployment', 'Poverty']

    selected_years = st.multiselect('Select years', year_list, default=year_list[:1])
    selected_states = st.multiselect('Select states', states_list, default=states_list[:1])
    selected_column = st.selectbox('Select data to display', columns_list)

    df_filtered = df_reshaped[df_reshaped['Year'].isin(selected_years)]
    if selected_states:
        df_filtered = df_filtered[df_filtered['States'].isin(selected_states)]

    df_filtered_sorted = df_filtered.sort_values(by=selected_column, ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)

# Tab Home
with tabs[0]:
    st.title("Latar Belakang")
    st.write("""
        Data yang digunakan dalam analisis ini dipilih dengan tujuan memberikan wawasan yang mendalam tentang dinamika sosial-ekonomi 
        yang memengaruhi masyarakat Amerika Serikat. Empat aspek utama menjadi fokus dalam penelitian ini:

        1. *GDP (Gross Domestic Product)*: GDP adalah indikator yang digunakan untuk mengukur total nilai barang dan jasa 
        yang diproduksi oleh suatu negara dalam periode tertentu. Data ini mencerminkan kinerja ekonomi Amerika Serikat dan 
        memberikan wawasan tentang pertumbuhan atau penurunan ekonomi.

        2. *Population (Populasi)*: Data populasi memberikan gambaran jumlah penduduk yang dapat memengaruhi berbagai aspek sosial 
        dan ekonomi. Informasi ini berguna untuk memahami bagaimana distribusi penduduk di berbagai negara bagian memengaruhi 
        kebutuhan layanan publik, pasar tenaga kerja, dan perkembangan ekonomi lokal.

        3. *Poverty (Kemiskinan)*: Tingkat kemiskinan menjadi indikator penting dalam menilai kesejahteraan masyarakat. Data ini 
        memberikan gambaran proporsi penduduk yang hidup di bawah garis kemiskinan, yang secara langsung berkaitan dengan akses 
        terhadap pendidikan, layanan kesehatan, dan peluang ekonomi.

        4. *Unemployment (Pengangguran)*: Tingkat pengangguran adalah parameter utama untuk mengukur kesehatan pasar tenaga kerja. 
        Data ini memberikan wawasan tentang peluang kerja di berbagai negara bagian dan bagaimana kondisi ekonomi lokal dapat 
        memengaruhi stabilitas sosial.

        Dengan menganalisis data ini, kami berharap dapat mengidentifikasi pola-pola utama dan memberikan rekomendasi yang relevan 
        untuk pengambil kebijakan atau pihak yang berkepentingan.
    """)

# Tab Data dan Analisis
with tabs[1]:
    st.markdown("# Data dan Analisis")
    
    # Choropleth Map - Peta Besar sebagai Spotlight
    st.subheader("Visualisasi Peta")
    choropleth = px.choropleth(
        df_filtered,
        locations="States Code",
        color=selected_column,
        locationmode="USA-states",
        color_continuous_scale=selected_color_theme,
        scope="usa",
        labels={selected_column: selected_column}
    )
    choropleth.update_layout(
        title=f"Distribusi {selected_column} di ({', '.join(map(str, selected_states))}) pada tahun ({', '.join(map(str, selected_years))})",
        template='plotly_dark',
        height=600,  # Membuat peta lebih besar
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(choropleth, use_container_width=True)

    # Heatmap
    st.subheader("Visualisasi Heatmap")
    heatmap = alt.Chart(df_reshaped).mark_rect().encode(
        y=alt.Y('Year:O', axis=alt.Axis(title="Tahun", labelFontSize=14, titleFontSize=16)),
        x=alt.X('States:O', axis=alt.Axis(title="Negara Bagian", labelFontSize=14, titleFontSize=16)),
        color=alt.Color(f'mean({selected_column}):Q', scale=alt.Scale(scheme=selected_color_theme)),
        tooltip=['Year', 'States', alt.Tooltip(f'mean({selected_column}):Q', title='Rata-rata')],
    ).properties(
        width=800,
        height=400
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16
    )
    st.altair_chart(heatmap, use_container_width=True)

    # Perbandingan Bar Chart
    st.subheader("Perbandingan Antar Negara Bagian")
    bar_chart = alt.Chart(df_filtered_sorted).mark_bar().encode(
        x=alt.X('States:N', sort='-y', axis=alt.Axis(title="Negara Bagian", labelFontSize=14, titleFontSize=16)),
        y=alt.Y(selected_column, axis=alt.Axis(title=f"{selected_column}", labelFontSize=14, titleFontSize=16)),
        color=alt.Color(selected_column, scale=alt.Scale(scheme=selected_color_theme), legend=None),
        tooltip=['States', selected_column],
    ).properties(
        width=800,
        height=400
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16
    )
    st.altair_chart(bar_chart, use_container_width=True)

        # Line Chart
    st.subheader("Tren Data Antar Tahun")
    line_chart = alt.Chart(df_filtered).mark_line(point=True).encode(
        x=alt.X('Year:O', axis=alt.Axis(title="Tahun", labelFontSize=14, titleFontSize=16)),
        y=alt.Y(selected_column, axis=alt.Axis(title=f"{selected_column}", labelFontSize=14, titleFontSize=16)),
        color=alt.Color('States:N', legend=alt.Legend(title="Negara Bagian")),
        tooltip=['Year', 'States', selected_column],
    ).properties(
        width=800,
        height=400
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16
    )
    st.altair_chart(line_chart, use_container_width=True)
    
    # Analisis Sederhana
    st.subheader("Analisis Data")
    if not df_filtered.empty:
        avg_value = df_filtered[selected_column].mean()
        max_value = df_filtered[selected_column].max()
        max_state = df_filtered[df_filtered[selected_column] == max_value]['States'].values[0]
        min_value = df_filtered[selected_column].min()
        min_state = df_filtered[df_filtered[selected_column] == min_value]['States'].values[0]
        std_dev = df_filtered[selected_column].std()

        st.markdown(f"""
            Berdasarkan analisis, rata-rata {selected_column} untuk tahun {', '.join(map(str, selected_years))} menunjukkan nilai rata-rata sebesar {avg_value:,.2f}, 
            yang mencerminkan kondisi umum di negara bagian tersebut. <br>
            
            Nilai tertinggi dicapai oleh negara bagian {max_state} dengan angka sebesar {max_value:,.2f}, 
            menunjukkan kondisi yang lebih unggul dibandingkan negara bagian lainnya. Sebaliknya, nilai terendah dicatat oleh 
            negara bagian {min_state} dengan angka sebesar {min_value:,.2f}, menunjukkan tantangan dalam indikator ini. <br>
            
            Tingkat variasi antar negara bagian dapat dilihat dari deviasi standar sebesar {std_dev:,.2f}, 
            yang menggambarkan seberapa besar perbedaan nilai dari rata-rata di negara bagian tersebut.
        """, unsafe_allow_html=True)
    else:
        st.write("Data tidak tersedia untuk tahun atau negara bagian yang dipilih.")

    # Tombol Unduh Data
    st.subheader("Unduh Data")
    csv_data = df_filtered.to_csv(index=False)
    st.download_button(
        label="Download Data sebagai CSV",
        data=csv_data,
        file_name="filtered_data.csv",
        mime="text/csv"
    )

# Tab Referensi
with tabs[2]:
    st.title("Referensi")
    st.write("""
        Data yang digunakan dalam analisis ini diperoleh dari sumber-sumber berikut:
        
        - *Bureau of Economic Analysis of the United States*
        - *Bureau of Labor Statistics of the United States*
        - *U.S. Census Bureau, Current Population Survey, 1960 to 2024 Annual Social and Economic Supplements (CPS ASEC)*
    """)
    
    st.caption("""
       
        
        This application is built by :
        - *Dwi Artiaty Nasution*
        - *Fatimatuzzahro*
        - *Ilham Wahyu Firmansyah*
        - *Muhammad Ricky Arzaaq*
    """)