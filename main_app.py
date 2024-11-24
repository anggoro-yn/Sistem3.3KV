import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.title('Perbandingan Tegangan') 

options = ['21 Nov', '22 Nov', '23 Nov']
selected_option = st.selectbox('Pilih Tanggal', options)

if selected_option == '21 Nov':
    df_path = 'LP10_20241121.csv'
    df2_path = 'GI_20241121a.csv'
elif selected_option == '22 Nov':
    df_path = 'LP10_20241122.csv'
    df2_path = 'GI_20241122a.csv'
else:
    df_path = 'LP10_20241123.csv'
    df2_path = 'GI_20241123a.csv'    

# Membaca dataset 3.3KV
df = pd.read_csv(df_path, sep=';')
# Menggabungkan kolom 'Date' dan 'Time' menjadi satu kolom 'Datetime'
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d-%m-%y %I:%M:%S %p')
# Membuang kolom 'Date' dan 'Time' 
df = df.drop(columns=['Date', 'Time', 'Hz','V 12','V 23', 'V 31', 'V L1', 'V L2', 'V L3'])
# Membuang baris yang memiliki nilai datetime duplikat 
df = df.drop_duplicates(subset=['Datetime'], keep='first')
# Membuang baris yang memiliki nilai 'V 12' kurang dari 2.5 
df = df[df['V'] >= 2.5] #

# Membaca dataset GI
df2 = pd.read_csv(df2_path, sep = ";")
# Membuang kolom 
df2 = df2.drop(columns=['Timestamp UTC', 'Source'])
# Mengubah kolom 'Timestamp' menjadi tipe data datetime 
df2['Timestamp'] = pd.to_datetime(df2['Timestamp'], format='%Y-%m-%d %H.%M.%S') 
# Mengganti koma dengan titik dan mengubah tipe data dari string ke float
df2['Value'] = df2['Value'].str.replace(',', '.').astype(float)

# Mengubah dataframe menjadi format yang diinginkan
df2 = df2.pivot_table(index='Timestamp', columns='Measurement', values='Value').reset_index()

# Mengganti nama kolom untuk kemudahan penggunaan
df2.columns.name = None  # Menghapus nama kolom yang dihasilkan oleh pivot_table
df2 = df2.rename(columns={
    "Voltage L-L Avg High": "High",
    "Voltage L-L Avg Low": "Low",
    "Voltage L-L Avg Mean": "Mean"
})

# Tampilkan hasil
#st.write(df2)

#######################################
#######################################

col1, col2 = st.columns([1,2])
with col1:
    st.write('\n\n')
    LP10Max = df['V'].max()
    st.metric("Tegangan LP10 Max (kV)", value=LP10Max)
    LP10Min = df['V'].min()
    st.metric("Tegangan LP10 Min (kV)", value=LP10Min)
    GIMax = df2['Mean'].max()
    st.metric("Tegangan GI Max (kV)", value=round(GIMax/1000, 2))
    GIMin = df2['Mean'].min()
    st.metric("Tegangan GI Min (kV)", value=round(GIMin/1000, 2))
    
with col2:
    # Membuat plotly figure
    fig = go.Figure()

    # Warna yang akan digunakan 
    color_v = '#1f77b4' # warna biru untuk V 12 
    color_value = '#ff7f0e' # warna oranye untuk Value

    # Menambahkan lineplot dari df (sumbu y primer) 
    fig.add_trace(go.Scatter(x=df['Datetime'], y=df['V'], mode='lines', name='V 3.3KV', line=dict(color=color_v)))

    # Menambahkan lineplot dari df2 (sumbu y sekunder) 
    fig.add_trace(go.Scatter(x=df2['Timestamp'], y=df2['Mean'], mode='lines', name='V 150KV', line=dict(color=color_value), yaxis='y2'))

    # Menambahkan lineplot dari df2 (sumbu y sekunder) 
    #fig.add_trace(go.Scatter(x=df2['Timestamp'], y=df2['High'], mode='lines', name='V 150KV', line=dict(color=color_value), yaxis='y2'))

    # Menambahkan lineplot dari df2 (sumbu y sekunder) 
    #fig.add_trace(go.Scatter(x=df2['Timestamp'], y=df2['Low'], mode='lines', name='V 150KV', line=dict(color=color_value), yaxis='y2'))


    # Menambahkan layout untuk dua sumbu y
    fig.update_layout(
        title='Perbandingan Tegangan GI dan Sistem 3.3KV',
        xaxis_title='Waktu',
        yaxis=dict(
            title='V 12',
            titlefont=dict(
                color='#1f77b4'
            ),
            tickfont=dict(
                color='#1f77b4'
            )
        ),
        yaxis2=dict(
            title='Value',
            titlefont=dict(
                color='#ff7f0e'
            ),
            tickfont=dict(
                color='#ff7f0e'
            ),
            anchor='x',
            overlaying='y',
            side='right'
        ),
        legend=dict(
            x=0,
            y=1,
            traceorder='normal',

            
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        )
    )

    # Tampilkan plot di Streamlit
    st.plotly_chart(fig)

