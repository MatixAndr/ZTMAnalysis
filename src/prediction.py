import joblib
from rich.table import Table

def predict_arrival(api_key: str):
    # Wczytaj model
    model = joblib.load("models/v1/model.pkl")
    
    # Pobierz dane i przetwórz
    raw_data = fetch_data(api_key)
    
    # Logika predykcji (przykład)
    table = Table(title="Przewidywane przyjazdy")
    table.add_column("Przystanek")
    table.add_column("Czas (min)")
    
    table.add_row("Gen. Maczka", "5")
    table.add_row("Niska", "8")
    
    console.print(table)