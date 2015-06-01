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

class SimplePatch:


	@staticmethod
	def patch(input_name, output_name, patch_name):
		src = open(input_name, "r")
		if not src:
			print "Could not open source file for patch %s\n" % input_name
			return False

		dest = open(output_name, "w")
		if not dest:
			print "Could not open destination file for patch %s\n" % output_name
			src.close()
			return False

		patch = open(patch_name, "r")
		if not patch:
			print "Could not open patch file %s\n" % patch_name
			src.close()
			dest.close()
			return False

		try:
			CHUNK = re.compile('@@\s-(\d+)(?:,(\d*))?\s\+(\d+)(?:,(\d*))?\s@@')
			patch_line = patch.readline()
			curr_src_line = 1
			while patch_line:
				#print ">" + patch_line
				if patch_line[0:3] =="---" or patch_line[0:3] == "+++":
					#skip indicator line
					pass

				elif patch_line[0:2] == "@@":
					#start of chunk line
					m = CHUNK.match(patch_line)
					if m:
						src_start = int(m.group(1))
						src_length = 1
						if m.group(2):
							src_length = int(m.group(2))

						#Check for chunk length indicator. 
						#If it is 0 then src_range must be incremented by 1
						if src_length == 0:
							src_start +=1

						# Copy src -> dest upto line src_start
						#print "%d,%d" % (curr_src_line,src_start)
						for src_line in range(curr_src_line,src_start):
							s = src.readline()
							#print "copy %s" % s
							dest.write(s)
						curr_src_line = src_start

				elif patch_line[0] == " ":
					#similar line - copy to dest
					#print "copy"
					dest.write(src.readline())
					curr_src_line += 1

				elif patch_line[0] == "-":
					#print "remove"
					#remove src line
					src.readline()
					curr_src_line += 1

				elif patch_line[0] == '+':
					#print "add"
					#add line
					dest.write(patch_line[1:])
			
				patch_line = patch.readline()
			#Finished patch file, copy remainder of input to output
			src_line = src.readline()
			while src_line:
				dest.write(src_line)
				src_line = src.readline()
		finally:
			src.close()
			dest.close()
			patch.close()



