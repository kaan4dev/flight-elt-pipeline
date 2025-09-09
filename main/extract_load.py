import requests
import pandas as pd

API_KEY = "ddccb4994fc11e824e16e64e1b35b878"
url = "http://api.aviationstack.com/v1/flights"

params = {
    "access_key": API_KEY,
    "dep_iata": "JFK",  # nyc
    "arr_iata": "LHR",  # london
    "limit": 100 
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    flights = data.get("data", [])
    if flights:
        print(f"{len(flights)} flights founded:")
        for i, flight in enumerate(flights, 1):
            departure_time = flight['departure'].get('scheduled', 'Unknown')
            arrival_time = flight['arrival'].get('scheduled', 'Unknown')
            departure_terminal = flight['departure'].get('terminal', 'Unknown')
            arrival_terminal = flight['arrival'].get('terminal', 'Unknown')
            departure_gate = flight['departure'].get('gate', 'Unknown')
            arrival_gate = flight['arrival'].get('gate', 'Unknown')
            delay = flight['departure'].get('delay', '0') or flight['arrival'].get('delay', '0')
            flight_number = flight['flight'].get('number', 'Unknown')
            airline = flight['airline'].get('name', 'Unknown')
            status = flight['flight_status']
            print(f"Flight {i}: {flight['departure']['iata']} → {flight['arrival']['iata']}, "
                  f"Flight No: {flight_number}, Airline: {airline}, "
                  f"Departure: {departure_time} (Terminal: {departure_terminal}, Gate: {departure_gate}), "
                  f"Arrival: {arrival_time} (Terminal: {arrival_terminal}, Gate: {arrival_gate}), "
                  f"Delay: {delay} min, State: {status}")

        # load
        df = pd.DataFrame(flights)
        df.to_csv('flights_records_raw.csv', index=False)
        print("flights are recorded to the  'flights_records_raw.csv' file.")
    else:
        print("\nData cannot be found.")
else:
    print(f"Error: {response.status_code} - {response.text}")


