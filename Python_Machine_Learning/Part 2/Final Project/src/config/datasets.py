datasets = {
    "real_estate": {
        "raw_path": "data/raw/real_estate.csv",
        "cleaned_path": "data/processed/cleaned_real_estate.csv",
        "final_path": "data/processed/final_real_estate.csv",
        "target": "price",
        "plot": [
            {
                "type" : "scatterplot",
                "x" : "sqft",
                "y" : "price"
            },
            {
                "type" : "scatterplot",
                "x" : "price",
                "y" : "year_built"
            },
            {
                "type" : "scatterplot",
                "y" : "property_tax",
                "x" : "insurance"
            },
            {
                "type" : "boxplot",
                "y" : "property_type",
                "x" : "sqft"
            },
            {
                "type" : "boxplot",
                "y" : "property_type",
                "x" : "price"
            },
            {
                "type" : "heatmap"
            },
            {
                "type" : "histplot",
                "df" : "lot_size"
            }
        ]
    },
    "loan_eligibility" : {
        "raw_path": "data/raw/credit.csv",
        "cleaned_path": "data/processed/cleaned_credit.csv",
        "final_path": "data/processed/final_credit.csv",
        "target": "Loan_Approved",
        "plot" : [
            {
                "type" : "countplot",
                "x" : "Loan_Approved"
            },
            {
                "type" : "distplot",
                "x" : "LoanAmount"
            }
        ]   
    }
}