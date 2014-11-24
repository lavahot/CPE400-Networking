#!/usr/bin/python

#Zachary Carlson
#Thomas 'Taylor' Mansfield
#MacCallister Higgins
#CPE 400 Project 2
import random
import riprouter as rip

class NetworkMap(object):
	"""Contains all of the nodes in a network."""
	def __init__(self, netMap=[]):
		super(NetworkMap, self).__init__()
		self.netMap=netMap

	def advertise(self, routerID):
		"""Will send out advertisements to each of the nodes connected to this."""
		# for router in netMap:
		for router in self.netMap:
			pass

	def iterate(self):
		"""Iterate through all of the routers on the network and send one RIP advertisement each."""
		# Initialize change in router table for this iteration.
		for router in self.netMap:
			pass

	def mapNet(self):
		"""Map the entire network until there are no updates to the routing tables."""
		pass

def main():
	nmap = NetworkMap([rip.Router('A')])

if __name__ == "__main__": main()
