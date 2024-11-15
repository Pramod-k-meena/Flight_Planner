import time
import random
from planner import Planner
from flight import Flight

import matplotlib.pyplot as plt

def generate_random_flights(num_flights, seed=42):
    random.seed(seed)
    flights = []
    for flight_id in range(num_flights):
        origin = random.randint(1, 100)
        destination = random.randint(1, 100)
        start_time = random.randint(1,1000)
        end_time = start_time + random.randint(1, 1000)
        flights.append(Flight(flight_id, origin,start_time, destination, end_time, random.randint(100, 1000)))
    flights.append(Flight(num_flights, 0,100, 0, 200, 120))
    return flights

def measure_time(func, *args):
    start_time = time.perf_counter_ns()
    func(*args)
    end_time = time.perf_counter_ns()
    return end_time - start_time

def plot_time_complexity():
    input_sizes = [i for i in range(1, 10000,5)]
    init_times = []
    lfer = []
    cf = []
    lfcr = []

    for size in input_sizes:
        flights = generate_random_flights(size)
        
        # Measure time for __init__
        init_time = measure_time(Planner, flights)
        init_times.append(init_time)
        
        # Measure time for other functions
        planner = Planner(flights)
        lfer_time = measure_time(planner.least_flights_earliest_route,random.randint(1,100),random.randint(1,100),0,float('inf'))  # Replace with actual function
        lfer.append(lfer_time)
        cf_time = measure_time(planner.cheapest_route,random.randint(1,100),random.randint(1,100),0,float('inf'))  # Replace with actual function
        cf.append(cf_time)
        lfcr_time = measure_time(planner.least_flights_cheapest_route,random.randint(1,100),random.randint(1,100),0,float('inf'))  # Replace with actual function
        lfcr.append(lfcr_time)



    plt.plot(input_sizes[1:], init_times[1:], label='init')
    plt.plot(input_sizes, lfer, label='Least Flights Earliest Route')
    plt.plot(input_sizes, cf, label='Cheapest Route')
    plt.plot(input_sizes, lfcr, label='Least Flights Cheapest Route')
    plt.xlabel('Input Size')
    plt.ylabel('Time Taken (s)')
    plt.title('Time Complexity of Planner Class')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    plot_time_complexity()
