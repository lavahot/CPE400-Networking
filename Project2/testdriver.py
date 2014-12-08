#!/usr/bin/python

#Zachary Carlson
#Thomas 'Taylor' Mansfield
#MacCallister Higgins
#CPE 400 Project 2 TEST DRIVER

import RIP
import riprouter as rip
import networkx as nx
import matplotlib.pyplot as plt


#######################################################################################
#######################################################################################

def convert(routerD):	# Converts router list/dictionary into usable graph

	# Initializations
	graph = nx.Graph()

	# Iterate through dictionary
	for key in routerD:
		# Add nodes
		graph.add_node(routerD[key].ip)
		# Add edges
		for index in range(len(routerD[key].neighbors)):
			graph.add_edge(routerD[key].ip,(routerD[key].neighbors[index]))

	# Return converted graph
	return graph

#######################################################################################
#######################################################################################

def draw_graph(graph):	# Draws resulting graph from previous function

    # extract nodes from graph
    #nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    # create networkx graph
    #G=nx.Graph()

    # add nodes
    #for node in nodes:
        #G.add_node(node)

    # add edges
    #for edge in graph:
        #G.add_edge(edge[0], edge[1])

    # draw graph
    pos = nx.shell_layout(graph)
    nx.draw(graph, pos)

    # show graph
    plt.show()

#######################################################################################
#######################################################################################

def testSummary(printing):
	#TESTS
	#TEST 0: No data
	print("----------------------TEST 0-------------------------------")
	nmap0 = RIP.NetworkSimulation({"1": rip.Router("1"),
			 			 		   "2": rip.Router("2"),
			 			 		   "3": rip.Router("3")})
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 0 Print BEFORE---------------------------------")
		print("-----------------------------------------------------")
		nmap0.printNET()
	
	nmap0.mapNet()
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 0 Print AFTER----------------------------------")
		print("-----------------------------------------------------")
		nmap0.printNET()
	#NOT PRINTING
	if printing == False:
		nmap0comparison = RIP.NetworkSimulation({"1": rip.Router("1"),
			 			 		   				 "2": rip.Router("2"),
			 			 		   				 "3": rip.Router("3")})
		if nmap0.netMap == nmap0comparison.netMap:
		   	print("PASS")
		else:
			print("FAIL")
	#TEST 1
	print("----------------------TEST 1------------------------------")
	nmap1 = RIP.NetworkSimulation(
		{"1": rip.Router("1", {"u": ["-", 1]}, ["2", "3"]),
		 "2": rip.Router("2", {"w": ["-", 1]}, ["1"]),
		 "3": rip.Router("3", {}, ["1"])}
		 )
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 1 Print BEFORE----------------------------------")
		print("-----------------------------------------------------")
		nmap1.printNET()
	nmap1.mapNet()
	#"3" need to add: "w": ["1", 3]
	#"2" needs to add "u" : ["1", 2]
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 1 Print AFTER-----------------------------------")
		print("-----------------------------------------------------")
		nmap1.printNET()
	#NOT PRINTING
	if printing == False:
		nmap1comparison = RIP.NetworkSimulation({"1": rip.Router("1", {"u": ["-", 1], "w": ["2", 2]}, ["2", "3"]),
			 			 		   				 "2": rip.Router("2", {"w": ["-", 1], "u" : ["1", 2]}, ["1"]) ,
			 			 		   				 "3": rip.Router("3", {"w": ["1", 3], "u" : ["1", 2]}, ["1"])})
		if nmap1.netMap == nmap1comparison.netMap:
		   	print("PASS")
		else:
			print("FAIL")
	#TEST 2
	print("----------------------TEST 2------------------------------")
	nmap2 = RIP.NetworkSimulation(
		{"1": rip.Router("1", {}, ["2", "3"]),
		 "2": rip.Router("2", {}, ["1", "3"]),
		 "3": rip.Router("3", {}, ["1", "2"])}
		 )
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 2 Print BEFORE----------------------------------")
		print("-----------------------------------------------------")
		nmap2.printNET()
	nmap2.mapNet()
	nmap2.breakConnection("1", "2")
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 2 Print AFTER-----------------------------------")
		print("-----------------------------------------------------")
		#1 and 2 should have no neighbors
		nmap2.printNET()
	#NOT PRINTING
	if printing == False:
		nmap2comparison = RIP.NetworkSimulation({"1": rip.Router("1", {}, ["3"]),
			 			 		   				 "2": rip.Router("2", {}, ["3"]),
			 			 		   				 "3": rip.Router("3", {}, ["1", "2"])})
		if nmap2.netMap == nmap2comparison.netMap:
		   	print("PASS")
		else:
			print("FAIL")
	#TEST 3
	print("----------------------TEST 3------------------------------")
	nmap3 = RIP.NetworkSimulation(
		{"1": rip.Router("1", {"u":["2", 2]}, ["2"]),
		 "2": rip.Router("2", {"u":["-", 1]}, ["1"])}
		 )
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 3 Print BEFORE----------------------------------")
		print("-----------------------------------------------------")
		nmap3.printNET()
	nmap3.mapNet()
	nmap3.randomBreakConnection()
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 3 Print AFTER-----------------------------------")
		print("-----------------------------------------------------")
		#1 and 2 should have no neighbors
		nmap3.printNET()
	#NOT PRINTING
	if printing == False:
		nmap3comparison = RIP.NetworkSimulation({"1": rip.Router("1", {}, []),
			 			 		   				 "2": rip.Router("2", {"u":["-", 1]}, []),
			 			 		   				 })
		if nmap3.netMap == nmap3comparison.netMap:
		   	print("PASS")
		else:
			print("FAIL")
	#TEST 4
	print("----------------------TEST 4------------------------------")
	nmap4 = RIP.NetworkSimulation(
		{"1": rip.Router("1", {"u":["2", 2]}, ["2", "3"]),
		 "2": rip.Router("2", {"u":["-", 1]}, ["1"]),
		 "3": rip.Router("3", {"u":["1", 3]}, ["1"])
		 })
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 4 Print BEFORE----------------------------------")
		print("-----------------------------------------------------")
		nmap4.printNET()
	nmap4.breakConnection("1", "2")
	nmap4.mapNet()
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 4 Print AFTER-----------------------------------")
		print("-----------------------------------------------------")
		#1 and 2 should have no neighbors
		nmap4.printNET()
	#NOT PRINTING
	if printing == False:
		nmap4comparison = RIP.NetworkSimulation(
			{"1": rip.Router("1", {}, ["3"]),
		 	 "2": rip.Router("2", {"u":["-", 1]}, []),
		 	 "3": rip.Router("3", {}, ["1"])
		 	})
		if nmap4.netMap == nmap4comparison.netMap:
		   	print("PASS")
		else:
			print("FAIL")
	#TEST 5
	print("----------------------TEST 5------------------------------")
	nmap5 = RIP.NetworkSimulation(
		{"A": rip.Router("A", {"u": ["-", 1], "w": ["-", 1]}, ["C", "B"]),
		 "B": rip.Router("B", {}, ["A", "G"]),
		 "C": rip.Router("C", {"x": ["-", 1]}, ["A", "D"]),
		 "D": rip.Router("D", {"z": ["-", 1], "y": ["-", 1]}, ["H", "I", "C"]),
		 "E": rip.Router("E", {"s": ["-", 1]}, ["F", "I"]),
		 "F": rip.Router("F", {"q": ["-", 1]}, ["G", "E", "H"]),
		 "G": rip.Router("G", {}, ["F", "B"]),
		 "H": rip.Router("H", {"r": ["-", 1]}, ["F", "D"]),
		 "I": rip.Router("I", {}, ["D", "E"])
		 })
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 5 Print BEFORE----------------------------------")
		print("-----------------------------------------------------")
		nmap5.printNET()
	nmap5.mapNet()
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 5 Print AFTER-----------------------------------")
		print("-----------------------------------------------------")
		nmap5.printNET()
	#NOT PRINTING
	if printing == False:
		nmap5comparison = RIP.NetworkSimulation(
			{"A": rip.Router("A", {"q": ["-", 1], "r": ["-", 1],"s": ["-", 1], "x": ["-", 1], "y": ["-", 1], "z": ["-", 1] "u": ["-", 1], "w": ["-", 1]}, ["C", "B"]),
		 	 "B": rip.Router("B", {}, ["A", "G"]),
		 	 "C": rip.Router("C", {"x": ["-", 1]}, ["A", "D"]),
		 	 "D": rip.Router("D", {"z": ["-", 1], "y": ["-", 1]}, ["H", "I", "C"]),
		 	 "E": rip.Router("E", {"s": ["-", 1]}, ["F", "I"]),
		 	 "F": rip.Router("F", {"q": ["-", 1]}, ["G", "E", "H"]),
		 	 "G": rip.Router("G", {}, ["F", "B"]),
		 	 "H": rip.Router("H", {"r": ["-", 1]}, ["F", "D"]),
		 	 "I": rip.Router("I", {}, ["D", "E"])
		 })
		if nmap5.netMap == nmap5comparison.netMap:
		   	print("PASS")
		else:
			print("FAIL")
