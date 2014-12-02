#ROUTER CLASS
#Zachary Carlson
#Thomas 'Taylor' Mansfield
#MacCallister Higgins
#CPE 400 Project 2

class Router():
	"""Router Class"""
	def __eq__(self, other):
		"""Equality only checks router ids"""
		return self.id == other.id #Router ID

	def __init__(self, rid, table = {}, neighbors = []):
		self.id = rid #Router ID/KEY
		self.neighbors = []#List of neighbors
		self.ripTable = {"Destination Subnet": ["Next Router", "Number of Hops"]} #RIP Table
		self.ripTableCap = 25 #Maximum number of rows allowed in the RIP Table
		self.hopCap = 15
		self.bAdvertising = True
		self.bUpdated = False
		if table:
			for row in table:
				if len(table[row]) == 2:
					self.addRipRow(row, table[row][0], table[row][1] )
		
	def addRipRow(self, subnet, nextR, hops):
		"""Adds row to table and updates neighbors if needed"""
		#ensure table isn't over the cap and that hops are under hopCap
		if len(self.ripTable) <= self.ripTableCap and hops < self.hopCap:
			#update neighbors if needed
			if hops == 2 and nextR not in self.neighbors:
				self.addNeighbor(nextR)
			self.ripTable[subnet] = [nextR, hops]
			return True
		else:
			return False
	
	def addNeighbor(self, neighborID):
		#add neighbor to list		
		if neighborID not in self.neighbors:
			self.neighbors.append(neighborID)
	def advertise(self, neighbor):
		#update their tables
		pass