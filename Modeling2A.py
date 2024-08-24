import numpy as np
import math
import time
import pandas as pd 

def travelTime(freeflow, numvehicles, capacity, alpha, beta):
    return freeflow*(1+alpha*(numvehicles/capacity)**beta) + np.random.normal(0,2)

def capacity(l_car, d_spacing, lanes, length):
    return math.floor((lanes*length)/(l_car + d_spacing))

def freeflow(length,v_limit):
    return (length/v_limit)*(60/1000)

def probability_numerator(edge):
    N_uv = edges_vehicles[edge]
    total_time = 0
    if N_uv == 0:
        return 1/edge_info[edge][0]
    if N_uv >= edge_info[edge][1]: #makes sure the probability is 0 if capacity is at a maximum
        return 0 
    for cars in vehicles:
        if vehicles[cars][1] == edge: 
            total_time += vehicles[cars][2]
    return 1/((1/N_uv)*total_time)

def probability_denominator(node,initializing):
    total = 0
    for edge in node_out_edges[node]:
        if edges_vehicles[edge] == 0:
            total += 1/edge_info[edge][0] #Using freeflow if roads are empty
        elif edges_vehicles[edge] >= edge_info[edge][1]:
            if initializing == 1:
                edge_info[edge][2] += 1 # Congestion in terms of cars that cant enter the road counter
        else:
            total += probability_numerator(edge)
    if total == 0:
        return 1
    return total

def probability(node,edge,initializing):
    return probability_numerator(edge)/probability_denominator(node,initializing)

l_car = 4.5
d_spacing = 55
alpha = 0.15
beta = 4

# [Length, V_lim, lanes]
edge_data = {"1_A": [30000,100,2], "1_B": [50000,100,2],"A_C": [40000,100,2],"B_C": [60000,100,2],"C_D":
              [20000,100,2],"C_E": [30000,100,2],"C_2": [70000,100,2],"D_2": [40000,100,2],"E_2": [50000,100,2]}
edges_vehicles = {"1_A": 0, "1_B": 0,"A_C": 0,"B_C": 0,"C_D": 0,"C_E": 0,"C_2": 0,"D_2": 0,"E_2": 0}

# Possible other nodes 
node_out_edges = {"1": ["1_A","1_B"], "A":["A_C"], "B": ["B_C"], "C": ["C_D","C_E","C_2"], "D": ["D_2"], "E": ["E_2"]}

# setting up information of the edges
edge_info = {}
vehicles = {}   
edge_times ={}
for key in edge_data.keys():    # This sets up dictionaries for edge info with freeflow/capacity data, [2] is congestion amount
    data = edge_data[key]       # Edge_times is simply a dictionary of lists in which all travel times are saved for saving to excel later.
    edge_info[key] = [freeflow(data[0],data[1]),capacity(l_car, d_spacing,data[2],data[0]),0]
    edge_times[key] = []

vehicle_id = 0
start_time = time.time()
peak_hour = False
initializing = 0

for min in range(1,241):
    if min > 120: 
        initializing = 1
    print(min)
    incoming_traffic = round(np.random.normal(85,1.5))
    if peak_hour:
        incoming_traffic = round(np.random.normal(95,1))
    for car in range(1,incoming_traffic+1):
        vehicle_id += 1
        vehicles[vehicle_id] = [initializing, "1", 0, 0, "", 0, 0, ""] # part of initiliazation or not, Current place, time left on road, total time spent, route 
    for car in vehicles:
        if vehicles[car][1] != "2":
            vehicles[car][3] += 1 #adds minute to total expired time if vehicle has not arrived at city 2 
        if vehicles[car][1] in node_out_edges.keys(): # Checks if  the vehicle is currently at a node inbetween edges
            prob_list = []
            for out_edge in node_out_edges[vehicles[car][1]]:  
                prob_list.append(probability(vehicles[car][1],out_edge,initializing))
            if sum(prob_list) < 0.99:
                vehicles[car][6] += 1
                vehicles[car][7] += vehicles[car][1]
                continue
            next_edge = np.random.choice(node_out_edges[vehicles[car][1]],p = prob_list) #stochastically pick next edge based on probabilties defined in functions at the start
            vehicles[car][1] = next_edge #updates where vehicle is currently
            vehicles[car][4] += (next_edge + " ") #updates road taken
            tt = travelTime(edge_info[next_edge][0],edges_vehicles[next_edge],edge_info[next_edge][1],alpha,beta)
            vehicles[car][5] += edge_info[next_edge][0]
            vehicles[car][2] = tt #updates travel time
            if initializing == 1: 
                edge_times[next_edge].append(tt) 
            edges_vehicles[next_edge] += 1
        if vehicles[car][1] not in node_out_edges.keys() and vehicles[car][1] != "2": # checks if vehicle is at an edge
            vehicles[car][2] -= 1 # takes a minute of the travel time
            if vehicles[car][2] < 0: # checks if travel time has expired. 
                edges_vehicles[vehicles[car][1]] -= 1 #remove vehicle from edge amount counter
                vehicles[car][1] = vehicles[car][1].split("_")[1] #updates vehicle position

print("Simulation Time: --- %s seconds ---" % (time.time() - start_time))

travel_time = []
route = []
freeflow_time = []
congestions = []
minutes_waited = []
where_waited = []
for car in vehicles: 
    if vehicles[car][0] == 1 and vehicles[car][1] == "2":
        travel_time.append(vehicles[car][3])
        route.append(vehicles[car][4])
        freeflow_time.append(vehicles[car][5])
        minutes_waited.append(vehicles[car][6])
        where_waited.append(vehicles[car][7])

for edge in edge_info:
    congestions.append(edge_info[edge][2])

df1 = pd.DataFrame({'Total Travel Time': travel_time, 'Route': route, 'Freeflow Time': freeflow_time, 'Minutes Waited': minutes_waited, 'Where?': where_waited})
df2 = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in edge_times.items() ]))
df3 = pd.DataFrame({"Edge": edge_info.keys(), "Individual Car Congestions": congestions })

with pd.ExcelWriter("test.xlsx") as writer:
    df1.to_excel(writer, sheet_name = "Sheet1")
    df2.to_excel(writer, sheet_name = "Sheet2")
    df3.to_excel(writer, sheet_name = "Sheet3")