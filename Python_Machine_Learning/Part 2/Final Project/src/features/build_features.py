import pandas as pd
import os 

# Feature engineering
def create_dummy_var(data_path):
    
    df = pd.read_csv(data_path)
        
    file_name = os.path.basename(data_path)
    
    if file_name == "cleaned_real_estate.csv":
        
        # domain knowledge
        df['popular']= ((df.beds == 2)&(df.baths == 2)).astype(int)
        df['recession'] = ((df.year_sold >= 2010) & (df.year_sold<=2013)).astype(int)
        
        # interaction features
        df['property_age'] = df.year_sold - df.year_built
        df.drop(index=df[df.property_age<0].index, inplace=True)
    
    if file_name == "cleaned_credit.csv":
        
        df = df.drop('Loan_ID', axis=1)
        
        df['Loan_Approved'] = df['Loan_Approved'].replace({'Y':1, 'N':0}).astype(int)
    
    cat_cols = df.select_dtypes(exclude=['number']).columns
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True).astype(int)
    
    file_name = file_name.replace("cleaned_", "final_")
    
    df.to_csv(f"data/processed/{file_name}", index=False)
    
    return df