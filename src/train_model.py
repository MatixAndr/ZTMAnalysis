import joblib
import pandas as pd
from .data_preprocessing import preprocess_data
from models.v1.model import create_model
from rich.console import Console

console = Console()

def train_model():
    try:
        # Wczytaj surowe dane
        raw_df = pd.read_json("data/raw/bus_data_180.json")
        
        # Przetwarzanie
        X, y = preprocess_data(raw_df)
        
        # Trenowanie
        model = create_model()
        model.fit(X, y)
        
        # Zapisz model
        joblib.dump(model, "models/v1/model.pkl")
        console.print("[bold green]Model zapisany![/bold green]")
        
    except FileNotFoundError:
        console.print("[bold red]Brak danych! Uruchom z opcją --train najpierw[/bold red]")