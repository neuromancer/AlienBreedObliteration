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


from pathfinder import *
from collisiontilemap import *


class ManhattanHeuristic(Heuristic):
	def __init__(self, min_cost):
		self.min_cost = min_cost
		
	def get_cost(self, x, y, tx, ty):
		hcost = self.min_cost * (abs(x-tx) + abs(y-ty));
		#print "H Cost %d" % hcost
		return hcost


class TileMapPathMap(PathMap):
	def __init__(self, level):
		self.tile_data = CollisionTileData(level)		
	
	def get_width(self):
		return len(self.tile_data.tile_map[0])
	
	def get_height(self):
		return len(self.tile_data.tile_map)
	
	def blocked(self, x, y):
		#TODO Should take account of direction for special walls
		blocked = self.tile_data.tile_map[y][x] != CollisionTileData.NOT_BLOCKED
		#print "Alienpath %d,%d: %d" % (y,x, blocked)
		return blocked
	
	def get_cost(self, start_x, start_y, target_x, target_y):
		# this will always be horizontal/vertical adjacent nodes
		# bit more for diagonal
		if start_x == target_x or start_y == target_y:
			return 1
		return 2
			
	def is_valid_tile(self, x, y):
		return x>0 and x < self.get_width() and y>0 and y < self.get_height() and not self.blocked(x,y)
