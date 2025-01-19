import asyncio
from elastic_connector import CustomElasticsearchConnector
from pandas import DataFrame, concat, read_csv
from sklearn.model_selection import cross_val_score, train_test_split
from joblib import dump, load
from pipelining_utilities import adapt_for_retraining, adapt_cicids2017_for_training

def get_self_created_flow_data() -> DataFrame:
    CEC = CustomElasticsearchConnector() # TODO API KEy must be loaded here
    data = asyncio.run(CEC.get_all_flows(onlyunseen= False, size=None)) # TODO THIS WILL BE DIFFERENT IN FUTURE CEC VERSIONS
    for_retraining = data[data["has_been_seen"] == "true"][['flow_data','attack_class']]
    return for_retraining.rename(columns={'attack_class': 'attack_type'})

def merge_own_flows_into_trainigdataset(own_data:DataFrame):
    trainingdata = load("DataFrame_with_balanced_dataset.pkl")
    added_classes = own_data['attack_type'].str.lower().value_counts()
    class_names = added_classes.index.str.lower()
    selected = trainingdata[trainingdata['attack_type'].str.lower().isin(class_names.str.lower())] # unnecessary?

    dfs = []
    for name in class_names:
        # Extrahiere Daten für jede Klasse
        df = selected[selected['attack_type'].str.lower() == name]
        # sample down to make space for own flow data
        n = 5000 - added_classes[name]
        df = df.sample(n=n, random_state=0)
        # add own flows of respective group
        own_flows_of_same_class = own_data[own_data['attack_type']==name]
        df.add(own_flows_of_same_class)
        dfs.append(df)
    
    # Kombiniere alle bearbeiteten Klassen
    df = concat(dfs, ignore_index = True)
    df.sample(frac=1)
    return df

def train_the_model(data:DataFrame):
    # split Data without type of attack
    features = data.drop('attack_type', axis = 1)
    labels = data['attack_type']
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size = 0.25, random_state = 0)

    # dritter Random Forest
    from sklearn.ensemble import RandomForestClassifier
    rf3 = RandomForestClassifier(n_estimators = 15, max_depth = 8, max_features = 20, random_state = 0)
    rf3.fit(X_train, y_train)

    # evaluate the model
    cv_rf1 = cross_val_score(rf3, X_train, y_train, cv = 5)
    print('Random Forest Model mit eigenen Daten')
    print(f'\nCross-validation scores:', ', '.join(map(str, cv_rf1)))
    print(f'\nMean cross-validation score: {cv_rf1.mean():.2f}')

    dump(rf3,"new_model.pkl")

    return cv_rf1
    
if __name__ == '__main__':
    own_data = get_self_created_flow_data()
    trainingdata = merge_own_flows_into_trainigdataset(own_data=own_data)
    processed_data, scaler, ipca, ipca_size  = adapt_cicids2017_for_training(data=trainingdata, balance_the_data=False)
    train_the_model(processed_data)
