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

import mygame

from unit import *
from movement import *
from utils import *

class PlayerKeyHandler:
	
	BACKWARDS_DELAY = 200
	
	def __init__(self, unit, my_game):
		self._unit = unit
		self._running_and_firing_last_time = None
		self._running_and_firing = None
		self._firing = False
		self._moving = False
		self._running = False
		self._quit = False
		self._change_weapons = False
		self.my_game = my_game
		self.key_set = KeySet.load_key_set()
		self.previous_movement = Movement()
		
	def handle(self, time):
		movement = self.previous_movement
		movement.none()
				
		keystate = self.my_game.get_key_pressed()
		
		if keystate & self.key_set.left > 0:
			if keystate & self.key_set.up > 0:
				movement.from_state('moveupleft')
			elif keystate & self.key_set.down >0:
				movement.from_state('movedownleft')
				
			else:
				movement.from_state('moveleft')
		
		elif keystate & self.key_set.right > 0:
			if keystate & self.key_set.up > 0:
				movement.from_state('moveupright')
			elif keystate & self.key_set.down >0:
				movement.from_state('movedownright')
			else:
				movement.from_state('moveright')
				
		elif keystate & self.key_set.up > 0:
			movement.from_state('moveup')
		
		elif keystate & self.key_set.down >0:
			movement.from_state('movedown')


		if keystate & self.key_set.walls >0:
			if Cheats.getCheatButtonEnabled():
				Cheats.toggleWalkThroughWalls()
				#Cheats.toggleNoCollisions()
				#Cheats.toggleNoAudio()
				#Cheats.toggleNoCountdown()
				#Cheats.toggleLogCollisionsInfo()
			
		self._change_weapons = keystate & self.key_set.change_weapon >0
		
		self._firing = keystate & self.key_set.fire >0
		
		self._intex = keystate & self.key_set.intex >0
		
		self._quit = keystate & self.key_set.escape >0
		
		self._running = keystate & self.key_set.run >0
		if self._running:
			movement.run()
		
		
		self._moving = not movement.is_none() 
		
		if self._firing and self._moving:
			self._running_and_firing_last_time = time
			
		if not self._running_and_firing:
			if self._firing and self._moving:
				#remember which direction we were running and firing in...
				self._running_and_firing = movement		
		
		else:
			if not self._firing:
				self._running_and_firing = None
		 	else:
				if not self._moving and self._running_and_firing_last_time:
					if time - self._running_and_firing_last_time > PlayerKeyHandler.BACKWARDS_DELAY:
						self._running_and_firing = None
		
					
		backwards = False
		if self._running_and_firing:
			if self._direction_opposite(self._running_and_firing, movement):
				backwards = True
		
		
		if not self._moving: 
			#if not dying then stop animating
			if self._unit.current_state() != 'dying':
				self._unit.stop()



		#apply movement animation
		if not movement.is_none():
			if not backwards:
				state = movement.to_state_name()
				
			else:
				state = movement.reverse().to_state_name()
				
			self._unit.enter_state(state, time)

		return movement

	def _direction_opposite(self, movement1, movement2):
		reverse = movement1.reverse()
		return movement2 == reverse
		
		
	def is_firing(self):
		return self._firing
	
	def change_weapons(self):
		return self._change_weapons
	
	def is_intex(self):
		return self._intex
	
	def is_quit(self):
		return self._quit
