import pandas as pd
import json

df = pd.read_csv('flights_records_raw.csv')

def parse_json_column(column, column_name):
    if pd.isna(column):
        return {}
    try:
        column = column.replace("None", "null")
        column = column.replace("'", '"')
        return json.loads(column)
    except json.JSONDecodeError as e:
        print(f"JSON error ({column_name}): {e}, column content: {column}")
        return {}

df['departure'] = df['departure'].apply(parse_json_column, column_name='departure')
df['arrival'] = df['arrival'].apply(parse_json_column, column_name='arrival')
df['airline'] = df['airline'].apply(parse_json_column, column_name='airline')
df['flight'] = df['flight'].apply(parse_json_column, column_name='flight')

df['departure_iata'] = df['departure'].apply(lambda x: x.get('iata', 'Unknown'))
df['departure_scheduled'] = df['departure'].apply(lambda x: x.get('scheduled', 'Unknown'))
df['departure_terminal'] = df['departure'].apply(lambda x: x.get('terminal', 'Unknown'))
df['departure_gate'] = df['departure'].apply(lambda x: x.get('gate', 'Unknown'))
df['departure_delay'] = df['departure'].apply(lambda x: x.get('delay', 0))

df['arrival_iata'] = df['arrival'].apply(lambda x: x.get('iata', 'Unknown'))
df['arrival_scheduled'] = df['arrival'].apply(lambda x: x.get('scheduled', 'Unknown'))
df['arrival_terminal'] = df['arrival'].apply(lambda x: x.get('terminal', 'Unknown'))
df['arrival_gate'] = df['arrival'].apply(lambda x: x.get('gate', 'Unknown'))
df['arrival_delay'] = df['arrival'].apply(lambda x: x.get('delay', 0))

df['airline_name'] = df['airline'].apply(lambda x: x.get('name', 'Unknown'))
df['flight_number'] = df['flight'].apply(lambda x: x.get('number', 'Unknown'))

df['departure_scheduled'] = pd.to_datetime(df['departure_scheduled'], format='%Y-%m-%dT%H:%M:%S%z', errors='coerce')
df['arrival_scheduled'] = pd.to_datetime(df['arrival_scheduled'], format='%Y-%m-%dT%H:%M:%S%z', errors='coerce')

df['departure_delay'] = pd.to_numeric(df['departure_delay'], errors='coerce').fillna(0)
df['arrival_delay'] = pd.to_numeric(df['arrival_delay'], errors='coerce').fillna(0)

df = df.drop(['departure', 'arrival', 'airline', 'flight', 'aircraft', 'live'], axis=1)

df.to_csv('flights_transformed.csv', index=False)
print("Veriler 'flights_transformed.csv' dosyasına dönüştürülerek kaydedildi.")