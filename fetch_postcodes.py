import json
import pandas as pd
import requests

# Function to load JSON response from a URL
def loadJsonResponse(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception if the request was not successful
    return response.json()['result']

# Function to validate a postcode
def validatePostcode(postcode):
    url = f'https://api.postcodes.io/postcodes/{postcode}/validate'
    return loadJsonResponse(url)

# Function to find nearest postcodes to a given postcode
def findnearestPostcode(postcode):
    url = f'https://api.postcodes.io/postcodes/{postcode}/nearest'
    return loadJsonResponse(url)

# Function to fetch a random postcode
def randomPostcode():
    url = 'https://api.postcodes.io/random/postcodes'
    return loadJsonResponse(url)

# Function to query postcodes
def queryPostcode(postcode):
    url = f'https://api.postcodes.io/postcodes?q={postcode}'
    return loadJsonResponse(url)

# Function to get autocomplete suggestions for a postcode
def getAutoCompletePostcode(postcode):
    url = f'https://api.postcodes.io/postcodes/{postcode}/autocomplete'
    return loadJsonResponse(url)

# Function to fetch and update postcodes
def fetch_and_update_postcodes(seen_postcodes, vehicle_id):
    unique_postcodes = 0
    # Loop until we have 10 unique postcodes
    while unique_postcodes <= 10:
        print(f'{unique_postcodes} unique postcodes for list {seen_postcodes}')
        
        new_postcode = seen_postcodes.pop()  # Get a postcode from the set
        print(new_postcode, type(new_postcode))
        
        if new_postcode in seen_postcodes:
            continue  # Skip if the postcode is already seen

        seen_postcodes.add(new_postcode)  # Add the postcode to the set
        
        new_postcode = new_postcode[:3] + '%20' + new_postcode[-3:]  # Format the postcode
        print(new_postcode, 'formatted')
        
        nearest_postcodes = findnearestPostcode(new_postcode)  # Find nearest postcodes

        for result in nearest_postcodes:
            extracted_postcode = result['postcode']
            seen_postcodes.add(extracted_postcode)
            extracted_postcode = extracted_postcode[:3] + '%20' + extracted_postcode[-3:]
            print(f"Nearest postcode to {new_postcode}: {extracted_postcode}")
        
        unique_postcodes = len(seen_postcodes)  # Update the count of unique postcodes

    print(f"Found {unique_postcodes} unique postcodes in total.")
    print(seen_postcodes)
    
    return pd.DataFrame({'postcode_api': list(seen_postcodes), 'vehicle_id': vehicle_id})

# Main function
def main():
    seen_postcodes_list = ['B23 7RJ', 'B18 5RE', 'B90 1SQ', 'B60 3JT', 'B67 6AX',
                           'B19 2AL', 'B32 1HP', 'B29 7SG', 'B92 9JH', 'B62 9QW']
    dataframes = []

    # Iterate over each starting postcode
    for i, postcode in enumerate(seen_postcodes_list, start=1):
        seen_postcodes = set([postcode])
        df = fetch_and_update_postcodes(seen_postcodes, i)
        dataframes.append(df)

    result = pd.concat(dataframes, ignore_index=True)
    result.to_csv('coordinates_data.csv', index=False)

if __name__ == "__main__":
    main()
