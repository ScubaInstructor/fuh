import asyncio
from datetime import datetime
import time
from sklearn.decomposition import IncrementalPCA
from sklearn.discriminant_analysis import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import (
    RandomizedSearchCV,
    cross_val_score,
    train_test_split,
)
import pandas as pd
from imblearn.over_sampling import SMOTE
from app.elastic_connector import CustomElasticsearchConnector
from app.model_visualisations import Model_Visualisator
from app.retrainer import compute_model_hash, create_boxplot_data_for_elastic
import joblib
import os
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.ensemble import RandomForestClassifier


CREAT_FIGS = True
# removed_columns = ['id', 'Flow ID','Src IP', 'Dst IP', 'Timestamp', ] # these wont only serve for overfitting the model
# ['Bwd URG Flags', 'CWR Flag Count', 'ECE Flag Count', 'Subflow Bwd Packets', 'Attempted Category'] # These are empty and not anymore included in cleaned data
# columns = [ 'Src Port', 'Dst Port', 'Protocol',
#        'Flow Duration', 'Total Fwd Packet', 'Total Bwd packets',
#        'Total Length of Fwd Packet', 'Total Length of Bwd Packet',
#        'Fwd Packet Length Max', 'Fwd Packet Length Min',
#        'Fwd Packet Length Mean', 'Fwd Packet Length Std',
#        'Bwd Packet Length Max', 'Bwd Packet Length Min',
#        'Bwd Packet Length Mean', 'Bwd Packet Length Std', 'Flow Bytes/s',
#        'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max',
#        'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std',
#        'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean',
#        'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags',
#        'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'Fwd RST Flags',
#        'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length',
#        'Fwd Packets/s', 'Bwd Packets/s', 'Packet Length Min',
#        'Packet Length Max', 'Packet Length Mean', 'Packet Length Std',
#        'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count',
#        'RST Flag Count', 'PSH Flag Count', 'ACK Flag Count', 'URG Flag Count',
#        'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio',
#        'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg',
#        'Fwd Bytes/Bulk Avg', 'Fwd Packet/Bulk Avg', 'Fwd Bulk Rate Avg',
#        'Bwd Bytes/Bulk Avg', 'Bwd Packet/Bulk Avg', 'Bwd Bulk Rate Avg',
#        'Subflow Fwd Packets', 'Subflow Fwd Bytes', 'Subflow Bwd Packets',
#        'Subflow Bwd Bytes', 'FWD Init Win Bytes', 'Bwd Init Win Bytes',
#        'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std',
#        'Active Max', 'Active Min', 'Idle Mean', 'Idle Std', 'Idle Max',
#        'Idle Min', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time', 'Label',
#        'Attempted Category']

