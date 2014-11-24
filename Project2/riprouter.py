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

	def __init__(self, rid, table = []):
		self.id = rid #Router ID
		self.neighbors = []#List of neighbors
		self.ripTable = [["Destination Subnet", "Next Router", "Number of Hops"]] #RIP Table
		self.ripTableCap = 25 #Maximum number of rows allowed in the RIP Table
		self.hopCap = 15
		if table:
			for row in table:
				if len(row) == 3:
					self.addRipRow(row[0], row[1], row[2] )
		
	def addRipRow(self, subnet, next, hops):
		"""Adds row to table and updates neighbors if needed"""
		#ensure table isn't over the cap and that hops are under hopCap
		if len(self.ripTable) <= self.ripTableCap and hops < self.hopCap:
			#update neighbors if needed
			if hops == 1 and next not in self.neighbors:
				self.neighbors.append(next)
			self.ripTable.append([subnet, next, hops])
			return True
		else:
			return False
