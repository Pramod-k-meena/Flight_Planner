import time
from flight import Flight
from planner import Planner

def load_test_cases_from_file(filename):
    test_cases = []
    with open(filename, 'r') as file:
        num_test_cases = int(file.readline().strip())  # Number of test cases
        
        for _ in range(num_test_cases):
            n = int(file.readline().strip())  # Number of flights for this test case
            flights = []
            
            # Read each flight's data
            for _ in range(n):
                flight_data = file.readline().strip().split()
                flight_no = int(flight_data[0])
                start_city = int(flight_data[1])
                departure_time = int(flight_data[2])
                end_city = int(flight_data[3])
                arrival_time = int(flight_data[4])
                fare = int(flight_data[5])
                flights.append(Flight(flight_no, start_city, departure_time, end_city, arrival_time, fare))
            
            # Read the start city, end city, t1, and t2 after flights data
            start_city, end_city, t1, t2 = map(int, file.readline().strip().split())
            test_cases.append((flights, start_city, end_city, t1, t2))
    
    return test_cases
def format_route(route):
    """Helper function to format the route for easy reading."""
    if not route:
        return "No route found"
    return [flight.flight_no for flight in route]  # Return array of flight numbers for debug
import time
def main():
    # Load test cases from file
    test_cases = load_test_cases_from_file('main tester files/main_tester_input.txt')
    
    # Open output file
    with open('main tester files/main_tester_output.txt', 'w') as output_file:
        start_time2 = time.time()
        for i, (flights, start_city, end_city, t1, t2) in enumerate(test_cases, start=1):
            # Create a flight planner instance
            flight_planner = Planner(flights)
            
            # Route 1: Least Flights, Earliest Arrival
            start_time = time.time()
            route1 = flight_planner.least_flights_earliest_route(start_city, end_city, t1, t2)
            route1_time = time.time() - start_time
            route1_flights_count = len(route1) if route1 else 0
            route1_arrival_time = route1[-1].arrival_time if route1 else "No route"
            #print(f"Route 1 Time: {route1_time:.4f}")
            
            # Route 2: Cheapest Route
            start_time = time.time()
            route2 = flight_planner.cheapest_route(start_city, end_city, t1, t2)
            route2_time = time.time() - start_time
            route2_total_cost = sum(flight.fare for flight in route2)
            #print(f"Route 2 Time: {route2_time:.4f}")
            
            # Route 3: Least Flights, Cheapest Route
            start_time = time.time()
            route3 = flight_planner.least_flights_cheapest_route(start_city, end_city, t1, t2)
            route3_time = time.time() - start_time
            route3_flights_count = len(route3)
            route3_total_cost = sum(flight.fare for flight in route3)
            #print(f"Route 3 Time: {route3_time:.4f}")
            
            # Write output in the specified format, including test case number
            print(f"Test Case {i}:\n")
            output_file.write(f"Test Case {i}:\n")
            output_file.write(f"Route 1: {route1_flights_count}, {route1_arrival_time}\n")
            output_file.write(f"Route 2: {route2_total_cost}\n")
            output_file.write(f"Route 3: {route3_flights_count}, {route3_total_cost}\n\n")
        end_time2 = time.time()
        print(end_time2-start_time2)

if __name__ == "__main__":
    main()