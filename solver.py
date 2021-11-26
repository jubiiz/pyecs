import numpy as np
import networkx as nx

SD = 4

def solve(graph, cycles):
    # finds the cycles,  initiates the intensity matrix, initiates the voltage matrix
    intensity_matrix = []
    voltage_matrix = []
    num_cycles = len(cycles)
    for cycle in cycles:
        row = []
        for i in range(num_cycles): # contains same num of edge as of nodes
            row.append(0)
        intensity_matrix.append(row)
        voltage_matrix.append([0])
    
    # fills the intensity and voltage matrix
    for i in range(len(cycles)):
        cycle = cycles[i]
        for j in range(len(cycle)):
            edge = graph.edges[(cycle[j], cycle[(j+1)%len(cycle)])] # the edge we want
            for p in edge["polarity"]:
                if edge["type"] == "resistance":
                    if cycle[j] == edge["polarity"][p]:   # if polarity is same as direction of loop : if the first letter of our edge is the same as the letter associated to the polarity of this cycle
                        intensity_matrix[i][p] += edge["resistance"]   # intensity_matrix[cycle_number][polarity_number]
                    else: 
                        intensity_matrix[i][p] -= edge["resistance"]
                else:
                    if cycle[j] == edge["polarity"][p]:
                        voltage_matrix[i][0] += edge["voltage"]
                    else:
                        voltage_matrix[i][0] -= edge["voltage"]
                    
    # use numpy to solve resulting matrices
    A = np.matrix(intensity_matrix)
    b = np.matrix(voltage_matrix)
    intensities = np.linalg.solve(A, b)
    intensities = intensities.tolist()

    # transfers those values into the graph
    for i in range(len(cycles)):
        cycle = cycles[i]
        for j in range(len(cycle)):
            edge_id = (cycle[j], cycle[(j+1)%len(cycle)])
            edge = graph.edges[edge_id] # the edge we want
            if edge["current"] == 0: # if edge hasn't been updated
                for p in edge["polarity"]: # for all the loops adjacent to that edge
                    if cycle[j] == edge["polarity"][p]:   # if polarity is same as direction of loop : if the first letter of our edge is the same as the letter associated to the polarity of this cycle
                        edge["current"] += intensities[p][0]   # intensity_matrix[cycle_number][polarity_number]
                        if edge["type"] == "resistance":
                            edge["voltage"] += (intensities[p][0] * edge["resistance"])
                    else: 
                        edge["current"] -= intensities[p][0] 
                        if edge["type"] == "resistance":
                            edge["voltage"] -= (intensities[p][0] * edge["resistance"])
                
                edge["current"] = round(edge["current"], SD)
                edge["voltage"] = round(edge["voltage"], SD)
                # set the direction of current (flow) in the direction of I 
                if edge["type"] != "battery":
                    edge["flow"] = edge_id[0]
                    if edge["current"] < 0:
                        edge["flow"] = edge_id[1]
                        edge["current"] *= -1
                        edge["voltage"] *= -1
                else:
                    edge["flow"] = edge["polarity"][p]
                    



    return(graph)

def build_polarity(graph, cycles):
    for i in range(len(cycles)):
        cycle = cycles[i]
        for j in range(len(cycle)):
            edge = (cycle[j], cycle[(j+1)%len(cycle)]) # the tuple denoting the edge we want
            if graph.edges[edge]["type"] == "resistance":
                graph.edges[edge]["polarity"][i] = cycle[j]      # the polarity is added to the edge we want
            else:
                polarity = graph.edges[edge]["polarity"][-1]
                graph.edges[edge]["polarity"][i] = polarity
                graph.edges[edge]["polarity"].pop(-1)

    return(graph)