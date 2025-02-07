#%%
from adapter.adapt_capture_to_trainingdata import adapt_cicids2017_for_training
from joblib import load
from datetime import datetime

from server.flask.retrainer import train_random_forest
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
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score, classification_report
trainingdata = load("flask_dash_app/app/datasources/DataFrame_with_balanced_dataset.pkl") # load("DataFrame_with_balanced_dataset.pkl")
processed_data, scaler, ipca, ipca_size  = adapt_cicids2017_for_training(data=mergeddata, balance_the_data=False)
model, X_train, y_train, X_test, y_test = train_random_forest(processed_data)
