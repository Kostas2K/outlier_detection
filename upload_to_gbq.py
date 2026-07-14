import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import seaborn as sns
import pyod
from pyod.models.knn import KNN
from pyod.models.lof import LOF 
from pyod.models.iforest import IForest
from sklearn.ensemble import IsolationForest
from IPython.display import display
import warnings 
warnings.filterwarnings('ignore')

from google.cloud import bigquery
import google.cloud.bigquery as gbq

def detect_outliers(df, var, method='knn', prob_value=0.1,
n_neighbors=20, contamination=0.05, n_estimators=100):
    """
    Detect outliers using K-Nearest Neighbors (KNN), Isolation Forest, or both.
    Parameters:
    df: pandas DataFrame
    var: column name to analyze
    method: 'knn', 'isolation_forest', or 'both'
    prob_value: threshold for KNN probability
    n_neighbors: number of neighbors for KNN
    contamination: expected proportion of outliers
    n_estimators: number of trees for Isolation Forest
    Returns:
    DataFrame with original data + outlier info
    """
    results = df.copy()

    if method in ['knn', 'both']:
        df_knn = df.loc[:, [var]]
        knn = KNN(n_neighbors=n_neighbors, contamination=contamination, n_jobs=-1)
        knn.fit(df_knn)
        probs = knn.predict_proba(df_knn)
        y_pred = knn.labels_
        y_scores = knn.decision_scores_
        knn_cols = pd.DataFrame(zip(y_pred, y_scores), columns=['outliers_knn', 'scores_knn'], index=df.index)
        results = results.join(knn_cols)

    if method in ['isolation_forest', 'both']:
        df_if = df.loc[:, [var]]
        clf = IsolationForest(n_estimators=n_estimators, max_samples='auto',
        contamination=contamination, max_features=1.0)
        clf.fit(df_if)
        df_if['anomaly_score']=clf.predict(df_if)
        df_if['score']=clf.decision_function(df_if[[var]])
        #inlier, outlier = df.loc[df.anomaly_score==1], df.lo
        df_if['outlier_inlier']=np.where((df_if['anomaly_score']==-1),'Outlier','Inlier')
        results = results.join(df_if[['score', 'anomaly_score', 'outlier_inlier']])
    return results

# Uploading big query table with outlier detection results
detect_outliers(df,'calc_refund_amt',method='both').to_gbq('dataset.outlier_detection', project_id='bq_project_id', if_exists='replace')
