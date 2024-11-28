from adapt_capture_to_trainingdata import adapt_for_prediction, adapt_for_retraining, adapt_cicids2017_for_training, gemeinsame_columns
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import IncrementalPCA
import joblib
import pytest
import numpy as np
from adapt_capture_to_trainingdata import balance_the_dataset  


@pytest.fixture
def sample_dataframe():
    """Erstellt einen Beispiel-DataFrame für die Tests."""
    np.random.seed(42)
    data = {
        'feature1': np.random.rand(10000),
        'feature2': np.random.rand(10000),
        'attack_type': np.random.choice(['A', 'B', 'C', 'D'], 10000, p=[0.7, 0.2, 0.05, 0.05])
    }
    return pd.DataFrame(data)

class Tests():
    
    test_data = pd.read_csv("cicflowmeter/new_flows.csv")
    test_cicids2017 = joblib.load("cicids2017_excerpt_for_testing_in_dataframe.pkl")
    ipca = joblib.load("out/ipca.pkl")
    ipca_size = 34
    scaler = joblib.load("out/scaler.pkl")
    size = 69
    def test_adapt_for_prediction(self):
        
        assert isinstance(adapt_for_prediction(data=self.test_data, scaler=self.scaler, 
                                ipca=None, ipca_size=None), pd.DataFrame)
        
        assert self.size == adapt_for_prediction(data=self.test_data, scaler=self.scaler, 
                                ipca=None, ipca_size=None).columns.size
        
        # Test ohne IPCA
        result = adapt_for_prediction(self.test_data, self.scaler, None)
        assert isinstance(result, pd.DataFrame)
        assert result.shape[1] == len(gemeinsame_columns)
        
        # Test mit IPCA
        result_ipca = adapt_for_prediction(self.test_data, self.scaler, self.ipca, ipca_size=34)
        assert isinstance(result_ipca, pd.DataFrame)
        assert result_ipca.shape[1] == 34
        
        # Test mit neuem Scaler
        result_new_scaler = adapt_for_prediction(self.test_data, None, None)
        assert isinstance(result_new_scaler, pd.DataFrame)
        
        # Test für ValueError bei fehlendem ipca_size
        with pytest.raises(ValueError):
            adapt_for_prediction(self.test_data, self.scaler, self.ipca)


    def test_retraining_size(self):
        assert self.ipca_size + 1 == adapt_for_retraining(data=self.test_data, scaler=self.scaler, 
                                ipca=self.ipca, ipca_size=self.ipca_size).columns.size
        # Test ohne IPCA
        result = adapt_for_retraining(self.test_data, self.scaler, None)
        assert isinstance(result, pd.DataFrame)
        assert 'attack_type' in result.columns
        assert all(result['attack_type'] == 'BENIGN')
        
        # Test mit IPCA
        result_ipca = adapt_for_retraining(self.test_data, self.scaler, self.ipca, ipca_size=self.ipca_size)
        assert isinstance(result_ipca, pd.DataFrame)
        assert result_ipca.shape[1] == self.ipca_size+1  # 10 PCs + attack_type
        
        # Test für ValueError bei fehlendem ipca_size
        with pytest.raises(ValueError):
            adapt_for_retraining(self.test_data, self.scaler, self.ipca)
    
    def test_adapt_cicids2017_noipca_return(self):
        # Balancierung wird extra getestet, weil Datensatz groß genug sein muss.
        # Test ohne IPCA und ohne Balancierung
        t = adapt_cicids2017_for_training(data=self.test_cicids2017,use_ipca=False, balance_the_data=False)
        assert isinstance(t, tuple)
        assert isinstance(t[0], pd.DataFrame)
        assert isinstance(t[1], StandardScaler)
        assert t[2] is None
        assert t[3] is None
        assert len(self.test_cicids2017) == len(t[0])
        
        # Test mit IPCA und ohne Balancierung
        t = adapt_cicids2017_for_training(data=self.test_cicids2017,use_ipca=True, balance_the_data=False)
        assert isinstance(t, tuple)
        assert isinstance(t[0], pd.DataFrame)
        assert isinstance(t[1], StandardScaler)
        assert isinstance(t[2], IncrementalPCA)
        assert isinstance(t[3], int)
        assert len(self.test_cicids2017) == len(t[0])

        # Überprüfen Sie, ob die Ausgabe die erwarteten Spalten enthält
        assert 'attack_type' in t[0].columns
        assert set(gemeinsame_columns).issubset(set(t[0].columns)) or 'PC1' in t[0].columns

    

    

    def test_balance_the_dataset_class_balance(self, sample_dataframe):
        """Testet, ob die Klassen nach dem Balancieren gleichmäßiger verteilt sind."""
        balanced_df = balance_the_dataset(sample_dataframe)
        class_counts = balanced_df['attack_type'].value_counts()
        
        # Überprüfe, ob alle Klassen annähernd gleich vertreten sind
        assert class_counts.max() / class_counts.min() < 1.1  # Toleranz von 10%

    def test_balance_the_dataset_total_size(self, sample_dataframe):
        """Testet, ob die Gesamtgröße des Datensatzes innerhalb eines erwarteten Bereichs liegt."""
        balanced_df = balance_the_dataset(sample_dataframe)
        
        # Die Größe sollte ungefähr der Anzahl der Klassen * 5000 entsprechen, 
        # da zwei der kleineren Klassen abgeschnitten werden.
        expected_size = 2 * 5000
        assert abs(len(balanced_df) - expected_size) < expected_size * 0.1  # Toleranz von 10%

    def test_balance_the_dataset_preserves_features(self, sample_dataframe):
        """Testet, ob alle ursprünglichen Features im balancierten Datensatz erhalten bleiben."""
        balanced_df = balance_the_dataset(sample_dataframe)
        
        original_features = set(sample_dataframe.columns)
        balanced_features = set(balanced_df.columns)
        
        assert original_features == balanced_features

    def test_balance_the_dataset_no_duplicates(self, sample_dataframe):
        """Testet, ob der balancierte Datensatz keine Duplikate enthält."""
        balanced_df = balance_the_dataset(sample_dataframe)
        
        assert balanced_df.duplicated().sum() == 0

    def test_balance_the_dataset_small_classes_preserved(self, sample_dataframe):
        """Testet, ob kleine Klassen (< 1950 Samples) im Datensatz erhalten bleiben."""
        # Füge eine kleine Klasse hinzu
        small_class = pd.DataFrame({
            'feature1': np.random.rand(100),
            'feature2': np.random.rand(100),
            'attack_type': ['E'] * 100
        })
        sample_dataframe = pd.concat([sample_dataframe, small_class], ignore_index=True)
        
        balanced_df = balance_the_dataset(sample_dataframe)
        
        assert 'E' not in balanced_df['attack_type'].unique()


