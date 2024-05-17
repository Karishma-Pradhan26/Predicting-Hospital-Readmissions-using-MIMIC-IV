# Predicting-Hospital-Readmissions-using-MIMIC-IV
Repository hosts our project on predicting 30-day hospital readmissions using the MIMIC-IV database, featuring data preprocessing, exploratory analysis, and machine learning models to explore patient demographics and readmission factors.

This project focuses on predicting hospital readmissions within 30 days using the MIMIC-IV database, specifically targeting kidney-related diagnoses. The aim is to harness advanced data analysis techniques and machine learning models to identify key predictors of readmission and support healthcare decision-making processes. Here's a breakdown of the project's main components and methodologies:


**Exploratory Data Analysis (EDA)**
The project begins with a comprehensive exploratory data analysis to understand the demographics, healthcare utilization, and other relevant metrics of the patients. This phase involves:
  - Analyzing the distribution of admitted patients by gender and the frequency of hospitalizations by admission location.
  - Investigating monthly trends in patient admissions and creating visualizations such as bar charts, line graphs, and heatmaps to identify patterns and correlations that could affect readmissions.
    
**Data Preprocessing and Feature Engineering**
Data from the MIMIC-IV database is prepared and processed through various steps:
  - **Data Selection and Merging**: Essential tables like admissions, patients, and diagnoses are merged based on specific identifiers.
  - **Indicator Analysis**: Key readmission indicators, such as length of stay and time between admissions, are calculated.
  - **Feature Engineering**: New features like previous admission counts and visit orders are engineered to provide a detailed picture of patient profiles and improve model accuracy.
    
**Machine Learning Models**
Several predictive models are developed and evaluated:
  - **Logistic Regression**: Serves as a baseline model to establish foundational relationships between features and readmission likelihood.
  - **Random Forest Classifier**: Utilized for its strength in handling complex and high-dimensional data, capturing nonlinear relationships which are crucial given the dataset's complexity.
  - **XGBoost**: Known for its performance and speed, it’s applied to enhance model accuracy and manage the class imbalance with techniques like SMOTE (Synthetic Minority Over-sampling Technique).
  
**Streamlit Dashboard**
An interactive Streamlit dashboard is designed to visualize data and predictions effectively, allowing healthcare professionals to access and interpret model outputs easily. This dashboard provides:
  - Patient demographics and diagnosis information.
  - Calculated probabilities of readmission based on historical data.
  - Visual tracking of vital lab results important for monitoring kidney functions.

**Objective and Impact**
The project aims to improve patient care and reduce healthcare costs by providing accurate predictions of readmission risks. It leverages data science and machine learning to provide actionable insights that can inform and enhance healthcare strategies and patient management.

