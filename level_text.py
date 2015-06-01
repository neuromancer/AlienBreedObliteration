"""	
	Written By:
 		Chris Humphreys
 		Email: < chris (--AT--) habitualcoder [--DOT--] com >
 
 	All python source code copyright Chris Humphreys 2010
	Level data, Obliteration name and some media copyright 
	Flash Jester Punk 2007
	Alien Breed name, concept and media copyright Team17 1992
 
	This file is part of alien breed obliteration wii edition
 
 	This program is free software; you can redistribute it and/or modify
 	it under the terms of the GNU General Public License as published by
 	the Free Software Foundation; either version 3 of the License, or
 	(at your option) any later version.
 
 	This program is distributed in the hope that it will be useful,
 	but WITHOUT ANY WARRANTY; without even the implied warranty of
 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 	GNU General Public License for more details.
 
 	You should have received a copy of the GNU General Public License
 	along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import re
from utils import *

class LevelTextLoader:

	def __init__(self, lev_filename):
		self.filename = get_config_pathname(lev_filename)
		self.__load_lev_text()
		
		
	def __load_lev_text(self): 
		MISSION = re.compile('.*^<MISSION text="([^"]*)">', re.M|re.S)
		
    		a = open(self.filename, "r")
		try:
			text = ""
			line = a.readline()
			while line:
				text += line
				print_debug(line,5)
				m = MISSION.match(text)
				if m:
					self.text = m.group(1)
	
				line = a.readline()
				
				if 'MAPTILEBITMAP' in line:
					break;
		finally:
			a.close() 

	def get_mission_text(self):
		return self.text
