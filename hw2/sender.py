import socket
import struct
import sys
import select
import hashlib

agentip = '127.0.0.1'
agentport = 8888
ip = '127.0.0.1'
port = 8887


class Header:
	def __init__(self, length, seqNumber, ackNumber, fin, syn, ack):
		self.length = length
		self.seqNumber = seqNumber
		self.ackNumber = ackNumber
		self.fin = fin
		self.syn = syn
		self.ack = ack

class segment:
	def __init__(self, header, data):
		self.header = header
		self.data = data


emptydata = ''
for i in range(1000):
	emptydata += '\0'
sendersocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sendersocket.bind((ip,port))
filename = sys.argv[1]
f = open(filename,'rb')
seqnum = 1
winseqnum = seqnum
maxseqnum = seqnum
endseqnum = 0
winsend = 0
timeout = 0
getacknum = 1
threshold = 16
winsize = 1
drop = 0
reads = [sendersocket]
while True:
	winseqnum = seqnum
	for i in range(winsize):
		change = 0
		f.seek(1000*(seqnum-1), 0)
		data = f.read(1000)
		header = Header(1000,seqnum,0,0,0,0)
		if 0 <= len(data) < 1000:
			if len(data) == 0:
				endseqnum = seqnum
				header.length = 0
				break
			for i in range(len(data),1000):
				header.length = len(data)
				data = data
		Message = segment(header, data)
		Message = struct.pack("6i1000s",Message.header.length, Message.header.seqNumber, Message.header.ackNumber, Message.header.fin, Message.header.syn, Message.header.ack, Message.data)
		sendersocket.sendto(Message,(agentip, agentport))
		seqnum += 1
		if seqnum > maxseqnum:
			maxseqnum = seqnum
			change = 1
		if change == 1:
			print('send    data    #',seqnum - 1,',    winsize =', winsize)
		else:
			print('resnd   data    #',seqnum - 1,',    winsize =',winsize)

	while winseqnum != seqnum:
		timeout = 0
		readable, writeable, exceptional = select.select(reads,[],[],1)
		if readable != []:
			for read in readable:
				ackdata, addr = sendersocket.recvfrom(10240)
				if addr[0] == agentip and addr[1] == agentport:
					length, seqNumber, ackNumber, fin, syn, ack, data = struct.unpack("6i1000s",ackdata)
					print('recv    ack     #',ackNumber)
					if ackNumber == winseqnum:
						winseqnum += 1
		else:
			threshold = max(int(winsize/2),1)
			winsize = 1
			timeout = 1
			seqnum = winseqnum
			print('time    out,             threshold = ',threshold)
			break
	if timeout == 0:
		if winsize < threshold:
			winsize = winsize*2
		else:
			winsize += 1
	if winseqnum == endseqnum:
		header = Header(0,0,0,1,0,0)
		Message = struct.pack("6i1000s",0,0,0,1,0,0,emptydata.encode('utf-8'))
		sendersocket.sendto(Message,(agentip, agentport))
		print('send    fin')
		ackdata, addr = sendersocket.recvfrom(10240)
		if addr[0] == agentip and addr[1] == agentport:
			length, seqNumber, ackNumber, fin, syn, ack, data = struct.unpack("6i1000s",ackdata)
			if fin == 1 and ack == 1:
				print('recv    finack')
				break 




