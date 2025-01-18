from elastic_connector import get_all_flows, get_training_dataset
from pandas import DataFrame, concat
from sklearn.model_selection import cross_val_score, train_test_split
from joblib import dump

def get_self_created_flow_data() -> DataFrame:
    data = get_all_flows(onlyunseen= False, size=None) # TODO size=None has not been tested by me yet, but looks okay in the sourcecode
    for_retraining = DataFrame()
    for df in data:
        if df["has_been_seen"]: # maybe this is redundant if we use the not classified text in attack_class
            for_retraining.add(df[['flow_data','attack_class']])
    return for_retraining

def merge_own_flows_into_trainigdataset(own_data:DataFrame):
    trainingdata = get_training_dataset()
    added_classes = own_data['attack_type'].value_counts()
    class_names = added_classes.index
    selected = trainingdata[trainingdata['attack_type'].isin(class_names)] # unnecessary?

    dfs = []
    for name in class_names:
        # Extrahiere Daten für jede Klasse
        df = selected[selected['attack_type'] == name]
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

    dump(rf3,"model.pkl")

    return cv_rf1
    
if __name__ == '__main__':
    own_data = get_self_created_flow_data()
    trainingdata = merge_own_flows_into_trainigdataset(own_data=own_data)
    train_the_model(trainingdata)
