#!/usr/bin/python

#Zachary Carlson
#Thomas 'Taylor' Mansfield
#MacCallister Higgins
#CPE 400 Project 2 TEST DRIVER
import RIP
import riprouter as rip

def testPrints():
	#TESTS
	print("----------------------TEST 0-------------------------------")
	nmap0 = RIP.NetworkSimulation({"1": rip.Router("1"),
			 			 		   "2": rip.Router("2"),
			 			 		   "3": rip.Router("3")})
	print("-----------------------------------------------------")
	print("TEST 0 Print BEFORE---------------------------------")
	print("-----------------------------------------------------")
	nmap0.printNET()
	nmap0.mapNet()
	print("-----------------------------------------------------")
	print("TEST 0 Print AFTER----------------------------------")
	print("-----------------------------------------------------")
	nmap0.printNET()

	print("----------------------TEST 1------------------------------")
	nmap1 = RIP.NetworkSimulation(
		{"1": rip.Router("1", {"u": ["-", 1], "w": ["2", 2]}, ["2", "3"]),
		 "2": rip.Router("2", {"w": ["-", 1]}, ["1"]),
		 "3": rip.Router("3", {"u": ["1", 2]}, ["1"])}
		 )
	print("-----------------------------------------------------")
	print("TEST 1 Print BEFORE----------------------------------")
	print("-----------------------------------------------------")
	nmap1.printNET()
	nmap1.mapNet()
	#"3" need to add: "w": ["1", 3]
	#"2" needs to add "u" : ["1", 2]
	print("-----------------------------------------------------")
	print("TEST 1 Print AFTER-----------------------------------")
	print("-----------------------------------------------------")
	nmap1.printNET()

def main():
	testPrints()

if __name__ == "__main__": main()