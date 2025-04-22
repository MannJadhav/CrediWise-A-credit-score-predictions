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

# Add custom background color
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #141E30, #243B55);
        color: #FFFFFF;
    }
    .css-18e3th9 {
        background-color: rgba(0,0,0,0) !important;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load the model
model = joblib.load(model_file)

# Title and Slogan
st.title("📈CrediWise💳")
st.markdown("### _Empowering Financial Decisions with AI_")

# Input fields
age = st.number_input("Age", min_value=18, max_value=100, value=None)
income = st.number_input("Monthly Income (₹)", min_value=0, value=None)
loan_amount = st.number_input("Loan Amount (₹)", min_value=0, value=None)
num_of_loans = st.slider("Number of Active Loans", 0, 10, value=None)
credit_mix = st.selectbox("Credit Mix", ["Select", "Standard", "Good", "Bad"])
outstanding_debt = st.number_input("Outstanding Debt (₹)", min_value=0, value=None)
interest_rate = st.slider("Interest Rate (%)", 0, 100, value=None)
delayed_payments = st.slider("Number of Delayed Payments", 0, 50, value=None)

# Ensure all fields are entered
if st.button("Predict Credit Score"):
    if None in [age, income, loan_amount, outstanding_debt, num_of_loans, interest_rate, delayed_payments] or credit_mix == "Select":
        st.warning("⚠️ Please fill out all fields to generate a prediction.")
    else:
        # Encode categorical variable
        credit_mix_encoded = {"Bad": 0, "Standard": 1, "Good": 2}[credit_mix]

        # Prepare input data
        input_data = np.array([[age, income, loan_amount, num_of_loans,
                                credit_mix_encoded, outstanding_debt,
                                interest_rate, delayed_payments]])

        # Make prediction
prediction = model.predict(input_data)
pred_proba = model.predict_proba(input_data)[0]

# If model returns string labels
decoded = {
    "Poor": ("Poor", "red", "High Risk - Immediate action needed"),
    "Standard": ("Standard", "orange", "Moderate Risk - Room for improvement"),
    "Good": ("Good", "blue", "Low Risk - Maintain current standing"),
    "Very Good": ("Very Good", "green", "Very Low Risk - Excellent standing"),
    "Excellent": ("Excellent", "purple", "Minimal Risk - Outstanding performance")
}

score_key = prediction[0]
score_label, color, description = decoded.get(score_key, ("Unknown", "gray", "Unable to determine"))

# Optional progress based on score rank
score_rank = list(decoded.keys()).index(score_key) if score_key in decoded else 0
progress = (score_rank + 1) / 5


        # Display results
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### Credit Score: **{score_label}**")
            progress = (score_value + 1) / 5
            st.progress(progress, text=f"Score: {score_value + 1}/5")
        with col2:
            st.markdown("### Risk Assessment")
            st.markdown(f"**Status**: _{description}_")

        # Confidence levels
        st.markdown("### Confidence Levels")
        for i, prob in enumerate(pred_proba):
            score_name = decoded.get(i, ("Unknown", "gray", ""))[0]
            st.bar_chart({score_name: prob})

        # Recommendations
        st.info("💡 **Recommendations**:\n" +
                "- Keep credit utilization below 30%\n" +
                "- Make payments on time\n" +
                "- Maintain a diverse credit mix")
