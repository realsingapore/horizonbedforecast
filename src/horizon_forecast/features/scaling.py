import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path

ARTIFACT_DIR = Path("artifacts")
ARTIFACT_DIR.mkdir(exist_ok=True, parents=True)

def fit_scaler(train_df: pd.DataFrame, feature_cols):
    scaler = StandardScaler()
    scaler.fit(train_df[feature_cols])
    joblib.dump(scaler, ARTIFACT_DIR / "scaler.pkl")
    return scaler

def transform_with_scaler(df: pd.DataFrame, feature_cols):
    scaler = joblib.load(ARTIFACT_DIR / "scaler.pkl")
    df_scaled = df.copy()
    df_scaled[feature_cols] = scaler.transform(df[feature_cols])
    return df_scaled