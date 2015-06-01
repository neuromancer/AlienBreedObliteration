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

import math


import mygame as mygame
from unit import *
from utils import *
from collision2 import *
from position import *
from keyboard import *
from movement import *
			
#For debugging bullet map collisions
#from pathfinder import *

class CharacterMovement:
			
	def __init__(self, display, player, attempt_bump):
		self.display = display
		
				
		self.collision2 = LevelMapCollision2(display.level)
		#self.collision2 = LevelMapCollision3(display.level)
		self.unit_collision2 = UnitCollision2(display.level)
		
		self.attempt_bump = attempt_bump
	
	def _calculate_unit_speed(self, player):
		#TODO determine from player info (130)
		#print "player configured speed %d" % player.get_speed()
		#pixels_per_second = 1000/int(player.get_speed())
		pixels_per_second = float(player.get_speed())
		if RESIZE:
			pixels_per_second *= RESIZE_FACTOR
			
		#print "pixels per second %d" % pixels_per_second
		pixels_per_frame = int(pixels_per_second / self.display.refresh_rate)
		self.speed = pixels_per_frame
		#self.speed = int(player.get_speed() / self.display.refresh_rate * 2.4)
		#self.diagonal_speed = int(math.sqrt(math.pow(self.speed, 2) / 2))
		self.diagonal_speed = self.speed
		
		#self.speed = 12
		#self.diagonal_speed = 10  #todo calc this
		#self.bump_speed = self.speed/2 # bumps are slower than normal walking
		#self.slide_speed = self.speed/2 #slides along a way are slower than normal
		self.bump_speed = self.speed
		self.slide_speed = self.speed

	
	def handle_movement(self, player_unit, player_movement, time):
		self._calculate_unit_speed(player_unit)
		
		scroll_x = 0
		scroll_y = 0
		
		if not player_movement.is_none():
			#check for map collisions....
			scroll_x=0
			scroll_y=0
			
			speed = self.speed
			diagonal_speed = self.diagonal_speed
			
			scroll_x, scroll_y = player_movement.get_delta(speed, diagonal_speed)
			
			
			new_x, new_y, collided_map = self.collision2.move(player_unit, scroll_x, scroll_y, self.attempt_bump)
			scroll_x = new_x - player_unit.get_rect().x
			scroll_y = new_y - player_unit.get_rect().y
						
			#a hack - hack in the old unit collision code...
			#Check for unit collisions
			pp = PlayerPosition(self.display, player_unit)
			scroll_x, scroll_y, closest_blocking_unit = self.move_until_first_unit_hit(player_unit, scroll_x, scroll_y, pp, collided_map, time)
			
			
			#move player's position
			player_unit.move(scroll_x, scroll_y)
			
		return scroll_x, scroll_y		
	
	
			
	def move_until_first_unit_hit(self, player_unit, scroll_x, scroll_y, pp,  collided_map, time):
		#Check for unit collisions within distance moved...
		unit_collisions = self.unit_collision2.get_unit_collisions(player_unit, mygame.Rect(pp.tl.v.x + scroll_x, pp.tl.v.y + scroll_y, pp.w, pp.h))
					
		#process all non-blocking collisions up until first blocking (solid) collision
		closest_blocking_unit = None
		for unit in unit_collisions:
			player_unit.collide_unit(unit[1], unit[3], time)
			if unit[1].is_blocking_collision(player_unit):
				closest_blocking_unit = unit
				break
		
		if closest_blocking_unit:
			scroll_x=0
			scroll_y=0
			#unit is to right of player, scroll to unit left position - player right edge 
			if unit[2].x > pp.tr.v.x:
				scroll_x = unit[2].x - pp.tr.v.x
			
			if (unit[2].x + unit[2].w) < pp.tl.v.x:
 				#unit to left, scroll to unit right edge
				scroll_x = -(pp.tl.v.x - (unit[2].x + unit[2].w))
				
			if unit[2].y > pp.bl.v.y:
				#unit below player
				scroll_y = unit[2].y - pp.bl.v.y
			
			if  unit[2].y + unit[2].h < pp.tl.v.y:
				#unit below player
				scroll_y = -(pp.tl.v.y - (unit[2].y + unit[2].h))
						
			#scroll_x = unit[2].x - pp.tl.v.x
			#scroll_y = unit[2].y - pp.tl.v.y
			#print_debug("hit unit at %d,%d" %(unit[2].x, unit[2].y),2)

		else:
			#not blocked by unit, perhaps by map obstruction
			if collided_map:
			 	# let subclasses know we collided with the map
				self.collided_map(player_unit, scroll_x, scroll_y, time)

		return scroll_x, scroll_y, closest_blocking_unit

	def collided_map(self, player_unit, scroll_x, scroll_y, time):
		return


	def is_current_position_blocked(self, unit):
		return self.collision2.is_current_position_blocked(unit)


	def calc_reverse_direction(self, direction):
		return direction.reverse()	
		

class PlayerMovement(CharacterMovement):
	
	def __init__(self, display, player, mygame):
		CharacterMovement.__init__(self, display, player, True)
		self.player1KeyHandler = PlayerKeyHandler(player, mygame)

	def handle_key_press(self, player, time):
		if player.current_state() != 'dying':
			player_movement = self.player1KeyHandler.handle(time)
			self.handle_movement(player, player_movement, time)
		else:
			print_debug("Ignoring player movement as player dying", 2)

	def handle_movement(self, player_unit, player_movement, time):
		scroll_x, scroll_y = CharacterMovement.handle_movement(self, player_unit, player_movement, time)
		#check if also need to scroll dislay if player near edge
		#if self.display.rect_at_edge(self.player_unit.rect):
		self.display.scroll(scroll_x, scroll_y)


	def get_key_handler(self):
		return self.player1KeyHandler

class BulletMovement(CharacterMovement):
	
	def __init__(self, display, player):
		CharacterMovement.__init__(self, display, player, False)
	
	def collided_map(self, bullet_unit, scroll_x, scroll_y, time):
		#Attempt to determine if obstruction is vertical or horizontal
		#bullet will travel up to the point adjacent to the obstruction
		#i.e. the last unobstructed position in the tile adjacent to the
		#obstructoin
		r = bullet_unit.get_rect()
		pos_x = r.x + scroll_x
		pos_y = r.y + scroll_y
		#Find the tile which includes the bullet position
		tile_x,tile_y = self.display.view_to_tile((pos_x,pos_y))
		#find the tile's top left coordinates
		tile_real_x, tile_real_y = self.display.tile_to_view((tile_x,tile_y))
		#determine which side of tile bullet has reached
		
		horizontalOrVertical = 0
		if pos_x == tile_real_x:
			#left edge - wall is vertical
			horizontalOrVertical = Movement.MAP_COLLISION_HORIZONTAL
		else :
			horizontalOrVertical = Movement.MAP_COLLISION_VERTICAL
		
		#Debug display collision tile...
		"""
		p = Path()
		p.append(Step(tile_x,tile_y))
		self.display.add_debug_alien_path(p)
		"""
		
		#Bullets need to know when they hit the map
		#print"Col %d" % horizontalOrVertical
		bullet_unit.collide_map(horizontalOrVertical,pos_x, pos_y, time)
		
		
class AlienMovement(CharacterMovement):
	
	def __init__(self, display, player):
		CharacterMovement.__init__(self, display, player, True)

