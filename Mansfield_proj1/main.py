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

def reportPacket(records, time, success, size, error):
	# Record format:
	# [Total sequences, total time, error, window size, error rate]
	records[0] += 1
	records[3] = size
	if not success:
		records[2] += 1
	records[1] += time
	records[4] = error


def stopAndWait(numPackets, packSize):
	packetList = makePacketList(numPackets, packSize, 8)
	listLen = len(packetList)
	error = 0
	allRecords = []

	for error in range(6):
		records = [0, 0, 0, 0, 0]
		for i in range(listLen):
			RTT = 0
			success = False
			while not success:
				RTT = random.randint(10,50)
				# RTT timeout
				if RTT> 45:
					reportPacket(records, 45, success, 1, float(error) / 10.0)
					continue
				# check for transmission failure twice, once for packet send, one for ack receipt.
				if (random.randint(1, 100) <= error or random.randint(1, 100) <= error):
					RTT += random.randint(10,50)
					continue
				success = True
				reportPacket(records, RTT, success, 1, float(error) / 10.0)
		allRecords.append(records)
	return allRecords


swRecords = stopAndWait(100, 100)
print "Stop and wait results."
print "Total packets | Total time (ms) | Total errors | Window Size | Error rate"
print('\n'.join('{} | {} | {} | {} | {}'.format(*k) for k in swRecords))
# print swRecords

def sendPacket():
	RTT = random.randint(10,50)
	# RTT timeout
	if RTT> 45:
		reportPacket(records, 45, success, 1, float(error) / 10.0)
	# check for transmission failure twice, once for packet send, one for ack receipt.
	if (random.randint(1, 100) <= error or random.randint(1, 100) <= error):
		RTT += random.randint(10,50)
		

def GoBackN(numPackets, packSize):
	packetList = makePacketList(numPackets, packSize, 8)
	listLen = len(packetList)

	base = packetList[0]
	nextseqnum = packetList[0]
	sendexpseqnum = 0
	recexpseqnum = 0
	for N in range(4, 17):
		# for each window size
		while (base <= listLen):
			# while there are packets in the queue
			while (nextseqnum <= base + N):
				# while there are serviceable packets in the window
				# sendPacket(packetList[nextseqnum], )
				pass

				


