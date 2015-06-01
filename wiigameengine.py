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
 
from utils import *
from director import *


class GameArguments:
	
	def __init__(self):
		self.level = 1
		self.fullscreen = True
		self.show_menu = True


def main():
	
	game_args = GameArguments()
	
	config = {}
	config['format'] = 16
	config['width'] = SCREEN_X
	config['height'] = SCREEN_Y
	config['depth'] = DEPTH	
	config['freq'] = 32000
	config['paletteimage'] = PALETTE_IMG
	
	director = Director(game_args, config)
	director.play()
	exit(1);
	
if __name__ == '__main__':
	main()
