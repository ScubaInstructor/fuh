import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import IncrementalPCA
from imblearn.over_sampling import SMOTE

import numpy as np

IPCA_SIZE = 34

"""
Functions for the datapipeline
"""
removed_columns = ['flow_id', 'ip_src', 'ip_dst', 'str_time', 'bw_urg_flag', 'cwe_cnt', 'ece_cnt', 'subfl_bw_pkt', ]    # these wont only serve for overfitting the model 

# the following columns are the ones which are not sparse, and which do not contain ipdresse and timestamps
COLUMNS = ['ip_src_prt', 'ip_dst_prt', 'protocol', 'flow_duration', 
           'fwd_pkt_stats', 'bwd_pkt_stats', 'tot_l_fw_pkt', 'tot_l_bw_pkt', 'fw_pkt_l_max', 'fw_pkt_l_min', 'fw_pkt_l_avg', 
           'fw_pkt_l_std', 'bw_iat_tot', 'bw_iat_avg', 'bw_iat_std', 'bw_iat_max', 'bw_iat_min', 'fw_psh_flag', 'bw_psh_flag', 
           'fw_urg_flag', 'fw_rst_flag', 'bw_rst_flag', 'fw_hdr_len', 'bw_hdr_len', 'fw_pkt_s', 'bw_pkt_s', 
           'pkt_len_min', 'pkt_len_max', 'pkt_len_avg', 'pkt_len_std', 'pkt_len_va', 'fin_cnt', 'syn_cnt', 'rst_cnt', 'pst_cnt', 
           'ack_cnt', 'urg_cnt', 'down_up_ratio', 'pkt_size_avg', 'fw_seg_avg', 'bw_seg_avg', 'fw_byt_blk_avg', 
           'fw_pkt_blk_avg', 'fw_blk_rate_avg', 'bw_byt_blk_avg', 'bw_pkt_blk_avg', 'bw_blk_rate_avg', 'subfl_fw_pk', 'subfl_fw_byt', 
           'subfl_bw_byt', 'fw_win_byt', 'bw_win_byt', 'Fw_act_pkt', 'fw_seg_min', 'atv_avg', 'atv_std', 'atv_max', 
           'atv_min', 'idl_avg', 'idl_std', 'idl_max', 'idl_min', 'icmp_code', 'icmp_type', 'cumulative_connection_duration']

def adapt_for_prediction(data: pd.DataFrame, scaler: StandardScaler, ipca: IncrementalPCA, 
          ipca_size: int = None) -> pd.DataFrame:
    """
    Prepares data for predictions by selecting only used features, optionally scaling, and transforming via PCA.

    Args: 
        data (pd.DataFrame): The input DataFrame containing the data to be processed. 
        scaler (StandardScaler): A pre-trained StandardScaler or None if a StandardScaler should be fit to this data. 
        ipca (IncrementalPCA): A pre-trained IncrementalPCA object or None if no PCA should be applied. 
        ipca_size (int, optional): The number of PCA components or None. Must be set if ipca is used. Defaults to None.

    Returns: 
        pd.DataFrame: The transformed DataFrame, ready for predictions.
    """
    
    if ipca: # check if ipca_size if set if we use ipca
        if not ipca_size:
            raise ValueError()

    data = data[COLUMNS]
    data = data[COLUMNS]
    
    if not scaler:
        scaler = StandardScaler()
        scaled_features: np.ndarray = scaler.fit_transform(data)
    else: 
        scaled_features: np.ndarray = scaler.transform(data)

    if ipca:
        transformed_features = ipca.transform(scaled_features)
        adapted_data = pd.DataFrame(transformed_features, columns = [f'PC{i+1}' for i in range(ipca_size)])
    else:
        adapted_data = pd.DataFrame(scaled_features, columns=COLUMNS)
        adapted_data = pd.DataFrame(scaled_features, columns=COLUMNS)
    return adapted_data

def adapt_for_retraining(data: pd.DataFrame, scaler: StandardScaler, ipca: IncrementalPCA, 
          ipca_size: int= IPCA_SIZE) -> pd.DataFrame:
    """

    Prepares data for re-training by selecting only used features, optionally scaling and transforming via PCA. An 'attack_type' column is added.

    Args: 
        data (pd.DataFrame): The input DataFrame containing the data to be processed. 
        scaler (StandardScaler): A pre-trained StandardScaler or None if a StandardScaler should be fit to this data. 
        ipca (IncrementalPCA): A pre-trained IncrementalPCA object 
        ipca_size (int): The number of PCA components defaults to 34.

    Returns: 
        pd.DataFrame: The transformed DataFrame, ready for re-training.
    """
    
    if ipca: # check if ipca_size if set if we use ipca
        if not ipca_size:
            raise ValueError()

    data = data[COLUMNS]
    data = data[COLUMNS]

    if not scaler:
        scaler = StandardScaler()
        scaled_features: np.ndarray = scaler.fit_transform(data)
    else:
        scaled_features: np.ndarray = scaler.transform(data)

    if ipca: # only when ipca is used
        transformed_features = ipca.transform(scaled_features)
        adapted_data = pd.DataFrame(transformed_features, columns = [f'PC{i+1}' for i in range(ipca_size)])
    else: # no ipca
        adapted_data = pd.DataFrame(scaled_features, columns=COLUMNS)
        adapted_data = pd.DataFrame(scaled_features, columns=COLUMNS)
    
    # The trainingdata is not from Attacks!
    cLength = len(adapted_data[adapted_data.columns[0]])
    e = ["BENIGN" for _ in range(cLength)] # Number for BENIGN is 0 if 'attack_number' is used
    adapted_data['attack_type'] = e

    return adapted_data

