"""Feature engineering helpers for model training and Streamlit inference."""

import pandas as pd
import os 

def create_dummy_var(data_path):
    """Create engineered features and one-hot encoded columns for a dataset.

    Reads a cleaned dataset, applies dataset-specific feature steps, one-hot
    encodes categorical variables, and writes the final dataset file.
    """
    
    df = pd.read_csv(data_path)
        
    file_name = os.path.basename(data_path)
    
    if file_name == "cleaned_real_estate.csv":
        
        # Domain features based on known housing market patterns.
        df['popular']= ((df.beds == 2)&(df.baths == 2)).astype(int)
        df['recession'] = ((df.year_sold >= 2010) & (df.year_sold<=2013)).astype(int)
        
        # Derived feature for property age.
        df['property_age'] = df.year_sold - df.year_built
        df.drop(index=df[df.property_age<0].index, inplace=True)
    
    if file_name == "cleaned_credit.csv":
        
        df = df.drop('Loan_ID', axis=1)
        
        df['Loan_Approved'] = df['Loan_Approved'].replace({'Y':1, 'N':0}).astype(int)
    
    if file_name == "cleaned_admission.csv":
        
        df = df.drop('Serial_No', axis=1)
        df = pd.get_dummies(df, columns=['University_Rating', 'Research'], drop_first=True).astype(int)
    else:
        cat_cols = df.select_dtypes(exclude=['number']).columns
        df = pd.get_dummies(df, columns=cat_cols, drop_first=True).astype(int)
    
    file_name = file_name.replace("cleaned_", "final_")
    
    df.to_csv(f"data/processed/{file_name}", index=False)
    
    return df

def streamlit_input(df, config, selected_display):
    """Transform Streamlit form input into model-ready feature columns."""
    
    # Encode categorical fields to mirror training-time feature engineering.
    if selected_display == "Loan Eligibility":

        # Create dummy variables
        df["Gender_Male"] = (df["Gender"] == "Male").astype(int)
        df["Married_Yes"] = (df["Married"] == "Yes").astype(int)

        df["Dependents_1"] = (df["Dependents"] == "1").astype(int)
        df["Dependents_2"] = (df["Dependents"] == "2").astype(int)
        df["Dependents_3+"] = (df["Dependents"] == "3+").astype(int)

        df["Education_Not Graduate"] = (
            df["Education"] == "Not Graduate"
        ).astype(int)

        df["Self_Employed_Yes"] = (
            df["Self_Employed"] == "Yes"
        ).astype(int)

        df["Property_Area_Semiurban"] = (
            df["Property_Area"] == "Semiurban"
        ).astype(int)

        df["Property_Area_Urban"] = (
            df["Property_Area"] == "Urban"
        ).astype(int)

        # Remove original categorical columns
        df.drop(
            columns=[
                "Gender",
                "Married",
                "Dependents",
                "Education",
                "Self_Employed",
                "Property_Area",
            ],
            inplace=True,
        )

    if selected_display == "UCLA Admission":
        df["University_Rating_2"] = (df["University_Rating"] == "2").astype(int)
        df["University_Rating_3"] = (df["University_Rating"] == "3").astype(int)
        df["University_Rating_4"] = (df["University_Rating"] == "4").astype(int)
        df["University_Rating_5"] = (df["University_Rating"] == "5").astype(int)

        df["Research_1"] = (df["Research"] == "1").astype(int)

        # Remove original categorical columns
        df.drop(
            columns=[
                "Research",
                "University_Rating"
            ],
            inplace=True,
        )
    for col in config["features"]:
        if col not in df.columns:
            df[col] = 0

    df = df[config["features"]]

    return df
