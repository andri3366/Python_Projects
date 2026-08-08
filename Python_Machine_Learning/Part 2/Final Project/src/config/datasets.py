"""Central dataset and model configuration registry.

Each dataset entry defines file paths, target settings, preprocessing options,
problem type, model list, and report plotting instructions.
"""

datasets = {
    "real_estate": {
        "raw_path": "data/raw/real_estate.csv",
        "cleaned_path": "data/processed/cleaned_real_estate.csv",
        "final_path": "data/processed/final_real_estate.csv",
        "target": "price",
        "scale" : False,
        "scaler" : None,
        "train_test_split" : {
            "test_size" : 0.2,
            "random_state" : 123
        },
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
                "data" : "raw",
                "x" : "sqft",
                "y" : "price"
            },
            {
                "type" : "scatterplot",
                "data" : "raw",
                "x" : "price",
                "y" : "year_built"
            },
            {
                "type" : "scatterplot",
                "data" : "raw",
                "y" : "property_tax",
                "x" : "insurance"
            },
            {
                "type" : "boxplot",
                "data" : "raw",
                "y" : "property_type",
                "x" : "sqft"
            },
            {
                "type" : "boxplot",
                "data" : "raw",
                "y" : "property_type",
                "x" : "price"
            },
            {
                "type" : "heatmap",
                "data" : "raw",
            },
            {
                "type" : "histplot",
                "data" : "raw",
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
        "train_test_split" : {
            "test_size" : 0.2,
            "random_state" : 123
        },
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
                "data" : "raw",
                "x" : "Loan_Approved"
            },
            {
                "type" : "distplot",
                "data" : "raw",
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
    },
    
    "ucla_nn" : {
        "raw_path": "data/raw/admission.csv",
        "cleaned_path": "data/processed/cleaned_admission.csv",
        "final_path": "data/processed/final_admission.csv",
        "target": "Admit_Chance",
        "scale" : True,
        "scaler" : "minmax",
        "train_test_split" : {
            "test_size" : 0.2,
            "random_state" : 123,
            "stratify" : True
        },
        "problem_type" : "classification",
        "models" : [
            {
                "name" : "MLPClassifier",
                "kwargs" : {
                        "hidden_layer_sizes" : 3,
                        "batch_size" : 50,
                        "max_iter" : 200,
                        "random_state" : 123
                    }
            },
            {
                "name" : "MLPClassifier",
                "kwargs" : {
                        "hidden_layer_sizes" : 3,
                        "batch_size" : 50,
                        "max_iter" : 200,
                        "random_state" : 123,
                        "activation" : "tanh"
                    }
            }
        ],
        "plot" : [
            {
                "type" : "scatterplot",
                "data" : "processed",
                "x" : "GRE_Score",
                "y" : "TOEFL_Score",
                "hue" : "Admit_Chance"
            },
            {
                "type" : "distplot",
                "data" : "processed",
                "x" : 'GRE_Score',
                "compare_scaled" : True
            },
            {
                "type" : "distplot",
                "data" : "processed",
                "x" : "TOEFL_Score",
                "compare_scaled" : True
            }
            
        ]   
    }
}