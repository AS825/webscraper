import json

def load_json_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def get_crew_size(passengers, crew_mapping):
    if passengers < 100:
        return crew_mapping["<100"]
    elif 100 <= passengers <= 140:
        return crew_mapping["100-140"]
    elif 141 <= passengers <= 170:
        return crew_mapping["141-170"]
    elif 171 <= passengers <= 200:
        return crew_mapping["171-200"]
    elif passengers >= 201:
        return crew_mapping["201+"]
    return "Unknown"

def update_flight_data(flights, passenger_mapping, crew_mapping):
    for flight in flights:
        plane = flight["Plane"]
        passengers = passenger_mapping.get(plane, "Unknown")
        flight["Passagiere"] = passengers
        
        if isinstance(passengers, int):
            crew_size = get_crew_size(passengers, crew_mapping)
            pilots = 2 if passengers <= 150 else 3
            flight["Crew"] = crew_size
            flight["Pilots"] = pilots
        else:
            flight["Crew"] = "Unknown"
            flight["Pilots"] = "Unknown"
    return flights

def save_json_data(data, filename):
    """ Save data to a JSON file """
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def calculate_passengers_and_crew():
    # Load mappings and flight data
    crew_mapping = load_json_data('crew_mapping.json')
    passenger_mapping = load_json_data('passenger_mapping.json')
    flights = load_json_data('flight_data_Departure.json')
    
    # Update flight data
    updated_flights = update_flight_data(flights, passenger_mapping, crew_mapping)
    
    # Save updated data
    save_json_data(updated_flights, 'updated_flight_data_Departure.json')
    print("Updated flight data has been saved.")

