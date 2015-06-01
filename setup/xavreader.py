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

import sys
import array
import binascii
import zlib
from decrypt import *
from xavindex import *
from struct import *

is_big_endian = False




class XavReader:

	def __init__(self, archive, destinations):
		self.archive = archive
		self.index = XavIndex()
		self.f = open(self.archive, "rb")
		self.destinations = destinations

	def close(self):
		self.f.close()

	def read_all(self):
		for fname in self.index.names():
			self.read(fname)


	def read(self, fname):
		offset, length = self.index.lookup(fname)
		d = Decryptor()
		decrypted = array('B')

		self.f.seek(offset)
		l=0
		byte = self.f.read(1)
		while byte != "" and l < length:
			#print binascii.hexlify(byte)
			b = unpack('B', byte)[0]
			r = d.decrypt(b)
			#print "%x" % r
			decrypted.append(r)
		        byte = self.f.read(1)
			l+=1

		#Throw away first 12 bytes - unused header
		for i in range(0,12):
			decrypted.pop(0)
		
		#If fname requires patching move to working
		#otherwise according to extension
		if fname in self.destinations["to_patch"]:
			output_name = self.destinations["working"] + fname
		else:
			extension = fname.split(".")[1]
			output_name = self.destinations[extension] + fname

		#Raw stream
		unpacked = zlib.decompress(decrypted, -15)
		with open(output_name, "wb") as out:
			out.write(unpacked)
		print "Extracted %s" % fname
		
	def decrypt_byte(self, byte):
		pass


