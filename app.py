import streamlit as st
import joblib
import numpy as np
import os
import gdown

# Direct download link from Google Drive
model_url = "https://drive.google.com/uc?id=1eJRjojxktkifRSFT-d0rIlL87P0PkQ1h"
model_file = "model.pkl"

# Download the model if it doesn't exist
if not os.path.exists(model_file):
    with st.spinner("Downloading model..."):
        gdown.download(model_url, model_file, quiet=False)

# Silently load the model
try:
    model = joblib.load(model_file)
except Exception as e:
    st.error("⚠️ An internal error occurred. Please try again later.")
    st.stop()

# Title and Slogan
st.title("📈CrediWise💳")
st.markdown("### _Empowering Financial Decisions with AI_")

# Input fields
age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1, key="age")
income = st.number_input("Monthly Income (₹)", min_value=0, value=50000, step=1000, key="income")
loan_amount = st.number_input("Loan Amount (₹)", min_value=0, value=200000, step=1000, key="loan_amount")
num_of_loans = st.slider("Number of Active Loans", 0, 10, value=2, key="num_of_loans")
credit_mix = st.selectbox("Credit Mix", ["Select", "Standard", "Good", "Bad"], index=0, key="credit_mix")
outstanding_debt = st.number_input("Outstanding Debt (₹)", min_value=0, value=100000, step=1000, key="outstanding_debt")
interest_rate = st.slider("Interest Rate (%)", 0, 100, value=10, key="interest_rate")
delayed_payments = st.slider("Number of Delayed Payments", 0, 50, value=5, key="delayed_payments")

# Ensure valid inputs before prediction
if (age and income and loan_amount and num_of_loans is not None and 
    outstanding_debt and interest_rate is not None and 
    delayed_payments is not None and credit_mix != "Select"):
    
    # Encode input and validate
    credit_mix_encoded = {"Bad": 0, "Standard": 1, "Good": 2}[credit_mix]
    input_data = np.array([[age, income, loan_amount, num_of_loans,
                            credit_mix_encoded, outstanding_debt,
                            interest_rate, delayed_payments]])

    try:
        # Make prediction
        prediction = model.predict(input_data)
        pred_proba = model.predict_proba(input_data)[0]

        # Define decoding map
        decoded = {
            "Poor": ("Poor", "red", "High Risk - Immediate action needed"),
            "Standard": ("Standard", "orange", "Moderate Risk - Room for improvement"),
            "Good": ("Good", "blue", "Low Risk - Maintain current standing"),
            "Very Good": ("Very Good", "green", "Very Low Risk - Excellent standing"),
            "Excellent": ("Excellent", "purple", "Minimal Risk - Outstanding performance")
        }

        # Decode prediction and compute score rank
        score_key = prediction[0]
        if score_key not in decoded:
            st.error(f"Unexpected prediction result: {score_key}")
            st.stop()

        score_label, color, description = decoded[score_key]
        score_rank = list(decoded.keys()).index(score_key)
        progress = (score_rank + 1) / len(decoded)

        # Display results in columns
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### Credit Score: **{score_label}**")
            st.progress(progress)
        with col2:
            st.markdown("### Risk Assessment")
            st.markdown(f"**Status**: _{description}_")

        # Confidence levels
        st.markdown("### Confidence Levels")
        chart_data = {list(decoded.keys())[i]: prob for i, prob in enumerate(pred_proba)}
        st.bar_chart(chart_data)

        # Recommendations
        st.info("💡 **Recommendations**:\n" +
                "- Keep credit utilization below 30%\n" +
                "- Make payments on time\n" +
                "- Maintain a diverse credit mix")

    except Exception as e:
        st.error(f"Error during prediction: {e}")
else:
    st.warning("⚠️ Please fill out all fields to generate a prediction.")
