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

import array, mygame


class LevelDataLoader:

	def __init__(self, level):
		self.level_width = level.level_width
		self.level_height = level.level_height
		
	

	def load_level_tile_data(self, fname):
		
		level_map_lower = []
		level_map_upper = []
		
		fileobj = open(fname, mode='rb')
		try:
			#discard leading word which is padding(?)
			pos = 4
			for y in range(0,self.level_height):
				a = array.array('H', range(0,self.level_width ))
				level_map_lower.append(a)
				b = array.array('H', range(0,self.level_width ))
				level_map_upper.append(b)
				#blank upper as not all bytes are set in the file
				for x in range(0,self.level_width):
					b[x] = 0

				for x in range(0,self.level_width):
					word =read_at2(fileobj, pos, 1)
					
					if word > 0x7fff:
						#upper level tile def (for previous tile) within lower level tile data
						level_map_upper[y][x-1] = word - 0x8000
						#advance file pointer
						pos+=2
						#re-read lower level tile which always follows upper (if present)
						word = read_at2(fileobj, pos, 1)
					
					level_map_lower[y][x] = word
						
					#advance file pointer
					pos+=2	

		finally:
			fileobj.close()


		return level_map_lower, level_map_upper




#http://www.python.org/search/hypermail/python-1993/0393.html
#http://www.python.org/doc/2.5.2/lib/module-array.html

def read_at2(file, pos, size):
	file.seek(pos)
	a = array.array('H')
	a.read(file, 1)
	
	#print a.itemsize
	if mygame.is_big_endian():
		#need to swap the byte order if big endian (e.g. WII)
		a.byteswap()

	Integer = a[0]
	return Integer
