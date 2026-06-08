datasets = {
    "real_estate": {
        "raw_path": "data/raw/real_estate.csv",
        "cleaned_path": "data/processed/cleaned_real_estate.csv",
        "final_path": "data/processed/final_real_estate.csv",
        "target": "price",
        "scale" : False,
        "scaler" : None,
        "test_size" : 0.2,
        "random_state" : 123,
        "problem_type" : "regression",
        "models" : [
            {
                "name" : "LinearRegression",
                "kwargs": {}
            },
            {
                "name" : "RandomForestRegressor",
                "kwargs" : {
                    "n_estimators" : 200,
                    "criterion" : "absolute_error"
                }
            }
        ],
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
        "scale" : True,
        "scaler" : "minmax",
        "test_size" : 0.2,
        "random_state" : 123,
        "problem_type" : "classification",
        "models" : [
            {
                "name" : "LogisticRegression",
                "kwargs" : {},
                "cv" : 5
            },
            {
                "name" : "DecisionTreeClassifier",
                "kwargs" : {}
            },
            {
                "name" : "RandomForestClassifier",
                "kwargs" : {},
                "cv" : 5
            }
        ],
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
    },

    "mall_customers" : {
        "raw_path": "data/raw/mall_customers.csv",
        "cleaned_path": "data/processed/cleaned_mall_customers.csv",
        "final_path": "data/processed/final_mall_customers.csv",
        "target": [
            {
                "name" : "income_spending",
                "features" : [
                    "Annual_Income",
                    "Spending_Score"
                ]
            },
            {
                "name" : "income_spending_age",
                "features" : [
                    "Annual_Income",
                    "Spending_Score",
                    "Age"
                ]
            }
        ],
        "scale" : False,
        "problem_type" : "clustering",
        "models" : [
            {
                "name" : "KMeans",
                "clusters" : [3,5],
                "cluster_range" : [3,9],
                "kwargs" : {}
            }
        ]
    }
}