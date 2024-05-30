import pandas as pd 
import numpy as np 
import pickle as pk 
import streamlit as st

model = pk.load(open('model.pkl','rb'))

st.header('Prediksi Harga Mobil Keluarga Kategori LMPV dan LSUV')

cars_data = pd.read_csv('lmpv_dataset.csv')

def get_brand_name(car_name):
    car_name = car_name.split(' ')[0]
    return car_name.strip()
cars_data['name'] = cars_data['name'].apply(get_brand_name)

name = st.selectbox('Pilih LMPV/LSUV', cars_data['name'].unique())
year = st.slider('Tahun Pembuatan', 2000,2024)
km_driven = st.slider('Jarak Tempuh', 5000,250000)
fuel = st.selectbox('Tipe Bahan Bakar', cars_data['fuel'].unique())
seller_type = st.selectbox('Tipe Penjual', cars_data['seller_type'].unique())
transmission = st.selectbox('Transmisi', cars_data['transmission'].unique())
engine = st.slider('kapasitas Mesin', min_value=1000, max_value=1500, step=100)
tax = st.slider('Pajak', 2020,2030)


if st.button("Prediksi"):
    input_data_model = pd.DataFrame(
    [[name,year,km_driven,fuel,seller_type,transmission,engine,tax]],
    columns=['name','year','km_driven','fuel','seller_type','transmission','engine','tax'])
    
    input_data_model['fuel'].replace(['Petrol', 'Hybrid'],[1,2], inplace=True)
    input_data_model['seller_type'].replace(['Dealer', 'Individual'],[1,2], inplace=True)
    input_data_model['transmission'].replace(['MT', 'AT'],[1,2], inplace=True)
    input_data_model['name'].replace(['Avanza', 'Ertiga', 'Xpander', 'Mobilio', 'Br-V', 'Rush', 'Xenia','Terios', 'Confero', 'Stargazer', 'Livina'], [1,2,3,4,5,6,7,8,9,10,11], inplace=True)

    car_price = model.predict(input_data_model)
    formatted_price = "{:,.0f}".format(car_price[0]).replace(',', '.')
    # st.markdown('Harga mobil berkisar Rp.'+ str(car_price[0]))
    st.markdown('Harga mobil berkisar Rp. '+ formatted_price)