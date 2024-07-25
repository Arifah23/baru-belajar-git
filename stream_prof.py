import streamlit as st
import pickle

# Function to load model from file
def load_model(filename):
    try:
        with open(filename, 'rb') as file:
            model = pickle.load(file)
        st.success(f"Model {filename} loaded successfully.")
        return model
    except FileNotFoundError:
        st.error(f"File {filename} tidak ditemukan.")
    except pickle.PickleError:
        st.error("Terjadi kesalahan saat memuat file pickle.")
    except Exception as e:
        st.error(f"Kesalahan tak terduga: {e}")
    return None

# Load the saved Random Forest model
model_filename = 'RF_Restaurant.sav'
random_forest_model = load_model(model_filename)

# Function to make predictions and determine profitability category
def predict_profitability(features):
    if random_forest_model is None:
        st.error("Model tidak dimuat. Tidak dapat melakukan prediksi.")
        return None
    try:
        # Make prediction using the model
        profitability_prediction = random_forest_model.predict([features])
        
        # Determine profitability category based on prediction
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

# Web title
st.title('Prediksi Profitabilitas Menu Restoran')

# Input data with valid example numbers for testing
menu_item = st.number_input('Menu Item (Encoded)', min_value=0)
menu_category = st.number_input('Menu Category (Encoded)', min_value=0)
ingredients = st.number_input('Ingredients (Encoded)', min_value=0)
price = st.number_input('Price (Encoded and Standardized)', min_value=-3.0, max_value=3.0, step=0.01)

# Create a button for prediction
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
