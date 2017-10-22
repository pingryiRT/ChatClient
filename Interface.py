from P2PPlatform import Network
from P2PPlatform import Peer
from P2PPlatform import Message
import socket

def getOwnIP():
	"""
	Attempts to autodetect the user's LAN IP address, and falls back to manual
	entry when autodetect fails.

	See http://stackoverflow.com/questions/166506 for details.
	"""

	# Send a packet to google who will reply to our IP
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('google.com', 53))
	IP = s.getsockname()[0]

	# Make sure the detected IP looks valid, and if not fallback
	while not validateIP(IP):
		IP = raw_input("Please enter a valid IP address: ")

	return IP


def validateIP(IP):
	"""
	Validates an IP address before joining network
	"""

	sections = IP.split(".") #Creating sections list with IP address split up each period

	if len(sections) != 4: #Check for 3 periods
		return False

	for section in sections:
		if not section.isdigit(): #Making sure all contents are ints
			return False
		section = int(section)
		if section < 0 or section > 255: #validate range of the number
			return False

	if sections[0] == "127": #not loop-back address
		return False

	return True



def getPort():
	"""
	Interactively determine a port. Proposes default, but allows overriding.
	"""

	DEFAULT = 12345

	port = raw_input("Default port: {}. Enter to continue or type an alternate. ".format(DEFAULT))

	if port == "":
		return DEFAULT

	return int(port)



class Interface(object):

	def __init__(self, network):
		self.network = network
		self.network.alerters.append(self.netMessage)



	def run(self):
		"""
		The main loop in an operating interface. Prompts the user for input (command or message) and processes that input.
		"""

		command = None
		while command != "/exit":
			command = raw_input("Please enter your message, or '/connect', '/approve', '/name', '/addPort', '/exit': ")
			if command == "/connect":
				self.connector()
			elif command == "/approve":
				self.approver()
			elif command == "/name":
				self.name()
			elif command == "/addPort":
				self.addPort()
			else:
				self.network.sender(command)



	########## NEEDED FOR NETWORK FUNCTION ##########

	def connector(self):
		"""
		Prompts user for data to connect to another peer, and establishes the connection.
		Warning. Uses global variable myNetwork.
		"""
		peerIP = raw_input("Enter it your peer's IP address: ")
		if validateIP(peerIP):
			peerPort = getPort()
			self.network.connect(peerIP, peerPort)
		else:
			print("Invalid IP.")

	def netMessage(self, message):
		"""
		Callback function that the network will call to alert about new messages.
		Just prints the received message to the screen.
		"""
		print("From {0!s}: {1!s}".format(message.sender, message.contents))

	def approver(self):
		"""
		Moves a peer that has connected to this network instance from the
		unconfirmedList to peerList, where messages can be sent and received.

		Warning. Uses global variable myNetwork.
		"""

		i = 0
		while i < len(self.network.unconfirmedList):
			peer = self.network.unconfirmedList[i]
			add = raw_input("y/n to add: " + str(peer) + " ").lower()
			if add == "y":
				self.network.approve(peer)
			i += 1

############## END OF NETWORK FUNCTION ###########
######### ADDITIONAL ########


	def name(self):
		"""
		Gives a peer a unique name identifier (determined by the input of the user)
		The name will be accessible through peer.name
		"""
		for peers in list(self.network.peerList):
			print(str(peers) + " " + str(self.network.peerList.index(peers)))
		index = int(raw_input("Please enter the index of the peer you would like to name: \n"))
		name = raw_input("Please enter the name of the peer you would like to name: \n")
		self.network.peerList[index].name = name


	def addPort(self):
		"""
		Adds a server port to a peer. The peer which has the port added, and the port number to be added is determined with user input
		"""
		for peers in list(self.network.peerList):
			print(str(peers) + " " + str(self.network.peerList.index(peers)))
		index = int(raw_input("Please enter the index of the peer you would like to add a port to: \n"))
		port = int(raw_input("Please enter the port for the peer: \n"))
		self.network.peerList[index].port = port

	#### END OF ADDITIONAL #######


######################## MAIN PROGRAM BELOW ##################################

# Initialize a network
myIP = getOwnIP()
print ("Detected IP: " + myIP)
print("I'll need your port.")
myPort = getPort()

myNetwork = Network(myIP, myPort)

# Create a user interface to handle future network interactions
myInterface = Interface(myNetwork)

# Prompt for an initial connection
adamNode = raw_input("Would you like to start a new network? y/N: ")
if adamNode == "" or adamNode[0].lower()!= "y":
	myInterface.connector()

# Activate the interface. This call is blocking until the interface terminates.
myInterface.run()

# Close down the network
myNetwork.shutdown()
