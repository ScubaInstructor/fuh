import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import IncrementalPCA
from imblearn.over_sampling import SMOTE

import numpy as np

"""
Functions for the datapipeline
"""
gemeinsame_columns = ['dst_port', 'flow_duration', 'tot_fwd_pkts', 'tot_bwd_pkts', 
                      'totlen_fwd_pkts', 'totlen_bwd_pkts', 'fwd_pkt_len_max', 
                      'fwd_pkt_len_min', 'fwd_pkt_len_mean', 'fwd_pkt_len_std', 
                      'bwd_pkt_len_max', 'bwd_pkt_len_min', 'bwd_pkt_len_mean', 
                      'bwd_pkt_len_std', 'flow_byts_s', 'flow_pkts_s', 
                      'flow_iat_mean', 'flow_iat_std', 'flow_iat_max', 
                      'flow_iat_min', 'fwd_iat_tot', 'fwd_iat_mean', 
                      'fwd_iat_std', 'fwd_iat_max', 'fwd_iat_min', 
                      'bwd_iat_tot', 'bwd_iat_mean', 'bwd_iat_std', 'bwd_iat_max', 
                      'bwd_iat_min', 'fwd_psh_flags', 'fwd_urg_flags', 
                      'fwd_header_len', 'bwd_header_len', 'fwd_pkts_s', 
                      'bwd_pkts_s', 'pkt_len_min', 'pkt_len_max', 'pkt_len_mean', 
                      'pkt_len_std', 'pkt_len_var', 'fin_flag_cnt', 'syn_flag_cnt', 
                      'rst_flag_cnt', 'psh_flag_cnt', 'ack_flag_cnt', 
                      'urg_flag_cnt', 'cwr_flag_count', 'ece_flag_cnt', 
                      'down_up_ratio', 'pkt_size_avg', 'fwd_seg_size_avg', 
                      'bwd_seg_size_avg', 'subflow_fwd_pkts', 'subflow_fwd_byts', 
                      'subflow_bwd_pkts', 'subflow_bwd_byts', 'init_fwd_win_byts', 
                      'init_bwd_win_byts', 'fwd_act_data_pkts', 'fwd_seg_size_min', 
                      'active_mean', 'active_std', 'active_max', 'active_min', 
                      'idle_mean', 'idle_std', 'idle_max', 'idle_min']


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

    data = data[gemeinsame_columns]
    
    if not scaler:
        scaler = StandardScaler()
        scaled_features: np.ndarray = scaler.fit_transform(data)
    else: 
        scaled_features: np.ndarray = scaler.transform(data)

    if ipca:
        transformed_features = ipca.transform(scaled_features)
        adapted_data = pd.DataFrame(transformed_features, columns = [f'PC{i+1}' for i in range(ipca_size)])
    else:
        adapted_data = pd.DataFrame(scaled_features, columns=gemeinsame_columns)
    return adapted_data

def adapt_for_retraining(data: pd.DataFrame, scaler: StandardScaler, ipca: IncrementalPCA, 
          ipca_size: int= None) -> pd.DataFrame:
    """

    Prepares data for re-training by selecting only used features, optionally scaling and transforming via PCA. An 'attack_type' column is added.

    Args: 
        data (pd.DataFrame): The input DataFrame containing the data to be processed. 
        scaler (StandardScaler): A pre-trained StandardScaler or None if a StandardScaler should be fit to this data. 
        ipca (IncrementalPCA): A pre-trained IncrementalPCA object or None if no PCA should be applied. 
        ipca_size (int): The number of PCA components or None. Must be set if ipca is used. Defaults to None.

    Returns: 
        pd.DataFrame: The transformed DataFrame, ready for re-training.
    """
    
    if ipca: # check if ipca_size if set if we use ipca
        if not ipca_size:
            raise ValueError()

    data = data[gemeinsame_columns]

    if not scaler:
        scaler = StandardScaler()
        scaled_features: np.ndarray = scaler.fit_transform(data)
    else:
        scaled_features: np.ndarray = scaler.transform(data)

    if ipca: # only when ipca is used
        transformed_features = ipca.transform(scaled_features)
        adapted_data = pd.DataFrame(transformed_features, columns = [f'PC{i+1}' for i in range(ipca_size)])
    else: # no ipca
        adapted_data = pd.DataFrame(scaled_features, columns=gemeinsame_columns)
    
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

    c = gemeinsame_columns + ['attack_type'] 
    data = data[c] 
    features = data.drop('attack_type', axis = 1)
    attacks = data['attack_type']

    # Scaling
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    # Principal Component Analysis
    if use_ipca:
        ipca_size = len(features.columns) // 2
        ipca = IncrementalPCA(n_components = ipca_size, batch_size = 500)
        for batch in np.array_split(scaled_features, len(features) // 500):
            ipca.partial_fit(batch) 
        transformed_features = ipca.transform(scaled_features)
        new_data = pd.DataFrame(transformed_features, columns = [f'PC{i+1}' for i in range(ipca_size)])
    else: # no ipca
        new_data = pd.DataFrame(scaled_features, columns=gemeinsame_columns)
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
