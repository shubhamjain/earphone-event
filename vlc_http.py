import requests
import urllib
import xml.etree.ElementTree as ET
import os

class vlc_http:

	SEEK_CUR = 1
	SEEK_BEGIN = 2
	
	port = 8080		# Port on which player interface exists
	sec_percentage = 0 	# Each second represents how much percentage of the media

	def __init__(self, port=8080):
		self.port = port

		# Check if VLC localhost page is accessible or not
		try:
			page = requests.get('http://localhost:'+str(self.port))
		except:
			raise Exception("There was a problem connecting with VLC localhost control. \
					Make sure that VLC is running and port address is correct.")
		self.set_sec_percentage()

	def get_attributes( self ):
		""" It parses the VLC status xml file and returns a dictionary of attributes. """
		page = requests.get('http://localhost:'+str(self.port)+'/requests/status.xml')
		
		attributes = {}
		et = ET.fromstring( page.text )
		
		for ele in et:
			# If element doesn't have sub elements.
			if len(ele) == 0:
				attributes[ ele.tag ] = ele.text
			else:
				attributes[ ele.tag ] = {}
				for subele in ele:
					if subele.tag == "category":
						subattr = attributes[ ele.tag ][ subele.get("name") ] = {}
						for _subele in subele:
							subattr[ _subele.get("name")] = _subele.text
					else:
						attributes[ ele.tag ][ subele.tag ] = subele.text

		return attributes

	def set_sec_percentage(self):
		""" Calculates and sets how much percentage of media each second represents for the seek() function. """
		attributes = self.get_attributes()

		media_length = int(attributes["length"])
		self.sec_percentage = 100 / media_length

	def send_command(self, command, val=None):
		""" Send commands to VLC http interface - seek, volume, pause/play etc .""" 
		
		if (val == None ):
			requests.get('http://localhost:'+str(self.port)+'/requests/status.xml?command=' + command )
		else:
			requests.get('http://localhost:'+str(self.port)+'/requests/status.xml?command=' + command + '&val=' + urllib.quote_plus(str(val)) )

##### COMMANDS

# Commands taking arguments.
	def seek(self, val, flag=SEEK_CUR):
		""" Seek the media to value given in seconds. By default, it seeks from current media position.
Additionaly, flag SEEK_BEGIN can be passed to seek from beginning position."""
		attributes = self.get_attributes()

		if( not("length" in attributes) ):
			raise Exception("No media being played for seek command to work.")

		if( flag == self.SEEK_CUR ):
			seek_offset = float(attributes["position"]) * int(attributes["length"])
		elif( flag == self.SEEK_BEGIN ):
			seek_offset = 0
		else:
			raise Exception("Unknown flag passed.")

		seek_val_sec = seek_offset + val

		seek_percentage = (seek_val_sec / int(attributes["length"])) * 100

		self.send_command("seek", str(seek_percentage) + "%")

	def set_volume(self, val):
		""" Sets the volume of VLC. The interface expects value between 0 and 512 while in the UI it is 0% to 200%. So a factor of 2.56 is used
to convert 0% to 200% to a scale of 0 to 512."""

		self.send_command("volume", 2.56 *  val)

	def play_file(self, in_file):
		""" Send the input file to be played. The in_file must be a valid playable resource."""

		if( not( os.path.isfile(infile) ) ):
			raise Exception("FileNotFound: The file " + infile + " does not exist.")
		else:
			self.send_command("in_file", "file://" + os.path.abspath(infile) )

# No-argument commands. 
	def play_pause(self):
		"""Toggle between play and pause."""

		self.send_command("pl_pause")

	def stop(self):
		"""Stops the player."""

		self.send_command("pl_stop")

	def fullscreen(self):
		""" Toggle fullscreen."""

		self.send_command("pl_stop")

	def next(self):
		""" Next media on the playlist. """

		self.send_command("pl_next")

	def previous(self):
		""" Previous media on the playlist. """

		self.send_command("pl_previous")
