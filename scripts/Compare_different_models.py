import pandas as pd
from sklearn.calibration import LabelEncoder
from sklearn.model_selection import RandomizedSearchCV, cross_val_score, train_test_split
from adapt import adapt_for_prediction, adapt_for_retraining, adapt_cicids2017_for_training
import joblib
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support as f_score
from sklearn.metrics import accuracy_score as ascore
from numpy import append



PATHPREFIX= "scripts/"
# Read datasets
cicids2017_data = joblib.load("scripts/data_sources/DataFrame_with_balanced_dataset.pkl")
data, scaler, ipca, ipca_size =  adapt_cicids2017_for_training(data=cicids2017_data, use_ipca=True, balance_the_data=False)
features = data.drop('attack_type', axis = 1)
labels = data['attack_type']
le = LabelEncoder()
le.fit(labels)
transformed_labels = le.transform(labels)
X_train, X_test, y_train, y_test = train_test_split(features, transformed_labels, test_size = 0.25, random_state = 0)
# full_cicids2017_data = pd.read_csv("scripts/data_sources/data_renamed.csv")
#bdata, bscaler, bipca, bipca_size =  adapt_cicids2017_for_training(data=full_cicids2017_data, use_ipca=True, balance_the_data=True, binary_switch=True)
#joblib.dump(bdata, "scripts/data_sources/bdata.pkl")
bdata = joblib.load("scripts/data_sources/bdata.pkl")
bfeatures = bdata.drop('attack_type', axis = 1)
mapping = {'DDoS': 'attack', 'DoS': 'attack', 'Port Scan': 'attack', 'Bot': 'attack', 'BENIGN': 'benign', 'Brute Force': 'attack', 'Web Attack': 'attack'}
binary_labels = bdata['attack_type'].replace(mapping)
le.fit(binary_labels)
transformed_binary_labels = le.transform(binary_labels)
b_X_train, b_X_test, b_y_train, b_y_test = train_test_split(bfeatures, transformed_binary_labels, test_size = 0.25, random_state = 0)


attack_data = data[data["attack_type"]!="BENIGN"]
attack_features = attack_data.drop('attack_type', axis = 1)
attack_labels = labels[labels!='BENIGN']
le.fit(attack_labels)
transformed_attack_labels = le.transform(attack_labels)
a_X_train, a_X_test, a_y_train, a_y_test = train_test_split(attack_features, transformed_attack_labels, test_size = 0.25, random_state = 0)


start_parameters = {'bootstrap': [True, False],
     'max_depth': [30, 40, 50, 60, 65, 70, 75, 80, 90, 100, None],
     'max_features': ['log2', 'sqrt'],
     'min_samples_leaf': [1, 2, 4],
     'min_samples_split': [2, 5, 10],
     'n_estimators': [400, 600, 700, 750, 800, 850, 900, 1000, 1200, 1400]}

def test_automatic_features_generation():
    rf = RandomForestRegressor(random_state = 42) 
    rf_random = RandomizedSearchCV(estimator = rf, param_distributions = start_parameters, n_iter = 10, cv = 2, verbose=2, random_state=42, n_jobs = -1)
    rf_random.fit(X_train, y_train)
    rf = rf_random.best_estimator_
    rf.fit(X_train, y_train)
    cv_rf1 = cross_val_score(rf, X_train, y_train, cv = 5)
    print(cv_rf1)

