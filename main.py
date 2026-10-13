import streamlit as st
import pandas as pd
import joblib

 #LOAD THE PRE-TRAINED MODEL#
model = joblib.load('decision_tree.pkl')

## The exact 11 columns your model expects to see, in order
input_columns = [
    "no_of_dependents",
    "education",
    "self_employed",
    "income_annum",
    "loan_amount",
    "loan_term",
    "cibil_score",
    "residential_assets_value",
    "commercial_assets_value",
    "luxury_assets_value",
    "bank_asset_value",
]

# WEB USER INTERFACE
st.title('SmartLoan Predictor')
st.markdown('Enter metrics below to evaluate application status')

# Create input forms
col1, col2 = st.columns(2)

with col1:
    dependents = st.number_input("Number of Dependents", min_value=0, step=1)
    education_text = st.selectbox("Education Level", ["Graduate", "Not Graduate"])
    self_employed_text = st.selectbox("Self Employed?", ["Yes", "No"])
    income_annum = st.number_input("Annual Income ($)", min_value=0, step=1000)
    loan_amount = st.number_input("Requested Loan Amount ($)", min_value=0, step=1000)

with col2:
    loan_term = st.number_input("Loan Term (Months)", min_value=1, step=1)
    cibil_score = st.slider("CIBIL Credit Score (Credit History)", 300, 900, 650)
    residential_assets = st.number_input(
        "Residential Asset Value ($)", min_value=0, step=1000
    )
    commercial_assets = st.number_input(
        "Commercial Asset Value ($)", min_value=0, step=1000
    )
    luxury_assets = st.number_input(
        "Luxury Asset Value ($)", min_value=0, step=1000
    )
    bank_assets = st.number_input("Bank Asset Value ($)", min_value=0, step=1000)

# PREDICTION MAPPING 

if st.button("Evaluate Application Status", type="primary"):

    # Convert user selections to matching numeric label values
    education = 1 if education_text == "Graduate" else 0
    self_employed = 1 if self_employed_text == "Yes" else 0

    # Build the dictionary mapped to your exact dataset column names
    new_data = {
        "no_of_dependents": dependents,
        "education": education,
        "self_employed": self_employed,
        "income_annum": income_annum,
        "loan_amount": loan_amount,
        "loan_term": loan_term,
        "cibil_score": cibil_score,
        "residential_assets_value": residential_assets,
        "commercial_assets_value": commercial_assets,
        "luxury_assets_value": luxury_assets,
        "bank_asset_value": bank_assets,
    }

    # Convert to DataFrame matching the structure your model expects
    df = pd.DataFrame([new_data], columns=input_columns)
    
    # Run Prediction
    prediction = model.predict(df)
    

    # Check your model's text outputs ("Approved" / "Rejected")
    result = str(prediction[0]).strip()

    if result == 'Approved':
        st.success('Congratultions your loan has been Approved')
    else: 
        st.error('Sorry your loan was declined')