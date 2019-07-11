import socket # Include library
import select
import sys

IRCSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
IRCSocket.connect( ( '127.0.0.1', 6667 ) )
Msg1 = 'NICK RA \r\n'
Msg2 = 'USER TA \r\n'
Msg3 = 'JOIN #CN_DEMO \r\n'
Msg4 = "PRIVMSG #CN_DEMO :I'm TA \r\n"
IRCSocket.send(bytes(Msg1, encoding = 'utf-8'))
IRCSocket.send(bytes(Msg2, encoding = 'utf-8'))
IRCSocket.send(bytes(Msg3, encoding = 'utf-8'))
IRCSocket.send(bytes(Msg4, encoding = 'utf-8'))
inputs = [sys.stdin, IRCSocket]
while True:
	readable, writeable, exceptional = select.select(inputs,[],[])
	for read in readable:
		if read == sys.stdin:
			sendMsg = input()
			IRCSocket.send(bytes("PRIVMSG bot_b05902050 :" + sendMsg + '\r\n', encoding = 'utf-8'))
		elif read == IRCSocket:
			IRCMsg = IRCSocket.recv( 4096 ).decode()
			if IRCMsg == 'PING localhost :localhost':
				continue
			Splitstring = IRCMsg.split(' :')
			IRCMsg = Splitstring[-1:][0][:-2]
			print(IRCMsg)
	#print(IRCMsg)