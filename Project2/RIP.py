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
		for router in self.netMap:
			if self.netMap[router].bAdvertising:
				for r in self.netMap[router].neighbors:
					self.netMap[router].advertise(self.netMap[r])
				update=True
		for router in self.netMap:
			if self.netMap[router].bUpdated:
				self.netMap[router].bAdvertising=True
		print self.netMap
		return update

	def mapNet(self):
		"""Map the entire network until there are no updates to the routing tables."""
		pass

def main():
	nmap = NetworkSimulation()

if __name__ == "__main__": main()