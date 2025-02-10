from time import sleep
from pandas import DataFrame
from sklearn.metrics import confusion_matrix, classification_report
from numpy import array, log1p, ndarray
import plotly.graph_objects as go 
from datetime import datetime
from math import floor


class Model_Visualisator():
    
    def create_confusion_matrix(self, model, X_test, y_test) -> ndarray:
        y_pred_rf = model.predict(X_test)
        return confusion_matrix(y_test, y_pred_rf)

    def extract_class_names(self, data):
        """
        Extracts the class names from a list of dictionaries representing a confusion matrix.

        Args:
            data: A list of dictionaries, where each dictionary contains the fields 'actual' and 'predicted'.

        Returns:
            A list of the unique class names. Sorted alphabetically.
        """
        class_names = set()
        for item in data:
            class_names.add(item['actual'])
            class_names.add(item['predicted'])
        result = list(class_names)
        result.sort()
        return result

    def create_storeable_list_from_cunfusion_matrix(self, confusion_matrix_data:ndarray, classes:list) -> list[dict]:
        """Creates a list of dictionaries to store confusion matrix data in elastic

        Args:
            confusion_matrix_data (ndarray): The confusionmatrix of a model
            classes (ndarray): The classes of the model

        Returns:
            list[dict]: the list ready to be stored in elastic. classes are stored alphabetically.
        """
        data_to_index = []
        classes.sort()
        for i, row in enumerate(confusion_matrix_data):
            for j, value in enumerate(row):
                data_to_index.append({
                    'actual': classes[i],
                    'predicted': classes[j],
                    'value': int(value)
                })
        return data_to_index

    def create_confusion_matrix_figure_from_elastic_data(self, data:list[dict]):
        """ Creates a confusion matrix figure from a models data stored in elastic using Plotly

        Args:
            data (list[dict]): the data from elastic, labelled "confusion_matrix"

        Returns:
            plotly.graph_objects.Figure: a Plotly figure of the confusion matrix
        """
        classes = self.extract_class_names(data=data)
        df = DataFrame(data)
        confusion_matrix_data = df.pivot_table(index='actual', columns='predicted', values='value').fillna(0)
        conf_matrix_log = log1p(confusion_matrix_data)
        
        # Create the Plotly figure
        fig = go.Figure(data=go.Heatmap(
            z=conf_matrix_log.values,
            x=classes,
            y=classes,
            colorscale='Blues',
            texttemplate="%{z:.2f}",
            showscale=True
        ))

        fig.update_layout(
            title='Confusion Matrix',
            xaxis_title='Predicted label',
            yaxis_title='True label',
            xaxis=dict(side='bottom'),
            yaxis=dict(autorange='reversed'), # To display the y-axis in the correct order
            margin=dict(l=100, r=100, b=100, t=100, pad=4)
        )
        
        return fig

    def create_metrics_overview_from_elastic_data(self, class_metric_data:list[list], classes:list):
        """Creates a heatmap of the metrics of a model stored in elastic using Plotly

        Args:
            class_metric_data (list[list]): the data from elastic labelled as "class_metric_data" 
                                            ordered for classes alphabetically
            classes (list): the classes of the model in alphabetic order

        Returns:
            plotly.graph_objects.Figure: A Plotly figure of the metrics overview
        """
        data = array(class_metric_data)
        rows = ['Precision', 'Recall', 'F1-score']

        # Create the Plotly figure
        fig = go.Figure(data=go.Heatmap(
            z=data,
            x=classes,
            y=rows,
            colorscale='Reds',
            texttemplate="%{z:.2f}",
            showscale=True
        ))

        fig.update_layout(
            title='Classification Report',
            xaxis_title='Classes',
            yaxis_title='Metrics',
            margin=dict(l=100, r=100, b=100, t=100, pad=4)
        )
        
        return fig

    def create_metrics_list_for_storing_in_elastic(self, model, X_test, y_test):
        target_names = model.classes_
        target_names.sort()
        y_pred_rf = model.predict(X_test)
        metrics = classification_report(y_true = y_test, y_pred = y_pred_rf, target_names = target_names, output_dict = True)
        precision = [metrics[target_name]['precision'] for target_name in target_names]
        recall = [metrics[target_name]['recall'] for target_name in target_names]
        f1_score = [metrics[target_name]['f1-score'] for target_name in target_names]
        return [precision, recall, f1_score]

    def create_boxplot_for_all_models(self, df:DataFrame) -> go.Figure:
        """
        Creates a horizontal bar plot using Plotly to compare model scores.

        Args:
            df (DataFrame): DataFrame containing 'score' and 'timestamp' columns.

        Returns:
            plotly.graph_objects.Figure: A Plotly figure of the model comparison.
        """
        scores = df["score"].tolist()
        labels = [datetime.strftime(d, "%Y-%m-%d %H:%M") for d in df["timestamp"].tolist()]
        
        # Create a Plotly figure
        fig = go.Figure(go.Bar(
            x=scores,
            y=labels,
            orientation='h',
            marker=dict(color=scores, colorscale='Greens'), # Color bars based on score
            text=scores, # Display score values on the bars
            texttemplate='%{text:.2f}', # Format the score values
            textposition='inside' # Position the text inside the bars
        ))

        floor_limit = floor(min(scores) * 10) / 10
        
        # Update the layout
        fig.update_layout(
            title='Model Comparison',
            xaxis_title='Accuracy Score',
            yaxis_title='Timestamp',
            xaxis=dict(range=[floor_limit, 1]),
            yaxis=dict(type='category'),
            margin=dict(l=120, r=20, t=60, b=60),
            height=400 # Adjust height as needed
        )
        
        return fig

if __name__ == '__main__':
    # from joblib import load
    # from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score, classification_report
    # trainingdata = load("flask_dash_app/app/datasources/DataFrame_with_balanced_dataset.pkl") # load("DataFrame_with_balanced_dataset.pkl")
    # from pipelining_utilities import adapt_cicids2017_for_training
    from elastic_connector import CustomElasticsearchConnector
    import asyncio
    # from datetime import datetime
    # processed_data, scaler, ipca, ipca_size  = adapt_cicids2017_for_training(data=trainingdata, balance_the_data=False)
    # model, X_train, y_train, X_test, y_test = train_random_forest(processed_data)
    # cm = create_confusion_matrix(model, X_test, y_test)
    # cm_list = create_storeable_list_from_cunfusion_matrix(cm, classes=list(model.classes_))
    # metrics = create_metrics_list_foe_storing_in_elastic(model, X_test, y_test)
    cec = CustomElasticsearchConnector()
    # asyncio.run(cec.save_model_properties("1234567890", datetime.now(), 23, 0.97, cm_list, metrics))
    # sleep (10)
    models = asyncio.run(cec.get_all_model_properties())   
    for i, d in models.iterrows():
        retrieved_cm_data = d["confusion_matrix"]
        retrieved_metrics = d["class_metric_data"]
        break
    mv = Model_Visualisator()
    bp = mv.create_boxplot_for_all_models(models)
    bp.show()
    cm_fig = mv.create_confusion_matrix_figure_from_elastic_data(retrieved_cm_data)
    cm_fig.show()
    classes = mv.extract_class_names(retrieved_cm_data)
    metrics_fig = mv.create_metrics_overview_from_elastic_data(retrieved_metrics, classes=classes)
    metrics_fig.show()

