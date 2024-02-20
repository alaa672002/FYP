import requests
import pandas as pd
import json
import time
from tqdm import tqdm
import config

def get_distance_and_duration(origin_lat, origin_lng, dest_lat, dest_lng, api_key, counter):
    """
    Get distance and duration between two points using Distance Matrix API.

    Args:
    - origin_lat (float): Latitude of the origin point.
    - origin_lng (float): Longitude of the origin point.
    - dest_lat (float): Latitude of the destination point.
    - dest_lng (float): Longitude of the destination point.
    - api_key (str): API key for accessing the Distance Matrix API.
    - counter (tqdm.tqdm): Progress counter for tracking API requests.

    Returns:
    - tuple: A tuple containing distance (in meters) and duration (in seconds).
    """
    try:
        # url = f"https://api.distancematrix.ai/maps/api/distancematrix/json?origins={origin_lat},{origin_lng}&destinations={dest_lat},{dest_lng}&key={api_key}"
        url = f"https://api-v2.distancematrix.ai/maps/api/distancematrix/json?origins={origin_lat},{origin_lng}&destinations={dest_lat},{dest_lng}&key={api_key}"
        
        response = requests.get(url)
        counter.update(1)  # Update the counter
        data = response.json()
        distance = data['rows'][0]['elements'][0]['distance']['value']
        duration = data['rows'][0]['elements'][0]['duration']['value']
        return distance, duration
    except Exception as e:
        print(f"Error occurred for request: {url}")
        print(f"Error message: {str(e)}")


def main(dataframe,vehicle_id,api_key,mode='both'):
    """
    Compute distance and duration matrices for given locations.

    Args:
    - dataframe (pd.DataFrame): DataFrame containing location data.
    - vehicle_id (int): ID of the vehicle associated with the data.
    - api_key (str): API key for accessing the Distance Matrix API.
    - mode (str, optional): Either 'distance', 'duration', or 'both'. Specifies whether to compute only distance matrix, only duration matrix, or both. Defaults to 'both'.
    """
    api_key = api_key
    df = dataframe
    locations = list(zip(df['latitude'], df['longitude']))

    distance_matrix = []
    duration_matrix = []
    total_requests = len(locations) ** 2  # Total number of requests to be made
    counter = tqdm(total=total_requests, desc="Progress")  # Initialize tqdm counter

    for origin_lat, origin_lng in locations:
        row_distances = []
        row_durations = []
        for dest_lat, dest_lng in locations:
            distance, duration = get_distance_and_duration(origin_lat, origin_lng, dest_lat, dest_lng, api_key, counter)
            if mode == 'distance':
                row_distances.append(distance)
            elif mode == 'duration':
                row_durations.append(duration)
            else:
                row_distances.append(distance)
                row_durations.append(duration)
        distance_matrix.append(row_distances)
        duration_matrix.append(row_durations)

    # Store data in JSON format
    if mode == 'distance' or mode == 'both':
        with open(f'data/distance_matrix/distance_matrix_{vehicle_id}.json', 'w') as distance_file:
            json.dump(distance_matrix, distance_file)
    if mode == 'duration' or mode == 'both':
        with open(f'data/duration_matrix/duration_matrix_{vehicle_id}.json', 'w') as duration_file:
            json.dump(duration_matrix, duration_file)

    # Close tqdm counter
    counter.close()

    print(f"{'Distance' if mode != 'duration' else 'Duration'} matrix:")
    for row in (distance_matrix if mode != 'duration' else duration_matrix):
        print(row)

if __name__ == "__main__":
    start1 = time.time()
    api_key = config.api_key 
    df = pd.read_csv('data/input/datafull.csv')
    # Group data by vehicle_id
    grouped_data = df.groupby('vehicle_id')

    # Create a dictionary to hold DataFrames for each vehicle_id
    vehicle_dataframes = {}

    # Iterate over groups and create a DataFrame for each vehicle_id
    for vehicle_id, group in grouped_data:
        vehicle_dataframes[vehicle_id] = group

    # Example usage: printing the first few rows of each DataFrame
    for vehicle_id, dataframe in vehicle_dataframes.items():
        print(f"Data for vehicle ID {vehicle_id}:")
        print(f'{dataframe} with {len(dataframe)} stops')  # Or any other operation you want to perform
        
        dataframe.to_csv(f'data/dfs/{vehicle_id}_df.csv',index=False)
        main(dataframe,vehicle_id,api_key,'both')

    stop1 = time.time()
    print("Time to run API:", stop1-start1)
