from src.data.make_dataset import load_and_preprocess_data
from src.features.build_features import create_dummy_var
from src.models.train import train_lr, train_rf
from src.models.predict import eval_model
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
        
        model, x_test, y_test = train_lr(X,y, dataset_name)
        
        
      
                    
        mae = eval_model(model, x_test, y_test)
        print(f"{model} MAE: {mae}")
        
        model, x_test, y_test = train_rf(X,y, dataset_name)
        mae = eval_model(model, x_test, y_test)
        print(f"{model} MAE: {mae}")
        
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
