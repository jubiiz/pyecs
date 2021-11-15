from matplotlib import pyplot as plt
from math import floor
import numpy as np
import os
import networkx as nx

class GraphCreatorGUI():
    def __init__(self, filename):
        self.dictionary = {"node1":[], "node2":[], "type":[], "resistance":[], "polarity":[], "voltage":[], "current":[], "flow":[]}
        self.path = os.path.join(os.getcwd(), f"graphs{os.sep}{filename}.csv")
        self.press = None
        self.fig, self.ax = plt.subplots()
        self.graph = nx.Graph()
        
        # sets ticks and size
        minor_ticks = np.linspace(0,20,21)
        self.ax.set_xticks(minor_ticks)
        self.ax.set_yticks(minor_ticks)
        self.ax.grid(True)

    def connect(self):
        """connects the event functions"""
        self.cidpress = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.cidrelease = self.fig.canvas.mpl_connect('button_release_event', self.onrelease)
        plt.show()

    def onclick(self, event):
        "When there is a click in the axes, log info for the current point"
        if event.inaxes != None:
            self.press = ((event.x, event.y), (event.xdata, event.ydata))
            self.press_case = (floor(event.xdata), floor(event.ydata))#find this
            """            print(event.inaxes)
            print(event.xdata)
            print(event.ydata)
            print(event.x)
            print(event.y)
            """
    def onrelease(self, event):
        # need to 1) check if the click is happening in the same cell, if so, do nothing
        # if not same cell, take the two cell coordinates ()
        # at the end reset the self.press
        new_case = (floor(event.xdata), floor(event.ydata))
        # not same case
        if new_case != self.press_case:
            # create new edge with (self.press_case, new_case) as nodes
            # to do so we need a tkinter popup asking for data
            type, value = input("type, value ").split()
            print("type and value are ", type, value)
            if value == "resistance":
                # add a resistance edge
                self.graph.add_edge(self.press_case, new_case, type="resistance", resistance=int(value), polarity={}, voltage=0, current=0)
            else:
                # add a battery edge
                self.graph.add_edge(self.press_case, new_case, type="battery", resistance=0, polarity={self.press_case}, voltage=int(value), current=0)
            
        # get stuff back to normal, ready for a new press
        self.press_case = None
        self.press = None

    def get_graph(self):
        return(self.graph)
            
        

    def disconnect(self):
        """disconnects the connections"""
        self.fig.canvas.mpl_disconnect(self.cidpress)
        self.fig.canvas.mpl_disconnect(self.cidrelease)

def main():
    gc = GraphCreatorGUI("graph1")
    gc.connect()
    inp = input("say something I'm giving up on you")
    graph = gc.get_graph()
    
    # my drawing part
    s3 = plt.subplot(111)
    nx.draw_planar(graph, with_labels=True)
    plt.show()
    gc.disconnect()




if __name__ == "__main__":
    main()