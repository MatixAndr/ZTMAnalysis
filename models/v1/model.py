from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def create_model() -> BaseEstimator:
    """Tworzy pipeline modelu z wybranym estymatorem"""
    return Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])