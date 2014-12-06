#!/usr/bin/python

#Zachary Carlson
#Thomas 'Taylor' Mansfield
#MacCallister Higgins
#CPE 400 Project 2 TEST DRIVER
import RIP
import riprouter as rip

def testSummary(printing):
	#TESTS
	#TEST 0: No data
	print("----------------------TEST 0-------------------------------")
	nmap0 = RIP.NetworkSimulation({"1": rip.Router("1"),
			 			 		   "2": rip.Router("2"),
			 			 		   "3": rip.Router("3")})
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 0 Print BEFORE---------------------------------")
		print("-----------------------------------------------------")
		nmap0.printNET()
	
	nmap0.mapNet()
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 0 Print AFTER----------------------------------")
		print("-----------------------------------------------------")
		nmap0.printNET()
	#NOT PRINTING
	if printing == False:
		nmap0comparison = RIP.NetworkSimulation({"1": rip.Router("1"),
			 			 		   				 "2": rip.Router("2"),
			 			 		   				 "3": rip.Router("3")})
		if nmap0.netMap == nmap0comparison.netMap:
		   	print("PASS")
		else:
			print("FAIL")
	#TEST 1
	print("----------------------TEST 1------------------------------")
	nmap1 = RIP.NetworkSimulation(
		{"1": rip.Router("1", {"u": ["-", 1]}, ["2", "3"]),
		 "2": rip.Router("2", {"w": ["-", 1]}, ["1"]),
		 "3": rip.Router("3", {}, ["1"])}
		 )
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 1 Print BEFORE----------------------------------")
		print("-----------------------------------------------------")
		nmap1.printNET()
	nmap1.mapNet()
	#"3" need to add: "w": ["1", 3]
	#"2" needs to add "u" : ["1", 2]
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 1 Print AFTER-----------------------------------")
		print("-----------------------------------------------------")
		nmap1.printNET()
	#NOT PRINTING
	if printing == False:
		nmap1comparison = RIP.NetworkSimulation({"1": rip.Router("1", {"u": ["-", 1], "w": ["2", 2]}, ["2", "3"]),
			 			 		   				 "2": rip.Router("2", {"w": ["-", 1], "u" : ["1", 2]}, ["1"]) ,
			 			 		   				 "3": rip.Router("3", {"w": ["1", 3], "u" : ["1", 2]}, ["1"])})
		if nmap1.netMap == nmap1comparison.netMap:
		   	print("PASS")
		else:
			print("FAIL")

	#TEST 2
	print("----------------------TEST 2------------------------------")
	nmap2 = RIP.NetworkSimulation(
		{"1": rip.Router("1", {}, ["2"]),
		 "2": rip.Router("2", {}, ["1"]),
		 "3": rip.Router("3", {}, ["1", "2"])}
		 )
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 2 Print BEFORE----------------------------------")
		print("-----------------------------------------------------")
		nmap2.printNET()
	nmap2.mapNet()
	nmap2.breakConnection("1", "2")
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 2 Print AFTER-----------------------------------")
		print("-----------------------------------------------------")
		#1 and 2 should have no neighbors
		nmap2.printNET()
	#NOT PRINTING
	if printing == False:
		nmap2comparison = RIP.NetworkSimulation({"1": rip.Router("1", {}, []),
			 			 		   				 "2": rip.Router("2", {}, []),
			 			 		   				 "3": rip.Router("3", {}, ["1", "2"])})
		if nmap2.netMap == nmap2comparison.netMap:
		   	print("PASS")
		else:
			print("FAIL")
	#TEST 3
	print("----------------------TEST 3------------------------------")
	nmap3 = RIP.NetworkSimulation(
		{"1": rip.Router("1", {}, ["2"]),
		 "2": rip.Router("2", {}, ["1"])}
		 )
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 3 Print BEFORE----------------------------------")
		print("-----------------------------------------------------")
		nmap3.printNET()
	nmap3.mapNet()
	nmap3.randomBreakConnection()
	if printing == True:
		print("-----------------------------------------------------")
		print("TEST 3 Print AFTER-----------------------------------")
		print("-----------------------------------------------------")
		#1 and 2 should have no neighbors
		nmap3.printNET()
	#NOT PRINTING
	if printing == False:
		nmap3comparison = RIP.NetworkSimulation({"1": rip.Router("1", {}, []),
			 			 		   				 "2": rip.Router("2", {}, []),
			 			 		   				 })
		if nmap3.netMap == nmap3comparison.netMap:
		   	print("PASS")
		else:
			print("FAIL")

	
def main():
	testSummary(False)

if __name__ == "__main__": main()