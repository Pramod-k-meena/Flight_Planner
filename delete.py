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
        

    def least_flights_ealiest_route(self, start_city, end_city, t1, t2):
        if start_city == end_city:
            return []
        
        visited = [(float('inf'), float('inf'))] * (self.max_city + 1)
        visited[start_city] = (0, t1)
        
        queue = [(0, t1, start_city)]
        best_flight = [None] * (self.max_city + 1)
        
        while queue:
            flight_count, last_arrival, current_city = queue.pop(0)
            
            if current_city == end_city:
                continue
                
            for flight in self.adj_lists[current_city]:
                if (current_city == start_city or flight.departure_time >= last_arrival + 20) and \
                flight.arrival_time <= t2 and flight.departure_time >= t1:
                    
                    new_count = flight_count + 1
                    curr_best_count, curr_best_time = visited[flight.end_city]
                    
                    if (new_count < curr_best_count) or \
                    (new_count == curr_best_count and flight.arrival_time < curr_best_time):
                        visited[flight.end_city] = (new_count, flight.arrival_time)
                        best_flight[flight.end_city] = flight
                        queue.append((new_count, flight.arrival_time, flight.end_city))
        
        result = []
        current_city = end_city
        while current_city != start_city:
            if(best_flight[current_city]==None):
                return []
            result.append(best_flight[current_city])
            current_city = best_flight[current_city].start_city
        result.reverse()
        return result

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
        
        visited = [(float('inf'), float('inf'))] * (self.max_city + 1)
        visited[start_city] = (0, 0)
        
        # Queue entries: (flight_count, total_cost, last_arrival, current_city)
        queue = [(0, 0, t1, start_city)]
        best_flight = [None] * (self.max_city + 1)
        
        while queue:
            flight_count, total_cost, last_arrival, current_city = queue.pop(0)
            
            if current_city == end_city:
                continue
                
            for flight in self.adj_lists[current_city]:
                if (current_city == start_city or flight.departure_time >= last_arrival + 20) and \
                flight.arrival_time <= t2 and flight.departure_time >= t1:
                    new_count = flight_count + 1
                    new_cost = total_cost + flight.fare
                    curr_best_count, curr_best_cost = visited[flight.end_city]
                    
                    # Update if:
                    # 1. We found a route with fewer flights OR
                    # 2. Same number of flights but cheaper total cost
                    if (new_count < curr_best_count) or \
                    (new_count == curr_best_count and new_cost < curr_best_cost):
                        visited[flight.end_city] = (new_count, new_cost)
                        best_flight[flight.end_city] = flight
                        queue.append((new_count, new_cost, flight.arrival_time, flight.end_city))
        
        # Check if we found a valid path
        if visited[end_city][0] == float('inf'):
            return []
            
        # Reconstruct path
        result = []
        current_city = end_city
        while current_city != start_city:
            if best_flight[current_city] is None:
                return []
            result.append(best_flight[current_city])
            current_city = best_flight[current_city].start_city
        result.reverse()
        return result