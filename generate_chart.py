import pandas as pd
import json

def load_and_prepare_data(file_path):
    file_path = 'updated_flight_data_Departure.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Ensure numeric data types for aggregation
    numeric_columns = ['Crew', 'Pilots', 'Passagiere']
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')  # Convert and set errors to coerce for safety
    
    # Fill missing numeric data with zero
    df[numeric_columns] = df[numeric_columns].fillna(0)
    
    # Optionally convert 'Time' to categorical if it's not already suitable for grouping
    # df['Time'] = df['Time'].astype(str)  # Uncomment if necessary
    
    return df

def aggregate_data(df):
    # Group by 'Time' and sum up the relevant columns
    aggregated_data_by_hour = df.groupby('Time')[['Crew', 'Pilots', 'Passagiere']].sum().reset_index()
    return aggregated_data_by_hour

def main():
    file_path = 'path_to_your_data.json'
    df = load_and_prepare_data(file_path)
    aggregated_data = aggregate_data(df)
    
    # Save the aggregated data to a JSON file
    aggregated_data.to_json('aggregated_data_by_hour.json', orient='records')
    print("Aggregated data saved successfully.")

if __name__ == "__main__":
    main()
