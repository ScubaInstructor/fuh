from pipelining_utilities import balance_the_dataset
import pandas as pd
import joblib

def create_balanced_and_sample():
    cicids2017_data = pd.read_csv("server/flask/data_renamed.csv") # Cic_IDS-2017 
    cicids2017_data =  balance_the_dataset(new_data=cicids2017_data)
    joblib.dump(cicids2017_data,"DataFrame_with_balanced_dataset.pkl")

if __name__ == '__main__':
    create_balanced_and_sample()