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

from utils import *
from levelstate import *

"""
Some Units have complex Actions (for example Triggers) written using a simple action language. The ActionHandler class processes these actions.

examples:
	
	IFMODENORMAL SETGAMEMODE Boss SETUNITSTATE bossdoorin closed
	EXPLOSION SETUNITSTATE bossdoor open SETUNITSTATE shipdoor open SETGAMEMODE CountDown
	IFNODOMES LOADNEXTLEVEL level7.lev

"""

class ActionHandler:
		
	@staticmethod
	def perform_action(level, action, unit, them, time):
		
		parts = action.split(" ")
		current_part = 0
		num = len(parts)
		
		while (current_part < num):
			#Check optional preconditions...
			if current_part < num and parts[current_part][0:2] == 'IF':
				if not ActionHandler._check_preconditions(parts[current_part], level, them):
					return
				current_part += 1
				
			#Handle optional EXPLOSION command...
			if current_part < num and parts[current_part] == 'EXPLOSION':
				ActionHandler._explosions(level, unit, time)
				current_part += 1
				
			#Handle optional LOADNEXTLEVEL levelXX.lev command...
			if current_part < num and parts[current_part] == 'LOADNEXTLEVEL':
				print_debug("Level complete",3)
				level.level_complete()
				current_part += 2  # skip level number
				
				
			#Handle optional SETGAMEMODE abc command...
			if current_part < num and parts[current_part] == 'SETGAMEMODE':
				mode = parts[current_part+1]
				ActionHandler._set_game_mode(mode, level, time)
				current_part +=2 # skip mode name
				
			#Handle option SETUNITSTATE unit state
			if current_part < num and parts[current_part] == 'SETUNITSTATE':
				unit_name = parts[current_part+1]
				state = parts[current_part+2]
				ActionHandler._set_unit_state(unit_name, state, level, time)
				current_part += 3 # skip arguments
				
	
	@staticmethod
	def _set_game_mode(mode, level, time):
		if mode == 'Boss':
			level.enter_boss_mode()
		elif mode == 'CountDown':
			level.start_countdown()
		elif mode == 'EndGame':
			level_state = level.get_level_state()
			level_state.set_game_mode(LevelState.END_GAME)
			level_state.set_level_complete()
		else:
			print "Unknown SETGAMEMODE mode %s" % mode
	
	@staticmethod
	def _explosions(level, unit, time):
		level.add_random_explosions(unit.get_rect(), 5, 1000)
		level.add_big_explosion(unit.get_rect().x, unit.get_rect().y)
			
			
	@staticmethod
	def _check_preconditions(action, level, them):
		level_state = level.get_level_state()
		if action == 'IFNOBOSS':
			return level_state.get_game_mode() == LevelState.COUNTDOWN
		
		elif action == 'IFMODENORMAL':
			return level_state.get_game_mode() == LevelState.NORMAL
		
		elif action == 'IFBLUEPASS':
			return them.get_player_stats().blue_pass
		
		elif action == 'IFNODOMES' or action == 'IFNOEGGS' or action == 'IFNOHOSTAGES':
			return level.get_level_state().get_no_domes_left()
		
		else:
			print "Unknown precondition '%s'" % action
			return True
		
			
	@staticmethod
	def _set_unit_state(unit_name, state, level, time):
		if state=='closed':
			level.close_door_by_name(unit_name, time)
		elif state=='open':
			level.open_door_by_name(unit_name, time)
		else:
			print "Unknown SETUNITSTATE state %s" % state
