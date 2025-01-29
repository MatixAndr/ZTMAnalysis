import csv
import os
import requests
from datetime import datetime
from rich import print

# Globalny licznik plików i nazwa bazowa
current_file_counter = 1
BASE_FILENAME = "bus_data_180"

def get_current_filename():
    return f"data/raw/{BASE_FILENAME}_{current_file_counter}.csv"

def save_raw_data(raw_data: dict):
    global current_file_counter
    
    os.makedirs("data/raw", exist_ok=True)
    
    # Sprawdź rozmiar aktualnego pliku
    current_file = get_current_filename()
    if os.path.exists(current_file):
        file_size = os.path.getsize(current_file) / (1024 * 1024)  # w MB
        if file_size >= 100:
            current_file_counter += 1
            current_file = get_current_filename()

    # Nagłówki CSV (dostosuj do struktury danych z API)
    fieldnames = ["Time", "Lines", "Lon", "Lat", "Brigade", "VehicleNumber", "Direction"]

    # Tryb: 'a' (append) jeśli plik istnieje, 'w' (write) jeśli nowy
    mode = 'a' if os.path.exists(current_file) else 'w'
    
    with open(current_file, mode, newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # Dodaj nagłówek tylko dla nowego pliku
        if mode == 'w':
            writer.writeheader()
        
        # Zapisz wszystkie rekordy
        for bus in raw_data.get('result', []):
            writer.writerow({
                "Time": datetime.now().isoformat(),
                "Lines": bus.get('Lines'),
                "Lon": bus.get('Lon'),
                "Lat": bus.get('Lat'),
                "Brigade": bus.get('Brigade'),
                "VehicleNumber": bus.get('VehicleNumber'),
                "Direction": bus.get('Direction')
            })
    
    # print(f"[bold yellow]Zapisano do {current_file}[/bold yellow]")

def fetch_data(api_key: str, line: str = "180") -> dict:
    url = f"https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=XXX&apikey={api_key}&type=1&line={line}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return {"result": response.json()['result']}  # Dopasuj strukturę do potrzeb CSV
    return {"result": []}