def adapt_cicids2017_for_training(data: pd.DataFrame, use_ipca: bool = True, 
                       balance_the_data: bool = True) -> tuple[
                           pd.DataFrame, StandardScaler, IncrementalPCA, int]:
    """
    Prepares CICIDS2017 data for training, including scaling, optional PCA, and data balancing.

    Args:
        data (pd.DataFrame): The input DataFrame containing CICIDS2017 data.
        use_ipca (bool, optional): Whether IncrementalPCA should be used. Defaults to True.
        balance_the_data (bool, optional): Whether the data should be balanced. Defaults to True.

    Returns:
        tuple: A tuple consisting of:
            - pd.DataFrame: The transformed and possibly balanced DataFrame.
            - StandardScaler: The fitted StandardScaler.
            - IncrementalPCA: The trained IncrementalPCA object (or None if not used).
            - int: The number of PCA components (or None if PCA was not used).
    """

    c = COLUMNS + ['attack_type'] 
    c = COLUMNS + ['attack_type'] 
    data = data[c] 
    features = data.drop('attack_type', axis = 1)
    attacks = data['attack_type']

    # Scaling
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    # Principal Component Analysis
    if use_ipca:
        ipca_size = IPCA_SIZE
        ipca = IncrementalPCA(n_components = ipca_size, batch_size = 500)
        for batch in np.array_split(scaled_features, len(features) // 500):
            ipca.partial_fit(batch) 
        transformed_features = ipca.transform(scaled_features)
        new_data = pd.DataFrame(transformed_features, columns = [f'PC{i+1}' for i in range(ipca_size)])
    else: # no ipca
        new_data = pd.DataFrame(scaled_features, columns=COLUMNS)
        new_data = pd.DataFrame(scaled_features, columns=COLUMNS)
        ipca = None
        ipca_size = None

    new_data['attack_type'] = attacks.values

    # Create balanced dataset
    if balance_the_data:
        adapted_data = balance_the_dataset(new_data)
    else: # dont balance
        adapted_data = new_data

    return adapted_data, scaler, ipca, ipca_size

def balance_the_dataset(new_data):
    """
    Balances the dataset by undersampling large attack classes and oversampling small attack classes.

    This function performs the following steps:
    1. Selects classes with more than 1950 samples.
    2. Limits large classes to a maximum of 5000 samples.
    3. Applies SMOTE (Synthetic Minority Over-sampling Technique) to balance smaller classes.
    4. Shuffles the resulting dataset.

    Args:
        new_data (pd.DataFrame): The original, unbalanced dataset.

    Returns:
        pd.DataFrame: The balanced dataset.
    """
    # Zähle die Häufigkeit jeder Klasse
    class_counts = new_data['attack_type'].value_counts()
    # Wähle nur Klassen mit mehr als 1950 Samples
    selected_classes = class_counts[class_counts > 1950]
    class_names = selected_classes.index
    # Filtere den Datensatz auf die ausgewählten Klassen
    selected = new_data[new_data['attack_type'].isin(class_names)]

    dfs = []
    for name in class_names:
        # Extrahiere Daten für jede Klasse
        df = selected[selected['attack_type'] == name]
        # Begrenze große Klassen auf 5000 Samples
        if len(df) > 2500:
            df = df.sample(n = 5000, random_state = 0)
        dfs.append(df)
    
    # Kombiniere alle bearbeiteten Klassen
    df = pd.concat(dfs, ignore_index = True)
    
    
    # If no CPU count found Error 
    # import os
    # os.environ['LOKY_MAX_CPU_COUNT'] = '4'


    # Vorbereitung für SMOTE
    X = df.drop('attack_type', axis=1)
    y = df['attack_type']

    # Anwenden von SMOTE zur Überabtastung der Minoritätsklassen
    smote = SMOTE(sampling_strategy='auto', random_state=0)
    X_upsampled, y_upsampled = smote.fit_resample(X, y)

    # Erstelle einen neuen, balancierten DataFrame
    blnc_data = pd.DataFrame(X_upsampled)
    blnc_data['attack_type'] = y_upsampled

    # Mische den Datensatz
    blnc_data = blnc_data.sample(frac=1)
    

    return blnc_data