# old_mapping_for_columns = {"flow_id":"Flow ID","ip_src":"Src IP","ip_src_prt":"Src Port","ip_dst":"Dst IP",
# "ip_dst_prt":"Dst Port","protocol":"Protocol","str_time":"Timestamp","flow_duration":"Flow Duration","fwd_pkt_stats":"Total Fwd Packet",
# "bwd_pkt_stats":"Total Bwd packets","tot_l_fw_pkt":"Total Length of Fwd Packet","tot_l_bw_pkt":"Total Length of Bwd Packet","fw_pkt_l_max":"Fwd Packet Length Max",
# "fw_pkt_l_min":"Fwd Packet Length Min","fw_pkt_l_avg":"Fwd Packet Length Mean","fw_pkt_l_std":"Fwd Packet Length Std",
# "bw_iat_tot":"Bwd IAT Total","bw_iat_avg":"Bwd IAT Mean","bw_iat_std":"Bwd IAT Std","bw_iat_max":"Bwd IAT Max","bw_iat_min":"Bwd IAT Min",
# "fw_psh_flag":"Fwd PSH Flags","bw_psh_flag":"Bwd PSH Flags","fw_urg_flag":"Fwd URG Flags","bw_urg_flag":"Bwd URG Flags","fw_rst_flag":"Fwd RST Flags",
# "bw_rst_flag":"Bwd RST Flags","fw_hdr_len":"Fwd Header Length","bw_hdr_len":"Bwd Header Length","fw_pkt_s":"Fwd Packets/s","bw_pkt_s":"Bwd Packets/s",
# "pkt_len_min":"Packet Length Min","pkt_len_max":"Packet Length Max","pkt_len_avg":"Packet Length Mean","pkt_len_std":"Packet Length Std","pkt_len_va":"Packet Length Variance",
# "fin_cnt":"FIN Flag Count","syn_cnt":"SYN Flag Count","rst_cnt":"RST Flag Count","pst_cnt":"PSH Flag Count","ack_cnt":"ACK Flag Count","urg_cnt":"URG Flag Count",
# "cwe_cnt":"CWR Flag Count","ece_cnt":"ECE Flag Count","down_up_ratio":"Down/Up Ratio","pkt_size_avg":"Average Packet Size","fw_seg_avg":"Fwd Segment Size Avg",
# "bw_seg_avg":"Bwd Segment Size Avg","fw_byt_blk_avg":"Fwd Bytes/Bulk Avg","fw_pkt_blk_avg":"Fwd Packet/Bulk Avg","fw_blk_rate_avg":"Fwd Bulk Rate Avg","bw_byt_blk_avg":"Bwd Bytes/Bulk Avg",
# "bw_pkt_blk_avg":"Bwd Packet/Bulk Avg","bw_blk_rate_avg":"Bwd Bulk Rate Avg","subfl_fw_pk":"Subflow Fwd Packets","subfl_fw_byt":"Subflow Fwd Bytes","subfl_bw_pkt":"Subflow Bwd Packets",
# "subfl_bw_byt":"Subflow Bwd Bytes","fw_win_byt":"FWD Init Win Bytes","bw_win_byt":"Bwd Init Win Bytes","Fw_act_pkt":"Fwd Act Data Pkts","fw_seg_min":"Fwd Seg Size Min",
# "atv_avg":"Active Mean","atv_std":"Active Std","atv_max":"Active Max","atv_min":"Active Min","idl_avg":"Idle Mean","idl_std":"Idle Std","idl_max":"Idle Max",
# "idl_min":"Idle Min","icmp_code":"ICMP Code","icmp_type":"ICMP Type","cumulative_connection_duration":"Total TCP Flow Time","label":"Label"}


