from src.data.make_dataset import load_and_preprocess_data
from src.features.build_features import create_dummy_var
from src.models.train import train_lr, train_rf, prep_model, train_model
from src.models.predict import eval_model, cross_validate
from src.config.datasets import datasets
from src.visualization.visualize import create_report, plot_feature_importance

import pandas as pd
if __name__ == "__main__":
    
    for dataset_name, config in datasets.items():
        
        print(f"\nProcessing: {dataset_name}")
        
        eda = pd.read_csv(config["raw_path"])
        
        load_and_preprocess_data(config["raw_path"])
        create_dummy_var(config["cleaned_path"])
        
        df = pd.read_csv(config["final_path"])

        X = df.drop(config["target"], axis=1)
        y = df[config["target"]]
        
        X_train, X_test, y_train, y_test, scaler = prep_model(X,y,config)

        for model_config in config["models"]:
            
            model = train_model(X_train, y_train, dataset_name, model_config)
            
            metric = eval_model(model, X_test, y_test, config["problem_type"])
            print(f"{type(model).__name__} Metrics: {metric}")
            
            cv_score = cross_validate(model, X_train, y_train, model_config, config["problem_type"])
            if cv_score is not None:
                print(f"{type(model).__name__} CV Score: {cv_score}")
        # if dataset_name == "real_estate":
        #     model, x_test, y_test = train_lr(X,y, dataset_name)
        #     mae = eval_model(model, x_test, y_test)
        #     print(f"{model} MAE: {mae}")
        
        #     model, x_test, y_test = train_rf(X,y, dataset_name)
        #     mae = eval_model(model, x_test, y_test)
        #     print(f"{model} MAE: {mae}")
        
        # elif dataset_name == "loan_eligibility":
        #     model, x_test, y_test = train_lr(X,y, dataset_name)

        create_report(dataset_name, model, X, eda)
        
    # data_path = "data/raw/real_estate.csv"
    # df = load_and_preprocess_data(data_path)
    
    # X, y = create_dummy_var(df)
    
    # model, x_test, y_test = train_lr(X,y)
    # acc, cm = eval_model(model, x_test, y_test)
    # print(f"Accuracy: {acc}")
    # print(f"Confusion Matrix: {cm}")
    
    # model, x_test, y_test = train_rf(X,y)
    # acc, cm, mae = eval_model(model, x_test, y_test)
    # print(f"Accuracy: {acc}")
    # print(f"Confusion Matrix: {cm}")
    # print(f"Mean Absolute Error: {mae}")
