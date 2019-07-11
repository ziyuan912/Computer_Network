import socket # Include library
import requests
import sys
import select
from bs4 import BeautifulSoup
from random import randint


horoscope = ['Capricorn', 'Aquarius', 'Pisces', 'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius']
IRCSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
IRCSocket.connect( ( '127.0.0.1', 6667 ) )
Msg1 = 'NICK bot_b05902050 \r\n'
Msg2 = 'USER b05902050 \r\n'
Msg3 = 'JOIN #CN_DEMO \r\n'
Msg4 = "PRIVMSG #CN_DEMO :I'm b05902050 \r\n"

IRCSocket.send(bytes(Msg1, encoding = 'utf-8'))
IRCSocket.send(bytes(Msg2, encoding = 'utf-8'))
IRCSocket.send(bytes(Msg3, encoding = 'utf-8'))
IRCSocket.send(bytes(Msg4, encoding = 'utf-8'))
while True:
	IRCMsg = IRCSocket.recv( 4096 ).decode()
	if IRCMsg.split(' ')[0] == 'PING':
		continue
	Splitstring = IRCMsg.split(':')
	name = Splitstring[1]
	name = name.split('!')[0]
	#print(name)
	IRCMsg = Splitstring[-1:][0][:-2]
	print(IRCMsg)
	if IRCMsg in horoscope:
		IRCSocket.send(bytes("PRIVMSG " + name + " :今日運勢 想不到吧 \r\n", encoding = 'utf-8'))
	if IRCMsg == '!guess':
		IRCSocket.send(bytes("PRIVMSG " + name + " :猜一個1~10之間的數字！ \r\n", encoding = 'utf-8'))
		ans = randint(1,10)
		record = [0 for i in range(10)]
		while True:
			IRCMsg = IRCSocket.recv( 4096 ).decode()
			Splitstring = IRCMsg.split(':')
			IRCMsg = Splitstring[-1:][0][:-2]
			if IRCMsg.isnumeric():
				guess = int(IRCMsg)
				if 1 <= guess <= 10:
					if guess == ans:
						IRCSocket.send(bytes("PRIVMSG " + name + " :正確答案為" + str(ans) + "! 恭喜猜中\r\n", encoding = 'utf-8'))
						break
					elif guess < ans:
						msg = "大於" + str(guess) + "!"
					else:
						msg = "小於" + str(guess) + "!"
					if record[guess - 1] == 1:
						IRCSocket.send(bytes("PRIVMSG " + name + " :你猜過" + str(guess) + "了=_= " + msg + " \r\n", encoding = 'utf-8'))
					else:
						IRCSocket.send(bytes("PRIVMSG " + name + " :" + msg + " \r\n", encoding = 'utf-8'))
						record[guess - 1] = 1
	if IRCMsg[:6] == '!song ':
		searchMsg = IRCMsg[6:]
		url = "https://www.youtube.com/results?search_query=" + searchMsg
		request = requests.get(url)
		soup = BeautifulSoup(request.content, "html.parser")
		song = soup.find("div", {"class": "yt-lockup-video"})
		data = song.select("a[rel='spf-prefetch']")
		IRCSocket.send(bytes("PRIVMSG " + name + " :https://www.youtube.com" + data[0].get("href") + " \r\n", encoding = 'utf-8'))
	if IRCMsg == '!chat':
		print("========" + name + "想跟你聯繫========")
		inputs = [sys.stdin, IRCSocket]
		stop = 0
		while True:
			if stop:
				print("========" + name + "已離開聊天室========")
				break
			readable, writeable, exceptional = select.select(inputs,[],[])
			for read in readable:
				if read == sys.stdin:
					sendMsg = input()
					IRCSocket.send(bytes("PRIVMSG " + name + " :" + sendMsg + '\r\n', encoding = 'utf-8'))
				elif read == IRCSocket:
					IRCMsg = IRCSocket.recv( 4096 ).decode()
					Splitstring = IRCMsg.split(':')
					IRCMsg = Splitstring[-1:][0][:-2]
					print(name + " :",IRCMsg)
					if IRCMsg == "!bye":
						stop = 1
						break


