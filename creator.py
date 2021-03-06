import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import os
from math import *


class GraphCreatorGUI():
    def __init__(self):
        # creates a matplotlib plot
        self.press = None
        self.fig, self.ax = plt.subplots()
        self.graph = nx.Graph()
        self.ax.set_xlim(left=0, right=21)
        self.ax.set_ylim(bottom=0, top=21)
        
        # sets ticks and size
        minor_ticks = np.linspace(0,20,21)
        self.ax.set_xticks(minor_ticks)
        self.ax.set_yticks(minor_ticks)
        self.ax.grid(True)

    def connect(self):
        """connects the event functions then displays the graph"""
        self.cidpress = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.cidrelease = self.fig.canvas.mpl_connect('button_release_event', self.onrelease)
        plt.show()

    def onclick(self, event):
        "When there is a click in the axes, log info for the current point"
        if event.inaxes != None:
            self.press = ((event.x, event.y), (event.xdata, event.ydata))
            self.press_case = (floor(event.xdata), floor(event.ydata))#find this
            
    def onrelease(self, event):
        # need to 1) check if the click is happening in the same cell, if so, do nothing
        # if not same cell, take the two cell coordinates ()
        # at the end reset the self.press
        new_case = (floor(event.xdata), floor(event.ydata))
        # not same case
        if new_case != self.press_case:
            # create new edge with (self.press_case, new_case) as nodes
            type, value = input("enter edge type and value, separated by a space \n").split(" ")
            print("type and value are ", type, value)
            if type == "resistance" or type == "r":
                # add a resistance edge
                self.graph.add_edge(self.press_case, new_case, type="resistance", resistance=int(value), polarity={}, voltage=0, current=0, flow=0)
                style = "ko-"
            else:
                # add a battery edge
                self.graph.add_edge(self.press_case, new_case, type="battery", resistance=0, polarity={-1:self.press_case}, voltage=int(value), current=0, flow=0)
                style = "bo:"


        # show edge in graph
        x = [self.press_case[0]+0.5, new_case[0]+0.5]
        y = [self.press_case[1]+0.5, new_case[1]+0.5]
        self.ax.plot(x, y, style)
        # add info text
        self.ax.text(((x[0]+x[1])/2), ((y[0]+y[1])//2), f'{type} {value}', {'ha': 'center', 'va': 'center', 'bbox': {'fc': '0.8', 'pad': 0}}, rotation=30)
        plt.show()
        # ready for new press (delete past data)
        self.press_case = None
        self.press = None         
        

    def disconnect(self):
        """disconnects the connections"""
        self.fig.canvas.mpl_disconnect(self.cidpress)
        self.fig.canvas.mpl_disconnect(self.cidrelease)

def graph_from_pandas(filename=None):
    """
    creates and return a graph from a csv file using pandas
    uses "|" as the delimiter for the csv file
    filename : the name of the input file, without the suffix (.csv) (ex: graph1)
    file must be in "graphs" folder
    """
    import pandas as pd
    if filename == None:
        print("you must enter a filename with your command, like: 'csv graph1'")
    path = os.path.join(os.getcwd(), "graphs{}{}.csv".format(os.sep, filename))
    df = pd.read_csv(path, delimiter="|")
    g = nx.Graph()
    num_rows = len(df)
    # for every row, add the necessary components to the graph
    for i in range(num_rows):
        # builds polarity:
        polarity = {}
        # if it already is given
        if not pd.isna(df["polarity"][i]):
            # multiple polarities are split by '#'
            for p in df["polarity"][i].split("#"):
                loop_num = p.split(":")[0]
                # must convert cells to tuples rather than strings : '(1, 2)' to (1, 2)
                start = to_tuple(p.split(":")[1])
                polarity[int(loop_num)] = start
        g.add_edge(to_tuple(df["node1"][i]), to_tuple(df["node2"][i]), type=df["type"][i], resistance=df["resistance"][i], polarity=polarity, voltage=df["voltage"][i], current=df["current"][i], flow=df["flow"][i])
    
    return(g)

def graph_from_GUI():
    """
    returns the GUI interface object, ready for input
    """
    c = GraphCreatorGUI()
    c.connect()
    c.disconnect()
    return(c)

def to_tuple(s):
    """
    correcly formats a 'string tuple' to an actual tuple (like from '(1, 2)' to (1, 2))
    leaves non-tuple stuff to not tuples
    """
    if s[0] != "(":
        return(s)
    s = s.strip(")").strip("(").split(", ")
    s = [int(x) for x in s]
    s = tuple(s)
    return(s)

def buildgraph():
    """
    deprecated in-code graph building
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
