import time
from Interface import Interface
from P2PPlatform import Network


######################## MAIN PROGRAM BELOW ##################################
myIP = myInterface.getOwnIP()
print ("Detected IP: " + myIP)
print("I'll need your port.")
myPort = myInterface.getPort()



# Initialize a network
myNetwork = Network(myIP, myPort)


#add network reference to interface
myInterface.network = myNetwork

myInterface.run()
