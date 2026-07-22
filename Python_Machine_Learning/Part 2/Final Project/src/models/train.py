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
    
    split_kwargs = config["train_test_split"].copy()
    
    if "stratify" in split_kwargs:
        split_kwargs["stratify"] = y
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, **split_kwargs)

    scaler = None
    X_scaled = None
    
    if config.get("scale") :
        
        if config.get("scaler") == "standard":
            scaler = StandardScaler()
        else:
            scaler = MinMaxScaler()
            
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        
        X_scaled = pd.DataFrame(
            X_train,
            columns=X.columns
        )
        
    return X_train, X_test, y_train, y_test, scaler, X_scaled

def prep_cluster(X, config):

    scaler = None

    if config.get("scale"):

        if config.get("scaler") == "standard":
            scaler = StandardScaler()
        else:
            scaler = MinMaxScaler()
        
    X = scaler.fit_transform()

    return X, scaler

def train_model(X_train, y_train, dataset_name, model_config, feature_name=None, save_model=True, model_index=None):
    
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
        with open(file_name, 'wb') as f:
            pickle.dump(final_model, f)
        
    return model
    