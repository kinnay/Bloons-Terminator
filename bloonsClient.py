
"""
Copyright (C) 2015 Yannik Marchand
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY Yannik Marchand ""AS IS"" AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Yannik Marchand BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
The views and conclusions contained in the software and documentation 
are those of the authors and should not be interpreted as representing
official policies, either expressed or implied, of Yannik Marchand.
"""


import socket, struct
import zlib,base64

Version = "999999.09"

class Command:
	def __init__(self):
		self.client = client.gameClient

	def say(self,msg):
		self.client.sendChat(msg)

	def send(self,msg):
		self.client.send(msg)

class BLOONWAVE(Command):

	possibleBloons = ["GroupRed1","SpacedBlue1","GroupBlue1","SpacedPink1","GroupGreen1","SpacedBlack","GroupYellow1",
					  "SpaceWhite1","GroupPink1","SpaceLead1","GroupWhite1","SpaceZebra1","GroupBlack1",
					  "SpaceRainbow1","GroupZebra1","GroupRainbow1","GroupLead1","GroupCeremic1","Moab2","BFB1","ZOMG1"]

	bloonString = possibleBloons[0]
	for i in possibleBloons[1:]:
		bloonString+=", "+i
	
	def execute(self,args):
		if not args:
			self.help()
		else:
			bloon = self.getBloon(args[0])
			if bloon:
				self.send("ISentABloonWave,1,"+bloon+",0,0")
			else:
				self.say("Unknown bloon type, say /help bloonwave to get a list of bloon wave types.")

	def help(self):
		self.say("Makes me send a bloon wave at you.")
		self.say("Usage: /bloonwave BloonType")
		self.say("Where BloonType can be one of the following:")
		self.say(self.bloonString)
		self.say("Example: /bloonwave ZOMG1")

	#Case insensitive bloon type
	def getBloon(self,bloon):
		for i in self.possibleBloons:
			if bloon.lower() == i.lower():
				return i

#Some people write /bloon wave instead of /bloonwave for some reason
class BLOON(Command):
	def execute(self,args):
		if args[0] == "wave":
			cmd = BLOONWAVE()
		else:
			cmd = NotFound()
		cmd.execute(args[1:])

	def help(self):
		NotFound().help()
		
class CONTACT(Command):
	def execute(self,args):
		self.say("Email: bloonsterminator@airmail.cc")
		self.say("Source code: https://github.com/Kinnay/Bloons-Terminator")

	def help(self):
		self.say("Shows my contact information.")

class DISCONNECT(Command):
	def execute(self,args):
		print "Disconnect"
		self.client.running = False

	def help(self):
		self.say("Makes me disconnect. You\"ll receive a win by default.")

class SAY(Command):
	def execute(self,args):
		if not args:
			self.help()
		else:
			self.say(" ".join(args))

	def help(self):
		self.say("Makes me say something in the chat.")
		self.say("Usage: /say <message>")
		self.say("Example: /say hello")

class SETLIVES(Command):
	def execute(self,args):
		if not args:
			self.help()
		else:
			try: self.client.lives = int(args[0])
			except ValueError:
				self.say(args[0]+" is not a valid number")

	def help(self):
		self.say("Change my amount of lives.")
		self.say("Usage: /setlives <number>")
		self.say("Example: /setlives 99")

class STARTROUND(Command):
	def execute(self,args):
		self.send("ImReadyToStartARound")

	def help(self):
		self.say("Wait until the end of the round and start the next round.")

class SURRENDER(Command):
	def execute(self,args):
		self.send("ISurrender")
		self.client.running = False

	def help(self):
		self.say("Makes me surrender. You\"ll receive a win.")

class HELP(Command):
	def execute(self,args):
		if not args:
			self.sendGeneralHelp()
		else:
			cmd = getCommand(args[0])
			cmd.help()

	def sendGeneralHelp(self):
		self.say("/disconnect /surrender /startround /bloonwave /setlives /say /contact")
		self.say("Say /help <command> for a more detailed explanation of the command")
		self.say("Example: /help startround")

	def help(self):
		self.say("Prints a list of all available commands.")
		self.say("Can also be used to get information about a command.")

class NotFound(Command):
	def execute(self,args):
		self.say("Command not found. Say /help for a list of available commands.")

	def help(self):
		self.execute([])

def getCommand(cmd):
	if cmd.strip("/").upper() in globals():
		return globals()[cmd.strip("/").upper()]()
	return NotFound()

