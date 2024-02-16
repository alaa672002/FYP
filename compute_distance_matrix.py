
import pandas as pd
import googlemaps
from itertools import tee
import config
import time
from itertools import islice

#input: CSV file with id,latitude, longitude and capacities
# desired output: list with matrix distance for each point consumed by or tools
start1 = time.time()

df = pd.read_csv('data.csv')
#print(df)

API_key = config.api_key #enter your google maps api key here
try:
    gmaps = googlemaps.Client(key=API_key)
except ValueError as e :
    print(f'Error consulting API: {e}')


#empty list - will be used to store calculated distances
time_list = []
distance_list = []
origin_id_list = []
destination_id_list = []

for (i1, row1) in df.iterrows():
  #print("origin")
  #print(row1['ID'])
  LatOrigin = row1['latitude']
  LongOrigin = row1['longitude']
  origin = (LatOrigin, LongOrigin)
  origin_id = row1['order_id']
  for (i2, row2) in  df.iterrows():
    #print("destination id")
    #print(row2['ID'])
    LatDestination = row2['latitude']
    LongDestination = row2['longitude']
    destination_id = row2['order_id']
    destination = (LatDestination, LongDestination)

    print(destination,destination_id)

    try:
        result = gmaps.distance_matrix(origin, destination, mode='driving')
        #uncomment for cool api logs
        #print(result)
        result_distance = result["rows"][0]["elements"][0]["distance"]["value"]
        result_time = result["rows"][0]["elements"][0]["duration"]["value"]
        time_list.append(result_time)
        distance_list.append(result_distance)
        origin_id_list.append(origin_id)
        destination_id_list.append(destination_id)
        #print(df)
    except Exception as e :
       print(f'Error consulting API: {e}')

size=(len(df.latitude))
#print(distance_list)
#print(result_time)
#print(result_distance)
#print(origin_id)
#print(destination_id)

  
# Input list initialization
Input = distance_list
  
# list of length in which we have to split
number_containers = len(df['order_id'])
print("Number of Containers: ",number_containers)

length_to_split = number_containers*[number_containers]
#print(length_to_split)
  
# Using islice
Inputt = iter(Input)
Output = [list(islice(Inputt, elem))
          for elem in length_to_split]
  

stop1 = time.time()
start2 = time.time()
# Printing Output
print("API list", Input)
#print("Split length list: ", length_to_split)
print("List of Lists", Output)