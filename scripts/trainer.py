from sklearn.model_selection import cross_val_score, train_test_split
import pandas as pd

from adapt import adapt_for_prediction, adapt_for_retraining, adapt_cicids2017_for_training
import joblib

PATHPREFIX= "server/"
# Read datasets
cicids2017_data = pd.read_csv(PATHPREFIX+"data_sources/data_renamed.csv")
own_data = pd.read_csv(PATHPREFIX+"data_sources/my_training_flows.csv")

# Feeding Data inclusive own Data

cicids2017_data, scaler, ipca, ipca_size =  adapt_cicids2017_for_training(data=cicids2017_data, use_ipca=True)
joblib.dump(scaler, PATHPREFIX+"scaler.pkl")
if ipca:
    joblib.dump(ipca, PATHPREFIX+f"ipca_mit_size_{ipca_size}.pkl") # only when true pls
    print(f"Dumped ipca with {ipca_size} Output-Features")
own_data = adapt_for_retraining(data=own_data,scaler=scaler, ipca=ipca, ipca_size=ipca_size)

data = pd.concat([cicids2017_data, own_data])

features = data.drop('attack_type', axis = 1)
labels = data['attack_type']
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size = 0.25, random_state = 0)

# dritter Random Forest
from sklearn.ensemble import RandomForestClassifier
rf3 = RandomForestClassifier(n_estimators = 15, max_depth = 8, max_features = 20, random_state = 0)
rf3.fit(X_train, y_train)

cv_rf1 = cross_val_score(rf3, X_train, y_train, cv = 5)
print('Random Forest Model mit eigenen Daten')
print(f'\nCross-validation scores:', ', '.join(map(str, cv_rf1)))
print(f'\nMean cross-validation score: {cv_rf1.mean():.2f}')
joblib.dump(rf3,PATHPREFIX+"model.pkl")

# Prediction
# flow_for_prediction = joblib.load("flow1.pkl")
# flow_for_prediction = adapt_for_prediction(flow_for_prediction,scaler,ipca,ipca_size)
# print(rf3.predict(flow_for_prediction))
# import joblib


print("done")
