"""Project training and reporting entry point.

This script loops through every configured dataset and runs an end-to-end
preprocessing, training, evaluation, and report generation pipeline.
"""

from src.data.make_dataset import load_and_preprocess_data
from src.features.build_features import create_dummy_var
from src.models.train import train_lr, train_rf, prep_model, train_model, prep_cluster
from src.models.predict import eval_model, cross_validate
from src.config.datasets import datasets
from src.visualization.visualize import create_report, plot_feature_importance, create_cluster_report, create_pair, create_cluster_metrics

from sklearn.metrics import silhouette_score
from matplotlib.backends.backend_pdf import PdfPages

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

if __name__ == "__main__":
    # Iterate through all dataset pipelines defined in src/config/datasets.py.
    for dataset_name, config in datasets.items():
        
        print(f"\nProcessing: {dataset_name}")
        
        eda = pd.read_csv(config["raw_path"])
        
        # Stage 1: raw data cleaning.
        load_and_preprocess_data(config["raw_path"])

        if config["problem_type"] in ["regression", "classification"]:

            # Stage 2: feature engineering and categorical encoding.
            create_dummy_var(config["cleaned_path"])
        
            df = pd.read_csv(config["final_path"])

            X = df.drop(config["target"], axis=1)
            y = df[config["target"]]
            
            # Stage 3: split data and apply optional scaling.
            X_train, X_test, y_train, y_test, scaler, X_train_scaled, X_test_scaled = prep_model(X,y,config)

            trained_models = []
            
            # Stage 4: train all configured models and log evaluation metrics.
            for i, model_config in enumerate(config["models"]):
                
                if config.get("scale"):
                    train_data = X_train_scaled
                    test_data = X_test_scaled
                else:
                    train_data = X_train
                    test_data = X_test

                model = train_model(
                    train_data,
                    y_train,
                    dataset_name,
                    model_config,
                    model_index=i
                )
                # model = train_model(X_train, y_train, dataset_name, model_config, model_index=i)
                
                trained_models.append(model)
                
                # metric = eval_model(model, X_test, y_test, config["problem_type"])
                metric = eval_model(model, test_data, y_test, config["problem_type"])
                print(f"{type(model).__name__} Metrics: {metric}")
                
                # cv_score = cross_validate(model, X_train, y_train, model_config, config["problem_type"])
                cv_score = cross_validate(model, train_data, y_train, model_config, config["problem_type"])
                if cv_score is not None:
                    print(f"{type(model).__name__} CV Score: {cv_score}")

            # Stage 5: export EDA/model visualizations into a PDF report.
            # create_report(dataset_name, trained_models, X, eda, df, X_scaled)
            create_report(dataset_name, trained_models, X, eda, df, X_train_scaled)

        elif config["problem_type"] == "clustering":

            df = pd.read_csv(config["cleaned_path"])

            pdf = PdfPages(str(REPORTS_DIR / f"{dataset_name}_report.pdf"))
        
            with pdf as r:

                # Plot pair plot
                create_pair(r, df)

                for feature_set in config["target"]:

                    print(f"Feature Set: {feature_set['name']}")

                    feature_name = feature_set["name"]
                    X = df[feature_set["features"]]

                    if config["scale"]:
                        X_cluster, scaler = prep_cluster(X, config)
                    else:
                        X_cluster = X

                    # Evaluate candidate k values before saving final cluster models.
                    for model_config in config["models"]:
                        
                        # elbow and silhouette 

                        start = model_config["cluster_range"][0]
                        stop = model_config["cluster_range"][1]

                        K = []
                        WCSS = []
                        SIL = []
                        best_k = None
                        best_silhouette = -1

                        for k in range(start, stop):

                            test_config = model_config.copy()
                            test_config["kwargs"] = {
                                **model_config.get("kwargs", {}),
                                "n_clusters" : k
                            }

                            test_model = train_model(X_cluster, None, dataset_name, test_config, feature_name, save_model=False)

                            K.append(k)

                            WCSS.append(test_model.inertia_)
                            score = silhouette_score(X_cluster, test_model.labels_)
                            SIL.append(score)

                            if score > best_silhouette:
                                best_silhouette = score
                                best_k = k

                        create_cluster_metrics(r, K, WCSS, SIL, feature_name)

                        print(f"Best k for {feature_name}: {best_k} (silhouette={best_silhouette:.3f})")

                        # Use the best-performing cluster count for persisted models.
                        save_config = model_config.copy()
                        save_config["kwargs"] = {
                            **model_config.get("kwargs", {}),
                            "n_clusters": best_k
                        }
                        train_model(X_cluster, None, dataset_name, save_config, feature_name)

                        # Use the configured cluster counts for visualizations.
                        for n_clusters in model_config.get("clusters", [best_k]):
                            current_config = model_config.copy()
                            current_config["kwargs"] = {
                                **model_config.get("kwargs", {}),
                                "n_clusters" : n_clusters
                            }
                            model = train_model(X_cluster, None, dataset_name, current_config, feature_name, save_model=False)

                            print("Done KMeans")
                            create_cluster_report(r, model, X_cluster, feature_name, n_clusters)
