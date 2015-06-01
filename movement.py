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

class Movement:
	
	MAP_COLLISION_HORIZONTAL = 1
	MAP_COLLISION_VERTICAL = 2

	def __init__(self):
		self.none()
	
	def none(self):
		self.x = 0
		self.y = 0
		self.arc_x = 0.0
		self.arc_y = 0.0
	
	
	@staticmethod
	def create(x, y):
		m = Movement()
		m.set(x,y)
		return m
	
	def set(self,x,y):
		self.x =x
		self.y = y
	
	def is_none(self):
		return self.x == 0 and self.y == 0
	
	def get_delta(self, speed, diagonal_speed):
		if self.is_diagonal():
			s = diagonal_speed
		else:
			s = speed
			
		return int(self.x * s + self.arc_x * speed), int(self.y *s + self.arc_y * speed)
		
	def is_diagonal(self):
		return self.x != 0 and self.y !=0
	
	def reverse(self):
		r = Movement()
		r.x = -self.x
		r.y = -self.y
		return r
	
	def to_state_name(self):
		if self.x ==0:
			if self.y >0:
				return 'movedown'
			elif self.y == 0:
				return None
			else:
				return 'moveup'
		elif self.x <0:
			if self.y >0:
				return 'movedownleft'
			elif self.y == 0:
				return 'moveleft'	
			else:
				return 'moveupleft'
		else:
			if self.y >0:
				return 'movedownright'
			elif self.y == 0:
				return 'moveright'
			else:
				return 'moveupright'
		
	@staticmethod
	def new_from_state(state):
		movement = Movement()
		movement.none()
		movement.from_state(state)
		return movement
		
	def from_state(self, state):
		if state == 'moveup':
			return self.set(0, -1)
		elif state == 'movedown':
			return self.set(0, 1)
		elif state == 'moveright':
			return self.set(1,0)
		elif state == 'moveleft':
			return self.set(-1, 0)
		elif state == 'moveupright':
			return self.set(1, -1)
		elif state == 'moveupleft':
			return self.set(-1, -1)
		elif state == 'movedownleft':
			return self.set(-1, 1)
		elif state == 'movedownright':
			return self.set(1, 1)
		else:
			return self.none()
	
	@staticmethod
	def new_none():
		return Movement()
	
	@staticmethod
	def new_random():
		movement = Movement()
		movement.set(get_random_int(-1,1), get_random_int(-1,1))
		return movement
	
	def random(self):
		self.set(get_random_int(-1,1), get_random_int(-1,1))
	
	def bounce(self, horizontalOrVertical):
		#bounce at 45 degrees at random
		r = mygame.randint(0,1)
		if r:
			d = -1
		else:
			d = 1
		
		if horizontalOrVertical == Movement.MAP_COLLISION_HORIZONTAL:
			#bullet collided whilst travelling horizontally (i.e. wall vertical)
			self.x = -self.x
			self.y = d * self.x + self.y
		else:
			self.y = -self.y
			self.x = d * self.y + self.x
	
		
	def run(self):
		self.x *= 1.5
		self.y *= 1.5
			
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
