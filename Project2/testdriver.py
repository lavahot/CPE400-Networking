#!/usr/bin/python

#Zachary Carlson
#Thomas 'Taylor' Mansfield
#MacCallister Higgins
#CPE 400 Project 2 TEST DRIVER

import RIP
import riprouter as rip
import networkx as nx
import matplotlib.pyplot as plt
import Queue

# Global Lists
subnet=[]
router=[]

#######################################################################################
## Application and Transport Layer Implementation
#######################################################################################
# Calculates Checksum for UDP packet
def checksum(data):
	return '%2X' % (-(sum(ord(c) for c in data) % 256) & 0xFF)

#######################################################################################
#######################################################################################
# Turns string into buffer of UDP packets (IPV6)
# UDP Packet Format: |-Source-|-Destination-|-Length-|-Checksum-|-Data-|
def udp(data, source, destination):

	# Initializations
	buffer = Queue.Queue()
	
	# Split raw data into sections for separate UDP packets
	dataList = data.split()

	# Populate UDP packet structures with data and place in buffer
	for i in range(len(dataList)):
		buffer.put([source,destination,len(dataList),checksum(dataList[i]),dataList[i]])

	# Return buffer of UDP packets
	return buffer

#######################################################################################
#######################################################################################
# Checks if at correct router that directly connects to the right subnet
def routerCheck(nmap,currentRouter,subDest):
	#print routerTest.netMap[currentRouter].ripTable
	#nmap5.netMap['A'].ripTable['x'][1]
	#if nmap.netMap[currentRouter].ripTable[subDest][1] == 1:
	#if nmap.netMap['A'].ripTable['x'][1] == 1:
		#return True
	#else:
		#return False

	for key in nmap.netMap:
		#print currentRouter
		if nmap.netMap[key].ip == currentRouter:
			for key2 in nmap.netMap[key].ripTable:
				if nmap.netMap[key].ripTable[key2]:
					if nmap.netMap[key].ripTable[key2][1] == 1:
						#print "success"
						return True
					else:
						return False
				else:
					print "Subnet not in table, Cannot Transmit File"
		#else:
			#print nmap.netMap[key].ip,"Failure to find router in netMap"



#######################################################################################
#######################################################################################
# Loads file, parses it into UDP packets, and sends it from one subnet to another
# through the network based on RIP table mappings
def fileTransfer(subSource, subDest, nmap):	

	# Initializations
	rawData = "12345678 12345678 12345678 12345678"
	packet = 0
	hops = 0

	# Turn file into UDP packets
	buffer = udp(rawData, subSource, subDest)

	# Find Local Router (first connect, subSource->first router)
	# Search through each router
	for key in nmap.netMap:
		# Search through subnet list for hop == 1
		for key2 in nmap.netMap[key].ripTable:
			#print nmap.netMap[key].ripTable
			if nmap.netMap[key].ripTable[subSource][1] == 1:
				homeRouter = nmap.netMap[key].ip
				#print "current router", currentRouter


	# Loop through file transmission of all packets
	# For each packet
	while not buffer.empty():
		# Check for destination
		currentPacket = buffer.get()
		currentRouter = homeRouter
		delivered = False
		# Loop until delivered
		while delivered == False:
			# Check if at final router
			if routerCheck(nmap,currentRouter,subDest) == True:
				# Find/Send to next router in riptable of local router
				nextRouter = nmap.netMap[currentRouter].ripTable[subDest][0]
				#print nextRouter
				# Update source of UDP packet
				currentRouter = nextRouter
				hops += 1
			else:
				delivered = True
		# Output Transfer Results of single packet
		print "Packet ", (packet+1), " has been transferred to the destination subnet in ", hops, " hops"
		# Update packet counter
		packet = packet + 1
		hops = 0


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
############################################
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
############################################
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
		# Application and Transport Layer Testing
		fileTransfer("u", "w", nmap1)
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
############################################
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
############################################
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
############################################
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
############################################
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
	# Application and Transport Layer Testing before break
	fileTransfer("x", "z", nmap5)

	nmap5.breakConnection("A", "E")
	nmap5.mapNet()
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 5 Print AFTER Breaks----------------------------")
		print("-----------------------------------------------------")
		nmap5.printNET()
		drawNet(nmap5)

	# Application and Transport Layer Testing after break
	fileTransfer("x", "z", nmap5)

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


def main():
	testSummary(False)

	
if __name__ == "__main__": main()
