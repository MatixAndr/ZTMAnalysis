import argparse
from rich.console import Console
from tqdm import tqdm
import time
from src.data_fetch import fetch_data, save_raw_data
from src.train_model import train_model
from src.prediction import predict_arrival

console = Console()

def main():
    parser = argparse.ArgumentParser(description="ZTM 180 Predictor")
    parser.add_argument("--train", action="store_true", help="Run in training mode")
    args = parser.parse_args()

    api_key = input("Podaj klucz API ZTM Warszawa: ")
    
    if args.train:
        console.print("[bold green]Uruchamiam tryb treningowy...[/bold green]")
        for _ in tqdm(range(1440), desc="Zbieranie danych (24h)"):
            raw_data = fetch_data(api_key, line="180")
            save_raw_data(raw_data)
            time.sleep(60)
        train_model()
    else:
        console.print("[bold blue]Uruchamiam predykcję...[/bold blue]")
        while True:
            predict_arrival(api_key)
            time.sleep(60)

if __name__ == "__main__":
    main()