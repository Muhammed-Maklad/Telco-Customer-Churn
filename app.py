import streamlit as st
import pandas as pd
import joblib
import os


model_path = 'logistic_regression_model.pkl'
model = joblib.load(model_path)

def preprocess_input(user_data):
    try:
        mappings = {
            'gender': {'Female' : 0, 'Male' : 1},
            'seniorcitizen': {'No': 0, 'Yes': 1},
            'partner': {'No': 0, 'Yes': 1},
            'dependents': {'No': 0, 'Yes': 1},
            'internetservice': {'DSL': 0, 'Fiber optic': 1, 'No': 2},
            'onlinesecurity': {'No': 0, 'Yes': 1, 'No internet service': 2},
            'onlinebackup': {'No': 0, 'Yes': 1, 'No internet service': 2},
            'deviceprotection': {'No': 0, 'Yes': 1, 'No internet service': 2},
            'techsupport': {'No': 0, 'Yes': 1, 'No internet service': 2},
            'streamingtv': {'No': 0, 'Yes': 1, 'No internet service': 2},
            'streamingmovies': {'No': 0, 'Yes': 1, 'No internet service': 2},
            'contract': {'Month-to-month': 0, 'One year': 1, 'Two year': 2},
            'paperlessbilling': {'No': 0, 'Yes': 1},
            'paymentmethod': {'Electronic check': 0, 'Mailed check': 1, 'Bank transfer (automatic)': 2, 'Credit card (automatic)': 3},
            'phoneservice': {'No': 0, 'Yes': 1},
            'multiplelines': {'No': 0, 'Yes': 1, 'No phone service': 2}
        }

        for column, mapping in mappings.items():
            if column in user_data.columns:
                user_data[column] = user_data[column].map(mapping).fillna(user_data[column])

        expected_columns = ['tenure', 'monthlycharges', 'totalcharges', 'seniorcitizen', 'partner', 
                            'dependents', 'internetservice', 'onlinesecurity', 'onlinebackup', 
                            'deviceprotection', 'techsupport', 'streamingtv', 'streamingmovies', 
                            'contract', 'paperlessbilling', 'paymentmethod', 'gender', 
                            'phoneservice', 'multiplelines']

        for column in expected_columns:
            if column not in user_data.columns:
                user_data[column] = 0

        user_data = user_data[expected_columns]
        return user_data
    except Exception as e:
        st.error(f"Error in preprocessing input: {str(e)}")
        return None



st.image('Prediction.png', use_column_width=True)

st.sidebar.header('Customer Information')
gender = st.sidebar.selectbox('Gender', ['Female','Male'], help="Customer's gender")
tenure = st.sidebar.slider('Tenure (Months)', 0, 72, 1, help="How long the customer has been with the company (in months)")
monthlycharges = st.sidebar.slider('Monthly Charges', 18.25, 118.75, 29.85, step=0.01, help="The amount customer pays monthly")
totalcharges = st.sidebar.slider('Total Charges', 18.8, 8684.8, 29.85, step=0.01, help="Total amount charged to the customer")
seniorcitizen = st.sidebar.selectbox('Senior Citizen', ['No', 'Yes'], help="Is the customer a senior citizen?")
partner = st.sidebar.selectbox('Partner', ['No', 'Yes'], help="Does the customer have a partner?")
dependents = st.sidebar.selectbox('Dependents', ['No', 'Yes'], help="Does the customer have dependents?")
internetservice = st.sidebar.selectbox('Internet Service', ['DSL', 'Fiber optic', 'No'], help="Type of internet service")
onlinesecurity = st.sidebar.selectbox('Online Security', ['No', 'Yes', 'No internet service'], help="Does the customer have online security?")
onlinebackup = st.sidebar.selectbox('Online Backup', ['No', 'Yes', 'No internet service'], help="Does the customer have online backup?")
deviceprotection = st.sidebar.selectbox('Device Protection', ['No', 'Yes', 'No internet service'], help="Does the customer have device protection?")
techsupport = st.sidebar.selectbox('Tech Support', ['No', 'Yes', 'No internet service'], help="Does the customer have tech support?")
streamingtv = st.sidebar.selectbox('Streaming TV', ['No', 'Yes', 'No internet service'], help="Does the customer have streaming TV?")
streamingmovies = st.sidebar.selectbox('Streaming Movies', ['No', 'Yes', 'No internet service'], help="Does the customer have streaming movies?")
contract = st.sidebar.selectbox('Contract', ['Month-to-month', 'One year', 'Two year'], help="Contract type")
paperlessbilling = st.sidebar.selectbox('Paperless Billing', ['No', 'Yes'], help="Is the customer on paperless billing?")
paymentmethod = st.sidebar.selectbox('Payment Method', ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], help="Preferred payment method")
phoneservice = st.sidebar.selectbox('Phone Service', ['No', 'Yes'], help="Does the customer have phone service?")
multiplelines = st.sidebar.selectbox('Multiple Lines', ['No', 'Yes', 'No phone service'], help="Does the customer have multiple lines?")


user_data = pd.DataFrame({
    'tenure': [tenure],
    'monthlycharges': [monthlycharges],
    'totalcharges': [totalcharges],
    'seniorcitizen': [seniorcitizen],
    'partner': [partner],
    'dependents': [dependents],
    'internetservice': [internetservice],
    'onlinesecurity': [onlinesecurity],
    'onlinebackup': [onlinebackup],
    'deviceprotection': [deviceprotection],
    'techsupport': [techsupport],
    'streamingtv': [streamingtv],
    'streamingmovies': [streamingmovies],
    'contract': [contract],
    'paperlessbilling': [paperlessbilling],
    'paymentmethod': [paymentmethod],
    'gender': [gender],
    'phoneservice': [phoneservice],
    'multiplelines': [multiplelines]
})

# Preprocess user input
processed_data = preprocess_input(user_data)

if st.sidebar.button('Predict'):
    with st.spinner('Predicting...'):
        if processed_data is not None:
            prediction = model.predict(processed_data)
            if prediction[0] == 1:
                st.image('Churn.png', use_column_width=True)
            else:
                st.image('Stay.png', use_column_width=True)
        else:
            st.image('Error.png', use_column_width=True)

st.markdown("""
    <div style="display: flex; justify-content: center;">
        <a href="https://www.linkedin.com/in/muhammed-maklad/" target="_blank">
            <button style="padding:10px 20px; background-color:#0a66c2; color:white; border:none; border-radius:5px; cursor:pointer; font-family: 'Comic Sans MS', sans-serif; font-size:16px;">
                Connect with me on LinkedIn
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)