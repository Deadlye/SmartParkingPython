import os
from XivelyConnect import XivelyConnection
import time

FEED_ID = None
API_KEY = None

def writeKeys():
	try:
		file = open("Keys.txt", "r")
		global FEED_ID
		FEED_ID = file.readline()
		
		global API_KEY
		API_KEY = file.readline()
		
		return True
	except:
		return False

#Need at least 5 sec between 2 getValue on the same channel (otherwise doesn't do the request)
if __name__ == "__main__":
	if writeKeys():
		xivConnect = XivelyConnection(API_KEY, FEED_ID)
		
		timerParkingSpot = {}
		
		while True:	
			datastreams = xivConnect.getChannelList()	
			
			if not datastreams == None:
				for datastream in datastreams:
					val = xivConnect.getValue(datastream)
					#if a parking spot is booked, we set when the parking spot will be taken
					if val == "Booked":
						if not datastream in timerParkingSpot:
							timerParkingSpot[datastream] = time.time() + 20	#set when the parking spot will be taken
						else:
							if timerParkingSpot[datastream] < time.time():
								xivConnect.updateDatastream(datastream, "Taken")
								timerParkingSpot[datastream] = time.time() + 30 #set when the parking spot will be free
					
					#if a parking spot is taken, we set when the parking spot will be free again
					elif val == "Taken":
						if timerParkingSpot[datastream] < time.time():
							xivConnect.updateDatastream(datastream, "Free")
							del timerParkingSpot[datastream]		
				
				time.sleep(10) #Otherwise too much request
			else:
				print("Can't get the channel list")
	else:
		print("Can't write keys")