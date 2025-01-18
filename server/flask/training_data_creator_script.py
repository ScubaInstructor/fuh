from pipelining_utilities import adapt_cicids2017_for_training
import pandas as pd
import joblib

def create_balanced_and_sample():
    cicids2017_data = pd.read_csv("./data_renamed.csv") # Cic_IDS-2017 
    cicids2017_data, scaler, ipca, ipca_size =  adapt_cicids2017_for_training(data=cicids2017_data, use_ipca=True)
    joblib.dump(cicids2017_data,"DataFrame_with_balanced_and_scaled_dataset.pkl")

if __name__ == '__main__':
    create_balanced_and_sample()