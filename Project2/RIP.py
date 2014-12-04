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
		if testIndex == 0:
			#no rip tables
			self.netMap={"1": rip.Router("1"),
			 			 "2": rip.Router("2"),
			 			 "3": rip.Router("3")}
		if testIndex == 1:
			#basic test where everything is accurate
			self.netMap={"1": rip.Router("1"),
			 			 "2": rip.Router("2"),
			 			 "3": rip.Router("3")}
		if testIndex == 2:
			#testing for how it handles cycles
			self.netMap={"1": rip.Router("1"), 
						 "2": rip.Router("2"), 
						 "3": rip.Router("3")}

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
		print self.netMap
		return update

	def mapNet(self):
		"""Map the entire network until there are no updates to the routing tables."""
		#each router takes turns mapping
		for router in self.netMap:
			#unmark all routers
			for node in self.netMap:
				self.netMap[node].bMark = False
			router.bAdvertising = True
			router.bMark = True
			advertsing = True
			while advertising:
				iterate()
				advertising = False
				#check if any nodes are advertising
				for node in self.netMap:
					if node.bAdvertising:
						advertising = True
						break
def main():

	#TESTS
	nmap = NetworkSimulation(0)
	#build all of the RIP tables for each node
	#nmap.mapNet()

if __name__ == "__main__": main()