
import string
import socket
import struct
import base64
import zlib
import sys


VERSION = "999999.09"

NKID = "123458"
NAME = "The Bloons Terminator"
SCORE = "100000"
PROFILE = "http://www.mariowiki.com/images/1/17/MP9_Select_Kamek.png"


def is_numeric(s):
	return all(c in string.digits for c in s)


class Command:
	def __init__(self, client):
		self.client = client

	def say(self, msg):
		self.client.chat(msg)

	def call(self, *args):
		self.client.call(*args)
		
		
class UNKNOWN(Command):
	def execute(self, args):
		self.say("Command not found. Say /help for a list of available commands.")

	def help(self):
		self.execute([])


good_luck = False

class BLOONWAVE(Command):
	bloon_table = (
		("Red", "GroupRed1"),
		("BlueSpaced", "SpacedBlue1"),
		("BlueGrouped", "GroupBlue1"),
		("Green", "GroupGreen1"),
		("Yellow", "GroupYellow1"),
		("PinkSpaced", "SpacedPink1"),
		("PinkGrouped", "GroupPink1"),
		("BlackSpaced", "SpacedBlack"),
		("BlackGrouped", "GroupBlack1"),
		("WhiteSpaced", "SpaceWhite1"),
		("WhiteGrouped", "GroupWhite1"),
		("LeadSpaced", "SpaceLead1"),
		("LeadGrouped", "GroupLead1"),
		("ZebraSpaced", "SpaceZebra1"),
		("ZebraGrouped", "GroupZebra1"),
		("RainbowSpaced", "SpaceRainbow1"),
		("RainbowGrouped", "GroupRainbow1"),
		("Ceramic", "SpaceCerem1"),
		("MOAB", "Moab2"),
		("BFB", "BFB1"),
		("ZOMG", "ZOMG1")
	)
	
	def execute(self, args):
		global good_luck
		
		if not args:
			self.help()
		else:
			bloon = self.find(args[0])
			if bloon:
				if bloon == "ZOMG1" and not good_luck:
					good_luck = True
					self.say("Good luck!")
				self.call("ISentABloonWave", "1", bloon, "0", "0")
			else:
				self.say("Unknown bloon type, say /help bloonwave to get a list of bloon types.")

	def help(self):
		bloon_list = self.build_list()
		self.say("Makes me send a bloon wave at you.")
		self.say("Usage: /bloonwave BloonType")
		self.say("Where BloonType can be one of the following:")
		self.say(bloon_list)
		self.say("Example: /bloonwave ZOMG")

	def find(self, type):
		for key, value in self.bloon_table:
			if key.lower() == type.lower():
				return value
				
	def build_list(self):
		return ", ".join(x[0] for x in self.bloon_table)
		

class BLOON(Command):
	def execute(self, args):
		if args[0] == "wave":
			self.say("/bloon wave is not a valid command. You probably meant /bloonwave.")
		else:
			UNKNOWN(self.client).execute()

	def help(self):
		UNKNOWN(self.client).execute()

		
class CONTACT(Command):
	def execute(self, args):
		self.say("Email: bloonsterminator@airmail.cc")
		self.say("Source code: https://github.com/Kinnay/Bloons-Terminator")

	def help(self):
		self.say("Shows my contact information.")


class DISCONNECT(Command):
	def execute(self, args):
		print("Disconnect")
		self.client.close()

	def help(self):
		self.say("Makes me disconnect. You'll receive a win by default.")


class SAY(Command):
	def execute(self, args):
		if not args:
			self.help()
		else:
			self.say(" ".join(args))

	def help(self):
		self.say("Makes me say something in the chat.")
		self.say("Usage: /say <message>")
		self.say("Example: /say hello")


class SETLIVES(Command):
	def execute(self, args):
		if not args:
			self.help()
		else:
			if all(c in string.digits for c in args[0]):
				lives = int(args[0])
				lives = min(lives, 999999)
				self.client.lives = lives
			else:
				self.say("%s is not a valid number" %args[0])

	def help(self):
		self.say("Changes my number of lives.")
		self.say("Usage: /setlives <number>")
		self.say("Example: /setlives 99")


