import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.svm import SVC

from sklearn.metrics import accuracy_score,classification_report,roc_auc_score,f1_score
import joblib

df = pd.read_csv("events_pc1_dataset.csv",index_col=0,parse_dates=True)

print(f"Dataset shape :{df.shape}")

X = df[["total_events","mean_tone","total_mentions"]]
y = df["PC1_Direction"]

split = int(0.8*len(df))
X_train , X_test = X.iloc[:split],X.iloc[split:] 
y_train , y_test = y.iloc[:split],y.iloc[split:]

print(f"training size : {len(X_train)} and testing size : {len(X_test)}")

models = {
    
}