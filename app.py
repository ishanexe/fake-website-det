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

# 1) Ask for the website URL and auto‑extract two features
website_url = st.text_input("Please enter the website URL:")
if website_url:
    if not validators.url(website_url):
        st.error("Invalid URL—please enter a valid URL.")
    else:
        url_length = len(website_url)
        has_https  = 1 if 'https' in website_url else 0

        st.markdown("**Extracted Features:**")
        st.write(f"- URL Length: {url_length}")
        st.write(f"- Contains HTTPS: {'Yes' if has_https else 'No'}")

        # 2) Ask for the remaining 5 features
        st.markdown("### Now enter the other details:")
        domain_reg_length = st.number_input("Domain registration length (days):", min_value=1, value=365)
        suspicious_url     = st.radio("Contains suspicious keywords?", [True, False])
        domain_age         = st.number_input("Domain age (years):", min_value=0, value=1)
        has_dns_record     = st.radio("Has a DNS record?", [True, False])
        url_shortened      = st.radio("Is the URL shortened?", [True, False])

        # 3) Prepare feature vector in the exact order your model expects
        features = [
            url_length,
            has_https,
            domain_reg_length,
            int(suspicious_url),
            domain_age,
            int(has_dns_record),
            int(url_shortened)
        ]

        # 4) Predict on button click
        if st.button("Predict"):
            pred = model.predict(np.array(features).reshape(1, -1))[0]
            label = "Phishing 🔴" if pred == 1 else "Legitimate 🟢"
            st.success(f"Prediction: **{label}**")
