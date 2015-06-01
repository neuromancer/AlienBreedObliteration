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

from levelstate import *

class DelayedCommand:

	def __init__(self, delay):
		self.delay = delay
		self._last_update = None
		self.done=False
		

	def update(self, time):
		if not self.done:
			if self._last_update:
				if time - self._last_update > self.delay:
					self.execute(time)
					self.done = True
			else:
				self._last_update = time
		return self.done

	def execute(self, time):
		return
	
class DelayedKillUnitCommand(DelayedCommand):
	def __init__(self, behaviour, unit):
		DelayedCommand.__init__(self, 100)
		self.behaviour = behaviour
		self.unit = unit
		
	def execute(self, time):
		self.behaviour.explode_me_and_adjacent_barrels(self.unit, time)
		return

class DelayedExplosion(DelayedCommand):
	def __init__(self, x, y, delay, level):
		DelayedCommand.__init__(self, delay)
		self.x =x
		self.y =y
		self.level = level
		
	def execute(self, time):
		self.level.add_big_explosion(self.x, self.y)

class DelayedLevelCompleteCommand(DelayedCommand):
	
	def __init__(self, level, success):
		DelayedCommand.__init__(self, 500)
		self.level = level
		self.success = success
	
	def execute(self, time):
		level_state = self.level.get_level_state()
		if self.success:
			level_state.set_level_complete()
		else:
			level_state.set_game_over()
		if level_state.get_game_mode() == LevelState.COUNTDOWN:
			self.level.get_countdown().stop()
		

class DelayedEnterIntexCommand(DelayedCommand):
			
	def __init__(self, level, enter_scanner):
		DelayedCommand.__init__(self, 0)
		self.level = level
		self.enter_scanner = enter_scanner
	
	def execute(self, time):
		if self.enter_scanner:
			self.level.get_level_state().enter_scanner()
			self.level.intex_menu.start_scanner()
		else:
			self.level.get_level_state().enter_intex()
			self.level.intex_menu.start()
		
