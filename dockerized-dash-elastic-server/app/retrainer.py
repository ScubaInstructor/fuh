import asyncio
from datetime import datetime
from os import makedirs
from shutil import copyfile
from .elastic_connector import CustomElasticsearchConnector
from pandas import DataFrame, concat, json_normalize, read_csv
from sklearn.model_selection import cross_val_score, train_test_split
from joblib import dump, load
from numpy import ndarray
from .pipelining_utilities import adapt_cicids2017_for_training, COLUMNS
import zipfile
from sklearn.metrics import precision_recall_fscore_support as f_score
from sklearn.metrics import accuracy_score as ascore

from .model_visualisations import Model_Visualisator
from . import MODELPATH, MODELARCHIVEPATH, MODELNAME, APPPATH, ZIPFILENAME

DEBUGGING = True

def get_self_created_flow_data() -> DataFrame:
    """
    Fetches self-created flow data from Elasticsearch.

    Returns:
        DataFrame: A DataFrame containing flow data that has been seen, 
                    with the 'attack_class' column renamed to 'attack_type'.
    """
    CEC = CustomElasticsearchConnector() 
    data = asyncio.run(CEC.get_all_flows(view="seen", size=10000))
    if len(data) > 0:
        for_retraining = data[data["has_been_seen"] == True][['flow_data','attack_class']]
        return for_retraining.rename(columns={'attack_class': 'attack_type'})
    else: 
        return DataFrame()

def merge_own_flows_into_trainigdataset_for_multiclassifier(own_data:DataFrame):
    """
    Merges self-created flow data into the training dataset. Classes are sampled to the size of 5000 but 
    do always include the selfcreated flows.

    Args:
        own_data (DataFrame): DataFrame containing self-created flow data.

    Returns:
        DataFrame: A DataFrame containing the merged training dataset. Class size is 5000.
    """
    # TODO paths must be fixed someday
    trainingdata = read_csv(APPPATH + "/datasources/balanced_dataset_cicids201_improved.csv")
    trainingdata = trainingdata.rename(columns={"label": "attack_type"}) # From here on the attack_type is used.
    attacks = trainingdata["attack_type"]
    trainingdata = trainingdata[COLUMNS]
    trainingdata["attack_type"] = attacks
    if len(own_data) == 0:
        df =  trainingdata
    else:
        added_classes = own_data['attack_type'].str.lower().value_counts()
        class_names = added_classes.index.str.lower()
        #selected = trainingdata[trainingdata['attack_type'].str.lower().isin(class_names.str.lower())] # unnecessary?

        dfs = []

        # TODO check for namedifferences in newly classified flows

        for name in class_names:
            # Extrahiere Daten für jede Klasse
            df = trainingdata[trainingdata['attack_type'].str.lower() == name]
            # sample down to make space for own flow data
            n = max(5000 - added_classes[name], 0)
            df = df.sample(n=n, random_state=0)
            # add own flows of respective group
            own_flows_of_same_class = own_data[own_data['attack_type'].str.lower()==name]
            own_flows_of_same_class.reset_index(drop=True, inplace=True)
            addition = concat([own_flows_of_same_class[['attack_type']], json_normalize(own_flows_of_same_class['flow_data'])], axis=1)
            addition = addition[COLUMNS + ['attack_type'] ]
            df = df[COLUMNS + ['attack_type'] ]
            df = concat([df, addition], ignore_index=True)
            dfs.append(df)
        
        all_classes = trainingdata['attack_type'].unique().tolist()
        remaining_classes = [cls for cls in all_classes if cls.lower() not in class_names] 
        for name in remaining_classes:
            # Extrahiere Daten für jede Klasse
            df = trainingdata[trainingdata['attack_type'].str.lower() == name.lower()]
            df = df[COLUMNS + ['attack_type'] ]
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
    makedirs(APPPATH +MODELARCHIVEPATH, exist_ok = True)

    # create zipfile
    zf = zipfile.ZipFile(APPPATH +MODELPATH + ZIPFILENAME, "w")

    for f in files:
        # dump new file
        dump(files[f],f"{f}.pkl")
        # write file to zip
        zf.write(f"{f}.pkl")
    zf.close()
    # Copy the model to archive with the name of the ip of the elastic document
    copyfile(zf.filename, f"{APPPATH + MODELARCHIVEPATH}/{elastic_id}.zip")

