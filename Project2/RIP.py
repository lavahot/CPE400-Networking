#!/usr/bin/python

#Zachary Carlson
#Thomas 'Taylor' Mansfield
#MacCallister Higgins
#CPE 400 Project 2
import random
import riprouter as rip

class NetworkSimulation(object):
	"""Contains all of the nodes in a network."""
	def __init__(self, index, netMap=[]):
		super(NetworkSimulation, self).__init__()
		
		self.testing(index)

	def testing(self, testIndex):
		#BUILD A NETWORK MAP FOR TESTING
		#ROUTER CONSTRUCTOR: def __init__(self, ip, table = {}, neighbors = []):
		if testIndex == 0:
			#no rip tables
			self.netMap={"1": rip.Router("1"),
			 			 "2": rip.Router("2"),
			 			 "3": rip.Router("3")}
		if testIndex == 1:
			#basic test where everything is accurate, once this test is done, 
			#"3" need to add: "w": ["1", 3]
			#"2" needs to add "u" : ["1", 2]
			self.netMap={"1": rip.Router("1", {"u": ["-", 1],
											   "w": ["2", 2]},
											   ["2", "3"]
											   ),
			 			 "2": rip.Router("2", {"w": ["-", 1]}, ["1"]),
			 			 "3": rip.Router("3", {"u": ["1", 2]}, ["1"])}
		if testIndex == 2:
			#testing for how it handles cycles
			self.netMap={"1": rip.Router("1"), 
						 "2": rip.Router("2"), 
						 "3": rip.Router("3")}
	def printNET(self):
		for router in self.netMap:
			#Router IP 
			#self.neighbors = []#List of neighbor's IP Addresses
			#self.ripTable = {"Destination Subnet": ["Next Router", "Number of Hops"]} #RIP Table Subnets end in 0
			#self.bAdvertising = True
			#self.bUpdated = False
			#self.bMark = False
			print(" ")
			print("Router IP:" + self.netMap[router].ip + " ---------")
			print("Neighbors:")
			for neighbor in self.netMap[router].neighbors:
				print("\t"),
				print neighbor,
			print("\nTable:"),
			for row in self.netMap[router].ripTable:
				print ("\n\t"), 
				for v in self.netMap[router].ripTable[row]:
					print v,
					print ("\t"),
			print("\nbAdvertising:"),
			print self.netMap[router].bAdvertising
			print("bUpdated:"),
			print self.netMap[router].bUpdated
			print("bMark:"), 
			print self.netMap[router].bMark
			print("----------------------------------")
			print(" ")
		pass
	def iterate(self):
		"""Iterate through all of the routers on the network that are advertising and has each router advertise to each of it's neighbors."""
		# Initialize change in router table for this iteration.
		for router in self.netMap:
			self.netMap[router].bUpdated=False
		update=False
		#for each router
		for router in self.netMap:
			#if the router is advertising
			if self.netMap[router].bAdvertising:
				#for each neighbor ip address
				for r in self.netMap[router].neighbors:
					#advertise to that neighbor if that neighbor has not already advertised
					if not self.netMap[r].bMark:
						self.netMap[router].advertise(self.netMap[r])
					if self.netMap[r].bUpdated:
						update=True # we updated at least 1 neighbor's table
				#router is done advertising and is marked
				self.netMap[router].bAdvertising = False
				self.netMap[router].bMark = True
		return update

	def mapNet(self):
		"""Map the entire network until there are no updates to the routing tables."""
		#each router takes turns mapping
		for router in self.netMap:
			#unmark all routers
			for node in self.netMap:
				self.netMap[node].bMark = False
			self.netMap[router].bAdvertising = True
			self.netMap[router].bMark = True
			advertising = True
			while advertising == True:
				self.iterate()
				advertising = False
				#check if any nodes are advertising
				for node in self.netMap:
					if self.netMap[node].bAdvertising:
						advertising = True
						break

def test():
	#TESTS
	print("----------------------TEST 0-------------------------------")
	nmap0 = NetworkSimulation(0)
	print("-----------------------------------------------------")
	print("TEST 0 Print BEFORE---------------------------------")
	print("-----------------------------------------------------")
	nmap0.printNET()
	nmap0.mapNet()
	print("-----------------------------------------------------")
	print("TEST 0 Print AFTER----------------------------------")
	print("-----------------------------------------------------")
	nmap0.printNET()

	print("----------------------TEST 1------------------------------")
	nmap1 = NetworkSimulation(1)
	print("-----------------------------------------------------")
	print("TEST 1 Print BEFORE----------------------------------")
	print("-----------------------------------------------------")
	nmap1.printNET()
	nmap1.mapNet()
	print("-----------------------------------------------------")
	print("TEST 1 Print AFTER-----------------------------------")
	print("-----------------------------------------------------")
	nmap1.printNET()

def main():
	test()

if __name__ == "__main__": main()