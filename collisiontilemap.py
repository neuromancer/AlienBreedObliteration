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

import array

#Special tiles

#Blank
#Door
#Lift
#
#
# 5 Hidden Wall
#
#7 Block if player above tile
#8 Block if player below tile
#9 Block if pplayer to left
#10 Block if player to right
#11 Block if player above and to left
#12 Block if player below and to left
#13 Block if player below and to right
#14 Block if player above and to right


class CollisionTileData:
	NOT_BLOCKED = 0
	BLOCKED = 1
	BLOCKED_ABOVE = 2
	BLOCKED_BELOW = 3
	BLOCKED_LEFT = 4
	BLOCKED_RIGHT = 5
	BLOCKED_ABOVE_LEFT = 6
	BLOCKED_BELOW_LEFT = 7
	BLOCKED_BELOW_RIGHT = 8
	BLOCKED_ABOVE_RIGHT = 9
	
	def __init__(self, level):
		#create a simpler level_tile array structure
		self.tile_map = []
		tiles = level.tile_set
		for y in range(0, level.level_height):
			#unsigned short
			a = array.array('H', range(0, level.level_width))
			for x in range(0, level.level_width):
				a[x] = self._is_tile_blocking(x,y, tiles, level.level_map_lower, level.level_map_upper)
			self.tile_map.append(a)

		self.tile_w, self.tile_h = tiles[0].image.get_width(),tiles[0].image.get_height()
		self.max_map_tile_x = level.level_width
		self.max_map_tile_y = level.level_height
		
		self.max_map_x = level.level_width * self.tile_w
		self.max_map_y = level.level_height * self.tile_h
		
		
		
	def _is_tile_blocking(self, x, y, tile_set, level_map_lower, level_map_upper):
		lower_tile = int(level_map_lower[y][x])
		upper_tile = int(level_map_upper[y][x])
		
		lower_type = tile_set[lower_tile].tile_type
		upper_type = tile_set[upper_tile].tile_type
		
		blocked = (lower_type == 'obstruction' or upper_type == 'obstruction')
		if blocked:
			if self._is_special_tile(lower_tile) or self._is_special_tile(upper_tile):
				b = self._decode_special_tile(lower_tile)
				if b != CollisionTileData.NOT_BLOCKED:
					return b	
				return self._decode_special_tile(upper_tile)		
			else:
				return CollisionTileData.BLOCKED
		else:
			return CollisionTileData.NOT_BLOCKED


	def _is_special_tile(self, t1):
		return t1 >= 7 and t1 <= 14

	def _decode_special_tile(self, tile):
		if tile == 7:
			return CollisionTileData.BLOCKED_ABOVE
		elif tile == 8:
			return CollisionTileData.BLOCKED_BELOW
		elif tile == 9:
			return CollisionTileData.BLOCKED_LEFT
		elif tile == 10:
			return CollisionTileData.BLOCKED_RIGHT
		elif tile == 11:
			return CollisionTileData.BLOCKED_ABOVE_LEFT
		elif tile == 12:
			return CollisionTileData.BLOCKED_BELOW_LEFT
		elif tile == 13:
			return CollisionTileData.BLOCKED_BELOW_RIGHT
		elif tile == 14:
			return CollisionTileData.BLOCKED_ABOVE_RIGHT
		else:
			return CollisionTileData.NOT_BLOCKED
	
