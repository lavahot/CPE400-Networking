
# List structure for RIP messages: each row is a sublist, 
# each sublist contains first the destination subnet, 
# then the next router, then the number of hops.

import random
import riprouter as rtr

class NetworkMap(object):
	"""Contains all of the nodes in a network."""
	def __init__(self, netMap={}):
		super(NetworkMap, self).__init__()
		self.netMap=netMap



	# def genMap(nodes, edges):
	# 	"""Randomly generate nodes.

	# 		Notes: add nodes in alphabetical order. For edges, randomly add edges between known existing nodes.
	# 		""" 
	# 	pass
	# 	if nodes <= 26:
	# 		# if edges > nodes - 1:
	# 		# 	print "Too many edges, must be fewer than the number of nodes." 
			
	# 		for node in range(0,nodes):
	# 			netMap[ ord("a") + node ] = ''
	# 		for edge in range(0,edges):
	# 			# netMap[ ord("a") + randint(0,node-1) ] = 	
	# 	else:
	# 		print "Too many nodes. Must be between 1 and 26."


	def advertise(self, router):
		"""Will send out advertisements to each of the nodes connected to this."""
		# for router in netMap:
		for node in self.netMap[router][1]:
			nodeupdate=False
			for subnet in self.netMap[router][0]:
				if subnet not in self.netMap[node][0]:
					self.netMap[node][0][subnet] = (router,self.netMap[router][0][subnet][1] + 1)
					nodeupdate=True
				else:
					if self.netMap[node][0][subnet][1] > self.netMap[router][0][subnet][1]:
						self.netMap[node][0][subnet] = (router,self.netMap[router][0][subnet][1] + 1)
						nodeupdate=True
			if nodeupdate:
				self.netMap[node][3]=True
		self.netMap[router][2]=False

	def iterate(self):
		"""Iterate through all of the routers on the network and send one RIP advertisement each."""
		# Initialize change in router table for this iteration.
		for router in self.netMap:
			self.netMap[router][3]=False
		update=False
		for router in self.netMap:
			if self.netMap[router][2]:
				self.advertise(router)
				update=True
		for router in self.netMap:
			if not self.netMap[router][3]:
				self.netMap[router][2]=False
		print self.netMap
		return update

	def mapNet(self):
		"""Map the entire network until there are no updates to the routing tables."""
		pass

# Make new dictionary. Each router countains itself a tuple with a dictionary of all known 
# subnets as well as the routers it is currently connected to and its advertising status 
# and whether it's been updated on a particular iteration. 
# This example is from Fig 4.34 in the textbook.

nmap = NetworkMap({ 'A': [{ 'u': ['-',1]}, ('B', 'C'), True, False],
					'B': [{ 'v': ['-',1], 'w': ['-',1]}, ('A', 'D'), True, False],
					'C': [{ 'z': ['-',1]}, ('A', 'D'), True, False],
					'D': [{ 'x': ['-',1], 'y': ['-',1]}, ('B', 'C'), True, False]})

# Go through one iteration.
nmap.iterate()