class STARTROUND(Command):
	def execute(self, args):
		self.call("ImReadyToStartARound")

	def help(self):
		self.say("Waits until the end of the round and starts the next round.")


class SURRENDER(Command):
	def execute(self, args):
		self.call("ISurrender")
		self.client.close()

	def help(self):
		self.say("Makes me surrender. You'll receive a win.")


class HELP(Command):
	def execute(self, args):
		if not args:
			self.send_general_help()
		else:
			cmd = get_command(self.client, args[0])
			cmd.help()

	def send_general_help(self):
		self.say("/disconnect /surrender /startround /bloonwave /setlives /say /contact")
		self.say("Say /help <command> for a more detailed explanation of the command")
		self.say("Example: /help startround")

	def help(self):
		self.say("Prints a list of all available commands.")
		self.say("Can also be used to get information about a command.")


COMMAND_LIST = [
	"bloonwave", "contact", "disconnect", "say",
	"setlives", "startround", "surrender", "help"
]
		
COMMAND_TABLE = {
	"bloonwave": BLOONWAVE,
	"bloon": BLOON,
	"contact": CONTACT,
	"disconnect": DISCONNECT,
	"say": SAY,
	"setlives": SETLIVES,
	"startround": STARTROUND,
	"surrender": SURRENDER,
	"help": HELP
}

def get_command(client, cmd):
	if cmd.lower() in COMMAND_TABLE:
		return COMMAND_TABLE[cmd.lower()](client)
	return UNKNOWN(client)
	
	
TOWER_IDS = [
	"BananaFarm", "BombTower", "BoomerangThrower", "DartMonkey",
	"DartlingGun", "GlueGunner", "IceTower", "MonkeyAce",
	"MonkeyApprentice", "MonkeyBuccaneer", "MonkeyVillage",
	"MortarTower", "NinjaMonkey", "SniperMonkey", "SpikeFactory",
	"SuperMonkey", "TackTower"
]

TOWER_NAMES = [
	"banana farms", "bomb towers", "boomerang throwers", "dart monkeys",
	"dartling guns", "glue gunners", "ice towers", "monkey aces",
	"monkey apprentices", "monkey buccaneers", "monkey villages",
	"mortar towers", "ninja monkeys", "sniper monkeys", "spike factories",
	"super monkeys", "tack towers"
]

TOWER_THRESHOLD = [
	5, 12, 12, 12, 5, 8, 8, 5,
	12, 5, 5, 5, 12, 12, 10, 10,
	10
]

class Tracker:
	def __init__(self, client):
		self.client = client
		self.towers = [0] * len(TOWER_IDS)
		self.printed = [False] * len(TOWER_IDS)
		
		self.question = None
		self.surrender = 0
		self.prev_lives = 150
		
	def handle(self, msg):
		if self.question and msg.lower() == "yes":
			self.client.chat("Then please say /%s" %self.question)
		elif msg.lower() == "hacker":
			self.client.chat("Don't worry, you can win this game if you're smart")
		self.question = None
		
	def set_lives(self, lives):
		if self.prev_lives >= 16 and lives < 16:
			self.client.chat("Be careful! You're almost dead.")
		self.prev_lives = lives
		
	def hover(self, x, y):
		if x >= 365 and x <= 380 and y >= 577 and y <= 596:
			self.surrender += 1
			if self.surrender == 5:
				self.client.chat("Please don't surrender")
				self.client.chat("You can win this game if you're smart")
		else:
			self.surrender = 0
			
	def build(self, tower):
		if tower in TOWER_IDS:
			id = TOWER_IDS.index(tower)
			self.towers[id] += 1
			if self.towers[id] == TOWER_THRESHOLD[id] and not self.printed[id]:
				self.client.chat("Wow so many %s" %TOWER_NAMES[id])
				self.printed[id] = True
		
	def sell(self, tower):
		if tower in TOWER_IDS:
			id = TOWER_IDS.index(tower)
			self.towers[id] -= 1


