# app2.py modifications
import streamlit as st
from joblib import load
import pandas as pd
from test_charts import engine, is_patient_alive, process_patient_data

st.set_page_config(layout="wide")

# Load the trained model and data
MODEL_PATH = 'rf_model.joblib'
DATA_PATH = 'copy_of_data_latest.csv'
rf_pipeline = load(MODEL_PATH)
copy_of_data = pd.read_csv(DATA_PATH)

def predict_readmission(subject_id, data, model):
    # Existing implementation remains unchanged...
    patient_data = data[data['subject_id'] == subject_id]
    
    if not patient_data.empty:
        latest_visit = patient_data.iloc[-1]
        
        features = ['gender', 'anchor_age', 'los_24 hour interval', 'hospital_expire_flag',
                    'icd_code', 'severity', 'previous_admissions_count', 'readmit','admission_location', 'insurance']
        input_data = latest_visit[features].to_frame().transpose()
        for feature in ['gender', 'icd_code']:
            input_data[feature] = input_data[feature].astype(str)
        
        prediction_proba = model.predict_proba(input_data)[0][1]
        prediction = "Yes" if prediction_proba > 0.35 else "No"  # Adjust the threshold as necessary
        diagnosis = latest_visit['long_title']  # Adjust this if 'long_title' is not the correct column name
        age = latest_visit['anchor_age']
        gender = latest_visit['gender']
        visit_order = latest_visit['visit_order']
        
        return gender, visit_order, prediction, f"{prediction_proba:.2%}", diagnosis, age
    else:
        return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"
    
st.title("Hospital Readmission Prediction")
subject_id = st.number_input("Enter Patient ID", step=1, format="%d")

if st.button("Generate"):
    message, fig = process_patient_data(subject_id, engine)
    if fig:
        gender, visit_order, prediction, probability, diagnosis, age = predict_readmission(subject_id, copy_of_data, rf_pipeline)
        
        # Layout for predictions
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col1:
            st.metric(label="Patient Age", value=age)
        with col2:
            st.metric(label="Gender", value=gender)
        with col3:
            st.metric(label="Number of Visits", value=visit_order)
        with col4:
            st.metric(label="Readmission Probability", value=probability)
        with col5:
            st.metric(label="Readmission within next 30 days", value=prediction)
            
        st.write(f"Diagnosis: **{diagnosis}**")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(message)