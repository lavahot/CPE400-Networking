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
		super(NetworkMap, self).__init__()
		self.netMap={"132.192.192.68": rip.Router("132.192.192.68"), "132.192.192.67": rip.Router("132.192.192.67")}
		#build a network map

	def advertise(self, router):
		"""Will send out advertisements to each of the nodes connected to this."""
		for neighbor in self.netMap[router][1]: #foreach router that this router is connected to
			neighborupdate=False #new bool
			for subnet in self.netMap[router][0]: #foreach destination in the dictionary of destinations of the router
				if subnet not in self.netMap[neighbor][0]: #if this subnet is not in their particular table, it looks into their table and adds a hop
					self.netMap[neighbor][0][subnet] = (router,self.netMap[router][0][subnet][1] + 1) 
					neighborupdate=True
				elif self.netMap[neighbor][0][subnet][1] > self.netMap[router][0][subnet][1] + 1: #if the router you are connected to doesn't have a better router, fix it  
					self.netMap[neighbor][0][subnet] = (router,self.netMap[router][0][subnet][1] + 1)
					neighborupdate=True
			if neighborupdate:
				self.netMap[neighbor][3]=True #mark it as updated
		self.netMap[router][2]=False #marks current router as no longer advertising

	def iterate(self):
		"""Iterate through all of the routers on the network and send one RIP advertisement each."""
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