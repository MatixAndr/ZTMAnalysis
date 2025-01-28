import requests
from math import radians, sin, cos, sqrt, atan2
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def fetch_nearby_buses(my_lat, my_lon, radius_km=10):
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

if __name__ == "__main__":
    warsaw_lat = 52.231838
    warsaw_lon = 21.005995
    
    buses = fetch_nearby_buses(warsaw_lat, warsaw_lon)
    print(f"Found {len(buses)} buses within 10km radius:")
    for bus in buses:
        print(f"Bus {bus.get('Lines', 'N/A')}: {bus['distance_km']}km away")
