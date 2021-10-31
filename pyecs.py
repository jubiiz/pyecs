import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


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
    print(intensities)



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
    g.add_edge("A", "D", type="resistance", resistance=3300, polarity={}, voltage=None, current=None)
    g.add_edge("A", "C", type="resistance", resistance=330, polarity={}, voltage=None, current=None)
    g.add_edge("C", "B", type="resistance", resistance=33000, polarity={}, voltage=None, current=None)
    g.add_edge("B", "D", type="resistance", resistance=27000, polarity={}, voltage=None, current=None)
    g.add_edge("C", "D", type="resistance", resistance=5600, polarity={}, voltage=None, current=None)
    print(nx.cycle_basis(g))"""

    # build the circuit
    g = nx.Graph()
    g.add_edge("A", "B", type="battery", resistance=0, polarity={"B"}, voltage=12)
    g.add_edge("D", "E", type="battery", resistance=0, polarity={"D"}, voltage=24)
    g.add_edge("B", "C", type="resistance", resistance=3, polarity={}, voltage=None, current=None)
    g.add_edge("A", "F", type="resistance", resistance=0, polarity={}, voltage=None, current=None)
    g.add_edge("C", "D", type="resistance", resistance=6, polarity={}, voltage=None, current=None)
    g.add_edge("C", "F", type="resistance", resistance=9, polarity={}, voltage=None, current=None)
    g.add_edge("F", "E", type="resistance", resistance=0, polarity={}, voltage=None, current=None)


    # my drawing part
    s3 = plt.subplot(111)
    nx.draw_planar(g)
    plt.show()
    cycles = nx.cycle_basis(g)
    g = build_polarity(g, cycles)
    solved = solve(g, cycles)




if __name__ == "__main__":
    main()