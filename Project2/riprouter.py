#ROUTER CLASS
#Zachary Carlson
#Thomas 'Taylor' Mansfield
#MacCallister Higgins
#CPE 400 Project 2

class Router():

	# Needed for graphing (dictionaries are unhashable)
	def __hash__(self):
		return id(self)

	"""Router Class"""
	def __eq__(self, other):
		"""Equality only checks router ids"""
		if self.ip != other.ip: #Router IP
			return False
		if self.neighbors != other.neighbors:
			return False
		if self.ripTable != other.ripTable:
			return False
		if self.ripTableCap != other.ripTableCap:
			return False
		if self.hopCap != other.hopCap:
			return False
		if self.buffer != other.buffer:
			return False
		#if self.bAdvertising != other.bAdvertising:
		#	return False
		#if self.bUpdated != other.bUpdated:
		#	return False
		#if self.bMark != other.bMark:
		#	return False
		return True

	def __init__(self, ip, table = {}, rNeighbors = []):
		self.ip = ip #Router IP 
		self.neighbors = [] #List of neighbor's IP Addresses
		#self.ripTable = {"Destination Subnet": ["Next Router", "Number of Hops"]} #This line causes issues with advertise
		self.ripTable = {}
		self.ripTableCap = 25 #Maximum number of rows allowed in the RIP Table
		self.hopCap = 15
		self.bAdvertising = True
		self.bUpdated = False
		self.bMark = False
		self.buffer = []#list of packets that represents it's buffer
		if rNeighbors:
			for neighbor in rNeighbors:
				self.addNeighbor(neighbor)
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
	
	def addNeighbor(self, neighborIP):
		"""adds the neighborIP to the list of neighbors, does not affect tables"""
		#add neighbor to list		
		if neighborIP not in self.neighbors:
			self.neighbors.append(neighborIP)
	def removeNeighbor(self, neighborIP):
		"""removes the neighborIP from the list of neighbors, and updates tables"""
		#add neighbor to list		
		if neighborIP in self.neighbors:
			self.neighbors.remove(neighborIP)
		#iterate through table and build a new table where next router is != neighborIP
		newTable = {}
		for row in self.ripTable:
			if self.ripTable[row][0] != neighborIP:
				newTable[row] = self.ripTable[row]
		self.ripTable = newTable
	def advertise(self, neighbor):
		"""Will send out an advertisement to the connected neighbor if that neighbor is in fact a valid neighbor"""
		#check if neighbor is valid
		if neighbor.ip in self.neighbors and self.ip in neighbor.neighbors:
			newTable = {}
			for subnet in neighbor.ripTable:
				#if that table's next router is not this router, add it to the new table
				if neighbor.ripTable[subnet][0] != self.ip:
					newTable[subnet] = neighbor.ripTable[subnet]
				#if our router's table has the subnet, add it to the new table
				elif subnet in self.ripTable.keys():
					newTable[subnet] = neighbor.ripTable[subnet]
			#set new table
			neighbor.ripTable = newTable
			#foreach destination subnet in the destinations of this router
			for subnet in self.ripTable:
				#if this subnet is not in their particular table, it looks into their table and adds a hop
				if subnet not in neighbor.ripTable.keys():
					neighbor.ripTable[subnet] = [self.ip, self.ripTable[subnet][1] + 1]
				#if the neighbor self is connected to doesn't have a better route and self's soluton doesn't go through the neighbor with the better route 
				elif neighbor.ripTable[subnet][1] > self.ripTable[subnet][1] + 1 and neighbor.ripTable[subnet][0] != self.ip:
					neighbor.ripTable[subnet] = [self.ip, self.ripTable[subnet][1] + 1]
			#if nUpdate=True
			neighbor.bUpdated = True
			neighbor.bAdvertising = True
		#if self thinks it has a connection but the conencted router doesn't have a connection to self
		elif neighbor.ip in self.neighbors:
			self.removeNeighbor(neighbor.ip)