#######################################################################################
#######################################################################################
	
def main():
	testSummary(True)

	# Intializations
	nmap0 = RIP.NetworkSimulation({"1": rip.Router("192.168.1.1"), "2": rip.Router("2"), "3": rip.Router("3")})
	nmap1 = RIP.NetworkSimulation(
		{"1": rip.Router("1", {"u": ["-", 1]}, ["2", "3"]),
		 "2": rip.Router("2", {"w": ["-", 1]}, ["1"]),
		 "3": rip.Router("3", {}, ["1"])}
		 )
	nmap2 = RIP.NetworkSimulation(
		{"1": rip.Router("1", {}, ["2"]),
		 "2": rip.Router("2", {}, ["1"]),
		 "3": rip.Router("3", {}, ["1", "2"])}
		 )
	nmap3 = RIP.NetworkSimulation(
		{"1": rip.Router("1", {}, ["2"]),
		 "2": rip.Router("2", {}, ["1"])}
		 )

	# Convert router dictionary to graph
	g1 = convert(nmap0.netMap)
	g2 = convert(nmap1.netMap)
	g3 = convert(nmap2.netMap)
	g4 = convert(nmap3.netMap)

	# Draw Graph
	#graph = [(nmap0.netMap["1"].ip, 21),(21, 22),(21, 23), (23, 24),(24, 25), (25, nmap0.netMap["1"].ip)]
	draw_graph(g1)
	draw_graph(g2)
	draw_graph(g3)
	draw_graph(g4)

	# Wait for subnet kill

	# Generate random subnet kill based on likelihood

if __name__ == "__main__": main()
