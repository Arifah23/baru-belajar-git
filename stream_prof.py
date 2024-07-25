import streamlit as st
import pickle

# Fungsi untuk memuat model dari file
def load_model(filename):
    try:
        with open(filename, 'rb') as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        st.error(f"File {filename} tidak ditemukan.")
    except pickle.PickleError:
        st.error("Terjadi kesalahan saat memuat file pickle.")
    except Exception as e:
        st.error(f"Kesalahan tak terduga: {e}")
    return None

# Muat model Random Forest yang telah disimpan
model_filename = 'RF_Restaurant.sav'
random_forest_model = load_model(model_filename)

# Debugging tambahan
if random_forest_model is None:
    st.error("Model tidak dimuat. Pastikan file model ada di lokasi yang benar dan tidak korup.")
else:
    st.success("Model berhasil dimuat.")

# Fungsi untuk melakukan prediksi dan menentukan kategori profitabilitas
def predict_profitability(features):
    if random_forest_model is None:
        st.error("Model tidak dimuat. Tidak dapat melakukan prediksi.")
        return None
    try:
        # Melakukan prediksi dengan model
        profitability_prediction = random_forest_model.predict([features])
        
        # Menentukan kategori profitabilitas berdasarkan prediksi
        if profitability_prediction[0] == 0:
            return 'low'
        elif profitability_prediction[0] == 1:
            return 'medium'
        elif profitability_prediction[0] == 2:
            return 'high'
        else:
            st.error("Kategori profitabilitas tidak valid.")
            return None
    except Exception as e:
        st.error(f"Kesalahan saat melakukan prediksi: {e}")
        return None

# Judul web
st.title('Prediksi Profitabilitas Menu Restoran')

# Input data dengan contoh angka valid untuk pengujian
menu_item = st.number_input('Menu Item (Encoded)', min_value=0)
menu_category = st.number_input('Menu Category (Encoded)', min_value=0)
ingredients = st.number_input('Ingredients (Encoded)', min_value=0)
price = st.number_input('Price (Encoded and Standardized)', min_value=-3.0, max_value=3.0, step=0.01)

# Membuat tombol untuk prediksi
if st.button('Prediksi'):
    try:
        features = [int(menu_item), int(menu_category), int(ingredients), float(price)]
        profitability_prediction = predict_profitability(features)
        if profitability_prediction:
            st.success(f'Profitabilitas: {profitability_prediction}')
        else:
            st.error("Prediksi gagal.")
    except ValueError:
        st.error("Pastikan semua input diisi dengan angka yang valid.")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
