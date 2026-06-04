import pandas as pd
import os

def load_and_preprocess_data(data_path):
    
    df = pd.read_csv(data_path)
    
    # handle duplicates
    df.drop_duplicates(inplace=True)
    
    # impute missing values
    for col in df.columns:
        
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col].fillna(df[col].median())
        else:
            df[col].fillna(df[col].mode()[0])
            
    # handle based on file
    file_name = os.path.basename(data_path)
    
    if file_name == "real_estate.csv":
        df['basement']= df['basement'].fillna(0)
        df.basement=df.basement.astype(int)
        
        # remove guilty outlier
        df = df.drop(102)
        
        # save file
        df.to_csv('data/processed/cleaned_real_estate.csv', index=None)
    else:
        data_output = "data/processed/"
        clean_name = "cleaned_" + file_name
        clean_path = data_output + clean_name
        df.to_csv(clean_path, index=None)
    
    return df