class Client:
	def __init__(self,server,port):
		self.server = server
		self.port = port
		self.socket = socket.socket()
		self.running = True

	def connect(self):
		self.socket.connect((self.server,self.port))

	def start(self):
		self.started()
		while self.running:
			for i in self.socket.recv(1024).split("\n"):
				split = i.split(",")
				self.receive(split[0],split[1:])
		self.socket.close()

	def started(self):
		pass

	def receive(self,msg):
		pass

	def send(self,msg):
		self.socket.send(msg+"\n")

class GameClient(Client):

	round = 0
	lives = 150
	chatStarted = 0
	towers = []
	
	def started(self):
		self.send("FindMyGame,"+client.battleId+",0")
		self.sync = "1.0"

	def sendChat(self,msg):
		length = struct.pack(">H",len(msg))
		print "Terminator> "+msg
		self.send("RelayMsg,SentChatMsg,"+base64.encodestring(zlib.compress(length+msg)).replace("\n",""))

	def recvChat(self,msg):
		print "Opponent> "+msg
		if msg.startswith("/"):
			message = msg.split(" ")
			cmd = message[0]
			args = message[1:]
			command = getCommand(cmd)
			command.execute(args)
		#This is a common mistake
		elif msg in ["help","contact","disconnect","surrender","startround","bloonwave","setlives","say"]:
			self.sendChat("Commands start with a /. Did you mean /"+msg+" ?")

	def chatStart(self):
		if not self.chatStarted:
			print "Game started"
			self.sendChat("Hello, I\"m the Bloons Terminator")
			self.sendChat("You can command me through the chat")
			self.sendChat("Say /help for a list of commands")
			self.chatStarted = 1

	def receive(self,msg,args):
		if msg == "GimmeUrPlayerInfo":
			self.send("HeresMyPlayerInfo,"+client.getPlayerInfo())
		elif msg == "FoundYourGame":
			print "Found your game"
			print args
		elif msg == "OpponentReadyStatus":
			print "Opponent is ready"
			self.send("MyReadyToPlayStatus,true")
		elif msg == "OpponentHasLoaded":
			self.send("MyGameIsLoaded")
			self.chatStart()
		elif msg == "OpponentRequestsSync":
			self.send("HeresMySyncData,"+self.sync+","+str(self.lives))
			self.send("GimmeOpponentSyncData")
		elif msg == "OpponentRequestsMyTowerLoadout":
			#When the opponent snoops the tower loadout
			#he'll see 4 monkey buccaneers
			print "Opponent requests tower loadout"
			self.send("IChangedMyTowerLoadout,8:8:8:8")
		elif msg == "OpponentSyncRetrieved":
			self.sync = args[0]
		elif msg == "ServerStartingARound":
			self.round+=1
			print "Round "+str(self.round)+" started"
		elif msg == "RelayMsg":
			if args[0] == "SentMousePos":
				self.send("RelayMsg,SentMousePos,400,400")
			elif args[0] == "SentChatMsg":
				self.recvChat(zlib.decompress(base64.decodestring(args[1]))[2:])
		elif msg == "OpponentSurrendered":
			print "Opponent surrendered"
		elif msg == "OpponentChangedTowerLoadout":
			#The tower loadout of the opponent
			print "Opponent Towers: "+args[0]
		elif msg == "OpponentDisconnected":
			print "Opponent disconnected"
			self.running = False
		elif msg == "OpponentDied":
			print "Opponent died"
			self.send("ILived")

class MenuClient(Client):
	def started(self):
		print "Connecting..."
		self.send("Hello,"+Version)
		#self.say("FindMeAQuickBattle",None,0)
		self.say("FindMyCustomBattle","342098105")

	def say(self,msg,p2,p3=-1):
		if p2 == None:
			p2 = ""
		self.send(msg+","+Version+","+p2+","+str(p3))

	def receive(self,msg,args):
		if msg == "GimmeUrPlayerInfo":
			self.send("HeresMyPlayerInfo,"+self.getPlayerInfo())
		elif msg == "FindingYouAMatch":
			print "Finding match..."
		elif msg == "FoundYouAGame":
			print "Found game, connecting..."
			self.battleId = args[2]
			print args
			self.connectGame(args[0],int(args[1]))
			#args[0] is the server address, args[1] the port

	def connectGame(self,server,port):
		self.gameClient = GameClient(server,port)
		self.gameClient.connect()
		self.gameClient.start()
		self.running = False

	def getPlayerInfo(self):
		#Connect with an account that doesn't exist
		id = "123458" #nkid of the imaginary account
		name = "The Bloons Terminator" #username
		battleScore = "100000"
		_71 = "0"
		_2Q = "http://www.mariowiki.com/images/1/17/MP9_Select_Kamek.png" #The profile picture
		return id+","+name+","+battleScore+","+_71+","+_2Q

client = MenuClient("battlesmain.ninjakiwi.com",4480)
client.connect()
client.start()
