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

import os,sys,math,getopt
from utils import *
from director import *
from text import *

class GameArguments:

	def __init__(self):
		self.level = 1
		self.fullscreen = True
		self.show_menu = False



def main(argv):
	
	game_args = GameArguments()
	hardware_accelerate = True
	
	try:
		opts, args = getopt.getopt(argv, "l:fmh", ["level=", "fullscreen","menu", "hardwareaccel"])
		for opt, arg in opts:
			if opt in ("-l", "--level"):
				game_args.level = int(arg)
			if opt in ("-f", "--fullscreen"):
				game_args.fullscreen = True
			if opt in ("-m", "--menu"):
				game_args.show_menu = True
			if opt in ("-h", "--hardware"):
				hardware_accelerate = True
	except getopt.GetoptError:
        	sys.exit(2)

	print "Little endian %d" % mygame.is_little_endian(True)

	config = {}
	config['format'] = 8
	config['width'] = SCREEN_X
	config['height'] = SCREEN_Y
	config['depth'] = DEPTH
	config['paletteimage'] = PALETTE_IMG
	config['freq'] = FREQ
	if hardware_accelerate:
		config['hardware'] = True

	director = Director(game_args, config)
	director.play()
	exit(1);
	


# http://onlamp.com/pub/a/python/2005/12/15/profiling.html
# http://www.swig.org/

PROFILE=False

if __name__ == '__main__':
	if PROFILE:
		import hotshot
		prof = hotshot.Profile("hotshot_edi_stats")
		prof.runcall(main, sys.argv[1:])
		prof.close()
	
	main(sys.argv[1:])


#remove level load_units mixer hack


#http://www.parallelrealities.co.uk
