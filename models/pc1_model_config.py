from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

THRESHOLD = 0.49
SIGN = -1
C_VALUE = 10

def build_model():
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(C=C_VALUE, max_iter=1000))
    ])
    return model