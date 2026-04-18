# Julnar Naal Assi. ID: 122169
# Sadeen Jehad Faqeeh. Id: 1222177

import math
import random  # FOR RANDOM GENERATION OF PACKAGE DATA IF NUMBER EXCEEDS THRESHOLD
import matplotlib.pyplot as plt  # FOR VISUALIZING DELIVERY ROUTES
import time  # FOR MEASURING COMPUTATION TIME OF ALGORITHMS

# CLASS REPRESENTING A PACKAGE WITH LOCATION, WEIGHT, AND PRIORITY
class Package:
    def __init__(self, id, x, y, weight, priority):
        self.id = id
        self.x = x
        self.y = y
        self.weight = weight
        self.priority = priority

# CLASS REPRESENTING A VEHICLE WITH CAPACITY AND ASSIGNED ROUTE
class Vehicle:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.route = []  # LIST OF PACKAGE OBJECTS

    def total_weight(self):
        # SUM OF PACKAGE WEIGHTS IN THE CURRENT ROUTE
        return sum(pkg.weight for pkg in self.route)

    def route_distance(self):
        # TOTAL DISTANCE OF ROUTE FROM DEPOT (0,0) TO ALL PACKAGES AND BACK
        distance = 0.0
        curr_x, curr_y = 0, 0
        for pkg in self.route:
            distance += euclidean_distance(curr_x, curr_y, pkg.x, pkg.y)
            curr_x, curr_y = pkg.x, pkg.y
        distance += euclidean_distance(curr_x, curr_y, 0, 0)
        return distance

# EUCLIDEAN DISTANCE CALCULATION BETWEEN TWO COORDINATES
def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# SUM OF ROUTE DISTANCES FOR ALL VEHICLES
def total_distance(vehicles):
    return sum(v.route_distance() for v in vehicles)

# DEEP COPY OF THE SOLUTION (VEHICLES WITH THEIR RESPECTIVE ROUTES)
def deep_copy_solution(vehicles):
    new_vehicles = []
    for v in vehicles:
        new_v = Vehicle(v.id, v.capacity)
        new_v.route = list(v.route)
        new_vehicles.append(new_v)
    return new_vehicles

# INITIAL GREEDY SOLUTION BASED ON PRIORITY
def create_initial_solution(packages, vehicles):
    sorted_packages = sorted(packages, key=lambda p: p.priority)
    solution = [Vehicle(i, vehicles[i].capacity) for i in range(len(vehicles))]
    for pkg in sorted_packages:
        best_v = None
        for v in solution:
            if v.total_weight() + pkg.weight <= v.capacity:
                if best_v is None or v.total_weight() < best_v.total_weight():
                    best_v = v
        if best_v:
            best_v.route.append(pkg)
    return solution

# MUTATION FUNCTION FOR BOTH ALGORITHMS
def mutate_solution(solution):
    if len(solution) < 2:
        return solution
    new_solution = deep_copy_solution(solution)
    v1, v2 = random.sample(new_solution, 2)
    if v1.route and v2.route:
        p1 = random.choice(v1.route)
        p2 = random.choice(v2.route)
        if v1.total_weight() - p1.weight + p2.weight <= v1.capacity and \
           v2.total_weight() - p2.weight + p1.weight <= v2.capacity:
            v1.route.remove(p1)
            v2.route.remove(p2)
            v1.route.append(p2)
            v2.route.append(p1)
    return new_solution

# SIMULATED ANNEALING OPTIMIZER
def simulated_annealing(packages, vehicles):
    t = 1000
    alpha = 0.95
    t_min = 1
    iterations = 100
    current_solution = create_initial_solution(packages, vehicles)
    current_cost = total_distance(current_solution)
    best_solution = current_solution
    best_cost = current_cost
    while t > t_min:
        for _ in range(iterations):
            new_solution = mutate_solution(current_solution)
            new_cost = total_distance(new_solution)
            delta = new_cost - current_cost
            if delta < 0 or random.random() < math.exp(-delta / t):
                current_solution = new_solution
                current_cost = new_cost
                if current_cost < best_cost:
                    best_solution = current_solution
                    best_cost = current_cost
        t *= alpha
    return best_solution

# CROSSOVER FOR GENETIC ALGORITHM
def crossover(parent1, parent2, vehicles):
    child = [Vehicle(i, vehicles[i].capacity) for i in range(len(vehicles))]
    assigned = set()
    for i in range(len(parent1)):
        for pkg in parent1[i].route:
            if pkg.id not in assigned and child[i].total_weight() + pkg.weight <= child[i].capacity:
                child[i].route.append(pkg)
                assigned.add(pkg.id)
    for i in range(len(parent2)):
        for pkg in parent2[i].route:
            if pkg.id not in assigned and child[i].total_weight() + pkg.weight <= child[i].capacity:
                child[i].route.append(pkg)
                assigned.add(pkg.id)
    return child

# GENETIC ALGORITHM OPTIMIZER
def genetic_algorithm(packages, vehicles, population_size=50, mutation_rate=0.05, generations=500):
    population = [create_initial_solution(packages, vehicles) for _ in range(population_size)]
    for _ in range(generations):
        population = sorted(population, key=total_distance)
        new_population = population[:10]
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:20], 2)
            child = crossover(parent1, parent2, vehicles)
            if random.random() < mutation_rate:
                child = mutate_solution(child)
            new_population.append(child)
        population = new_population
    return min(population, key=total_distance)

