import streamlit as st
import pickle
import joblib
import os
from src.predict import predict_posting

# with open('model/lr_model.pkl', 'rb') as f:
#     model = joblib.load(f)

# with open('model/lr_vectorizer.pkl', 'rb') as f:
#     vectorizer = joblib.load(f)

# with open('model/lr_cat_features.pkl', 'rb') as f:
#     cat_columns = joblib.load(f)

base_dir = os.path.dirname(__file__)
model_path = os.path.join(base_dir, 'model/lr_model.pkl')
vectorizer_path = os.path.join(base_dir, 'model/lr_vectorizer.pkl')
cat_features_path = os.path.join(base_dir, 'model/lr_cat_features.pkl')

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)
cat_columns = joblib.load(cat_features_path)
    
st.title("Fake Job Postings Detection")
st.write("This app detects whether a job posting is fake or not based on its description and other features.")
st.write("Please enter the job posting details below:")

text = st.text_area("Job Description")

telecommuting = st.selectbox("Work From Home ", ["No", "Yes"])
has_company_logo = st.selectbox("Has Company Logo", ["No", "Yes"])
has_questions = st.selectbox("Has Questions", ["No", "Yes"])

employment_type = st.selectbox(
    "Employment Type", 
    ["Full-time", "Part-time", "Contract", "Temporary", "Missing","Other"]
)

required_education = st.selectbox(
    "Required Education",
    ["Missing", "Bachelor's Degree", "High School or equivalent", "Unspecified", "Master's Degree", "Associate Degree", "Certification", "Some College Coursework Completed", "Professional", "Vocational", "Some High School Coursework", "Doctorate", "Vocational - Degree", "Vocational - HS Degree"]
)

required_experience = st.selectbox(
    "Required Experience",
    ["Internship", "Entry level", "Mid-Senior level", "Associate", "Director", "Internship", "Executive", "Missing"]
)

country = st.selectbox(
    "Country",
    ["AU", "CA", "DE", "GB", "IN", "Missing", "NZ", "Other", "US"]
)

if st.button('Analyze Posting'):
    
    result = predict_posting(
        text,
        telecommuting,
        has_company_logo,
        has_questions,
        employment_type,
        required_experience,
        required_education,
        country
    )
    
    st.success(
        f"Prediction: {result['label']} "
    )
    
    st.write(f"Confidence: {result['confidence']:.2f}")