def compute_model_hash(model) -> str:
        """Compute the hash of the model without writing it to disk using the sha265 algorithm.
        
        Args:
            - model = the trained model
        
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

def create_boxplot_data_for_elastic(mergeddata):
    """
    Transform Boxplot Data to elasticsearch storeable format.
    """

    def _create_metrics_list(data):
        """
        Creates a list of mertic objects
        """
        metrics = []
        
        # Hilfsfunktion, um eine Liste von Dictionaries für eine Metrik zu erstellen
        def create_metric_data(metric_name, data_series):
            metric_data = {}
            for c in data_series.columns:
                metric_data[c] = data_series[c]
            return metric_data

        # Berechne die verschiedenen Metriken
        metrics.append({"metric_name": "mean", **create_metric_data("mean", data.mean(numeric_only=True).to_frame().T)})
        metrics.append({"metric_name": "min", **create_metric_data("min", data.min(numeric_only=True).to_frame().T)})
        metrics.append({"metric_name": "max", **create_metric_data("max", data.max(numeric_only=True).to_frame().T)})
        metrics.append({"metric_name": "q1", **create_metric_data("q1", data.quantile(0.25, numeric_only=True).to_frame().T)})
        metrics.append({"metric_name": "median", **create_metric_data("median", data.median(numeric_only=True).to_frame().T)})
        metrics.append({"metric_name": "q3", **create_metric_data("q3", data.quantile(0.75, numeric_only=True).to_frame().T)})
        
        return metrics

    result = []
    
    # For complete Dataset
    analysis_data_complete = mergeddata.drop(["attack_type","ip_dst_prt"], axis=1)
    metrics_complete = _create_metrics_list(analysis_data_complete)
    result.append({"class": "complete", "metrics": metrics_complete})
    
    # By class
    classes = list(mergeddata["attack_type"].unique())
    for c in classes:
        class_data = mergeddata[mergeddata["attack_type"]==c].drop(["attack_type","ip_dst_prt"], axis=1)
        metrics_class = _create_metrics_list(class_data)
        result.append({"class": c, "metrics": metrics_class})
    
    return result

def retrain() -> str:
    """
    Retrains the model using self-created flow data. Stores the model as {elastic_id}.zip in the modelarchive, and sets the new model hash.

    Returns:
        str: the new hashvalue
    """
    own_data = get_self_created_flow_data()
    mergeddata = merge_own_flows_into_trainigdataset_for_multiclassifier(own_data=own_data)
    processed_data, scaler, ipca, ipca_size  = adapt_cicids2017_for_training(data=mergeddata, balance_the_data=False)
    model, X_train, y_train, X_test, y_test = train_random_forest(processed_data)
    predicted = model.predict(X_test)
    score = ascore(y_test,predicted)
    own_flow_count = own_data.shape[0]
    model_hash = compute_model_hash(model)
    dump(model,  APPPATH + MODELPATH + MODELNAME)
    # prepare Model Propertis for elastic
    boxplotdata = create_boxplot_data_for_elastic(mergeddata)
    mv = Model_Visualisator()
    cm = mv.create_confusion_matrix(model, X_test, y_test)   
    cm_data_as_list = mv.create_storeable_list_from_cunfusion_matrix(cm, classes=list(model.classes_))
    metrics = mv.create_metrics_list_for_storing_in_elastic(model, X_test, y_test) 
    # Save model and properties to elastic
    cec = CustomElasticsearchConnector()
    elastic_id = asyncio.run(cec.save_model_properties(hash_value=model_hash, timestamp=datetime.now(), 
                                                       own_flow_count=own_flow_count, score=score, 
                                                       confusion_matrix_data=cm_data_as_list, class_metric_data=metrics, boxplotdata=boxplotdata))
    create_transferrable_zipfile(elastic_id, model, scaler, ipca)
    return model_hash



if __name__ == '__main__':
    #retrain()
    x = get_self_created_flow_data()
    print(x)