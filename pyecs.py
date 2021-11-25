from matplotlib import pyplot as plt
from math import floor
import numpy as np
import os
import networkx as nx

from creator import *
from solver import *

# number of decimals to be conserved in the answers
SD = 4

class CLI():
    def __init__(self):
        self.graph = None
        self.filename = None
        self.savename = None
        self.cycles = None
        self.command = None
        self.cmd = {"help":self.help, "quit":quit, "build":self.build, "solve":self.solve_class,\
             "show":self.show_class}
        self.loop()

    def loop(self):
        print("""\
        PYthon Electronic Circuit Solver (PYECS) 
        by Julien Audet
        Electricity and Magnetism - 203-NYB-05
        for help, type "help"
        to exit, type "exit"
        """)
        while self.command != "quit":
            self.command = input("=> ")
            try:
                self.cmd[self.command.split(" ")[0]]()

            except Exception as e:
                if e.__class__ == KeyError:
                    print("Sorry, I don't recognize that as a possible command,\nplease enter a valid comand or type 'help'")  
                else:
                    print(e.__class__)

    def help(self):
        with open("help.txt", "r") as h:
            for line in h:
                print(line)


    def build(self):
        """builds graph according to source:
            - csv
            - gui    
        """
        source = input("please input where you want to build your file from\ncsv or gui\n").split(" ")
        if len(source) == 0:
            print("usage : '=> build source'\n no graph was made : no source given\nsource are 'gui' or 'csv'")
            return None
        # build from csv file
        elif source[0] == "csv":
            try:
                self.filename = source[1]
                g = graph_from_pandas(self.filename)
                self.graph = g
            except:
                print("need a file to import csv from")
        # build from GUI
        elif source[0] == "gui":
            c = graph_from_GUI()
            self.graph = c.graph
            self.graph_class = c
        else:
            print("Source not in sources. Type help to know what are valid sources")     

    def solve_class(self):
        if self.graph == None:
            print("first input a graph please")
            return None
        else:
            self.cycles = nx.cycle_basis(self.graph)
            self.graph = build_polarity(self.graph, self.cycles)
            self.graph = solve(self.graph, self.cycles)

    def show_class(self):
        target = input("input what to show, see help for details\n")
        if self.graph is not None:

            # shows the list of nodes
            if target == "full":
                for node in self.graph.adj:
                    for edge in self.graph.adj[node]:
                        print("node {} to node {} : ".format(node, edge), self.graph.adj[node][edge])                


            # shows the plot of the data
            elif target == "plot":

                fig, ax = plt.subplots()
                ax.set_xlim(left=0, right=21)
                ax.set_ylim(bottom=0, top=21)
                # sets ticks and size
                minor_ticks = np.linspace(0,20,21)
                ax.set_xticks(minor_ticks)
                ax.set_yticks(minor_ticks)
                ax.grid(True)
                for s_n in self.graph.adj: # s_n for start node
                    for e_n in self.graph.adj[s_n]: # e_n for end node
                        # plotting line from s_n to e_n
                        x = [s_n[0]+0.5, e_n[0]+0.5]
                        y = [s_n[1]+0.5, e_n[1]+0.5]
                        type = self.graph.adj[s_n][e_n]["type"]
                        if type == "resistance":
                            style = "ko-"
                        else:
                            style = "bo:"
                        ax.plot(x, y, style)
                plt.show()

            else:
                print("select valid target")
        else:
            print("no graph loaded")
            
def main():
    cli = CLI()

    """

        # my drawing part
        s3 = plt.subplot(111)
        nx.draw_planar(solved, with_labels=True)
        plt.show()
    """



if __name__ == "__main__":
    main()