# ROUTE VISUALIZER
def visualize_routes(vehicles):
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta']
    plt.figure(figsize=(8, 8))
    for i, v in enumerate(vehicles):
        color = colors[i % len(colors)]
        x = [0] + [pkg.x for pkg in v.route] + [0]
        y = [0] + [pkg.y for pkg in v.route] + [0]
        plt.plot(x, y, marker='o', color=color, label=f'vehicle {v.id}')
        for pkg in v.route:
            plt.text(pkg.x, pkg.y, f'{pkg.id}', fontsize=8, color=color)
    plt.scatter(0, 0, color='black', s=100, label='depot (0,0)')
    plt.title("DELIVERY ROUTES")
    plt.xlabel("X (KM)")
    plt.ylabel("Y (KM)")
    plt.grid(True)
    plt.legend()
    plt.show()

# USER INTERFACE MENU
def run_menu():
    vehicles = []
    packages = []

    def get_validated_input(prompt, val_type=float, condition=lambda x: True, error_msg="INVALID INPUT"):
        while True:
            val_str = input(prompt)
            try:
                val = val_type(val_str)
                if not condition(val):
                    raise ValueError
                return val
            except ValueError:
                print(f"  {error_msg} (YOU ENTERED: '{val_str}')")

    def input_data():
        nonlocal vehicles, packages
        vehicles.clear()
        packages.clear()
        print("\n------ ENTER VEHICLE INFO ------")
        num_vehicles = get_validated_input("ENTER NUMBER OF VEHICLES: ", int, lambda x: x > 0, "PLEASE ENTER A VALID POSITIVE INTEGER.")
        for i in range(num_vehicles):
            capacity = get_validated_input(f"  ENTER CAPACITY FOR VEHICLE {i} (KG): ", float, lambda x: x > 0, "PLEASE ENTER A VALID POSITIVE NUMBER.")
            vehicles.append(Vehicle(i, capacity))
        print("\n------ ENTER PACKAGE INFO ------")
        num_packages = get_validated_input("ENTER NUMBER OF PACKAGES: ", int, lambda x: x >= 0, "PLEASE ENTER A VALID NON-NEGATIVE INTEGER.")
        if num_packages > 50:
            print("GENERATING PACKAGES RANDOMLY...")
            for i in range(num_packages):
                x = random.uniform(0, 100)
                y = random.uniform(0, 100)
                weight = random.uniform(1, 50)
                priority = random.randint(1, 5)
                packages.append(Package(i, x, y, weight, priority))
        else:
            for i in range(num_packages):
                print(f"\nPACKAGE {i}")
                x = get_validated_input("  X-COORDINATE (0 TO 100 KM): ", float, lambda x: 0 <= x <= 100, "X MUST BE IN [0, 100] KM.")
                y = get_validated_input("  Y-COORDINATE (0 TO 100 KM): ", float, lambda x: 0 <= x <= 100, "Y MUST BE IN [0, 100] KM.")
                w = get_validated_input("  WEIGHT (KG): ", float, lambda x: x > 0, "WEIGHT MUST BE GREATER THAN 0.")
                p = get_validated_input("  PRIORITY (1-5): ", int, lambda x: 1 <= x <= 5, "PRIORITY MUST BE BETWEEN 1 AND 5.")
                packages.append(Package(i, x, y, w, p))

    input_data()

    while True:
        print("\nCHOOSE AN OPTION:")
        print("1. SIMULATED ANNEALING")
        print("2. GENETIC ALGORITHM")
        print("3. RESET VEHICLE/PACKAGE DATA")
        print("Q. QUIT")
        choice = input("ENTER YOUR CHOICE (1/2/3/Q): ").strip().lower()
        if choice not in ['1', '2', '3', 'q']:
            print("INVALID CHOICE. PLEASE ENTER 1, 2, 3, OR Q.")
            continue
        if choice == 'q':
            print("EXITING.....")
            break
        if choice == '3':
            input_data()
            continue
        if not vehicles or not packages:
            print("\n PLEASE INPUT VEHICLE AND PACKAGE DATA FIRST.")
            continue
        start_time = time.time()
        result = simulated_annealing(packages, vehicles) if choice == '1' else genetic_algorithm(packages, vehicles)
        end_time = time.time()
        elapsed = end_time - start_time
        print("\n------ SOLUTION ------")
        for v in result:
            print(f"VEHICLE {v.id} | CAPACITY: {v.capacity}KG | DISTANCE: {v.route_distance():.2f} KM")
            path = ' -> '.join([f"PACKAGE{pkg.id}({pkg.x},{pkg.y})" for pkg in v.route])
            print(f"  PATH: (0,0) -> {path} -> (0,0)")
            for pkg in v.route:
                print(f"  PACKAGE {pkg.id} -> ({pkg.x},{pkg.y}) | {pkg.weight}KG | PRIORITY {pkg.priority}")
            pkg_path = ' -> '.join([f"PACKAGE{pkg.id}" for pkg in v.route])
            print(f"  PACKAGE PATH: {pkg_path}")
        print(f"TOTAL DISTANCE: {total_distance(result):.2f} KM")
        print(f"COMPUTATION TIME: {elapsed:.2f} SECONDS")
        delivered_ids = {pkg.id for v in result for pkg in v.route}
        all_ids = {pkg.id for pkg in packages}
        undelivered = sorted(all_ids - delivered_ids)
        if undelivered:
            print("\n UNDELIVERED PACKAGES :(")
            for pkg_id in undelivered:
                print(f"  PACKAGE {pkg_id}")
        else:
            print("\n ALL PACKAGES DELIVERED! :) ")
        visualize_routes(result)

if __name__ == "__main__":
    run_menu()
