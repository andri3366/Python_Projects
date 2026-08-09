"""Streamlit application for interactive predictions and clustering output.

The app loads trained models from disk, renders dataset-specific input forms,
transforms user input to training-compatible features, and returns predictions.
"""

import streamlit as st
import pickle
import pandas as pd
from src.config.datasets import datasets
from src.features.build_features import streamlit_input
from src.models.train import load_model_artifact
from pathlib import Path

dataset_display_names = {
    "real_estate" : "Real Estate",
    "loan_eligibility" : "Loan Eligibility",
    "mall_customers" : "Mall Customers",
    "ucla_nn" : "UCLA Admission"
}

# Reverse lookup map used to fetch dataset configuration by UI label.
display_to_dataset = {v: k for k, v in dataset_display_names.items()}

# Input schema and final feature order expected by each model group.
problem_features = {
    "Real Estate": {
        "input" : {
            #"price",
            "year_sold" : "number",
            "property_tax" : "number",
            "insurance" : "number",
            "beds" : "number",
            "baths" : "number",
            "sqft" : "number",
            "year_built" : "number",
            "lot_size" : "number",
            "basement" : [0,1],
            "popular" : "",
            "recession" : "",
            "property_age" : "",
            "property_type_Condo" : [0,1]
        },
        "features" : [
            #"price",
            "year_sold",
            "property_tax",
            "insurance",
            "beds",
            "baths",
            "sqft",
            "year_built",
            "lot_size",
            "basement",
            "popular",
            "recession",
            "property_age",
            "property_type_Condo"
        ]
    },
    "Loan Eligibility": {
        "input" : {
            "ApplicantIncome" : "number",
            "CoapplicantIncome" : "number",
            "LoanAmount" : "number",
            "Loan_Amount_Term" : ["360", "180", "240", "120", "60"],
            "Credit_History" : [0,1],
            #"Loan_Approved",
            "Gender" : ["Female", "Male"],
            "Married" : ["No", "Yes"],
            "Dependents" : ["0", "1", "2", "3+"],
            "Education" : ["Graduate", "Not Graduate"],
            "Self_Employed" : ["No", "Yes"],
            "Property_Area" : ["Rural", "Semiurban", "Urban"]
        },
        "features": [
            "ApplicantIncome",
            "CoapplicantIncome",
            "LoanAmount",
            "Loan_Amount_Term",
            "Credit_History",
            "Gender_Male",
            "Married_Yes",
            "Dependents_1",
            "Dependents_2",
            "Dependents_3+",
            "Education_Not Graduate",
            "Self_Employed_Yes",
            "Property_Area_Semiurban",
            "Property_Area_Urban"
        ]
    },
    "Mall Customers": {
        "input" : {
            "Annual_Income" : "number",
            "Spending_Score" : "number",
            "Age" : "number"
        },
        "features": [
            "Annual_Income",
            "Spending_Score",
            "Age"
        ]
    },
    "UCLA Admission": {
        "input": {
            "GRE_Score" : "number",
            "TOEFL_Score" : "number",
            "SOP" : "number",
            "LOR" : "number",
            "CGPA" : "number",
            "University_Rating" : ["1","2","3","4","5"],
            "Research" : ["0","1"],
            # "Admit_Chance"
        },
        "features": [
            "GRE_Score",
            "TOEFL_Score",
            "SOP",
            "LOR",
            "CGPA",
            "University_Rating_2",
            "University_Rating_3",
            "University_Rating_4",
            "University_Rating_5",
            "Research_1",
            # "Admit_Chance"
        ]
    }
}
st.title("Machine Learning Predictors")

display_names = list(dataset_display_names.values())

selected_display = st.selectbox(
    "Choose a Problem", display_names
)

problem = display_to_dataset[selected_display]

config = problem_features[selected_display]
model_config = datasets[problem]

model_name = []

if problem == "mall_customers":
    # Show feature-set variants because clustering models are saved per feature set.
    for target in model_config["target"]:
        feature_text = ", ".join(target["features"])
        display_name = f"KMeans ({feature_text})"
        model_name.append(display_name) 
else:
    for model in model_config["models"]:
        display_name = model["name"]
        
        if model["name"] == "MLPClassifier":
            activation = model["kwargs"].get("activation")
            
            if activation:
                display_name = f"{display_name} ({activation})"
        
        model_name.append(display_name)
 
selected_model = st.selectbox(
    "Select Model", model_name
)

model_index = model_name.index(selected_model)

BASE_DIR = Path(__file__).resolve().parent
if selected_display in ["Real Estate", "Loan Eligibility", "UCLA Admission"]:
    # Supervised models are versioned by model index.
    original_model_name = model_config["models"][model_index]["name"]   
    # model_path = f"models/model_{original_model_name}_{problem}_{model_index}.pkl"
    model_path = BASE_DIR / "models" / f"model_{original_model_name}_{problem}_{model_index}.pkl"

elif selected_display == "Mall Customers":
    # Clustering models are versioned by feature-set suffix.
    original_model_name = model_config["models"][0]["name"]
    feature_suffix = model_config["target"][model_index]["name"]
    # model_path = f"models/model_{original_model_name}_{problem}_{feature_suffix}.pkl"
    model_path = BASE_DIR / "models" / f"model_{original_model_name}_{problem}_{feature_suffix}.pkl"
    
