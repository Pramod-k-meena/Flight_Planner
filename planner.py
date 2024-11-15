from flight import Flight

class Planner:
    def __init__(self, flights):
        """Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """

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
        pq = LinkedList()
        required_flight = None
        prv_flight = [None for _ in range(len(self.flights) + 1)]
        counter = [float('inf') for _ in range(len(self.flights) + 1)]
        least_count = float('inf')
        least_time = float('inf')
        for flight in self.adj_lists[start_city]:
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                pq.append((1, flight))
                counter[flight.flight_no] = 1
        while pq.is_empty() == False:
            entry = pq.pop_front()
            flight_count,  last_flight = entry
            last_arrival, current_city = last_flight.arrival_time, last_flight.end_city
            if current_city == end_city:
                if flight_count < least_count or (flight_count == least_count and last_arrival<least_time):
                    least_count = flight_count
                    least_time = last_arrival
                    required_flight = last_flight
                continue

            if(flight_count>=least_count):
                continue

            for flight in self.adj_lists[current_city]:
                if(flight.departure_time >= last_arrival + 20) and flight.arrival_time <= t2 and flight.departure_time >= t1:
                    if(flight_count+1 < counter[flight.flight_no]):
                        counter[flight.flight_no] = flight_count+1
                        prv_flight[flight.flight_no] = last_flight
                        pq.append((flight_count+1, flight))

        result = []
        current_flight = required_flight
        while current_flight:
            result.append(current_flight)
            current_flight = prv_flight[current_flight.flight_no]
        return result[::-1]


    def cheapest_route(self, start_city, end_city, t1, t2):
        if start_city == end_city:
            return []
        
        def compare_entries(x, y):
            return x[0] < y[0]  # Compare based on total_cost
        
        pq = Heap(comparison_function=compare_entries)
        cost = [float('inf') for _ in range(len(self.flights) + 1)]
        least_cost = float('inf')
        prv_flight = [None for _ in range(len(self.flights) + 1)]
        required_flight = None

        for flight in self.adj_lists[start_city]:
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                cost[flight.flight_no] = flight.fare
                pq.insert((flight.fare, flight))

        while len(pq)>0:
            entry = pq.extract()
            total_cost,  last_flight = entry
            last_arrival, current_city = last_flight.arrival_time, last_flight.end_city

            if current_city == end_city:
                if total_cost < least_cost:
                    least_cost = total_cost
                    required_flight = last_flight
                continue

            if(total_cost>=least_cost):
                continue

            for flight in self.adj_lists[current_city]:
                if(flight.departure_time >= last_arrival + 20) and flight.arrival_time <= t2 and flight.departure_time >= t1:
                    new_cost = total_cost + flight.fare
                    if(new_cost < cost[flight.flight_no]):
                        cost[flight.flight_no] = new_cost
                        prv_flight[flight.flight_no] = last_flight
                        pq.insert((new_cost, flight))

        result = []
        current_flight = required_flight
        while current_flight:
            result.append(current_flight)
            current_flight = prv_flight[current_flight.flight_no]
        return result[::-1]
    

    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        if start_city == end_city:
            return []
        pq = LinkedList()
        required_flight = None
        prv_flight = [None for _ in range(len(self.flights) + 1)]
        counter = [float('inf') for _ in range(len(self.flights) + 1)]
        least_count = float('inf')
        least_cost = float('inf')
        cost = [float('inf') for _ in range(len(self.flights) + 1)]
        for flight in self.adj_lists[start_city]:
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                cost[flight.flight_no] = flight.fare
                pq.append((1,flight.fare, flight))
                counter[flight.flight_no] = 1
        while pq.is_empty() == False:
            entry = pq.pop_front()
            flight_count,total_cost, last_flight = entry
            last_arrival, current_city = last_flight.arrival_time, last_flight.end_city
            if current_city == end_city:
                if flight_count < least_count or (flight_count == least_count and total_cost<least_cost):
                    least_count = flight_count
                    least_cost = total_cost
                    required_flight = last_flight
                continue

            if(flight_count>=least_count):
                continue
            
            for flight in self.adj_lists[current_city]:
                if(flight.departure_time >= last_arrival + 20) and flight.arrival_time <= t2 and flight.departure_time >= t1:
                    if(flight_count+1 < counter[flight.flight_no]) or (flight_count+1 == counter[flight.flight_no] and total_cost+flight.fare < cost[flight.flight_no]):
                        counter[flight.flight_no] = flight_count+1
                        cost[flight.flight_no] = total_cost+flight.fare
                        prv_flight[flight.flight_no] = last_flight
                        pq.append((flight_count+1,total_cost+flight.fare, flight))

        result = []
        current_flight = required_flight
        while current_flight:
            result.append(current_flight)
            current_flight = prv_flight[current_flight.flight_no]
        return result[::-1]



















class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, value):
        new_node = Node(value)
        if self.tail is None:  # List is empty
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def pop_front(self):
        if self.head is None:  # List is empty
            return None
        value = self.head.value
        self.head = self.head.next
        if self.head is None:  
            self.tail = None
        return value
    
    def is_empty(self):
        return self.head is None












class Heap:
    def __init__(self, comparison_function=None, init_array=None):
        self.comparison_function = comparison_function if comparison_function else lambda x, y: x < y
        self._heap = init_array if init_array is not None else []
        if self._heap:
            self._build_heap()

    def _build_heap(self):
        for i in range(len(self._heap) // 2 - 1, -1, -1):
            self._heapify_down(i)

    def insert(self, value):
        self._heap.append(value)
        self._heapify_up(len(self._heap) - 1)

    def extract(self):
        if not self._heap:
            return None
        if len(self._heap) == 1:
            return self._heap.pop()
        top_element = self._heap[0]
        self._heap[0] = self._heap.pop()
        self._heapify_down(0)
        return top_element

    def top(self):
        return self._heap[0] if self._heap else None

    def _heapify_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.comparison_function(self._heap[index], self._heap[parent]):
            self._heap[index], self._heap[parent] = self._heap[parent], self._heap[index]
            self._heapify_up(parent)

    def _heapify_down(self, index):
        least = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(self._heap) and self.comparison_function(self._heap[left], self._heap[least]):
            least = left
        if right < len(self._heap) and self.comparison_function(self._heap[right], self._heap[least]):
            least = right

        if least != index:
            self._heap[index], self._heap[least] = self._heap[least], self._heap[index]
            self._heapify_down(least)

    def __len__(self): 
        return len(self._heap)
