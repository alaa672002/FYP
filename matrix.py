import pandas as pd
import json
import urllib.request

def create_data():
    """Creates the data."""
    data = {}
    data['API_key'] = 'AIzaSyBmExJmKbPo-FXlY2sGx7JWBBQx9UhA4gs'
    # Read latitude and longitude from data.csv
    df = pd.read_csv('data.csv', nrows=24)
    data['addresses'] = [f"{row['latitude']},{row['longitude']}" for _, row in df.iterrows()]

    return data

def create_distance_matrix(data):
    addresses = data["addresses"]
    API_key = data["API_key"]
    # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
    max_elements = 100
    num_addresses = len(addresses)
    max_rows = max_elements // num_addresses
    q, r = divmod(num_addresses, max_rows)
    dest_addresses = addresses
    distance_matrix = []
    # Send q requests, returning max_rows rows per request.
    for i in range(q):
        origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)

    # Get the remaining r rows, if necessary.
    if r > 0:
        origin_addresses = addresses[q * max_rows: q * max_rows + r]
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)
    return distance_matrix

def send_request(origin_addresses, dest_addresses, API_key):
    """ Build and send request for the given origin and destination addresses."""
    def build_address_str(addresses):
        return '|'.join(addresses)

    request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
    origin_address_str = build_address_str(origin_addresses)
    dest_address_str = build_address_str(dest_addresses)
    request = request + '&origins=' + origin_address_str + '&destinations=' + \
              dest_address_str + '&key=' + API_key
    response = json.loads(urllib.request.urlopen(request).read())
    return response

def build_distance_matrix(response):
    distance_matrix = []
    for row in response['rows']:
        row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
        distance_matrix.append(row_list)
    return distance_matrix

########
# Main #
########
def main():
    """Entry point of the program"""
    # Create the data.
    data = create_data()
    distance_matrix = create_distance_matrix(data)
    print(distance_matrix)

if __name__ == '__main__':
    main()
