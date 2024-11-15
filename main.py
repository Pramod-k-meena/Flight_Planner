from flight import Flight
from planner import Planner

def main():
    flights = [Flight(0, 0, 0, 1, 80, 50),      # City 0 to 1
               Flight(1, 0, 0, 1, 80, 40),     # City 0 to 3
               Flight(2, 1, 100, 2, 110, 120),   # City 1 to 2
               ]
    
    flight_planner = Planner(flights)
    
    # The three tasks
    # route1 = flight_planner.least_flights_earliest_route(0, 1, 0, 800)
    # route2 = flight_planner.cheapest_route(1, 4, 0, 300)
    route3 = flight_planner.least_flights_cheapest_route(0, 2, 0, 800)
    
    # Note that for this given example there is a unique solution, but it may
    # not be true in general
    # if route1 == expected_route1:
    #     print("Task 1 PASSED")
    # else:
    #     print("Task 1 FAILED",route1)
    for flight in route3:
        print(f"Flight No: {flight.flight_no}, Start City: {flight.start_city}, "
              f"Departure Time: {flight.departure_time}, End City: {flight.end_city}, "
              f"Arrival Time: {flight.arrival_time}, Fare: {flight.fare}")
    print("-------------------------------------------------")
    # if route3 == expected_route3:
    #     print("Task 3 PASSED")
    # else:
    #     print("Task 3 FAILED",route3)

if __name__ == "__main__":
    main()
