from sklearn.metrics import accuracy_score, confusion_matrix, mean_absolute_error
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold

def eval_model(model, X_test, y_test, problem_type):
    
    y_pred = model.predict(X_test)
    
    if problem_type == "regression":
        mae = mean_absolute_error(y_test, y_pred)
        
        return {
            "MAE": mae
        }
    elif problem_type == "classification":
        
        acc = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        
        return {
            "Accuracy" : acc,
            "Confusion Matrix" : cm
        }
    else:
        raise ValueError(
            f"Unknown problem type: {problem_type}"
        )
        
def cross_validate(model, X_train, y_train, model_config, problem_type):
    
    cv = model_config.get("cv")
    
    if cv is None:
        return None
    
    kfold = KFold(n_splits=cv)
    
    if problem_type == "classification":
        
        scores = cross_val_score(model, X_train, y_train, cv=kfold)
        
    return {
                "Accuracy" : scores,
                "Mean accuracy" : scores.mean(),
                "Standard Deviation" : scores.std()
            }
    # model_name = type(model).__name__
    
    # if model_name in ["LinearRegression", "RandomForestRegressor"]:
    #     mae = mean_absolute_error(y_pred, y_test)
    #     return mae
    
    # print("No eval")
    # acc = accuracy_score(y_pred, y_test)
    
    # cm = confusion_matrix(y_test, y_pred)
    
    # return mae