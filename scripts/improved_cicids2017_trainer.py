import time
from sklearn.decomposition import IncrementalPCA
from sklearn.discriminant_analysis import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV, cross_val_score, train_test_split
import pandas as pd
from imblearn.over_sampling import SMOTE
from adapt import adapt_for_prediction, adapt_for_retraining, adapt_cicids2017_for_training
import joblib
import os
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 
from sklearn.ensemble import RandomForestClassifier


CREAT_FIGS = False
removed_columns = ['id', 'Flow ID','Src IP', 'Dst IP', 'Timestamp', ] # these wont only serve for overfitting the model 
columns = [ 'Src Port', 'Dst Port', 'Protocol',
       'Flow Duration', 'Total Fwd Packet', 'Total Bwd packets',
       'Total Length of Fwd Packet', 'Total Length of Bwd Packet',
       'Fwd Packet Length Max', 'Fwd Packet Length Min',
       'Fwd Packet Length Mean', 'Fwd Packet Length Std',
       'Bwd Packet Length Max', 'Bwd Packet Length Min',
       'Bwd Packet Length Mean', 'Bwd Packet Length Std', 'Flow Bytes/s',
       'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max',
       'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std',
       'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean',
       'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags',
       'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'Fwd RST Flags',
       'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length',
       'Fwd Packets/s', 'Bwd Packets/s', 'Packet Length Min',
       'Packet Length Max', 'Packet Length Mean', 'Packet Length Std',
       'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count',
       'RST Flag Count', 'PSH Flag Count', 'ACK Flag Count', 'URG Flag Count',
       'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio',
       'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg',
       'Fwd Bytes/Bulk Avg', 'Fwd Packet/Bulk Avg', 'Fwd Bulk Rate Avg',
       'Bwd Bytes/Bulk Avg', 'Bwd Packet/Bulk Avg', 'Bwd Bulk Rate Avg',
       'Subflow Fwd Packets', 'Subflow Fwd Bytes', 'Subflow Bwd Packets',
       'Subflow Bwd Bytes', 'FWD Init Win Bytes', 'Bwd Init Win Bytes',
       'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std',
       'Active Max', 'Active Min', 'Idle Mean', 'Idle Std', 'Idle Max',
       'Idle Min', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time', 'Label',
       'Attempted Category']

# These startparameters are only used to find best params for the RFC once!
# They are based on previous experiences...
start_parameters = {'bootstrap': [True, False],
     'max_depth': [30, 40, 50, 60, 65, 70, 75, 80, 90, 100, None],
     'max_features': ['log2', 'sqrt'],
     'min_samples_leaf': [1, 2, 4],
     'min_samples_split': [2, 5, 10],
     'n_estimators': [400, 600, 700, 750, 800, 850, 900, 1000, 1200, 1400]}

def load_data(directory:str, cutoff:int) -> pd.DataFrame:
    csv_files = {}
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            
            try:
                # read csv file
                df = pd.read_csv(file_path)
                if len(df) > cutoff:
                    print(f"read: {filename}")
                    # Save DataFrame to dictionary
                    csv_files[df["Label"].unique()[0]] = df
                else: 
                    print(f"omitted file {filename} because it has less than {cutoff} flows")
            except Exception as e:
                print(f"Error on file {filename}: {str(e)}")
    
    return pd.concat(csv_files, ignore_index=True )




