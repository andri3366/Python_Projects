"""Dataset loading and cleaning utilities.

This module reads raw datasets, applies basic cleaning rules, and writes
dataset-specific cleaned files into data/processed.
"""

import pandas as pd
import os

def load_and_preprocess_data(data_path):
    """Load a dataset from disk, clean it, and persist its cleaned version.

    The function applies shared cleaning steps (duplicates and missing values)
    and then dataset-specific logic based on filename.
    """
    
    df = pd.read_csv(data_path)
    
    # Remove duplicate records before any downstream transformations.
    df.drop_duplicates(inplace=True)
    
    # Fill missing numeric values with median and categorical values with mode.
    for col in df.columns:
        
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(df[col].mode()[0])
            
    # Apply per-dataset cleaning rules.
    file_name = os.path.basename(data_path)
    
    if file_name == "real_estate.csv":
        df['basement']= df['basement'].fillna(0)
        df.basement=df.basement.astype(int)
        
        # remove guilty outlier
        df = df.drop(102)
        
        # save file
        df.to_csv('data/processed/cleaned_real_estate.csv', index=None)
    elif file_name == "credit.csv":
           # Special conversion
        df['Credit_History'] = df['Credit_History'].astype('object')
        df['Loan_Amount_Term'] = df['Loan_Amount_Term'].astype('object')
        
        df.to_csv('data/processed/cleaned_credit.csv', index=None)
    elif file_name == "admission.csv":
        
        df['Admit_Chance']=(df['Admit_Chance'] >=0.8).astype(int)
        
        df['University_Rating'] = df['University_Rating'].astype('object')
        df['Research'] = df['Research'].astype('object')
        
        df.to_csv('data/processed/cleaned_admission.csv', index=None)
    else:
        data_output = "data/processed/"
        clean_name = "cleaned_" + file_name
        clean_path = data_output + clean_name
        df.to_csv(clean_path, index=None)
    
    return df