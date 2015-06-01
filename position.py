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

from level import *

class TilePos:
	def __init__(self, tx, ty):
		self.x = tx
		self.y = ty

class ViewPoint:
	def __init__(self, vx, vy):
		self.x = vx
		self.y =vy	
		
class Point:
	def __init__(self, x, y, tx, ty):
		self.t = TilePos(tx, ty)
		self.v = ViewPoint(x, y)
	
	@staticmethod
	def from_view(vx, vy, display):
		t = display.view_to_tile((vx, vy))
		return Point(vx,vy,t[0], t[1])
		
class PlayerPosition:
		
	def __init__(self, display, player_unit):
		self.w = player_unit.get_rect().w
		self.h = player_unit.get_rect().h
		
		pl_rect = player_unit.get_rect()
		
		self.tl = Point.from_view(pl_rect.x, pl_rect.y, display)
			
		self.tr = Point.from_view(pl_rect.x + self.w, pl_rect.y, display)
		
		self.bl = Point.from_view(pl_rect.x, pl_rect.y + self.h, display)
		
		self.br = Point.from_view(pl_rect.x + self.w, pl_rect.y + self.h, display)
		