try:
    model, scaler = load_model_artifact(model_path)
except FileNotFoundError:
    st.error(f"Model file not found: {model_path}")
    st.stop()
except Exception as e:
    st.error(f"Error Loading The Model: {str(e)}")
    st.stop()
    
st.header("Input Features")

user_input = {}

if selected_display == "Loan Eligibility":
    
    for feature, info in config["input"].items():
        
        if info == "number":
            if feature in ["ApplicantIncome","CoapplicantIncome", "LoanAmount"]:    
                user_input[feature] = st.number_input(feature.replace("_", " "), min_value=0, step=1000)
        elif isinstance(info, list):
            user_input[feature] = st.selectbox(feature.replace("_", " "), info)

if selected_display == "Real Estate":
    
    for feature, info in config["input"].items():
        if info == "number":
            if feature in ["year_sold", "year_built"]:
                user_input[feature] = st.number_input(feature.replace("_", " "), min_value=1880, max_value=2016, step=5)
            if feature in ["lot_size", "sqft"]:
                user_input[feature] = st.number_input(feature.replace("_", " "), min_value= 0, max_value=1221000, step=100000)
            if feature in ["property_tax", "insurance"]:
                user_input[feature] = st.number_input(feature.replace("_", " "), min_value=50, max_value=4550, step=100)
            if feature in ["beds"]:
                user_input[feature] = st.number_input(feature.replace("_", " "), min_value=1, max_value=5, step=1)
            if feature in ["baths"]:
                user_input[feature] = st.number_input(feature.replace("_", " "), min_value=1, max_value=6, step=1)
        if info == "":
            user_input["popular"] = int(user_input["beds"] == 2 and user_input["baths"] == 2)
            user_input["recession"] = int(user_input["year_sold"] >= 2010 and user_input["year_sold"] <= 2013)
            property_age = int(user_input["year_sold"] - user_input["year_built"])
            if property_age < 0:
                st.error("Year Built cannot be later than Year Sold")
                st.stop()
            user_input["property_age"] = property_age
        elif isinstance(info, list):
            user_input[feature] = st.selectbox(feature.replace("_", " "), info)

if selected_display == "Mall Customers":
    
    selected_features = model_config["target"][model_index]["features"]
    
    for feature, info in config["input"].items():
        if feature not in selected_features:
            continue
        if info == "number":
            if feature in ["Annual_Income"]:
                user_input[feature] = st.number_input(feature.replace("_", " "), min_value=15, max_value=137, step=10)
            if feature in ["Spending_Score"]:
                user_input[feature] = st.number_input(feature.replace("_", " "), min_value=1, max_value=99, step=5)
            if feature in ["Age"]:
                user_input[feature] = st.number_input(feature.replace("_", " "), min_value=18, max_value=70, step=1)

if selected_display == "UCLA Admission":
    
    for feature, info in config["input"].items():
        if info == "number":
            if feature in ["GRE_Score"]:
                user_input[feature] = st.number_input(feature.replace("_", " "), min_value=290, max_value=340, step=5)
            if feature in ["TOEFL_Score"]:
                user_input[feature] = st.number_input(feature.replace("_", " "), min_value=92, max_value=120, step=1)
            if feature in ["SOP", "LOR"]:
                user_input[feature] = st.number_input(feature.replace("_", " "), min_value=1, max_value=5, step=1)
            if feature in ["CGPA"]:
                user_input[feature] = st.number_input(feature.replace("_", " "), min_value=6.8, max_value=10.0, step=0.1, format="%.1f")
        elif isinstance(info, list):
            user_input[feature] = st.selectbox(feature.replace("_", " "), info)

if st.button("Predict", type="primary"):
    df = pd.DataFrame([user_input])

    if selected_display == "Loan Eligibility":
        df = streamlit_input(df, config, selected_display)
        # df = streamlit_input(df, config)
    if selected_display == "Real Estate":
        df = streamlit_input(df, config, selected_display)
    if selected_display == "UCLA Admission":
        df = streamlit_input(df, config, selected_display)
    if df.empty or df.shape[1] == 0:
        st.error("No features available for prediction.")
    else:
        try:
            if selected_display in ["Loan Eligibility", "UCLA Admission"] and scaler is not None:
                feature_columns = df.columns.tolist()
                df = pd.DataFrame(
                    scaler.transform(df),
                    columns=feature_columns,
                    index=df.index
                )

            # Input has been aligned to model feature columns at this point.
            prediction = model.predict(df)

            # # Verify model columns 
            # st.write("Features being sent to model:")
            # st.write(df)
            # st.write("Feature order:")
            # st.write(df.columns.tolist())
            # st.write(df.iloc[0].to_dict())


            # print("Model expects:", model.n_features_in_)
            # print("Data has:", df.shape[1])
            # print("Columns:", df.columns.tolist())

            if selected_display in ["Loan Eligibility", "Real Estate", "UCLA Admission"]:
                if prediction[0] == 1:
                    st.success("Approved!")
                else:
                    st.error("Not Approved!")
            elif selected_display == "Mall Customers":
                n_clusters = model.n_clusters
                st.success(f"Customer belong to cluster: {prediction[0]} "
                           f"(Model has {n_clusters} clusters)"
                           )
            
        except Exception as e:
            st.error(f"Error Making Prediction: {str(e)}")

if st.button("Reset Inputs"):
    st.rerun()
    