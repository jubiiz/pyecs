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
        print("sry bud haven't done that yet, contact me if u rlly need to use the code")


    def build(self):
        """builds graph according to source:
            - csv
            - gui    
        """
        source = input("please input where you want to build your file from\ncsv or gui\n ").split(" ")
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
        if target == "full":
            if self.graph is not None:
                for node in self.graph.adj:
                    for edge in self.graph.adj[node]:
                        print("node {} to node {} : ".format(node, edge), self.graph.adj[node][edge])
            else:
                print("no graph loaded")
        elif target == "plot":
            print("yeah gotta do this one from self.graph")

        else:
            print("select valid target")

def main():
    cli = CLI()

    """

        cycles = nx.cycle_basis(g)
        g = build_polarity(g, cycles)
        solved = solve(g, cycles)


        for n in g.adj:
            for e in g.adj[n]:
                print("node {} to node {} : ".format(n, e), g.adj[n][e])

        # my drawing part
        s3 = plt.subplot(111)
        nx.draw_planar(solved, with_labels=True)
        plt.show()
    """



if __name__ == "__main__":
    main()