# Commented lines are only zero values ever and hence omitted
mapping_for_columns = {  # "Flow ID":"flow_id",
    # "Src IP":"src_ip",
    "Src Port": "src_port",
    # "Dst IP":"dst_ip",
    "Dst Port": "dst_port",
    "Protocol": "protocol",
    # "Timestamp":"timestamp",
    "Flow Duration": "flow_duration",
    "Total Fwd Packet": "total_fwd_packet",
    "Total Bwd packets": "total_bwd_packets",
    "Total Length of Fwd Packet": "total_length_of_fwd_packet",
    "Total Length of Bwd Packet": "total_length_of_bwd_packet",
    "Fwd Packet Length Max": "fwd_packet_length_max",
    "Fwd Packet Length Min": "fwd_packet_length_min",
    "Fwd Packet Length Mean": "fwd_packet_length_mean",
    "Fwd Packet Length Std": "fwd_packet_length_std",
    "Bwd Packet Length Max": "bwd_packet_length_max",
    "Bwd Packet Length Min": "bwd_packet_length_min",
    "Bwd Packet Length Mean": "bwd_packet_length_mean",
    "Bwd Packet Length Std": "bwd_packet_length_std",
    "Flow Bytes/s": "flow_bytes_s",
    "Flow Packets/s": "flow_packets_s",
    "Flow IAT Mean": "flow_iat_mean",
    "Flow IAT Std": "flow_iat_std",
    "Flow IAT Max": "flow_iat_max",
    "Flow IAT Min": "flow_iat_min",
    "Fwd IAT Total": "fwd_iat_total",
    "Fwd IAT Mean": "fwd_iat_mean",
    "Fwd IAT Std": "fwd_iat_std",
    "Fwd IAT Max": "fwd_iat_max",
    "Fwd IAT Min": "fwd_iat_min",
    "Bwd IAT Total": "bwd_iat_total",
    "Bwd IAT Mean": "bwd_iat_mean",
    "Bwd IAT Std": "bwd_iat_std",
    "Bwd IAT Max": "bwd_iat_max",
    "Bwd IAT Min": "bwd_iat_min",
    "Fwd PSH Flags": "fwd_psh_flags",
    "Bwd PSH Flags": "bwd_psh_flags",
    "Fwd URG Flags": "fwd_urg_flags",
    # "Bwd URG Flags":"bwd_urg_flags",
    "Fwd RST Flags": "fwd_rst_flags",
    "Bwd RST Flags": "bwd_rst_flags",
    "Fwd Header Length": "fwd_header_length",
    "Bwd Header Length": "bwd_header_length",
    "Fwd Packets/s": "fwd_packets_s",
    "Bwd Packets/s": "bwd_packets_s",
    "Packet Length Min": "packet_length_min",
    "Packet Length Max": "packet_length_max",
    "Packet Length Mean": "packet_length_mean",
    "Packet Length Std": "packet_length_std",
    "Packet Length Variance": "packet_length_variance",
    "FIN Flag Count": "fin_flag_count",
    "SYN Flag Count": "syn_flag_count",
    "RST Flag Count": "rst_flag_count",
    "PSH Flag Count": "psh_flag_count",
    "ACK Flag Count": "ack_flag_count",
    "URG Flag Count": "urg_flag_count",
    # "CWR Flag Count":"cwr_flag_count",
    # "ECE Flag Count":"ece_flag_count",
    "Down/Up Ratio": "down_up_ratio",
    "Average Packet Size": "average_packet_size",
    "Fwd Segment Size Avg": "fwd_segment_size_avg",
    "Bwd Segment Size Avg": "bwd_segment_size_avg",
    "Fwd Bytes/Bulk Avg": "fwd_bytes_bulk_avg",
    "Fwd Packet/Bulk Avg": "fwd_packet_bulk_avg",
    "Fwd Bulk Rate Avg": "fwd_bulk_rate_avg",
    "Bwd Bytes/Bulk Avg": "bwd_bytes_bulk_avg",
    "Bwd Packet/Bulk Avg": "bwd_packet_bulk_avg",
    "Bwd Bulk Rate Avg": "bwd_bulk_rate_avg",
    "Subflow Fwd Packets": "subflow_fwd_packets",
    "Subflow Fwd Bytes": "subflow_fwd_bytes",
    # "Subflow Bwd Packets":"subflow_bwd_packets",
    "Subflow Bwd Bytes": "subflow_bwd_bytes",
    "FWD Init Win Bytes": "fwd_init_win_bytes",
    "Bwd Init Win Bytes": "bwd_init_win_bytes",
    "Fwd Act Data Pkts": "fwd_act_data_pkts",
    "Fwd Seg Size Min": "fwd_seg_size_min",
    "Active Mean": "active_mean",
    "Active Std": "active_std",
    "Active Max": "active_max",
    "Active Min": "active_min",
    "Idle Mean": "idle_mean",
    "Idle Std": "idle_std",
    "Idle Max": "idle_max",
    "Idle Min": "idle_min",
    "ICMP Code": "icmp_code",
    "ICMP Type": "icmp_type",
    "Total TCP Flow Time": "total_tcp_flow_time",
    "Label": "label",
}

swapped_mapping = {value: key for key, value in mapping_for_columns.items()}
columns = [value for key, value in mapping_for_columns.items()]
# These startparameters are only used to find best params for the RFC once!
# They are based on previous experiences...
start_parameters = {
    "bootstrap": [True, False],
    "max_depth": [30, 40, 50, 60, 65, 70, 75, 80, 90, 100, None],
    "max_features": ["log2", "sqrt"],
    "min_samples_leaf": [1, 2, 4],
    "min_samples_split": [2, 5, 10],
    "n_estimators": [400, 600, 700, 750, 800, 850, 900, 1000, 1200, 1400],
}


def load_data(directory: str, cutoff: int) -> pd.DataFrame:
    csv_files = {}
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)

            try:
                # read csv file
                df = pd.read_csv(file_path)
                if len(df) > cutoff:
                    print(f"read: {filename}")
                    # Save DataFrame to dictionary
                    csv_files[df["Label"].unique()[0]] = df
                else:
                    print(
                        f"omitted file {filename} because it has less than {cutoff} flows"
                    )
            except Exception as e:
                print(f"Error on file {filename}: {str(e)}")

    return pd.concat(csv_files, ignore_index=True)


