import asyncio
from datetime import datetime
from os import makedirs
from shutil import copyfile
from elastic_connector import CustomElasticsearchConnector
from pandas import DataFrame, concat, read_csv
from sklearn.model_selection import cross_val_score, train_test_split
from joblib import dump, load
from numpy import ndarray, append
from pipelining_utilities import adapt_cicids2017_for_training
import zipfile
from sklearn.metrics import precision_recall_fscore_support as f_score
from sklearn.metrics import accuracy_score
import hashlib
import io



DEBUGGING = True
ZIPFILE_NAME = "multiphase_model_scaler_ipca.zip"


def get_self_created_flow_data() -> DataFrame:
    """
    Fetches self-created flow data from Elasticsearch.

    Returns:
        DataFrame: A DataFrame containing flow data that has been seen, 
                    with the 'attack_class' column renamed to 'attack_type'.
    """
    CEC = CustomElasticsearchConnector() 
    data = asyncio.run(CEC.get_all_flows(view="seen" , exclude_pcap_data=True, size=None))
    for_retraining = data[data["has_been_seen"] == "true"][['flow_data','attack_class']]
    return for_retraining.rename(columns={'attack_class': 'attack_type'})

def merge_own_flows_into_trainigdataset_for_multiclassifier(own_data:DataFrame):
    """
    Merges self-created flow data into the training dataset. Classes are sampled to the size of 5000 but 
    do always include the selfcreated flows.

    Args:
        own_data (DataFrame): DataFrame containing self-created flow data.

    Returns:
        DataFrame: A DataFrame containing the merged training dataset. Class size is 5000.
    """
    trainingdata = load("datasources/DataFrame_with_balanced_dataset.pkl") # load("DataFrame_with_balanced_dataset.pkl")
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
    
    # Combine all classes
    df = concat(dfs, ignore_index = True)
    df.sample(frac=1)
    return df

def merge_own_flows_into_trainigdataset_for_binarylassifier(own_data:DataFrame):
    """
    Merges self-created flow data into the training dataset. Classes are sampled to the size of the bigger class but 
    do always include the selfcreated flows. This is for a binary classifier (Attack/No Attack).

    Args:
        own_data (DataFrame): DataFrame containing self-created flow data.

    Returns:
        DataFrame: A DataFrame containing the merged training dataset. Two classes are returned labeled ATTACK and BENIGN
    """
    trainingdata = load("scripts/data_sources/binary_dataset_unscaled.pkl")    # This dataset is already balanced to have a many benign as attack flows
    mapping = {'DDoS': 'ATTACK', 'DoS': 'ATTACK', 'Port Scan': 'ATTACK', 'Bot': 'ATTACK', 'BENIGN': 'benign', 'Brute Force': 'ATTACK', 'Web Attack': 'ATTACK'}
    own_data = own_data['attack_type'].replace(mapping)

    added_classes = own_data['attack_type'].value_counts()
    # class_names = added_classes.index.str.lower()
    # selected = trainingdata[trainingdata['attack_type'].isin(added_classes)] # unnecessary?

    dfs = []

    diff_benign_attack = added_classes["BENIGN"] - added_classes["ATTACK"] 
    

    if diff_benign_attack == 0:
        df = trainingdata
        df.add(own_data)
        dfs.append(df)
    elif diff_benign_attack > 0: # more benign flows than attack
        df = trainingdata[trainingdata['attack_type'] == "BENIGN"]
        n = len(trainingdata)/2 - diff_benign_attack # half the trainingdata is benign
        df = df.sample(n=n, random_state=0)
        df.add(own_data[own_data["BENIGN"]])
        dfs.append(df)
        df = trainingdata[trainingdata["attack_type"] == "ATTACK"]
        df.add(own_data[own_data["ATTACK"]])
        dfs.append(df)
    else:   # more attack flows than benign
        df = trainingdata[trainingdata['attack_type'] == "ATTACK"]
        n = len(trainingdata)/2 + diff_benign_attack # half the trainingdata is benign
        df = df.sample(n=n, random_state=0)
        df.add(own_data[own_data["ATTACK"]])
        dfs.append(df)
        df = trainingdata[trainingdata["attack_type"] == "BENIGN"]
        df.add(own_data[own_data["BENIGN"]])
        dfs.append(df)

    
    # Combine all classes
    df = concat(dfs, ignore_index = True)
    df.sample(frac=1)
    return df


def train_random_forest(data:DataFrame) -> tuple:
    """
    Trains a Random Forest model on the provided data.

    Args:
        data (DataFrame): The training data.

    Returns:
        tuple: A tuple containing the trained model, training features, training labels test features (X_test) and test labels (y_test).

    """
    # split data without type of attack
    features = data.drop('attack_type', axis = 1)
    labels = data['attack_type']
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size = 0.25, random_state = 0)

    # Random Forest
    from sklearn.ensemble import RandomForestClassifier
    rf = RandomForestClassifier(n_estimators = 15, max_depth = 8, max_features = 20, random_state = 0)
    rf.fit(X_train, y_train)

    return rf, X_train, y_train, X_test, y_test

