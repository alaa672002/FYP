import pandas as pd
import requests
import time

def convert_postcodes_to_coordinates(input_file, output_file):
    # Read the input CSV file
    data = pd.read_csv(input_file)
    
    # Initialize empty lists to store coordinates
    latitudes = []
    longitudes = []
    
    # Define Google Maps Geocoding API endpoint and your API key
    api_endpoint = 'https://maps.googleapis.com/maps/api/geocode/json'
    api_key = 'AIzaSyBmExJmKbPo-FXlY2sGx7JWBBQx9UhA4gs'  # Replace 'YOUR_API_KEY' with your actual API key
    
    # Iterate through postcodes and convert them to coordinates
    for postcode in data['postcode']:
        try:
            # Send request to Google Maps Geocoding API
            response = requests.get(api_endpoint, params={'address': postcode, 'key': api_key})
            response_json = response.json()
            
            # Parse response and extract coordinates
            if response_json['status'] == 'OK':
                location = response_json['results'][0]['geometry']['location']
                latitudes.append(location['lat'])
                longitudes.append(location['lng'])
            else:
                latitudes.append(None)
                longitudes.append(None)
        except Exception as e:
            print(f"Error occurred for postcode {postcode}: {e}")
            latitudes.append(None)
            longitudes.append(None)
        
        # Add a small delay to avoid overloading the API
        time.sleep(1)
    
    # Add coordinates to the dataframe
    data['latitude'] = latitudes
    data['longitude'] = longitudes
    
    # Save the dataframe to a new CSV file
    data.to_csv(output_file, index=False)

# Define input and output file paths
input_file = 'test.csv'
output_file = 'coordinates.csv'

# Convert postcodes to coordinates and save to a new file
convert_postcodes_to_coordinates(input_file, output_file)

print("Coordinates have been saved to coordinates.csv")
