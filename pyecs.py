import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import csv
import os

# number of decimals to be conserved in the answers
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
    """g = nx.Graph()
    g.add_edge("X", "B", type="resistance", resistance=6, polarity={}, voltage=0, current=0)
    g.add_edge("A", "X", type="battery", resistance=0, polarity={"X"}, voltage=75, current=0)
    g.add_edge("A", "Y", type="battery", resistance=0, polarity={"Y"}, voltage=125, current=0)
    g.add_edge("Y", "B", type="resistance", resistance=4, polarity={}, voltage=0, current=0)
    g.add_edge("A", "B", type="resistance", resistance=8.1, polarity={}, voltage=0, current=0)
    return(g)
    """

    g = nx.Graph()
    g.add_edge("A", "B", type="battery", resistance=0, polarity={-1:"B"}, voltage=9, current=0)
    g.add_edge("C", "B", type="resistance", resistance=10, polarity={}, voltage=0, current=0)
    g.add_edge("A", "C", type="resistance", resistance=25, polarity={}, voltage=0, current=0)
    g.add_edge("A", "E", type="resistance", resistance=75, polarity={}, voltage=0, current=0)
    g.add_edge("E", "C", type="resistance", resistance=100, polarity={}, voltage=0, current=0)
    g.add_edge("A", "F", type="resistance", resistance=100, polarity={}, voltage=0, current=0)
    g.add_edge("F", "E", type="resistance", resistance=50, polarity={}, voltage=0, current=0)
    g.add_edge("A", "G", type="resistance", resistance=0, polarity={}, voltage=0, current=0)
    g.add_edge("G", "C", type="resistance", resistance=15, polarity={}, voltage=0, current=0)
    return(g)


def graph_from_pandas(filename):
    """
    creates and return a graph from a csv file using pandas
    uses "|" as the delimiter for the csv file !!!need to modify the code or the file for them to be compatible with different delimiters!!!
    parameter filename : the name of the input file, without the suffix (.csv) (ex: graph1)
    file must be in "graphs" folder
    """
    import pandas as pd
    path = os.path.join(os.getcwd(), "graphs{}{}.csv".format(os.sep, filename))
    df = pd.read_csv(path, delimiter="|")
    g = nx.Graph()
    num_rows = len(df)
    # for every row, add the necessary stuff to the graph
    for i in range(num_rows):
        #works polarity:
        polarity = {}
        print(type(df["polarity"][i]))
        print((df["polarity"][i]))
        if not pd.isna(df["polarity"][i]):
            for p in df["polarity"][i].split("#"):
                loop_num = p.split(":")[0]
                start = p.split(":")[1]
                polarity[int(loop_num)] = start
        print()
        g.add_edge(df["node1"][i], df["node2"][i], type=df["type"][i], resistance=df["resistance"][i], polarity=polarity, voltage=df["voltage"][i], current=df["current"][i], flow=df["flow"][i])
    
    return(g)

def csv_from_GUI(output_name):
    fig, ax = plt.subplots()
    plt.show()

"""def graph_from_csv(filename):
    path = os.path.join(os.getcwd(), "graphs{}{}.csv".format(os.sep, filename))
    with open(path) as csv_file:
        r = csv.reader(csv_file, delimiter="|")
        col_names = r
        num_rows = 0
        for row in r:
            if num_rows != 0:
                node1 = row[0]
                node2 = row[1]
                type = row[2]
                resistance = row[3]
                #works polarity:
                polarity = {}
                for p in row[4].split(";"):
                    loop_num = p.split("-")[0]
                    start = p.split("-")[1]
                    polarity[int(loop_num)] = start
            num_rows += 1
"""
def main():

    
    #g = buildgraph()
    #print(n.adj)
    filename = "new_graph"
    csv_from_GUI(filename) 
    g=graph_from_pandas("graph1")

    cycles = nx.cycle_basis(n)
    g = build_polarity(g, cycles)
    solved = solve(g, cycles)


    for n in g.adj:
        for e in g.adj[n]:
            print("node {} to node {} : ".format(n, e), g.adj[n][e])

    # my drawing part
    s3 = plt.subplot(111)
    nx.draw_planar(solved, with_labels=True)
    plt.show()


if __name__ == "__main__":
    main()