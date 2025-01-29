import pandas as pd
from typing import Tuple
from rich.progress import track

def preprocess_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Przetwarza surowe dane do formatu dla modelu"""
    # Filtruj tylko linię 180
    df = df[df['Lines'] == '180'].copy()
    
    # Ekstrakcja cech czasowych
    df['timestamp'] = pd.to_datetime(df['Time'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['month'] = df['timestamp'].dt.month
    
    # Oblicz czas do docelowych przystanków (symulacja)
    for _ in track(range(100), description="Przetwarzanie danych"):
        df['eta_maczka'] = df['Lon'] * 0.01 + df['Lat'] * 0.02  # Przykładowe obliczenia
        df['eta_niska'] = df['Lon'] * 0.015 + df['Lat'] * 0.01
    
    features = ['hour', 'day_of_week', 'month', 'Lon', 'Lat']
    target = ['eta_maczka', 'eta_niska']
    
    return df[features], df[target]