def get_params_for_RandomForestRegressor():
    rf = RandomForestRegressor(random_state = 42)
    start_parameters = {'bootstrap': [True, False],
     'max_depth': [30, 40, 50, 60, 65, 70, 75, 80, 90, 100, None],
     'max_features': ['log2', 'sqrt'],
     'min_samples_leaf': [1, 2, 4],
     'min_samples_split': [2, 5, 10],
     'n_estimators': [400, 600, 700, 750, 800, 850, 900, 1000, 1200, 1400]}
    rf_random = RandomizedSearchCV(estimator = rf, param_distributions = start_parameters, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
    rf_random.fit(X_train, y_train)
    print(f"Best parameters for RandomForestRegressor are :{rf_random.best_params_}")
    return rf_random.best_params_

def test_RandomForestRegressor():
    rf = RandomForestRegressor(n_estimators =800, min_samples_split = 2, min_samples_leaf = 1, max_features = "log2", max_depth = 70, bootstrap = False)
    rf.fit(X_train, y_train)
    cv_rf1 = cross_val_score(rf, X_train, y_train, cv = 5)
    print('Random Forest Regressor')
    print(f'\nCross-validation scores:', ', '.join(map(str, cv_rf1)))
    print(f'\nMean cross-validation score: {cv_rf1.mean():.3f}') # Cross-validation scores: 0.9850073919623545, 0.9858620389891886, 0.9871152759675765, 0.9875248426548244, 0.9823437421692107

def get_params_for_RandomForestClassifier():
    rf = RandomForestClassifier()
    rf_random = RandomizedSearchCV(estimator = rf, param_distributions = start_parameters, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
    rf_random.fit(X_train, y_train)
    print(f"Best parameters for RandomForestClassifier are :{rf_random.best_params_}")
    return rf_random.best_params_

def train_RandomForestClassifier_as_in_use_now():
    rf = RandomForestClassifier(n_estimators = 15, max_depth = 8, max_features = 20, random_state = 0)
    rf.fit(X_train, y_train)
    cv_rf1 = cross_val_score(rf, X_train, y_train, cv = 5)
    print('Random Forest Model 1')
    print(f'\nCross-validation scores:', ', '.join(map(str, cv_rf1)))
    print(f'\nMean cross-validation score: {cv_rf1.mean():.2f}') # Cross-validation scores: 0.9813333333333333, 0.9828571428571429, 0.9843809523809524, 0.9874285714285714, 0.9860952380952381
    return rf

def train_optimal_RandomForestClassifier():
    rf = RandomForestClassifier(n_estimators = 800, max_depth = 70, max_features = 'sqrt', bootstrap=False, random_state = 0)
    rf.fit(X_train, y_train)
    cv_rf1 = cross_val_score(rf, X_train, y_train, cv = 5)
    print('Random Forest Model 2')
    print(f'\nCross-validation scores:', ', '.join(map(str, cv_rf1)))
    print(f'\nMean cross-validation score: {cv_rf1.mean():.2f}') # Cross-validation scores: 0.9935238095238095, 0.992, 0.9944761904761905, 0.993904761904762, 0.993904761904762
    return rf

def get_params_for_HistGradientBoostingRegressor():
    rf = HistGradientBoostingRegressor()
    param_grid = {
        'learning_rate': [0.01, 0.1, 0.15, 0.2, 0.25, 0.3],
        'max_iter': [100, 200, 300],
        'max_depth': [3, 5, 7, 9, 11],
    }
    rf_random = RandomizedSearchCV(estimator = rf, param_distributions = param_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
    rf_random.fit(X_train, y_train)
    print(f"Best parameters for RandomForestRegressor are :{rf_random.best_params_}")
    return rf_random.best_params_

def train_HistGradientBoostingRegressor():
    rf = HistGradientBoostingRegressor(max_iter = 300, max_depth = 9, learning_rate = 0.1)
    rf.fit(X_train, y_train)
    cv_rf1 = cross_val_score(rf, X_train, y_train, cv = 5)
    print('Hist Gradient Regressor Model')
    print(f'\nCross-validation scores:', ', '.join(map(str, cv_rf1)))
    print(f'\nMean cross-validation score: {cv_rf1.mean():.2f}') # Cross-validation scores: 0.9806813239808873, 0.9793451951918513, 0.9792971028927014, 0.9823925195486048, 0.9820095360548075

def train_RandomForestClassifier_with_f1():
    rf = RandomForestClassifier(n_estimators = 800, max_depth = 70, max_features = 'sqrt', bootstrap=False, random_state = 0)
    rf.fit(X_train, y_train)
    cv_model = cross_val_score(rf, X_train, y_train, cv = 5)
    cv_model_f1 = cross_val_score(rf, X_train, y_train, cv = 5,  scoring='f1_macro')
    print('Random Forest Model mit eigenen Daten')
    print(f'\nCross-validation scores:', ', '.join(map(str, cv_model)))
    print(f'\nMean cross-validation score: {cv_model.mean():.2f}')
    print(f'\nF1 scores:', ', '.join(map(str, cv_model_f1)))
    print(f"\nF1 score mean: {cv_model_f1.mean():.2f}")

def test_with_recall_and_accuracy(model, X_test, y_test):
    predicted = model.predict(X_test)
    precision, recall, fscore, support = f_score(y_test, predicted)
    accuracy = ascore(y_test,predicted)
    print(f"Mean of recall of benign and accuracy of all in one model: {append(accuracy, recall[0]).mean()}")

def twostage_classifier():
    b_rf = RandomForestClassifier(n_estimators = 750, min_samples_split= 2, min_samples_leaf = 1, max_features= 'sqrt', max_depth= 75, bootstrap= False)
    # b_rf_random = RandomizedSearchCV(scoring = "recall", estimator = b_rf, param_distributions = start_parameters, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
    # b_rf_random.fit(b_X_train, b_y_train)
    # print(f"Best parameters for Binary RandomForestClassifier are :{b_rf_random.best_params_}")
    # b_rf = b_rf_random.best_estimator_
    #print("starting fit b_rf")
    #b_rf.fit(b_X_train, b_y_train)
    #joblib.dump(b_rf, "scripts/data_sources/binary_rf.pkl")
    #cv_rf1 = cross_val_score(scoring= "recall", estimator=b_rf, X=X_train, y=y_train, cv = 5)
    #print(cv_rf1)
    b_rf = joblib.load("scripts/data_sources/binary_rf.pkl")
    b_predicted = b_rf.predict(b_X_test)
    precision, recall, fscore, support = f_score(b_y_test, b_predicted)
    print(f"Recall of binary classifier is {recall}")
    # a_rf = RandomForestClassifier(n_estimators = 1400, min_samples_split= 5, min_samples_leaf = 1, max_features= 'sqrt', max_depth= 75, bootstrap= True)
    # a_rf_random = RandomizedSearchCV(scoring = "accuracy", estimator = a_rf, param_distributions = start_parameters, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
    # a_rf_random.fit(a_X_train, a_y_train)
    # print(f"Best parameters for Multi RandomForestClassifier are :{a_rf_random.best_params_}")
    # a_rf = a_rf_random.best_estimator_
    # print("starting fit a_rf")
    # a_rf.fit(a_X_train, a_y_train)    
    # joblib.dump(a_rf, "scripts/data_sources/attack_rf.pkl")
    a_rf = joblib.load("scripts/data_sources/attack_rf.pkl")
    a_predicted = a_rf.predict(a_X_test)
    accuracy = ascore(a_y_test, a_predicted)
    print(f"Accuracy of multi classifier is {accuracy}")

    print(f"Mean of recall of benign and accuracy of all: {append(accuracy, recall[0]).mean()}")
    return b_rf, a_rf
 
    
# test_with_recall_and_accuracy(train_RandomForestClassifier_as_in_use_now(), X_test, y_test)   # 0.9733943946442756
# test_with_recall_and_accuracy(train_RandomForestClassifier(), X_test, y_test)   # Mean of recall of benign and accuracy of all: 0.9918086009304437
# Best Parameters for binary classifier for best recall are {'n_estimators': 750, 'min_samples_split': 2, 'min_samples_leaf': 1, 'max_features': 'sqrt', 'max_depth': 75, 'bootstrap': False}
# Best parameters for Multi RandomForestClassifier are :{'n_estimators': 1400, 'min_samples_split': 5, 'min_samples_leaf': 1, 'max_features': 'sqrt', 'max_depth': 75, 'bootstrap': True}
# twostage_classifier()   #Mean of recall of benign and accuracy of all: 0.9988890231084662

