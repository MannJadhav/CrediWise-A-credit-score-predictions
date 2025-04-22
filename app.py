import streamlit as st

# Example structure of your Streamlit application
def main():
    st.title("Credit Score Prediction App")

    # Input fields and layout
    st.subheader("Provide your details:")
    col1, col2 = st.columns(2)  # Consistent 4-space indentation for this line

    # Inputs in column 1
    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=25)
        income = st.number_input("Annual Income", min_value=0, value=50000)

    # Inputs in column 2
    with col2:
        debt = st.number_input("Debt Amount", min_value=0, value=1000)
        score = st.slider("Credit Score", min_value=300, max_value=850, value=600)

    # Prediction button
    if st.button("Predict"):
        st.write("Prediction logic goes here.")

if __name__ == "__main__":
    main()