#######################################
#######################################

df['V'] = df['V'] / 3.3
df2['Mean'] = df2['Mean'] / 150000

# Membuat plotly figure
fig = go.Figure()

# Warna yang akan digunakan 
color_v = '#1f77b4' # warna biru untuk V 12 
color_value = '#ff7f0e' # warna oranye untuk Value

# Menambahkan lineplot dari df (sumbu y primer) 
fig.add_trace(go.Scatter(x=df['Datetime'], y=df['V'], mode='lines', name='V 3.3KV', line=dict(color=color_v)))

# Menambahkan lineplot dari df2 (sumbu y sekunder) 
fig.add_trace(go.Scatter(x=df2['Timestamp'], y=df2['Mean'], mode='lines', name='V 150KV', line=dict(color=color_value), yaxis='y2'))

# Menambahkan garis horizontal pada y = 1.08 
fig.add_shape( 
    type='line', 
    x0=df['Datetime'].min(), 
    x1=df['Datetime'].max(), 
    y0=1.08, 
    y1=1.08, line=dict( 
        color="Red", 
        width=2, 
        dash="dash" 
    ) 
)
# Menambahkan label pada garis horizontal 
fig.add_annotation( 
    x=df['Datetime'].max() - pd.Timedelta(hours=5), 
    y=1.06, 
    text="High Tripping Limit (8% above nominal)", 
    showarrow=False, 
    yshift=10, font=dict( 
        color="Red", 
        size=12 
    ), 
    bgcolor="rgba(255, 255, 255, 0.7)", 
    bordercolor="Red" 
)
# Menambahkan garis horizontal pada y = 0.9 
fig.add_shape( 
    type='line', 
    x0=df['Datetime'].min(), 
    x1=df['Datetime'].max(), 
    y0=0.9, 
    y1=0.9, line=dict( 
        color="Red", 
        width=2, 
        dash="dash" 
    ) 
)
# Menambahkan label pada garis horizontal 
fig.add_annotation( 
    x=df['Datetime'].max() - pd.Timedelta(hours=5), 
    y=0.91, 
    text="Low Tripping Limit (10% below nonimal)", 
    showarrow=False, 
    yshift=10, font=dict( 
        color="Red", 
        size=12 
    ), 
    bgcolor="rgba(255, 255, 255, 0.7)", 
    bordercolor="Red" 
)

# Menambahkan layout untuk dua sumbu y
fig.update_layout(
    title='Perbandingan Tegangan GI dan Sistem 3.3KV (Per Unit Value)',
    xaxis_title='Waktu',
    yaxis=dict(
        title='V 3.3KV (PU)',
        titlefont=dict(
            color='#1f77b4'
        ),
        tickfont=dict(
            color='#1f77b4'
        ),
        range = [0.9, 1.1] # batas atas dan bawah sumbu y primer
    ),
    yaxis2=dict(
        title='V 150KV (PU)',
        titlefont=dict(
            color='#ff7f0e'
        ),
        tickfont=dict(
            color='#ff7f0e'
        ),
        anchor='x',
        overlaying='y',
        side='right',
        range = [0.9, 1.1] # batas atas dan bawah sumbu y sekunder
    ),
    legend=dict(
        x=0.05,
        y=0.05,
        traceorder='normal',
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    )
)

# Tampilkan plot di Streamlit
st.plotly_chart(fig)

##############################
# Menampilkan dataframe

# Mengembalikan ke nilai asal
df['V'] = df['V'] * 3.3
df2['Mean'] = df2['Mean'] * 150000

st.markdown("## Hasil pengukuran tegangan 3.3KV")
st.write(df)

st.markdown("## Hasil pengukuran tegangan Gardu Induk")
st.write(df2)