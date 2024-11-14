from flight import Flight
from planner import Planner

def main():
    flights = [
        Flight(0, 0, 0, 1, 50, 100),    # 0 to 1
        Flight(1, 0, 0, 2, 10, 100),    # 0 to 2
        Flight(2, 2, 30, 1, 40, 100),   # 2 to 1
        Flight(3, 1, 60, 3, 70, 100),   # 1 to 3
        Flight(4, 1, 70, 4, 80, 1000),   # 1 to 4
        Flight(5, 4, 100, 3, 110, 100), # 4 to 3
    ]
    flight_planner = Planner(flights)
    
    # The three tasks
    route2 = flight_planner.least_flights_ealiest_route(0, 3, 0, 3000000)
    route3 = flight_planner.cheapest_route(0, 3, 0, 300)
    route4 = flight_planner.least_flights_cheapest_route(0, 3, 0, 300)
    
    for flight in route2:
        print(f"Flight No: {flight.flight_no}, Start City: {flight.start_city}, "
              f"Departure Time: {flight.departure_time}, End City: {flight.end_city}, "
              f"Arrival Time: {flight.arrival_time}, Fare: {flight.fare}")
    print("-------------------------------------------------")
    for flight in route3:
        print(f"Flight No: {flight.flight_no}, Start City: {flight.start_city}, "
              f"Departure Time: {flight.departure_time}, End City: {flight.end_city}, "
              f"Arrival Time: {flight.arrival_time}, Fare: {flight.fare}")
    print("-------------------------------------------------")
    for flight in route4:
        print(f"Flight No: {flight.flight_no}, Start City: {flight.start_city}, "
              f"Departure Time: {flight.departure_time}, End City: {flight.end_city}, "
              f"Arrival Time: {flight.arrival_time}, Fare: {flight.fare}")
if __name__ == "__main__":
    main()