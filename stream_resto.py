import streamlit as st
import pickle

# Fungsi untuk memuat model dari file
def load_model(filename):
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    return model

# Muat model Random Forest yang telah disimpan
model_filename = 'RF_Restaurant.sav'
random_forest_model = load_model(model_filename)

# Fungsi untuk melakukan prediksi dan menentukan kategori profitabilitas
def predict_profitability(features):
    # Melakukan prediksi dengan model
    profitability_prediction = random_forest_model.predict([features])
    
    # Menentukan kategori profitabilitas berdasarkan prediksi
    if profitability_prediction[0] == 0:
        profitability_category = 'low'
    elif profitability_prediction[0] == 1:
        profitability_category = 'medium'
    else:
        profitability_category = 'high'
    
    return profitability_category

# Judul web
st.title('Prediksi Profitabilitas Menu Restoran')

# Input data dengan contoh angka valid untuk pengujian
menu_item = st.number_input('Menu Item (Encoded)', min_value=0)
menu_category = st.number_input('Menu Category (Encoded)', min_value=0)
ingredients = st.number_input('Ingredients (Encoded)', min_value=0)
price = st.number_input('Price (Encoded and Standardized)', min_value=-3.0, max_value=3.0, step=0.01)

# Inisialisasi variabel untuk prediksi
profitability_prediction = ''

# Membuat tombol untuk prediksi
if st.button('Prediksi'):
    try:
        # Convert input to appropriate data types
        menu_item = int(menu_item)
        menu_category = int(menu_category)
        ingredients = int(ingredients)
        price = float(price)

        # Melakukan prediksi
        profitability_prediction = predict_profitability([menu_item, menu_category, ingredients, price])

        # Menentukan kategori profitabilitas berdasarkan prediksi
        st.success(f'Profitabilitas: {profitability_prediction}')

    except ValueError:
        st.error("Pastikan semua input diisi dengan angka yang valid.")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
