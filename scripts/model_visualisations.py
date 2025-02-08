#%%
from pandas import DataFrame
from adapter.adapt_capture_to_trainingdata import adapt_cicids2017_for_training
from joblib import load
from datetime import datetime
from sklearn.model_selection import cross_val_score, train_test_split

df = load("/tmp/models.pkl")
df = df[df["own_flow_count"] > 0]
print(df)
# %%
scores = df["score"].tolist()
print(scores)
# %%
labels = [datetime.strftime(d, "%Y-%m-%d %H:%M") for d in df["timestamp"].tolist()]
print(labels)
# %%
import matplotlib.pyplot as plt
import seaborn as sns
from math import floor
palette = sns.color_palette('Greens', n_colors = len(scores))
fig, ax = plt.subplots(figsize = (9, 3))
ax.barh(labels, scores, color = palette)
floor_limit = floor(min(scores) * 10 ) / 10
ax.set_xlim([floor_limit, 1])
ax.set_xlabel('Accuracy Score')
ax.set_title('Model Comparison')

# %%
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

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score, classification_report
trainingdata = load("flask_dash_app/app/datasources/DataFrame_with_balanced_dataset.pkl") # load("DataFrame_with_balanced_dataset.pkl")
processed_data, scaler, ipca, ipca_size  = adapt_cicids2017_for_training(data=trainingdata, balance_the_data=False)
model, X_train, y_train, X_test, y_test = train_random_forest(processed_data)

# %%
def create_confusion_matrix(model, X_test, y_test) -> ndarray:
    y_pred_rf = model.predict(X_test)
    return confusion_matrix(y_test, y_pred_rf)

def create_figure(conf_matrix:ndarray, model) -> plt:
    plt.figure(figsize=(8, 7))  
    sns.heatmap(conf_matrix, annot=True, cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
    plt.set_title('Confusion Matrix')
    plt.set_xlabel('Predicted label')
    plt.set_ylabel('True label')
    fig.tight_layout()
    return plt

cm = create_confusion_matrix(model, X_test, y_test)
create_figure(cm, model).show()

# %%
from numpy import ndarray
def create_storeable_list(confusion_matrix_data:ndarray) -> list[dict]:
    data_to_index = []
    for i, row in enumerate(confusion_matrix_data):
        for j, value in enumerate(row):
            data_to_index.append({
                'actual': model.classes_[i],
                'predicted': model.classes_[j],
                'value': int(value)
            })
    return data_to_index

print(create_storeable_list(cm))

# %%
from numpy import log1p
data_to_index= create_storeable_list(cm)
def create_confusion_matrix_figure_from_elastic_data(data:list[dict]) -> plt:
    df = DataFrame(data_to_index)
    confusion_matrix_data = df.pivot_table(index='actual', columns='predicted', values='value').fillna(0)# %%
    conf_matrix_log = log1p(confusion_matrix_data)
    plt.figure(figsize=(8, 7))  
    sns.heatmap(conf_matrix_log, annot=True, cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
    plt.set_title('Confusion Matrix')
    plt.set_xlabel('Predicted label')
    plt.set_ylabel('True label')
    fig.tight_layout()
    return plt
create_confusion_matrix_figure_from_elastic_data(data_to_index).show()


# %%
from flask_dash_app.app.elastic_connector import CustomElasticsearchConnector
cec = CustomElasticsearchConnector()
from asyncio import run
all_models = await cec.get_all_model_properties()
print(all_models)
# %%
cm_data = []
for i, d in all_models.iterrows():
    cm_data = d["confusion_matrix"]
print(cm_data)
# %%
create_confusion_matrix_figure_from_elastic_data(cm_data).show()
# %%
