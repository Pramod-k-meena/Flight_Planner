from flight import Flight
from heap import *
#THERE IS STILL EROR IN EARLIEST THINGS (SECOND CRITERIAS)
class Planner:
    def __init__(self, flights):
        """Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        # self.flight_lookup = [None] * (len(flights) + 1)
        # for flight in flights:
        #     self.flight_lookup[flight.flight_no] = flight

        self.flights = flights
        max_city = 0
        for flight in flights:
            max_city = max(max_city, flight.start_city, flight.end_city)
        self.max_city = max_city
        
        self.adj_lists = [[] for _ in range(max_city + 1)]
        for flight in flights:
            self.adj_lists[flight.start_city].append(flight)
        

    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        if start_city == end_city:
            return []

        # lis: [(flight_count, current_city, last_arrival, path)]
        lis = [(0, t1 ,start_city, [])]
        earliest_arrival = float('inf')
        result = []
        visited = [float('inf')] * (self.max_city + 1)
        while lis:
            # Implementing a basic lis by popping the first element each time
            flight_count, last_arrival, current_city, path = lis.pop(0)

            # Check if we reached the destination with fewer flights and earlier arrival
            if current_city == end_city and last_arrival <= t2 and last_arrival < earliest_arrival:
                earliest_arrival = last_arrival
                result = path
                continue

            for flight in self.adj_lists[current_city]:
                if(current_city == start_city or flight.departure_time >= last_arrival + 20) and flight.arrival_time <= t2 and flight.departure_time >= t1:
                    if flight.arrival_time < visited[flight.end_city]:
                        visited[flight.end_city] = flight.arrival_time
                        lis.append((flight_count + 1, flight.arrival_time, flight.end_city, path + [flight]))

        return result

#THERE IS STILL EROR IN EARLIEST THINGS (SECOND CRITERIAS)

    def cheapest_route(self, start_city, end_city, t1, t2):
        if start_city == end_city:
            return []
        
        def compare_entries(x, y):
            return x[0] < y[0]  # Compare based on total_cost
        
        pq = Heap(comparison_function=compare_entries)
        visited = [float('inf')] * (self.max_city+1)

        pq.insert((0, t1, start_city, []))
        visited[start_city] = 0
        least_cost = float('inf')
        result = []

        while len(pq)>0:
            entry = pq.extract()
            total_cost, last_arrival, current_city, path = entry

            if current_city == end_city and total_cost < least_cost and last_arrival <= t2:
                least_cost = total_cost
                result = path
                continue

            for flight in self.adj_lists[current_city]:
                if(current_city == start_city or flight.departure_time >= last_arrival + 20) and flight.arrival_time <= t2 and flight.departure_time >= t1:
                    if flight.departure_time >= t1:
                        new_cost = total_cost + flight.fare
                        if new_cost < visited[flight.end_city]:
                            visited[flight.end_city] = new_cost
                            pq.insert((new_cost, flight.arrival_time, flight.end_city, path + [flight]))
        return result
    
    """
################# THIS IS  CORRECT JUST ANOTHER WITH TIME COMPLEXITY BETTER IN BELOW
"""

    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        if start_city == end_city:
            return []
        
        def compare_entries(x, y):
            # Prioritize by number of flights, then by cost
            return (x[0] < y[0]) or (x[0] == y[0] and x[1] < y[1])
        
        pq = Heap(comparison_function=compare_entries)
        visited = [float('inf')] * (self.max_city + 1)
        pq.insert((0, 0, t1, start_city, []))  # (flight_count, total_cost, last_arrival, current_city, path)
        visited[start_city] = 0
        result = []

        while len(pq) > 0:
            flight_count, total_cost, last_arrival, current_city, path = pq.extract()

            if current_city == end_city:
                result = path
                break

            for flight in self.adj_lists[current_city]:
                if(current_city == start_city or flight.departure_time >= last_arrival + 20) and flight.arrival_time <= t2 and flight.departure_time >= t1:
                    new_cost = total_cost + flight.fare
                    new_flight_count = flight_count + 1
                    if new_cost < visited[flight.end_city]:
                        visited[flight.end_city] = new_cost
                        pq.insert((new_flight_count, new_cost, flight.arrival_time, flight.end_city, path + [flight]))

        return result
