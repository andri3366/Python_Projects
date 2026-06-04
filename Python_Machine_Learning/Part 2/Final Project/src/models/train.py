from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import pickle

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

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

    rfmodel = model.fit(X_train,y_train)

    file_path = 'models/RFmodel_'
    file_extension = '.pkl'
    file_name = file_path + data + file_extension
    with open(file_name, 'wb') as f:
        pickle.dump(rfmodel, f)
        
        
    return rfmodel, X_test, y_test