def scale_and_pca(data: pd.DataFrame) -> tuple:
    # Scale The Dataset
    X = data.drop("label", axis=1)
    y = data["label"]
    scaler = StandardScaler()
    scaled_X = scaler.fit_transform(X)
    # Principal Component Analysis
    ipca_size = 34  # Magic
    ipca = IncrementalPCA(n_components=ipca_size, batch_size=500)
    for batch in np.array_split(scaled_X, len(X) // 500):
        ipca.partial_fit(batch)
    print(f"information retained: {sum(ipca.explained_variance_ratio_):.2%}")
    transformed_X = ipca.transform(scaled_X)
    new_data = pd.DataFrame(
        transformed_X, columns=[f"PC{i+1}" for i in range(ipca_size)]
    )
    new_data["label"] = y.values
    return new_data, scaler, ipca


def upsample_the_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
    X = dataset.drop("label", axis=1)
    y = dataset["label"]
    smote = SMOTE(sampling_strategy="auto", random_state=0)
    X_upsampled, y_upsampled = smote.fit_resample(X, y)
    blnc_data = pd.DataFrame(X_upsampled)
    blnc_data["attack_type"] = y_upsampled
    return blnc_data


def train_random_forest(data: pd.DataFrame, params: dict = None) -> tuple:
    """
    Trains a Random Forest model on the provided data.

    Args:
        data (DataFrame): The training data.

    Returns:
        tuple: A tuple containing the trained model, training features, training labels test features (X_test) and test labels (y_test).

    """
    # split data without type of attack
    features = data.drop("attack_type", axis=1)
    labels = data["attack_type"]
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.25, random_state=0
    )

    # Random Forest
    if params != None:
        rf = RandomForestClassifier(
            n_estimators=params["n_estimators"],
            max_depth=params["max_depth"],
            max_features=params["max_features"],
            min_samples_split=params["min_samples_split"],
            min_samples_leaf=params["min_samples_leaf"],
            bootstrap=params["bootstrap"],
            random_state=0,
        )
    else:
        rf = RandomForestClassifier(
            n_estimators=15, max_depth=8, max_features=20, random_state=0
        )
    start = time.time()
    rf.fit(X_train, y_train)
    end = time.time()
    print(f"Trainingduration: {end - start} seconds")
    return rf, X_train, y_train, X_test, y_test


# Create Confusion Matrix
def create_confusion_matrix(model, X_test, y_test) -> np.ndarray:
    y_pred_rf = model.predict(X_test)
    return confusion_matrix(y_test, y_pred_rf)


def create_figure(conf_matrix: np.ndarray, model) -> plt:
    plt.figure(figsize=(8, 7))
    sns.heatmap(
        conf_matrix,
        annot=True,
        cmap="Blues",
        xticklabels=model.classes_,
        yticklabels=model.classes_,
    )
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted label")
    plt.ylabel("True label")
    plt.tight_layout()
    return plt


# Create Metrics-Diagramm
def create_metrics_overview(model, X_test, y_test) -> plt:
    target_names = model.classes_
    y_pred_rf = model.predict(X_test)
    metrics = classification_report(
        y_true=y_test, y_pred=y_pred_rf, target_names=target_names, output_dict=True
    )
    precision = [metrics[target_name]["precision"] for target_name in target_names]
    recall = [metrics[target_name]["recall"] for target_name in target_names]
    f1_score = [metrics[target_name]["f1-score"] for target_name in target_names]
    data = np.array([precision, recall, f1_score])
    rows = ["Precision", "Recall", "F1-score"]
    print(metrics)
    plt.figure(figsize=(14, 6))
    sns.heatmap(
        data,
        cmap="Reds",
        annot=True,
        fmt=".2f",
        xticklabels=model.classes_,
        yticklabels=rows,
    )
    plt.title("Classification Report")
    plt.tight_layout()
    return plt


def get_params_for_RandomForestClassifier(X_train, y_train):
    rf = RandomForestClassifier()
    rf_random = RandomizedSearchCV(
        estimator=rf,
        param_distributions=start_parameters,
        n_iter=100,
        cv=3,
        verbose=2,
        random_state=42,
        n_jobs=-1,
    )
    rf_random.fit(X_train, y_train)
    print(f"Best parameters for RandomForestClassifier are :{rf_random.best_params_}")
    return rf_random.best_params_