class Client:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.socket = socket.socket()
		self.running = True
		
	def connect(self):
		print("Connecting to %s:%i" %(self.host, self.port))
		self.socket.connect((self.host, self.port))
		
	def close(self):
		self.running = False
		
	def start(self, *args):
		self.initialize(*args)
		
		buffer = ""
		while self.running:
			data = self.socket.recv(1024)
			if not data:
				return
				
			buffer += data.decode()
			while "\n" in buffer:
				line, buffer = buffer.split("\n", 1)
				parts = line.split(",")
				self.handle(parts[0], parts[1:])
				
		self.socket.close()
		
	def initialize(self): pass
	def handle(self, msg, args): pass
	
	def send(self, msg):
		self.socket.sendall(msg.encode() + b"\n")
		
	def call(self, cmd, *args):
		param = [cmd, *args]
		self.send(",".join(param))


class Tower:
	def __init__(self, type):
		self.type = type
		self.left = 0
		self.right = 0
		
	def upgrade(self, mode):
		if mode == 0:
			self.left += 1
		else:
			self.right += 1
		
		
class GameClient(Client):

	round = 0
	lives = 150
	opponent = 150
	welcome = False
	
	def initialize(self, battle_id):
		self.tracker = Tracker(self)
		self.towers = {}
		
		self.call("FindMyGame", battle_id, "0")		
		self.sync = "1.0"
		
	def chat(self, msg):
		print("<Terminator> %s" %msg)
		length = struct.pack(">H", len(msg))
		buffer = zlib.compress(length + msg.encode())
		b64 = base64.encodebytes(buffer).decode().replace("\n", "")
		
		self.call("RelayMsg", "SentChatMsg", b64)
		
	def handle(self, msg, args):
		if msg == "GimmeUrPlayerInfo":
			self.call("HeresMyPlayerInfo", NKID, NAME, SCORE, "0", PROFILE)
			
		elif msg == "FindingYourGame":
			pass
			
		elif msg == "FoundYourGame":
			print()
			print("Opponent name:", args[1])
			print("Battle score:", args[2])
			print("Profile:", args[4])
			print("Wins:", args[8])
			print("Losses:", args[9])
			print()
			
		elif msg == "OpponentReadyStatus":
			print("Opponent is ready\n")
			self.call("MyReadyToPlayStatus", "true")
			
		elif msg == "OpponentHasLoaded":
			self.call("MyGameIsLoaded")
			self.send_welcome()
			
		elif msg == "OpponentRequestsSync":
			self.call("HeresMySyncData", self.sync, str(self.lives))
			self.call("GimmeOpponentSyncData")
			
		elif msg == "OpponentRequestsMyTowerLoadout":
			#When the opponent snoops the tower loadout
			#he'll see 5 monkey buccaneers
			print("Opponent requests tower loadout")
			self.call("IChangedMyTowerLoadout", "8:8:8:8:8")
		
		elif msg == "OpponentSyncRetrieved":
			self.sync = args[0]
			
			lives = int(args[1])
			if lives != self.opponent:
				print("Opponent lives changed to %i" %lives)
				self.opponent = lives
				self.tracker.set_lives(lives)
		
		elif msg == "ServerStartingARound":
			self.round += 1
			print("Round %i started" %self.round)
		
		elif msg == "RelayMsg":
			if args[0] == "SentMousePos":
				self.call("RelayMsg", "SentMousePos", "400", "400")
				
				x = int(args[1])
				y = int(args[2])
				self.tracker.hover(x, y)
			
			elif args[0] == "SentChatMsg":
				text = zlib.decompress(base64.decodebytes(args[1].encode()))[2:]
				self.handle_chat(text.decode())
				
		elif msg == "OpponentBuiltATower":
			self.towers[args[0]] = Tower(args[1])
			print("Opponent built %s at (%s, %s)" %(args[1], args[2], args[3]))
			
			self.tracker.build(args[1])
			
		elif msg == "OpponentUpgradedATower":
			tower = self.towers[args[0]]
			tower.upgrade(int(args[1]))
			print("Opponent upgraded %s to %i/%i" %(tower.type, tower.left, tower.right))
			
		elif msg == "OpponentSoldATower":
			tower = self.towers[args[0]]
			print("Opponent sold %s" %tower.type)
			self.tracker.sell(tower.type)
			
		elif msg == "OpponentTowerTargetChanged":
			tower = self.towers[args[0]]
			target = ["first", "last", "strong", "close"][int(args[1])]
			print("Opponent changed %s target to '%s'" %(tower.type, target))
			
		elif msg == "OpponentChangedTargetReticle":
			tower = self.towers[args[0]]
			print("Opponent changed %s target to (%s, %s)" %(tower.type, args[1], args[2]))
			
		elif msg == "OpponentChangedAcePath":
			tower = self.towers[args[0]]
			print("Opponent changed %s path to %s" %(tower.type, args[1]))
			
		elif msg == "OpponentUsedAnAbility":
			tower = self.towers[args[0]]
			print("Opponent used %s on %s" %(args[1], tower.type))
			
		elif msg == "OpponentSentABloonWave":
			pass
		
		elif msg == "OpponentChangedTowerLoadout":
			#The tower loadout of the opponent
			print("Opponent Towers: "+args[0])
			
		elif msg == "OpponentChangedBattleOptions":
			mode = "Assault" if args[1] == "0" else "Defend"
			print("Battle options: %s (%s)" %(args[0], mode))
			
		elif msg == "OpponentSurrendered":
			print("Opponent surrendered")
		
		elif msg == "OpponentDisconnected":
			print("Opponent disconnected")
			self.close()
		
		elif msg == "OpponentDied":
			print("Opponent died")
			self.send("ILived")
			
		else:
			print("Unknown message: %s %s" %(msg, args))

	def handle_chat(self, msg):
		print("<Opponent>", msg)
		
		parts = msg.strip().split()
		
		cmd = parts[0].lower()
		if cmd.startswith("/"):
			command = get_command(self, cmd[1:])
			command.execute(parts[1:])
		
		#This is a common mistake
		elif cmd in COMMAND_LIST:
			self.chat("Commands start with a /. Did you mean /%s ?" %cmd)
			self.tracker.question = cmd
			
		else:
			self.tracker.handle(msg.strip())

	def send_welcome(self):
		if not self.welcome:
			print("Game started")
			self.chat("Hello, I'm the Bloons Terminator")
			self.chat("You can command me through the chat")
			self.chat("Say /help for a list of commands")
			self.welcome = True


class MenuClient(Client):
	def initialize(self):
		self.call("Hello", VERSION)
		if len(sys.argv) > 1:
			self.call("FindMyCustomBattle", VERSION, sys.argv[1], "-1")
		else:
			self.call("FindMeAQuickBattle", VERSION, "null", "0")

	def handle(self, msg, args):
		if msg == "GimmeUrPlayerInfo":
			print("Sending player info...")
			self.call("HeresMyPlayerInfo", NKID, NAME, SCORE, "0", PROFILE)
		elif msg == "FindingYouAMatch":
			print("Finding match...")
		elif msg == "CouldntFindYourCustomBattle":
			print("Custom battle not found")
			self.close()
		elif msg == "FoundYouAGame":
			print("Found game, connecting...")
			client = GameClient(args[0], int(args[1]))
			client.connect()
			client.start(args[2])
			self.close()
		else:
			print("Unknown message: %s %s" %(msg, args))

client = MenuClient("battlesmain.ninjakiwi.com", 4480)
client.connect()
client.start()
