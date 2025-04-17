import streamlit as st
import numpy as np
import joblib
import validators
from urllib.parse import urlparse

# Load the trained model
model = joblib.load('model.pkl')

# Streamlit page config
st.set_page_config(page_title="Phishing Website Detector", layout="centered")

# Title
st.title("🔒 Phishing Website Detection")

# Collecting user input for URL
website_url = st.text_input("Please enter the website URL:")

# If URL is entered, extract features automatically
if website_url:
    # Check if the URL is valid
    if not validators.url(website_url):
        st.error("The URL you entered is not valid. Please try again with a valid URL.")
    else:
        # Extract URL features
        url_length = len(website_url)
        has_https = 1 if 'https' in website_url else 0
        
        # Display extracted features
        st.markdown(f"**Extracted Features from URL:**")
        st.write(f"URL Length: {url_length}")
        st.write(f"Contains 'https': {'Yes' if has_https else 'No'}")
        
        # Ask for the remaining features based on the dataset
        st.markdown("### Please enter the remaining details:")

        # Domain Registration Length
        domain_reg_length = st.number_input("Enter the domain registration length:", min_value=1, value=10)

        # Suspicious URL (e.g., URL contains certain keywords like "login", "secure", etc.)
        suspicious_url = st.radio("Does the URL contain suspicious keywords?", options=[True, False])

        # Domain Age (in years)
        domain_age = st.number_input("Enter the domain age (in years):", min_value=1, value=5)

        # Has DNS Record (True = 1, False = 0)
        has_dns_record = st.radio("Does the domain have a DNS record?", options=[True, False])

        # URL Shortened (True = 1, False = 0)
        url_shortened = st.radio("Is the URL shortened?", options=[True, False])

        # Combine all feature inputs into a list
        features = [
            url_length,
            has_https,
            domain_reg_length,
            suspicious_url,
            domain_age,
            has_dns_record,
            url_shortened
        ]

        # Prediction on button click
        if st.button("Predict"):
            # Convert input data to an array
            input_data = np.array(features).reshape(1, -1)
            
            # Prediction
            prediction = model.predict(input_data)[0]
            
            # Show prediction result
            label = "Phishing 🔴" if prediction == 1 else "Legitimate 🟢"
            st.success(f"Prediction: **{label}**")