def scale_and_pca(data:pd.DataFrame) -> tuple:
    # Scale The Dataset
    X = data.drop('Label', axis=1)
    y = data['Label']
    scaler = StandardScaler()
    scaled_X = scaler.fit_transform(X)
    # Principal Component Analysis
    ipca_size = 34 # Magic
    ipca = IncrementalPCA(n_components = ipca_size, batch_size = 500)
    for batch in np.array_split(scaled_X, len(X) // 500):
        ipca.partial_fit(batch)
    print(f'information retained: {sum(ipca.explained_variance_ratio_):.2%}')
    transformed_X = ipca.transform(scaled_X)
    new_data = pd.DataFrame(transformed_X, columns = [f'PC{i+1}' for i in range(ipca_size)])
    new_data['Label'] = y.values
    return new_data, scaler, ipca

def upsample_the_dataset(dataset:pd.DataFrame)-> pd.DataFrame:    
    X = dataset.drop('Label', axis=1)
    y = dataset['Label']
    smote = SMOTE(sampling_strategy='auto', random_state=0)
    X_upsampled, y_upsampled = smote.fit_resample(X, y)
    blnc_data = pd.DataFrame(X_upsampled)
    blnc_data['attack_type'] = y_upsampled
    return blnc_data

def train_random_forest(data:pd.DataFrame, params:dict = None) -> tuple:
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
    if params != None:
        rf = RandomForestClassifier(n_estimators = params["n_estimators"], max_depth = params["max_depth"], 
                                    max_features = params["max_features"], min_samples_split = params['min_samples_split'], 
                                    min_samples_leaf= params['min_samples_leaf'], bootstrap= params['bootstrap'], random_state = 0)
    else:    
        rf = RandomForestClassifier(n_estimators = 15, max_depth = 8, max_features = 20, random_state = 0)
    start = time.time()
    rf.fit(X_train, y_train)
    end = time.time()
    print(f"Trainingduration: {end - start} seconds")
    return rf, X_train, y_train, X_test, y_test


# Create Confusion Matrix
def create_confusion_matrix(model, X_test, y_test) -> np.ndarray:
    y_pred_rf = model.predict(X_test)
    return confusion_matrix(y_test, y_pred_rf)

def create_figure(conf_matrix:np.ndarray, model) -> plt:
    plt.figure(figsize=(8, 7))  
    sns.heatmap(conf_matrix, annot=True, cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted label')
    plt.ylabel('True label')
    plt.tight_layout()
    return plt


# Create Metrics-Diagramm
def create_metrics_overview(model, X_test, y_test) -> plt:
    target_names = model.classes_
    y_pred_rf = model.predict(X_test)
    metrics = classification_report(y_true = y_test, y_pred = y_pred_rf, target_names = target_names, output_dict = True)
    precision = [metrics[target_name]['precision'] for target_name in target_names]
    recall = [metrics[target_name]['recall'] for target_name in target_names]
    f1_score = [metrics[target_name]['f1-score'] for target_name in target_names]
    data = np.array([precision, recall, f1_score])
    rows = ['Precision', 'Recall', 'F1-score']
    print(metrics)
    plt.figure(figsize = (14, 6))
    sns.heatmap(data, cmap = 'Reds', annot = True, fmt = '.2f', xticklabels = model.classes_, yticklabels = rows)
    plt.title('Classification Report')
    plt.tight_layout()
    return plt

def get_params_for_RandomForestClassifier(X_train, y_train):
    rf = RandomForestClassifier()
    rf_random = RandomizedSearchCV(estimator = rf, param_distributions = start_parameters, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
    rf_random.fit(X_train, y_train)
    print(f"Best parameters for RandomForestClassifier are :{rf_random.best_params_}")
    return rf_random.best_params_



if __name__ == '__main__':
    # load Data 
    raw_dataset =  load_data("nids-daten/sampled_CICIDS2017_improved_rnd_5000", 2000)

    # because of very sparse values we remove following columns
    sparse_columns = ['Bwd URG Flags', 'CWR Flag Count', 'ECE Flag Count', 'Subflow Bwd Packets', 'Attempted Category']
    useable_columns = [c for c in columns if c not in sparse_columns]
    raw_dataset = raw_dataset[useable_columns]

    # Check for Duplicates
    dups = raw_dataset[raw_dataset.duplicated()]
    print(f'Number of duplicates: {len(dups)}')
    missing_val = raw_dataset.isna().sum()
    print(missing_val.loc[missing_val > 0])
    print(f'Initial missing values: {raw_dataset.isna().sum().sum()}')
    # Dropping columns with only one unique value
    num_unique = raw_dataset.nunique()
    one_variable = num_unique[num_unique == 1]
    not_one_variable = num_unique[num_unique > 1].index

    dropped_cols = one_variable.index
    data = raw_dataset[not_one_variable]
    print(f'Dropped columns: {dropped_cols}')
    new_data, scaler, ipca = scale_and_pca(data)
    data = upsample_the_dataset(new_data) # This Data could be stored in a pkl file for later use...
    rf, X_train, y_train, X_test, y_test = train_random_forest(data)
    start = time.time()    
    print(cross_val_score(rf, X_train, y_train)) # mean 0.978429628 bei 3.590430974960327 s training
    end = time.time()
    print(f"Evaluationtime {end - start}")
    joblib.dump(rf, "scripts/model.pkl")
    joblib.dump(scaler, "scripts/scaler.pkl")
    joblib.dump(ipca, "scripts/ipca.pkl")
    pd.DataFrame.to_csv(data, "scripts/balanced_dataset_cicids201_improved.csv")
    # get_params_for_RandomForestClassifier(X_train, y_train) # returned {'n_estimators': 1400, 'min_samples_split': 5, 'min_samples_leaf': 1, 'max_features': 'log2', 'max_depth': 90, 'bootstrap': False}
    # best_params = {'n_estimators': 1400, 'min_samples_split': 5, 'min_samples_leaf': 1, 'max_features': 'log2', 'max_depth': 90, 'bootstrap': False}
    # rf, X_train, y_train, X_test, y_test = train_random_forest(data, best_params)
    # start = time.time()
    # print(cross_val_score(rf, X_train, y_train)) # mean 0.9875259279999999 bei 187.25912809371948 s training 
    # end = time.time()
    # print(f"Evaluationtime {end - start}")
    # Just pics following
    if CREAT_FIGS:
        cm = create_confusion_matrix(rf, X_test, y_test)
        confusion_matrix_fig = create_figure(cm, rf)
        confusion_matrix_fig.savefig("new_cicids2017_improved_random_forest_5000_classifier.png")
        confusion_matrix_fig.show()
    if CREAT_FIGS:
        metrics_overview = create_metrics_overview(model=rf, X_test=X_test, y_test=y_test)
        metrics_overview.savefig("new_cicids2017_improved_random_forest_5000_metrics_overview.png")
        metrics_overview.show()
