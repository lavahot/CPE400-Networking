#!/usr/bin/python

#Zachary Carlson
#Thomas 'Taylor' Mansfield
#MacCallister Higgins
#CPE 400 Project 2
import random
import riprouter as rip

class NetworkSimulation(object):
	"""Contains all of the nodes in a network."""
	def __init__(self, netMap=[]):
		super(NetworkSimulation, self).__init__()
		self.netMap={"132.192.192.68": rip.Router("132.192.192.68"), "132.192.192.67": rip.Router("132.192.192.67")}
		#build a network map

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
	nmap = NetworkSimulation()

if __name__ == "__main__": main()