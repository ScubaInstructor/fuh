import asyncio
from datetime import datetime
import hashlib
from os import makedirs, rename
from shutil import copyfile
from elastic_connector import CustomElasticsearchConnector
from pandas import DataFrame, concat, read_csv
from sklearn.model_selection import cross_val_score, train_test_split
from joblib import dump, load
from numpy import ndarray
from pipelining_utilities import adapt_for_retraining, adapt_cicids2017_for_training
import zipfile
from sklearn.metrics import precision_recall_fscore_support as f_score


DEBUGGING = True

def get_self_created_flow_data() -> DataFrame:
    """
    Fetches self-created flow data from Elasticsearch.

    Returns:
        DataFrame: A DataFrame containing flow data that has been seen, 
                    with the 'attack_class' column renamed to 'attack_type'.
    """
    CEC = CustomElasticsearchConnector() 
    data = asyncio.run(CEC.new_get_all_flows(onlyunseen= False, size=None)) # TODO THIS WILL BE DIFFERENT IN FUTURE CEC VERSIONS
    for_retraining = data[data["has_been_seen"] == "true"][['flow_data','attack_class']]
    return for_retraining.rename(columns={'attack_class': 'attack_type'})

def merge_own_flows_into_trainigdataset(own_data:DataFrame):
    """
    Merges self-created flow data into the training dataset. Classes are sampled to the size of 5000 but 
    to always include the selfcreated flows.

    Args:
        own_data (DataFrame): DataFrame containing self-created flow data.

    Returns:
        DataFrame: A DataFrame containing the merged training dataset. Class size is 5000.
    """
    trainingdata = load("server/flask/DataFrame_with_balanced_dataset.pkl") # load("DataFrame_with_balanced_dataset.pkl")
    added_classes = own_data['attack_type'].str.lower().value_counts()
    class_names = added_classes.index.str.lower()
    selected = trainingdata[trainingdata['attack_type'].str.lower().isin(class_names.str.lower())] # unnecessary?

    dfs = []

    # TODO check for namedifferences in newly classified flows

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
    
    # TODO assert all classes are 5000 entries strong

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

def compute_model_hash(model) -> str:
        """Compute the hash of a file using the sha265 algorithm.
        
        Args:
            - file_path (str) = the path to the file
        
        Returns:
            str: The hash value
        """
        import hashlib
        import io

        m = hashlib.sha256()
        with io.BytesIO() as memf:
            dump(model, memf)
            m.update(memf.getvalue())
        return m.hexdigest()

   
def retrain() -> ndarray:
    """
    Retrains the model using self-created flow data.

    Returns:
        ndarray: Cross-validation scores of the retrained model.
    """
    own_data = get_self_created_flow_data()
    mergeddata = merge_own_flows_into_trainigdataset(own_data=own_data)
    processed_data, scaler, ipca, ipca_size  = adapt_cicids2017_for_training(data=mergeddata, balance_the_data=False)
    model, X_train, y_train, X_test, y_test = train_random_forest(processed_data)
    score = get_f1_score(model, X_test, y_test)
    own_flow_count = own_data.shape[0]
    model_hash = compute_model_hash(model)
    from elastic_connector import CustomElasticsearchConnector
    cec = CustomElasticsearchConnector()
    elastic_id = asyncio.run(cec.save_model_properties(hash_value=model_hash, timestamp=datetime.now(), own_flow_count=own_flow_count, score=score))
    create_transferrable_zipfile(elastic_id, model, scaler, ipca)
    return evaluate_model(model, X_train, y_train)



if __name__ == '__main__':
    retrain()