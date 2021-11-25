from matplotlib import pyplot as plt
from math import floor
import numpy as np
import os
import networkx as nx
import pandas as pd

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
             "show":self.show_class, "save":self.save}
        self.loop()

    def loop(self):
        print("""\
        PYthon Electronic Circuit Solver (PYECS) 
        by Julien Audet
        Electricity and Magnetism - 203-NYB-05
        for help, type "help"
        to quit, type "quit"
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
            except Exception as e:
                print("need a file to import csv from, ", e.__class__)
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

            elif target == "clean":
                covered = []
                for node in self.graph.adj:
                    for edge in self.graph.adj[node]:
                        if edge not in covered:
                            print("node {} to node {} : ".format(node, edge), self.graph.adj[node][edge])                
                    covered.append(node)

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
    
    def save(self):
        """
        saves a copy of the current graph under a given filename
        """
        filename = input("What is the filename under which you want to save?\n")
        if filename is not None:
            path = os.path.join(os.getcwd(), "graphs{}{}.csv".format(os.sep, filename))
            df = {"node1":[], "node2":[], "type":[], "resistance":[], "polarity":[], "voltage":[], "current":[], "flow":[]}
            covered = []
            for s_n in self.graph.adj: # s_n for starting node
                for e_n in self.graph.adj[s_n]: # e_n for ending node
                    if e_n not in covered:
                        # add its info to the df
                        edge_data = self.graph.adj[s_n][e_n]
                        df["node1"].append(s_n)
                        df["node2"].append(e_n)
                        df["type"].append(edge_data["type"])
                        df["resistance"].append(edge_data["resistance"])
                        if len(edge_data["polarity"]) != 0:
                            polarity = ""
                            for p in edge_data["polarity"]:
                                polarity += f"{p}:{edge_data['polarity'][p]}#"
                            polarity = polarity.strip("#")
                            df["polarity"].append(polarity)
                        else:
                            df["polarity"].append(pd.NA)
                        df["voltage"].append(edge_data["voltage"])
                        df["current"].append(edge_data["current"])
                        df["flow"].append(edge_data["flow"])
                covered.append(s_n)
            print(df)
            df = pd.DataFrame(df)
            df.to_csv(path, sep='|', index=False)
            print("saved successfully")

        else:
            print("sorry, a filename is required")


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