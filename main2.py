from flight import Flight
from planner import Planner
import random
import time

def test_planner():
    # Helper function to print the route details
    def print_route(route):
        if not route:
            print("No route found.")
        else:
            total_fare = sum(flight.fare for flight in route)
            print(f"Total flights: {len(route)}, Total fare: {total_fare}")
            for flight in route:
                print(f"Flight {flight.flight_no}: {flight.start_city} -> {flight.end_city}, "
                      f"Departure: {flight.departure_time}, Arrival: {flight.arrival_time}, Fare: {flight.fare}")
        print()

    # Test Case 1: Simple direct flight
    flights = [
        Flight(1, 0, 100, 1, 200, 500)
    ]
    planner = Planner(flights)
    route = planner.least_flights_ealiest_route(0, 1, 0, 300)
    print("Test Case 1 - Simple Direct Flight:")
    print_route(route)

    # Test Case 2: No possible route due to time constraints
    flights = [
        Flight(1, 0, 100, 1, 200, 500)
    ]
    planner = Planner(flights)
    route = planner.least_flights_ealiest_route(0, 1, 300, 400)
    print("Test Case 2 - No Possible Route Due to Time Constraints:")
    print_route(route)

    # Test Case 3: Multiple routes with same number of flights, different arrival times
    flights = [
        Flight(1, 0, 100, 1, 300, 500),
        Flight(2, 0, 150, 1, 250, 500),
        Flight(3, 0, 200, 1, 200, 500)
    ]
    planner = Planner(flights)
    route = planner.least_flights_ealiest_route(0, 1, 0, 500)
    print("Test Case 3 - Multiple Routes with Same Number of Flights, Different Arrival Times:")
    print_route(route)

    # Test Case 4: Multiple routes with same number of flights, same arrival times, different fares
    flights = [
        Flight(1, 0, 100, 1, 200, 500),
        Flight(2, 0, 100, 1, 200, 400),  # Cheaper fare
        Flight(3, 0, 100, 1, 200, 600)
    ]
    planner = Planner(flights)
    route = planner.cheapest_route(0, 1, 0, 300)
    print("Test Case 4 - Multiple Routes with Same Arrival Time, Different Fares:")
    print_route(route)

    # Test Case 5: Testing 20-minute connection constraint
    flights = [
        Flight(1, 0, 100, 1, 200, 500),
        Flight(2, 1, 220, 2, 300, 500)  # Departs 20 minutes after arrival
    ]
    planner = Planner(flights)
    route = planner.least_flights_ealiest_route(0, 2, 0, 400)
    print("Test Case 5 - Testing 20-minute Connection Constraint:")
    print_route(route)

    # Test Case 6: Flight departs less than 20 minutes after arrival
    flights = [
        Flight(1, 0, 100, 1, 200, 500),
        Flight(2, 1, 210, 2, 300, 500)  # Departs only 10 minutes after arrival
    ]
    planner = Planner(flights)
    route = planner.least_flights_ealiest_route(0, 2, 0, 400)
    print("Test Case 6 - Flight Departs Less Than 20 Minutes After Arrival (Should Not Be Considered):")
    print_route(route)

    # Test Case 7: Flight departs exactly 20 minutes after arrival
    flights = [
        Flight(1, 0, 100, 1, 200, 500),
        Flight(2, 1, 220, 2, 300, 500)  # Departs exactly 20 minutes after arrival
    ]
    planner = Planner(flights)
    route = planner.least_flights_ealiest_route(0, 2, 0, 400)
    print("Test Case 7 - Flight Departs Exactly 20 Minutes After Arrival:")
    print_route(route)

    # Test Case 8: Maximum flights per city
    flights = []
    for i in range(100):
        flights.append(Flight(i, 0, 100 + i, 1, 200 + i, 500))
    planner = Planner(flights)
    route = planner.least_flights_ealiest_route(0, 1, 0, 300)
    print("Test Case 8 - Maximum Flights Per City:")
    print_route(route)

    # Test Case 9: Large number of flights to test efficiency
    flights = []
    num_flights = 10000
    for i in range(num_flights):
        start_city = random.randint(0, 50)
        end_city = random.randint(0, 50)
        if start_city == end_city:
            continue
        departure_time = random.randint(0, 10000)
        arrival_time = departure_time + random.randint(50, 500)
        fare = random.randint(100, 1000)
        flights.append(Flight(i, start_city, departure_time, end_city, arrival_time, fare))
    planner = Planner(flights)
    start_time = time.time()
    route = planner.cheapest_route(0, 25, 0, 20000)
    end_time = time.time()
    print("Test Case 9 - Large Number of Flights to Test Efficiency:")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    print_route(route)

    # Test Case 10: Testing with t1=0 and t2=infinite
    flights = [
        Flight(1, 0, 100, 1, 200, 500),
        Flight(2, 1, 220, 2, 300, 500),
        Flight(3, 2, 320, 3, 400, 500)
    ]
    planner = Planner(flights)
    route = planner.least_flights_cheapest_route(0, 3, 0, float('inf'))
    print("Test Case 10 - Testing with t1=0 and t2=Infinite:")
    print_route(route)

    # Test Case 11: No possible route due to 20-minute constraint
    flights = [
        Flight(1, 0, 100, 1, 200, 500),
        Flight(2, 1, 210, 2, 300, 500)  # Departs only 10 minutes after arrival
    ]
    planner = Planner(flights)
    route = planner.least_flights_cheapest_route(0, 2, 0, 500)
    print("Test Case 11 - No Possible Route Due to 20-Minute Constraint:")
    print_route(route)

if __name__ == "__main__":
    test_planner()
