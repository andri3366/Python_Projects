"""Model preparation and training utilities.

This module contains shared train/test preparation, optional scaling,
model factory mapping, and persistence helpers for trained estimators.
"""

from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPClassifier
import pickle
import pandas as pd

def train_lr(X, y, data):
    """Train and save a baseline linear regression model."""
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
    
    model = LinearRegression()
    lrmodel = model.fit(X_train, y_train)
    
    file_path = 'models/LRmodel_'
    file_extension = '.pkl'
    file_name = file_path + data + file_extension
    with open(file_name, 'wb') as f:
        pickle.dump(lrmodel, f)
        
        
    return model, X_test, y_test

def train_rf(X, y, data):
    """Train and save a baseline random forest regressor model."""
    
    model = RandomForestRegressor(n_estimators=200, criterion='absolute_error')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=data["test_size"], random_state=123)

    rfmodel = model.fit(X_train,y_train)

    file_path = 'models/RFmodel_'
    file_extension = '.pkl'
    file_name = file_path + data + file_extension
    with open(file_name, 'wb') as f:
        pickle.dump(rfmodel, f)
        
        
    return rfmodel, X_test, y_test

models = {
    "LinearRegression": LinearRegression,
    "LogisticRegression": LogisticRegression,
    "DecisionTreeClassifier" : DecisionTreeClassifier,
    "RandomForestRegressor": RandomForestRegressor,
    "RandomForestClassifier": RandomForestClassifier,
    "KMeans" : KMeans,
    "MLPClassifier" : MLPClassifier
}

def prep_model(X, y, config):
    """Split features/target and optionally scale training/test sets."""
    
    split_kwargs = config["train_test_split"].copy()
    
    if "stratify" in split_kwargs:
        split_kwargs["stratify"] = y
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, **split_kwargs)

    scaler = None
    X_train_scaled = None
    X_test_scaled = None
    # X_scaled = None
    
    if config.get("scale") :
        
        if config.get("scaler") == "standard":
            scaler = StandardScaler()
        else:
            scaler = MinMaxScaler()
            
        # X_train = scaler.fit_transform(X_train)
        # X_test = scaler.transform(X_test)
        
        # X_scaled = pd.DataFrame(
        #     X_train,
        #     columns=X.columns
        # )
        
        # Fit ONLY on training data
        X_train_scaled = pd.DataFrame(
            scaler.fit_transform(X_train),
            columns=X_train.columns,
            index=X_train.index
        )

        # Apply the already-fitted scaler to test data
        X_test_scaled = pd.DataFrame(
            scaler.transform(X_test),
            columns=X_test.columns,
            index=X_test.index
        )

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        scaler,
        X_train_scaled,
        X_test_scaled
    )
        
    # return X_train, X_test, y_train, y_test, scaler, X_scaled

def prep_cluster(X, config):
    """Scale clustering inputs when scaling is enabled in config."""

    scaler = None
    scaled_X = X.copy()

    if config.get("scale"):

        if config.get("scaler") == "standard":
            scaler = StandardScaler()
        else:
            scaler = MinMaxScaler()

        scaled_X = pd.DataFrame(
            scaler.fit_transform(X),
            columns=X.columns
        )

    return scaled_X, scaler

def train_model(X_train, y_train, dataset_name, model_config, feature_name=None, save_model=True, model_index=None, scaler=None):
    """Instantiate, fit, and optionally persist a configured model."""
    
    model_class = models[model_config["name"]]
    
    model = model_class(
        **model_config.get("kwargs", {})
    )
    
    if y_train is None:
        final_model = model.fit(X_train)
    else:
        final_model = model.fit(X_train, y_train)
    # final_model = model.fit(X_train, y_train)
    
    if save_model:
        if feature_name:
            file_path = 'models/model_'
            file_name = file_path + model_config["name"] + "_" + dataset_name + "_" + feature_name 
        else:
            file_path = 'models/model_'
            file_name = file_path + model_config["name"] + "_" + dataset_name

        if model_index is not None:
            file_name += f"_{model_index}"
        
        file_name += ".pkl"
        payload = final_model if scaler is None else {"model": final_model, "scaler": scaler}
        with open(file_name, 'wb') as f:
            pickle.dump(payload, f)
        
    return final_model


def load_model_artifact(file_path):
    """Load a pickled model or a model-plus-scaler bundle."""

    with open(file_path, "rb") as handle:
        payload = pickle.load(handle)

    if isinstance(payload, dict) and "model" in payload:
        return payload["model"], payload.get("scaler")

    return payload, None
    