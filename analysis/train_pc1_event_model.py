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
    "LogisticRegression":Pipeline([
        ("scaler",StandardScaler()),
        ("model",LogisticRegression(max_iter=1000))
    ]),

    "RandomForest":RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42
    ),

    "GradientBoosting":GradientBoostingClassifier(
        n_estimators = 100,
        learning_rate = 0.05,
        max_depth = 3 ,
        random_state = 42
    ),

    "SVM_RBF":Pipeline([
        ("scaler",StandardScaler()),
        ("model",SVC(kernel='rbf',probability=True))
    ])

}

results = []

for name,model in models.items():
    print(f"Training model: {name}")
    model.fit(X_train,y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:,1]

    acc = accuracy_score(y_test,y_pred)
    f1 = f1_score(y_test,y_pred)
    roc_auc = roc_auc_score(y_test,y_prob)

    results.append({
        "Model": name,
        "Accuracy":acc,
        "F1 Score":f1,
        "ROC AUC":roc_auc
    })

    print(f"{name} - Accuracy: {acc:.4f}, F1 Score: {f1:.4f}, ROC AUC: {roc_auc:.4f}")

results_df = pd.DataFrame(results).sort_values(by="ROC AUC",ascending=False)
print("\nModel Performance Summary:")
print(results_df)