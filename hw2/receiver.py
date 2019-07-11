import socket
import struct
import sys
 #coding=utf-8
agentip = '127.0.0.1'
agentport = 8888
ip = '127.0.0.1'
port = 8889


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


receiversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiversocket.bind((ip,port))

filename = sys.argv[1]
f = open(filename,'wb')
emptydata = ''
for i in range(1000):
	emptydata += '\0'
buf = []
bufsize = 32
expseqnum = 1
while True:
	recvdata, addr = receiversocket.recvfrom(2048)
	if addr[0] == agentip and addr[1] == agentport:
		length, seqNumber, ackNumber, fin, syn, ack, data = struct.unpack("6i1000s",recvdata)
		if fin == 1:
			print('recv    fin')
			#buf[len(buf)-1] = buf[len(buf)-1][:length]
			for i in buf:
				f.write(i)
			Message = segment(Header(0,0,0,1,0,1),emptydata)
			Message = struct.pack("6i1000s",Message.header.length, Message.header.seqNumber, Message.header.ackNumber, Message.header.fin, Message.header.syn, Message.header.ack, (Message.data).encode('utf-8'))
			receiversocket.sendto(Message,(agentip,agentport))
			print('send    finack')
			break
		elif bufsize == 0:
			print('drop    data    #',seqNumber)
			for i in buf:
				f.write(i)
			buf = []
			bufsize = 32
			Message = segment(Header(0,0,expseqnum - 1,0,0,1),emptydata)
			print('drop    data    #',seqNumber)
		elif expseqnum == seqNumber:
			print('recv    data    #',expseqnum)
			expseqnum += 1
			Message = segment(Header(0,0,seqNumber,0,0,1),emptydata)
			buf.append(data[:length])
			bufsize -= 1
		else:
			Message = segment(Header(0,0,expseqnum - 1,0,0,1),emptydata)
			print('drop    data    #',seqNumber)
		ackNumber = Message.header.ackNumber
		Message = struct.pack("6i1000s",Message.header.length, Message.header.seqNumber, Message.header.ackNumber, Message.header.fin, Message.header.syn, Message.header.ack, (Message.data).encode('utf-8'))
		receiversocket.sendto(Message,(agentip,agentport))
		print('send    ack     #',ackNumber)




