from flight import Flight
from heap import *

class Planner:
    def __init__(self, flights):
        """Initialize flight planner with flight data"""
        self.flights = flights
        # Create array of flight lists for each city
        # Find max city number first
        max_city = 0
        for flight in flights:
            max_city = max(max_city, flight.start_city, flight.end_city)
        self.max_city = max_city
        self.adj_lists = [[] for _ in range(max_city + 1)]
        for flight in flights:
            self.adj_lists[flight.start_city].append(flight)

    def _is_visited(self, visited_list, city, time):
        """Helper to check if state is visited"""
        for (c, t) in visited_list:
            if c == city and t == time:
                return True
        return False

    # def least_flights_ealiest_route(self, start_city, end_city, t1, t2):
        """BFS using list as queue to find route with minimum flights"""
        if start_city == end_city:
            return []

        # Use list as queue: [(city, arrival_time, path)]
        queue = [(start_city, t1, [])]
        # Track visited states for each hop count to avoid cycles
        visited = []  # [(city, arrival_time)]
        
        min_hops = float('inf')
        best_route = None
        earliest_arrival = float('inf')
        
        while queue:
            # Pop first element (simulate deque)
            current = queue.pop(0)
            current_city, last_arrival, path = current
            current_hops = len(path)
            
            if current_hops > min_hops:
                break
                
            # Check all possible next flights
            for flight in self.adj_lists[current_city]:
                if (flight.departure_time >= last_arrival + 20 and 
                    flight.departure_time >= t1 and 
                    flight.arrival_time <= t2):
                    
                    new_path = path + [flight]
                    
                    if flight.end_city == end_city:
                        if len(new_path) < min_hops:
                            min_hops = len(new_path)
                            best_route = new_path
                            earliest_arrival = flight.arrival_time
                        elif len(new_path) == min_hops and flight.arrival_time < earliest_arrival:
                            best_route = new_path
                            earliest_arrival = flight.arrival_time
                    else:
                        # Continue exploring if not visited
                        if not self._is_visited(visited, flight.end_city, flight.arrival_time):
                            visited.append((flight.end_city, flight.arrival_time))
                            queue.append((flight.end_city, flight.arrival_time, new_path))
        
        return best_route if best_route is not None else []
    # def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """BFS with cost optimization for ties in number of flights"""
        if start_city == end_city:
            return []

        # Queue entries: (city, arrival_time, total_cost, path)
        queue = [(start_city, t1, 0, [])]
        visited = []  # [(city, arrival_time)]
        
        min_hops = float('inf')
        best_route = None
        min_cost = float('inf')
        
        while queue:
            current = queue.pop(0)
            current_city, last_arrival, total_cost, path = current
            current_hops = len(path)
            
            if current_hops > min_hops:
                break
                
            for flight in self.adj_lists[current_city]:
                if (flight.departure_time >= last_arrival + 20 and 
                    flight.departure_time >= t1 and 
                    flight.arrival_time <= t2):
                    
                    new_cost = total_cost + flight.fare
                    new_path = path + [flight]
                    
                    if flight.end_city == end_city:
                        if len(new_path) < min_hops:
                            min_hops = len(new_path)
                            best_route = new_path
                            min_cost = new_cost
                        elif len(new_path) == min_hops and new_cost < min_cost:
                            best_route = new_path
                            min_cost = new_cost
                    else:
                        if not self._is_visited(visited, flight.end_city, flight.arrival_time):
                            visited.append((flight.end_city, flight.arrival_time))
                            queue.append((flight.end_city, flight.arrival_time, 
                                        new_cost, new_path))
        
        return best_route if best_route is not None else []
    
    
    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Find route using DFS approach from start_city to end_city within time window t1 to t2.
        Uses lists to track visited cities and their costs.
        Returns list of flight numbers for the cheapest valid path.
        """
        if start_city == end_city:
            return []
            
        # List to store visited cities: [(city, arrival_time, cost)]
        visited = []
        
        def is_visited_better(city, time, cost):
            """Check if city was visited at same/earlier time with better cost"""
            for v_city, v_time, v_cost in visited:
                if v_city == city and v_time == time and v_cost <= cost:
                    return True
            return False
        
        def add_visited(city, time, cost):
            """Add city to visited list"""
            visited.append((city, time, cost))
        
        def remove_visited(city, time, cost):
            """Remove specific city visit from list"""
            if (city, time, cost) in visited:
                visited.remove((city, time, cost))
        
        # Track the best solution found
        min_cost = float('inf')
        best_path = []
        
        def dfs_helper(current_city, current_time, current_cost, current_path):
            nonlocal min_cost, best_path
            
            # If current path is already more expensive than best found, prune it
            if current_cost >= min_cost:
                return
                
            # If we reached destination with better cost, update result
            if current_city == end_city:
                min_cost = current_cost
                best_path = current_path[:]
                return
                
            # Check all possible flights from current city
            for flight in self.adj_lists[current_city]:
                # Skip if flight doesn't meet time constraints
                if (flight.departure_time < current_time + 20 or
                    flight.departure_time < t1 or
                    flight.arrival_time > t2):
                    continue
                    
                next_city = flight.end_city
                new_cost = current_cost + flight.fare
                
                # Skip if we've visited this city at this time with better cost
                if is_visited_better(next_city, flight.arrival_time, new_cost):
                    continue
                
                # Add to visited
                add_visited(next_city, flight.arrival_time, new_cost)
                
                # Explore this path
                dfs_helper(next_city, 
                        flight.arrival_time,
                        new_cost,
                        current_path + [flight])
                
                # Backtrack: remove from visited
                remove_visited(next_city, flight.arrival_time, new_cost)
        
        # Start DFS from initial city
        dfs_helper(start_city, t1, 0, [])
        
        # Convert flight objects to flight numbers
        return [flight.flight_number for flight in best_path]