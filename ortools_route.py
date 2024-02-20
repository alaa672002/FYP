"""Capacited Vehicles Routing Problem (CVRP)."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import pandas as pd
import googlemaps
from itertools import tee

import time
import json

#input: CSV file with id,latitude, longitude and capacities
# desired output: list with matrix distance for each point consumed by or tools
start1 = time.time()


# Load the JSON file
# with open('distance_matrix_1.0.json', 'r') as json_file:
#     data = json.load(json_file)

with open('data/distance_matrix/distance_matrix_4_points.json', 'r') as json_file:
    data = json.load(json_file)


# Extract the first line (assuming it's a list of lists)
first_line = data

# Now you can use the variable 'first_line' as needed
print(first_line)

Output = first_line
num_points = len(first_line)
print(num_points)

df = pd.read_csv('data.csv', nrows=num_points)

# df = pd.read_csv('1.0_df.csv')

def create_data_model():
    """Stores the data for the problem."""
    data = {}
   

    #always 1 number bigger, because it has to return to base
    data['distance_matrix'] = Output
    
    # full container: 600 to 800kg
    # normal: a cada 10, 3 cheios, outros 7 de 50% pra cima
    # 30% cheios, outros 70% de 50% pra cima
    capacities = df['order_weight']
    print(capacities)

    data['demands'] = df['order_weight'].values.tolist()
    print(data['demands'])


    # 1 vehicle
    # capacity: 9000 to 12000 kg
    data['vehicle_capacities'] = [700]
    data['num_vehicles'] = 1

    data['depot'] = 0
    print("Input OR-Tools: ",data," ",type(data))
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                 route_load)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
        
    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))


def main():
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Setting first solution heuristic.
    
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(1)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print("no solution found")


if __name__ == '__main__':
    main()
    stop1 = time.time()
    print("Time to run routing:", stop1-start1)
