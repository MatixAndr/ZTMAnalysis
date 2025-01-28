import requests
from math import radians, sin, cos, sqrt, atan2
import json
from datetime import datetime
from dotenv import load_dotenv
import os
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

load_dotenv()

def get_coordinates(address):
    geolocator = Nominatim(user_agent="ztm_analysis")
    try:
        location = geolocator.geocode(f"{address}, Warsaw, Poland")
        if location:
            return location.latitude, location.longitude
        else:
            raise ValueError("Address not found")
    except GeocoderTimedOut:
        raise ValueError("Geocoding service timed out")

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def fetch_nearby_buses(my_lat, my_lon, radius_km=10, line_filter=None):
    url = "https://api.um.warszawa.pl/api/action/busestrams_get/"
    
    api_key = os.getenv('WARSAW_ZTM_API_KEY')
    if not api_key:
        raise ValueError("Please set WARSAW_ZTM_API_KEY environment variable")
    
    params = {
        'resource_id': 'f2e5503e-927d-4ad3-9500-4ab9e55deb59',
        'apikey': api_key,
        'type': 1  # 1 for buses, 2 for trams
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        nearby_buses = []
        
        for vehicle in data.get('result', []):
            try:
                if line_filter and vehicle.get('Lines') != line_filter:
                    continue
                    
                bus_lat = float(vehicle.get('Lat'))
                bus_lon = float(vehicle.get('Lon'))
                
                distance = haversine_distance(my_lat, my_lon, bus_lat, bus_lon)
                
                if distance <= radius_km:
                    vehicle['distance_km'] = round(distance, 2)
                    nearby_buses.append(vehicle)
            except (ValueError, TypeError):
                continue
        
        return nearby_buses
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def monitor_buses(address, line_number, radius_km=10):
    try:
        lat, lon = get_coordinates(address)
        print(f"\nMonitoring buses from: {address}")
        print(f"Coordinates: {lat}, {lon}")
        print(f"Looking for line: {line_number}")
        print(f"Radius: {radius_km}km")
        print("\nPress Ctrl+C to stop monitoring...\n")
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"🚌 Monitoring line {line_number} from {address}")
            print(f"Last update: {datetime.now().strftime('%H:%M:%S')}\n")
            
            buses = fetch_nearby_buses(lat, lon, radius_km, line_number)
            if buses:
                for bus in buses:
                    distance = bus['distance_km']
                    direction = bus.get('Direction', 'N/A')
                    print(f"→ Bus {bus.get('Lines', 'N/A')} is {distance}km away")
                    print(f"  Direction: {direction}")
                    print(f"  Brigade: {bus.get('Brigade', 'N/A')}\n")
            else:
                print(f"No buses of line {line_number} found within {radius_km}km")
            
            time.sleep(60)  # Update every minute
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    address = input("Enter your address in Warsaw: ")
    line_number = input("Enter bus line number to monitor: ")
    radius = float(input("Enter radius in kilometers (default 10): ") or 10)
    
    monitor_buses(address, line_number, radius)