def train_random_forest_for_binary(data:DataFrame) -> tuple:
    """
    Trains a Random Forest model for binary classification and optimised for best recall scores on the provided data.

    Args:
        data (DataFrame): The training data.

    Returns:
        tuple: A tuple containing the trained model, training features, training labels test features (X_test) and test labels (y_test).

    """
    # split data without type of attack
    features = data.drop('attack_type', axis = 1)
    labels = data['attack_type']
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size = 0.25, random_state = 0)

    # Random Forest
    from sklearn.ensemble import RandomForestClassifier
    rf = RandomForestClassifier(n_estimators = 750, min_samples_split= 2, min_samples_leaf = 1, max_features= 'sqrt', max_depth= 75, bootstrap= False)
    rf.fit(X_train, y_train)

    return rf, X_train, y_train, X_test, y_test

def train_random_forest_for_multiclass(data:DataFrame) -> tuple:
    """
    Trains a Random Forest model for multiclass classification and optimised for best accuracy scores on the provided data.

    Args:
        data (DataFrame): The training data.

    Returns:
        tuple: A tuple containing the trained model, training features, training labels test features (X_test) and test labels (y_test).

    """
    # split data without type of attack
    features = data.drop('attack_type', axis = 1)
    labels = data['attack_type']
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size = 0.25, random_state = 0)

    # Random Forest
    from sklearn.ensemble import RandomForestClassifier
    rf = RandomForestClassifier(n_estimators = 1400, min_samples_split= 5, min_samples_leaf = 1, max_features= 'sqrt', max_depth= 75, bootstrap= True)
    rf.fit(X_train, y_train)

    return rf, X_train, y_train, X_test, y_test


def evaluate_model(model, X_train, y_train):
    """
        Evaluates the model using cross-validation.

        Args:
            model: The trained model.
            X_train: The training features.
            y_train: The training labels.

        Returns:
            ndarray: Cross-validation scores.
    """    
    
    cv_model = cross_val_score(model, X_train, y_train, cv = 5)
    cv_model_f1 = cross_val_score(model, X_train, y_train, cv = 5,  scoring='f1_macro')
    if DEBUGGING:
        print('Random Forest Model mit eigenen Daten')
        print(f'\nCross-validation scores:', ', '.join(map(str, cv_model)))
        print(f'\nMean cross-validation score: {cv_model.mean():.2f}')
        print(f'\nF1 scores:', ', '.join(map(str, cv_model_f1)))
        print(f"\nF1 score mean: {cv_model_f1.mean():.2f}")
    return cv_model.mean()

def get_f1_score(model, X_test, y_test):
    predicted = model.predict(X_test)
    precision, recall, fscore, support = f_score(y_test, predicted)
    return fscore


def create_transferrable_zipfile(elastic_id, model, scaler, ipca):
    """
    Creates a zip file containing the model, scaler, and IPCA.

    Args:
        elastic_id: the id with wich this model is stored.
        model: The trained model.
        scaler: The scaler used for preprocessing.
        ipca: The IPCA used for dimensionality reduction.
    """

    files = {"model":model, "scaler":scaler, "ipca":ipca}
    
    # to store old models
    archive_dir = "old_models"
    makedirs(archive_dir, exist_ok = True)

    # create zipfile
    zf = zipfile.ZipFile("model_scaler_ipca.zip", "w")

    for f in files:
        # dump new file
        dump(files[f],f"{f}.pkl")
        # write file to zip
        zf.write(f"{f}.pkl")
    zf.close()
    # Copy the model to archive with the name of the ip of the elastic document
    copyfile(zf.filename, f"{archive_dir}/{elastic_id}.zip")

def create_transferrable_multiphase_classifier_zipfile(binary_model, binary_scaler, binary_ipca, 
                                                       multi_model, multi_scaler, multi_ipca):
    """
    Creates a zip file containing two models, two scalers, and two IPCAs.

    Args:
        elastic_id: the id with wich this model is stored.
        binary_model: The trained model for binary Classification.
        binary_scaler: The scaler used for preprocessing for binary_model.
        binary_ipca: The IPCA used for dimensionality reduction for binary_model.
        multi_model: The trained model for multiclass Classification.
        multi_scaler: The scaler used for preprocessing for multi_model.
        multi_ipca: The IPCA used for dimensionality reduction for multi_model.
    """
    files = {"binary_model":binary_model, "binary_scaler":binary_scaler, "binary_ipca":binary_ipca, 
             "multi_model":multi_model, "multi_scaler":multi_scaler, "multi_ipca":multi_ipca}
    
    # create zipfile
    zf = zipfile.ZipFile(ZIPFILE_NAME, "w")

    for f in files:
        # dump new file
        dump(files[f],f"{f}.pkl")
        # write file to zip
        zf.write(f"{f}.pkl")
    zf.close()
    m = hashlib.sha256()
    with io.BytesIO() as memf:
        dump(zf, memf)
        m.update(memf.getvalue())
    return m.hexdigest()
