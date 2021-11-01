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

def main():

    """# build the circuit
    g = nx.Graph()
    g.add_edge("A", "B", type="battery", resistance=0, polarity="A", voltage=9)
    g.add_edge("A", "D", type="resistance", resistance=3300, polarity={}, voltage=0, current=0)
    g.add_edge("A", "C", type="resistance", resistance=330, polarity={}, voltage=0, current=0)
    g.add_edge("C", "B", type="resistance", resistance=33000, polarity={}, voltage=0, current=0)
    g.add_edge("B", "D", type="resistance", resistance=27000, polarity={}, voltage=0, current=0)
    g.add_edge("C", "D", type="resistance", resistance=5600, polarity={}, voltage=0, current=0)
    print(nx.cycle_basis(g))"""

    """ # build the circuit
    g = nx.Graph()
    g.add_edge("A", "B", type="battery", resistance=0, polarity={"B"}, voltage=12)
    g.add_edge("D", "E", type="battery", resistance=0, polarity={"D"}, voltage=24)
    g.add_edge("B", "C", type="resistance", resistance=3, polarity={}, voltage=0, current=0)
    g.add_edge("A", "F", type="resistance", resistance=0, polarity={}, voltage=0, current=0)
    g.add_edge("C", "D", type="resistance", resistance=6, polarity={}, voltage=0, current=0)
    g.add_edge("C", "F", type="resistance", resistance=9, polarity={}, voltage=0, current=0)
    g.add_edge("F", "E", type="resistance", resistance=0, polarity={}, voltage=0, current=0)
    """

    """g = nx.Graph()
    g.add_edge("A", "B", type="battery", resistance=0, polarity={"B"}, voltage=9)
    g.add_edge("E", "F", type="battery", resistance=0, polarity={"F"}, voltage=5)
    g.add_edge("A", "C", type="resistance", resistance=100, polarity={}, voltage=0, current=0)
    g.add_edge("C", "D", type="resistance", resistance=100, polarity={}, voltage=0, current=0)
    g.add_edge("B", "D", type="resistance", resistance=100, polarity={}, voltage=0, current=0)
    g.add_edge("B", "F", type="resistance", resistance=0, polarity={}, voltage=0, current=0)
    g.add_edge("F", "D", type="resistance", resistance=100, polarity={}, voltage=0, current=0)
    g.add_edge("E", "C", type="resistance", resistance=100, polarity={}, voltage=0, current=0)
    """
    g = nx.Graph()
    g.add_edge("X", "B", type="resistance", resistance=6, polarity={}, voltage=0, current=0)
    g.add_edge("A", "X", type="battery", resistance=0, polarity={"X"}, voltage=75, current=0)
    g.add_edge("A", "Y", type="battery", resistance=0, polarity={"Y"}, voltage=125, current=0)
    g.add_edge("Y", "B", type="resistance", resistance=4, polarity={}, voltage=0, current=0)
    g.add_edge("A", "B", type="resistance", resistance=8.1, polarity={}, voltage=0, current=0)



    # my drawing part
    s3 = plt.subplot(111)
    nx.draw_planar(g, with_labels=True)
    plt.show()
    cycles = nx.cycle_basis(g)
    g = build_polarity(g, cycles)
    solved = solve(g, cycles)

    print(solved.adj)



if __name__ == "__main__":
    main()