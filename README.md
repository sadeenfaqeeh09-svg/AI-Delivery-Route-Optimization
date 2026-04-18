# 🧠 AI Delivery Route Optimization

## 📌 Description
This project focuses on solving a delivery route optimization problem using Artificial Intelligence techniques.

The goal is to assign packages to vehicles and determine the best delivery routes while minimizing the total distance traveled and respecting vehicle capacity constraints.

Two optimization approaches are implemented and compared:
- Simulated Annealing (SA)
- Genetic Algorithm (GA)

---

## 🎯 Objectives
- Optimize delivery routes for multiple vehicles
- Minimize total travel distance
- Respect vehicle capacity constraints
- Compare performance of different AI optimization algorithms

---

## ⚙️ Algorithms Used

### 🔹 Simulated Annealing
- Starts with an initial solution
- Iteratively improves it by exploring neighboring solutions
- Accepts worse solutions probabilistically to escape local minima

### 🔹 Genetic Algorithm
- Generates a population of solutions
- Applies selection, crossover, and mutation
- Evolves solutions over generations to find optimal routes

---

## 🚚 Problem Representation
- Each package has:
  - Location (coordinates)
  - Weight

- Each vehicle has:
  - Maximum capacity
  - Assigned packages

- The objective:
  - Minimize total route distance
  - Ensure capacity constraints are not violated

---

## 📊 Features
- Initial greedy solution generation
- Distance calculation for routes
- Capacity constraint handling
- Visualization of routes using matplotlib
- Comparison between SA and GA results

---

## ▶️ How to Run
Make sure you have the required libraries installed:
pip install matplotlib
python FinalV.py

---

## 📈 Output:
Optimized delivery routes
Total distance traveled
Visualization of routes (graph)
Comparison between algorithms performance

----

## 📁 Project Structure
AI-Delivery-Route-Optimization/
├── FinalV.py
├── 1221669_JulnarNaalAssi_SadeenFaqeeh_1222177_P1.pdf
└── README.md

---

## 🖥️ Environment
Programming Language: Python
Libraries: matplotlib, random, math
OS: Linux / Windows

---

## 👩‍💻 Authors
Sadeen Faqeeh
Julnar Naal Assi
