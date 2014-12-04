#!/usr/bin/python

#Zachary Carlson
#Thomas 'Taylor' Mansfield
#MacCallister Higgins
#CPE 400 Project 2 TEST DRIVER
import random
import riprouter as rip

class NetworkSimulation(object):
	"""Contains all of the nodes in a network."""
	def __init__(self, netMap={}):
		super(NetworkSimulation, self).__init__()
		self.netMap = netMap

	def printNET(self):
		for router in self.netMap:
			#Router IP
			#neighbors = []
			#ripTable = {"Destination Subnet": ["Next Router", "Number of Hops"]}
			#bAdvertising
			#bUpdated
			#bMark
			print(" ")
			print("Router IP:" + self.netMap[router].ip + " ---------")
			print("Neighbors:")
			for neighbor in self.netMap[router].neighbors:
				print("\t"),
				print neighbor,
			print("\nTable:"),
			for row in self.netMap[router].ripTable:
				print ("\n\t"),
				print row,
				print ("\t"), 
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
def main():
	print("Regular Main")

if __name__ == "__main__": main()
