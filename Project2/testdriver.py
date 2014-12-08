#!/usr/bin/python

#Zachary Carlson
#Thomas 'Taylor' Mansfield
#MacCallister Higgins
#CPE 400 Project 2 TEST DRIVER

import RIP
import riprouter as rip
import networkx as nx
import matplotlib.pyplot as plt

# Global Lists
subnet=[]
router=[]

#######################################################################################
#######################################################################################

# Usage example: drawNet(nmap5)

def drawNet(routerD):	# Draws Network Figure using only 1 Line

	# Initializations (Clear lists)
	del subnet[:]
	del router[:]

	# Build Graph from Dictionary
	g = convert(routerD.netMap)

	# Draw
	draw_graph(g,routerD.netMap)

#######################################################################################
#######################################################################################

def convert(routerD):	# Converts router list/dictionary into usable graph

	# Initializations
	graph = nx.Graph()

	# Iterate through dictionary
	for key in routerD:
		# Add nodes
		graph.add_node(routerD[key].ip,node_color="b")
		router.append(routerD[key].ip)
		# Add subnets
		subnets = (routerD[key].ripTable).viewkeys()
		for n in subnets:
			if routerD[key].ripTable[n][1] == 1:
				graph.add_node(n,node_color="r")
				graph.add_edge(routerD[key].ip,n,subnet=1)
				subnet.append(n)
		# Add edges
		for index in range(len(routerD[key].neighbors)):
			graph.add_edge(routerD[key].ip,(routerD[key].neighbors[index]),subnet=0)

	# Return converted graph
	return graph

#######################################################################################
#######################################################################################

def draw_graph(graph,routerD):	# Draws resulting graph from previous function

	# draw graph
	pos = nx.shell_layout(graph)

	#nx.draw_graphviz(graph,)
	#nx.draw(graph, pos, with_labels=True)
	
	nx.draw_networkx_nodes(graph,pos,with_labels=False, ax=None, label="Subnet", nodelist=subnet, node_color="g")
	nx.draw_networkx_nodes(graph,pos,with_labels=False, ax=None, label ="Router",nodelist=router, node_color="r")
	nx.draw_networkx_edges(graph,pos)
	nx.draw_networkx_labels(graph,pos)
	plt.axis('off')

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
		drawNet(nmap0)
	
	nmap0.mapNet()
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 0 Print AFTER----------------------------------")
		print("-----------------------------------------------------")
		nmap0.printNET()
		drawNet(nmap0)
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
		drawNet(nmap1)
	nmap1.mapNet()
	#"3" need to add: "w": ["1", 3]
	#"2" needs to add "u" : ["1", 2]
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 1 Print AFTER-----------------------------------")
		print("-----------------------------------------------------")
		nmap1.printNET()
		drawNet(nmap1)
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
		drawNet(nmap2)
	nmap2.mapNet()
	nmap2.breakConnection("1", "2")
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 2 Print AFTER-----------------------------------")
		print("-----------------------------------------------------")
		#1 and 2 should have no neighbors
		nmap2.printNET()
		drawNet(nmap2)
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
		drawNet(nmap3)
	nmap3.mapNet()
	nmap3.randomBreakConnection()
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 3 Print AFTER-----------------------------------")
		print("-----------------------------------------------------")
		#1 and 2 should have no neighbors
		nmap3.printNET()
		drawNet(nmap3)
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
		drawNet(nmap4)
	nmap4.breakConnection("1", "2")
	nmap4.mapNet()
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 4 Print AFTER-----------------------------------")
		print("-----------------------------------------------------")
		#1 and 2 should have no neighbors
		nmap4.printNET()
		drawNet(nmap4)
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
		{"A": rip.Router("A", {"x":["-", 1]}, ["B", "E"]),
		 "B": rip.Router("B", {}, ["A", "C"]),
		 "C": rip.Router("C", {}, ["B", "D"]),
		 "D": rip.Router("D", {}, ["C", "E"]),
		 "E": rip.Router("E", {"z":["-", 1]}, ["D", "A"])
		 })
	nmap5.mapNet()
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 5 Print BEFORE Break----------------------------")
		print("-----------------------------------------------------")
		nmap5.printNET()
		drawNet(nmap5)
	nmap5.breakConnection("A", "E")
	nmap5.mapNet()
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 5 Print AFTER Breaks----------------------------")
		print("-----------------------------------------------------")
		nmap5.printNET()
		drawNet(nmap5)
	#PASS OR FAIL SETTING
	if printing == False:
		nmap5comparison = RIP.NetworkSimulation(
		{"A": rip.Router("A", {"x":["-", 1], "z":["B", 5]}, ["B"]),
		 "B": rip.Router("B", {"x":["A", 2], "z":["C", 4]}, ["A", "C"]),
		 "C": rip.Router("C", {"x":["B", 3], "z":["D", 3]}, ["B", "D"]),
		 "D": rip.Router("D", {"x":["C", 4], "z":["E", 2]}, ["C", "E"]),
		 "E": rip.Router("E", {"x":["D", 5], "z":["-", 1]}, ["D"])
		 })
		if nmap5.netMap == nmap5comparison.netMap:
		   	print("PASS")
		else:
			print("FAIL")
#######################################################################################
#######################################################################################
def figurePrint():
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
	#draw_graph(g1)
	#draw_graph(g2)
	#draw_graph(g3)
	#draw_graph(g4)
	
	# Visualize Test Case 4
	#TEST 5
	printing = True;
	print("----------------------TEST 5------------------------------")
	nmap5 = RIP.NetworkSimulation(
		{"A": rip.Router("A", {"u": ["-", 1], "w": ["-", 1]}, ["C", "B"]),
		 "B": rip.Router("B", {}, ["A", "G"]),
		 "C": rip.Router("C", {"x": ["-", 1]}, ["A", "D"]),
		 "D": rip.Router("D", {"z": ["-", 1], "y": ["-", 1]}, ["H", "I", "C"]),
		 "E": rip.Router("E", {"s": ["-", 1]}, ["F", "J"]),
		 "F": rip.Router("F", {"q": ["-", 1]}, ["G", "E", "H"]),
		 "G": rip.Router("G", {}, ["F", "B"]),
		 "H": rip.Router("H", {"r": ["-", 1]}, ["F", "D"]),
		 "I": rip.Router("I", {}, ["D", "J"]),
		 "J": rip.Router("J", {}, ["I", "E"])
		 })
	nmap5.mapNet()
	nmap5.breakConnection("C", "D")
	nmap5.breakConnection("F", "E")
	nmap5.mapNet()
	nmap5.breakConnection("B", "G")
	nmap5.mapNet()
	nmap5.mapNet()
	nmap5.mapNet()
	g6 = convert(nmap5.netMap)
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 5 Print AFTER Isolated Network Break------------")
		print("-----------------------------------------------------")
		nmap5.printNET()
		draw_graph(g6)

	# Wait for subnet kill

	# Generate random subnet kill based on likelihood

def main():
	testSummary(True)

	
if __name__ == "__main__": main()
