import pickle
import streamlit as st

# Membaca model
try:
    with open('resto_model.sav', 'rb') as file:
        resto_model = pickle.load(file)
except FileNotFoundError:
    st.error("File model tidak ditemukan. Pastikan file berada di jalur yang benar.")
except Exception as e:
    st.error(f"Error saat memuat model: {e}")

# Judul web
st.title('Prediksi Harga Menu Restoran')

# Input data dengan contoh angka valid untuk pengujian
Profitability = st.text_input('Profitability', '1')
MenuCategory_Appetizer = st.text_input('MenuCategory_Appetizer', '0')
MenuCategory_Beverages = st.text_input('MenuCategory_Beverages', '1')
MenuCategory_Dessert = st.text_input('MenuCategory_Dessert', '0')
MenuCategory_MainCourse = st.text_input('MenuCategory_MainCourse', '0')

harga_menu = ''

# Membuat tombol untuk prediksi
if st.button('Prediksi'):
    try:
        # Convert input to appropriate data types
        Profitability = int(Profitability)
        MenuCategory_Appetizer = int(MenuCategory_Appetizer)
        MenuCategory_Beverages = int(MenuCategory_Beverages)
        MenuCategory_Dessert = int(MenuCategory_Dessert)
        MenuCategory_MainCourse = int(MenuCategory_MainCourse)

        # Melakukan prediksi
        price_prediction = resto_model.predict([[Profitability, MenuCategory_Appetizer, MenuCategory_Beverages,
                                                 MenuCategory_Dessert, MenuCategory_MainCourse]])

        # Menentukan kategori harga berdasarkan prediksi
        if price_prediction[0] == 1:
            harga_menu = 'low'
        elif price_prediction[0] == 2:
            harga_menu = 'medium'
        else:
            harga_menu = 'high'
        
        st.success(harga_menu)

    except ValueError:
        st.error("Pastikan semua input diisi dengan angka yang valid.")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
     