def archive_zipfile(elastic_id):
    # to store old models
    archive_dir = "old_models"
    makedirs(archive_dir, exist_ok = True)

    # Copy the model to archive with the name of the ip of the elastic document
    copyfile(ZIPFILE_NAME, f"{archive_dir}/{elastic_id}.zip")

def compute_model_hash(model) -> str:
        """Compute the hash of the model without writing it to disk using the sha265 algorithm.
        
        Args:
            - model = the trained model
        
        Returns:
            str: The hash value
        """
        
        m = hashlib.sha256()
        with io.BytesIO() as memf:
            dump(model, memf)
            m.update(memf.getvalue())
        return m.hexdigest()

def get_score_of_multimodel_classifier(binary_model, binary_X_test, binary_y_test, multi_model, mutli_X_test, mutli_y_test):
    b_predicted = binary_model.predict(binary_X_test)
    precision, recall, fscore, support = f_score(binary_y_test, b_predicted)
    print(f"Recall of binary classifier is {recall}")
    a_predicted = multi_model.predict(mutli_X_test)
    accuracy = accuracy_score(mutli_y_test, a_predicted)
    print(f"Accuracy of multi classifier is {accuracy}")
    recall_accuracy_mean = append(accuracy, recall[0]).mean()
    print(f"Mean of recall of benign and accuracy of all: {recall_accuracy_mean}")
    return recall_accuracy_mean

def retrain() -> ndarray:
    """
    Retrains the model using self-created flow data.

    Returns:
        ndarray: Cross-validation scores of the retrained model.
    """
    own_data = get_self_created_flow_data()
    merged_and_balanced_data = merge_own_flows_into_trainigdataset_for_multiclassifier(own_data=own_data)
    processed_data, scaler, ipca, ipca_size  = adapt_cicids2017_for_training(data=merged_and_balanced_data, balance_the_data=False)
    model, X_train, y_train, X_test, y_test = train_random_forest(processed_data)
    score = get_f1_score(model, X_test, y_test)
    own_flow_count = own_data.shape[0]
    model_hash = compute_model_hash(model)
    cec = CustomElasticsearchConnector()
    elastic_id = asyncio.run(cec.save_model_properties(hash_value=model_hash, timestamp=datetime.now(), own_flow_count=own_flow_count, score=score))
    create_transferrable_zipfile(elastic_id, model, scaler, ipca)
    return evaluate_model(model, X_train, y_train)

def retrain_multimodel_classifiers():
    own_data = get_self_created_flow_data()
    binary_merged_and_balanced_data = merge_own_flows_into_trainigdataset_for_binarylassifier(own_data=own_data)
    binary_processed_data, binary_scaler, binary_ipca, ipca_size  = adapt_cicids2017_for_training(data=binary_merged_and_balanced_data, balance_the_data=False)
    binary_model, binary_X_train, binary_y_train, binary_X_test, binary_y_test = train_random_forest_for_binary(binary_processed_data)
    multi_merged_and_balanced_data = merge_own_flows_into_trainigdataset_for_multiclassifier(own_data=own_data)
    multi_processed_data, multi_scaler, multi_ipca, ipca_size  = adapt_cicids2017_for_training(data=multi_merged_and_balanced_data, balance_the_data=False)
    multi_model, multi_X_train, multi_y_train, multi_X_test, multi_y_test = train_random_forest_for_multiclass(data=multi_processed_data)
    score = get_score_of_multimodel_classifier(binary_model=binary_model, binary_X_test=binary_X_test, binary_y_test=binary_y_test, 
                                       multi_model=multi_model, mutli_X_test=multi_X_test, mutli_y_test=multi_y_test)
    own_flow_count = own_data.shape[0]
    zip_hash = create_transferrable_multiphase_classifier_zipfile(binary_model=binary_model, binary_scaler=binary_scaler, binary_ipca=binary_ipca, 
                                                       multi_model=multi_model, multi_scaler=multi_scaler, multi_ipca=multi_ipca)
    cec = CustomElasticsearchConnector()    
    elastic_id = asyncio.run(cec.save_model_properties(hash_value=zip_hash, timestamp=datetime.now(), own_flow_count=own_flow_count, score=score))
    archive_zipfile(elastic_id)
    return score

if __name__ == '__main__':
    retrain_multimodel_classifiers()