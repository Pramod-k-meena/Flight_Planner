import random
import time
from tqdm import tqdm  # For progress bar
from flight import Flight
from planner import Planner

def parse_test_case(file_path):
    with open(file_path, 'r') as file:
        n, m = map(int, file.readline().strip().split())  # Read number of vertices and edges
        flights = []
        cities = set()  # To keep track of all unique cities
        
        for _ in range(m):
            u, v, cost, start_time, end_time = map(int, file.readline().strip().split())
            flight = Flight(len(flights), u, start_time, v, end_time, cost)
            flights.append(flight)
            cities.update([u, v])  # Add both the start and end cities to the set
    
    return flights, list(cities)  # Return both flights and list of unique cities

def write_to_output(output_file, message):
    output_file.write(message + "\n")

def compare_outputs(expected_file_path, output_file_path):
    with open(output_file_path, 'r') as output_file:
        actual_output = [line for line in output_file.readlines() if not line.startswith("Time taken") and not line.startswith("Total time taken")]

    with open(expected_file_path, 'r') as expected_file:
        expected_output = [line for line in expected_file.readlines() if not line.startswith("Time taken") and not line.startswith("Total time taken")]

    mismatches = []
    for i, (actual, expected) in enumerate(zip(actual_output, expected_output), 1):
        if actual != expected:
            mismatches.append((i, actual, expected))

    return mismatches

def main():
    file_path = 'tester files/C.txt'
    expected_file_path = 'tester files/tester_correct_output.txt'  # Update this to the correct file path
    
    flights, cities = parse_test_case(file_path)
    flight_planner = Planner(flights)
    
    # Set random seed for consistent results
    sampled_pairs = [(3472, 8812), (3898, 5857), (9188, 1890), (9172, 4200), (2490, 2577), (8742, 3844), (3091, 4143), (8932, 4592), (1973, 1739), (3019, 667), (8594, 1874), (9842, 560), (2512, 3816), (1745, 9447), (949, 6732), (7124, 618), (2868, 1502), (9985, 1041), (3950, 8661), (401, 9030)]

    with open("tester files/tester_output.txt", 'w') as output_file:
        # Track overall start time
        overall_start_time = time.time()
        
        # Initialize tqdm progress bar
        for start_city, destination in tqdm(sampled_pairs, desc="Processing city pairs", unit="pair"):
            # Track the start time for this pair
            start_time = time.time()
            output_lines = [
                f"Testing routes for start_city={start_city}, destination={destination}"
            ]
            
            # Task 1: Least Flights Earliest Route
            route1 = flight_planner.least_flights_earliest_route(start_city, destination, 0, 3000000000000)
            if route1:
                num_flights_task1 = len(route1)
                arrival_time_task1 = route1[-1].arrival_time if num_flights_task1 > 0 else None
                output_lines.append(f"Task 1: Least Flights Earliest Route - Number of flights: {num_flights_task1}, Arrival time: {arrival_time_task1}")
            else:
                output_lines.append("Task 1: No route found.")
            
            # Task 2: Cheapest Route
            route2 = flight_planner.cheapest_route(start_city, destination, 0, 3000000000000)
            if route2:
                total_cost_task2 = sum(flight.fare for flight in route2)
                output_lines.append(f"Task 2: Cheapest Route - Total cost: {total_cost_task2}")
            else:
                output_lines.append("Task 2: No route found.")
            
            # Task 3: Least Flights Cheapest Route
            route3 = flight_planner.least_flights_cheapest_route(start_city, destination, 0, 30000000000)
            if route3:
                num_flights_task3 = len(route3)
                total_cost_task3 = sum(flight.fare for flight in route3)
                output_lines.append(f"Task 3: Least Flights Cheapest Route - Number of flights: {num_flights_task3}, Total cost: {total_cost_task3}")
            else:
                output_lines.append("Task 3: No route found.")
            
            # Calculate and log time taken for this pair
            time_taken = time.time() - start_time
            output_lines.append(f"Time taken for start_city={start_city}, destination={destination}: {time_taken:.2f} seconds")
            write_to_output(output_file, "\n".join(output_lines))
        
        # Calculate and log overall time taken
        overall_time_taken = time.time() - overall_start_time
        write_to_output(output_file, f"Total time taken for all tests: {overall_time_taken:.2f} seconds")

    mismatches = compare_outputs(expected_file_path, "tester files/tester_output.txt")
    if not mismatches:
        print("All test cases passed.")
        print(f"Total time taken for all tests: {overall_time_taken:.2f} seconds")
    else:
        print("Mismatches found:")
        for i, actual, expected in mismatches:
            print(f"Test case {i}:")
            print("Expected output:")
            print(expected)
            print("Actual output:")
            print(actual)
        print(f"Total mismatches: {len(mismatches)}")

if __name__ == "__main__":
    main()