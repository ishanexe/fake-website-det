import streamlit as st
import numpy as np
import joblib

# Load the model
model = joblib.load('model.pkl')

# Streamlit page config
st.set_page_config(page_title="Phishing Website Detector", layout="centered")

# Title
st.title("🔒 Phishing Website Detector")

# Input fields for 30 features
st.markdown("Enter the feature values to predict if the website is phishing or legitimate.")

features = []
for i in range(1, 31):
    val = st.number_input(f"Feature {i}", value=0)
    features.append(val)

# Prediction on button click
if st.button("Predict"):
    input_data = np.array(features).reshape(1, -1)
    prediction = model.predict(input_data)[0]
    label = "Phishing 🔴" if prediction == 1 else "Legitimate 🟢"
    st.success(f"Prediction: **{label}**")
