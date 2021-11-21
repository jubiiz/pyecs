import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

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
                    if cycle[j] == p:
                        voltage_matrix[i][0] += edge["voltage"]
                    else:
                        voltage_matrix[i][0] -= edge["voltage"]
                    
    # use numpy to solve resulting matrices
    A = np.matrix(intensity_matrix)
    b = np.matrix(voltage_matrix)
    print(A, b)
    intensities = np.linalg.solve(A, b)
    intensities = intensities.tolist()
    print(intensities)

    # transfers those values into the graph
    for i in range(len(cycles)):
        cycle = cycles[i]
        for j in range(len(cycle)):
            edge_id = (cycle[j], cycle[(j+1)%len(cycle)])
            edge = graph.edges[edge_id] # the edge we want
            if edge["type"] == "resistance":
                if edge["current"] == 0:
                    for p in edge["polarity"]: 
                        if cycle[j] == edge["polarity"][p]:   # if polarity is same as direction of loop : if the first letter of our edge is the same as the letter associated to the polarity of this cycle
                            edge["current"] += intensities[p][0]   # intensity_matrix[cycle_number][polarity_number]
                            if edge["type"] == "resistance":
                                edge["voltage"] += (intensities[p][0] * edge["resistance"])
                        else: 
                            edge["current"] -= intensities[p][0] 
                            if edge["type"] == "resistance":
                                edge["voltage"] -= (intensities[p][0] * edge["resistance"])
                    # set the direction of current (flow) in the direction of I 
                    edge["flow"] = edge_id[0]
                    edge["current"] = round(edge["current"], SD)
                    edge["voltage"] = round(edge["voltage"], SD)
                    if edge["current"] < 0:
                        edge["flow"] = edge_id[0]
                        edge["current"] *= -1
                        edge["voltage"] *= -1
                    



    return(graph)

def build_polarity(graph, cycles):
    for i in range(len(cycles)):
        cycle = cycles[i]
        for j in range(len(cycle)):
            edge = (cycle[j], cycle[(j+1)%len(cycle)]) # the tuple denoting the edge we want
            if graph.edges[edge]["type"] == "resistance":
                graph.edges[edge]["polarity"][i] = cycle[j]      # the polarity is added to the edge we want

    return(graph)

def buildgraph():
    g = nx.Graph()
    g.add_edge("X", "B", type="resistance", resistance=6, polarity={}, voltage=0, current=0)
    g.add_edge("A", "X", type="battery", resistance=0, polarity={"X"}, voltage=75, current=0)
    g.add_edge("A", "Y", type="battery", resistance=0, polarity={"Y"}, voltage=125, current=0)
    g.add_edge("Y", "B", type="resistance", resistance=4, polarity={}, voltage=0, current=0)
    g.add_edge("A", "B", type="resistance", resistance=8.1, polarity={}, voltage=0, current=0)
    return(g)
    """

    g = nx.Graph()
    g.add_edge("A", "B", type="battery", resistance=0, polarity={"B"}, voltage=9, current=0)
    g.add_edge("C", "B", type="resistance", resistance=10, polarity={}, voltage=0, current=0)
    g.add_edge("A", "C", type="resistance", resistance=25, polarity={}, voltage=0, current=0)
    g.add_edge("A", "E", type="resistance", resistance=75, polarity={}, voltage=0, current=0)
    g.add_edge("E", "C", type="resistance", resistance=100, polarity={}, voltage=0, current=0)
    g.add_edge("A", "F", type="resistance", resistance=100, polarity={}, voltage=0, current=0)
    g.add_edge("F", "E", type="resistance", resistance=50, polarity={}, voltage=0, current=0)
    g.add_edge("A", "G", type="resistance", resistance=0, polarity={}, voltage=0, current=0)
    g.add_edge("G", "C", type="resistance", resistance=15, polarity={}, voltage=0, current=0)
    return(g)
    """
def main():

    
    g = buildgraph()


    cycles = nx.cycle_basis(g)
    g = build_polarity(g, cycles)
    solved = solve(g, cycles)


    for n in g.adj:
        for e in g.adj[n]:
            print("node {} to node {} : ".format(n, e), g.adj[n][e])

    # my drawing part
    s3 = plt.subplot(111)
    nx.draw_planar(g, with_labels=True)
    plt.show()


if __name__ == "__main__":
    main()