if __name__ == "__main__":
    # load Data
    raw_dataset = load_data("nids-daten/sampled_CICIDS2017_improved_rnd_5000", 2000)

    # Following Code is obseolete because of new Naming
    # because of very sparse values we remove following columns
    # sparse_columns = ['Bwd URG Flags', 'CWR Flag Count', 'ECE Flag Count', 'Subflow Bwd Packets', 'Attempted Category']
    # useable_columns = [c for c in columns if c not in sparse_columns]
    # raw_dataset = raw_dataset[useable_columns]
    # Row_with_now_columns_in_received_http_request = ["Bwd Packet Length Max",
    # "Bwd Packet Length Min",
    # "Bwd Packet Length Mean",
    # "Bwd Packet Length Std",
    # "Flow Bytes/s",
    # "Flow Packets/s",
    # "Flow IAT Mean",
    # "Flow IAT Std",
    # "Flow IAT Max",
    # "Flow IAT Min",
    # "Fwd IAT Total",
    # "Fwd IAT Mean",
    # "Fwd IAT Std",
    # "Fwd IAT Max",
    # "Fwd IAT Min"]
    # raw_dataset = raw_dataset.drop(Row_with_now_columns_in_received_http_request, axis=1)

    # Map Columns in Dataframe to values of the data in the http requests
    raw_dataset = raw_dataset.rename(columns=mapping_for_columns)
    raw_dataset = raw_dataset[columns]  # exclude unused Clumns
    # Check for Duplicates
    dups = raw_dataset[raw_dataset.duplicated()]
    print(f"Number of duplicates: {len(dups)}")
    missing_val = raw_dataset.isna().sum()
    print(missing_val.loc[missing_val > 0])
    print(f"Initial missing values: {raw_dataset.isna().sum().sum()}")
    # Dropping columns with only one unique value
    num_unique = raw_dataset.nunique()
    one_variable = num_unique[num_unique == 1]
    not_one_variable = num_unique[num_unique > 1].index

    dropped_cols = one_variable.index
    cleaned_data = raw_dataset[
        not_one_variable
    ]  # This Data could be stored in a pkl file for later use...
    pd.DataFrame.to_csv(
        cleaned_data,
        "flask_dash_app/app/datasources/balanced_dataset_cicids201_improved.csv",
    )
    print(f"Dropped columns: {dropped_cols}")
    new_data, scaler, ipca = scale_and_pca(cleaned_data)
    data = upsample_the_dataset(new_data)
    rf, X_train, y_train, X_test, y_test = train_random_forest(data)
    start = time.time()
    print(
        cross_val_score(rf, X_train, y_train)
    )  # mean 0.978429628 bei 3.590430974960327 s training
    end = time.time()
    print(f"Evaluationtime {end - start}")
    joblib.dump(rf, "flask_dash_app/app/models/model.pkl")
    joblib.dump(scaler, "flask_dash_app/app/models/scaler.pkl")
    joblib.dump(ipca, "flask_dash_app/app/models/ipca.pkl")
    pd.DataFrame.to_csv(
        cleaned_data,
        "flask_dash_app/app/datasources/balanced_dataset_cicids201_improved.csv",
    )
    # get_params_for_RandomForestClassifier(X_train, y_train) # returned {'n_estimators': 1400, 'min_samples_split': 5, 'min_samples_leaf': 1, 'max_features': 'log2', 'max_depth': 90, 'bootstrap': False}
    # best_params = {'n_estimators': 1400, 'min_samples_split': 5, 'min_samples_leaf': 1, 'max_features': 'log2', 'max_depth': 90, 'bootstrap': False}
    # rf, X_train, y_train, X_test, y_test = train_random_forest(data, best_params)
    # start = time.time()
    # print(cross_val_score(rf, X_train, y_train)) # mean 0.9875259279999999 bei 187.25912809371948 s training
    # end = time.time()
    # print(f"Evaluationtime {end - start}")

    model = rf
    model_hash = compute_model_hash(model)
    mv = Model_Visualisator()
    from sklearn.metrics import accuracy_score as ascore

    cm = mv.create_confusion_matrix(model, X_test, y_test)
    cm_data_as_list = mv.create_storeable_list_from_cunfusion_matrix(
        cm, classes=list(model.classes_)
    )
    metrics = mv.create_metrics_list_for_storing_in_elastic(model, X_test, y_test)
    predicted = model.predict(X_test)
    score = ascore(y_test, predicted)
    boxplotdata = create_boxplot_data_for_elastic(cleaned_data)
    # Save model and properties to elastic
    # Just pics following
    if CREAT_FIGS:
        cm = create_confusion_matrix(rf, X_test, y_test)
        confusion_matrix_fig = create_figure(cm, rf)
        confusion_matrix_fig.savefig(
            "new_cicids2017_improved_random_forest_5000_classifier.png"
        )
        confusion_matrix_fig.show()
    if CREAT_FIGS:
        metrics_overview = create_metrics_overview(
            model=rf, X_test=X_test, y_test=y_test
        )
        metrics_overview.savefig(
            "new_cicids2017_improved_random_forest_5000_metrics_overview.png"
        )
        metrics_overview.show()
