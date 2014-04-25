import os
import xively

class XivelyConnection:
	def __init__(self, apiKey, feedId):
		self.api = xively.XivelyAPIClient(apiKey)
		self.feedId = feedId
		self.refreshFeed()
		
	def refreshFeed(self):
		try:
			self.feed = self.api.feeds.get(self.feedId)
			return True
		except:
			return False
		
	def getChannelList(self):
		if self.refreshFeed():
			channels = []
			for channel in self.feed.datastreams:
				channels.append(channel.id)
			return channels
		else:
			return None
			
	def deleteChannel(self, channel):
		if self.refreshFeed():
			self.feed.datastreams.delete(channel)

	def getValue(self, channel):
		try:
			datastream = self.feed.datastreams.get(channel)
			return datastream.current_value
		except:
			print("Can't get value")
			return None

	def updateDatastream(self, channel, value):
		try:
			datastream = self.feed.datastreams.get(channel)
			datastream.current_value = value
			datastream.update()
			return True
		except:
			return False