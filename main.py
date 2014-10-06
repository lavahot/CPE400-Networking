import random

def makePacket(num, size):
	x = []
	for i in range(num):
		x.append(format(random.getrandbits(size), '#010b'))
	return x

def makePacketList(num, size, bsize):
	x = []
	for i in range(num):
		x.append(makePacket(size, bsize))
	return x

def reportPacket(records, seq, time, success):
	records.append((seq, time, success))

def stopAndWait(numPackets, packSize):
	packetList = makePacketList(numPackets, packSize, 8)
	listLen = len(packetList)
	records = []
	error = 0
	for i in range(listLen):
		if i == (listLen / 6) or i == (listLen * 2 /6) or i == (listLen * 3 /6) or i == (listLen * 4 /6) or i == (listLen * 5 /6):
			error += 1
		RTT = 0
		success = False
		while !success:
			RTT = random.randint(10,50)
			# RTT timeout
			if RTT> 45:
				reportPacket(records, i, RTT, success)
				continue
			# check for transmission failure twice, once for packet send, one for ack receipt.
			if (random.randint(1, 100) <= error or random.randint(1, 100) <= error):
				RTT += random.randint(10,50)
				continue
			success = True
			reportPacket(records, i, RTT, success)

# y = makePacketList(3, 3, 8)

stopAndWait(20, 20)
 