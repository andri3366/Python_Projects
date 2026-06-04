from sklearn.metrics import accuracy_score, confusion_matrix, mean_absolute_error

def eval_model(model, X_train, y_test):
    
    y_pred = model.predict(X_train)
    
    model_name = type(model).__name__
    
    if model_name in ["LinearRegression", "RandomForestRegressor"]:
        mae = mean_absolute_error(y_pred, y_test)
        return mae
    
    print("No eval")
    # acc = accuracy_score(y_pred, y_test)
    
    # cm = confusion_matrix(y_test, y_pred)
    
    # return mae