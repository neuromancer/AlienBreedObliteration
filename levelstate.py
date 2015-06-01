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


class LevelState:
	NORMAL = 0
	COUNTDOWN = 1
	BOSS = 2
	END_GAME = 3
	INTEX = 4
	SCANNER = 5
	IN_GAME_MENU = 6
	TRANSITION = 7
				
	def __init__(self):
		self._level_complete = False
		self._game_over = False
		self._game_mode = LevelState.NORMAL
		self._num_domes = 0
		
	def get_level_complete(self):
		return self._level_complete
	
	def set_level_complete(self):
		self._level_complete = True
		self._game_over = True

	def set_game_over(self):
		self._game_over = True
		
	def get_game_over(self):
		return self._game_over
	
	def set_player_dead(self,unit):
		 #TODO test and return if all players are dead...
		 return True
	
	def set_game_mode(self, mode):
		self._game_mode =  mode
		
	def get_game_mode(self):
		return self._game_mode

	def add_dome(self):
		self._num_domes += 1
		
	def remove_dome(self):
		self._num_domes -= 1
		
	def get_no_domes_left(self):
		return self._num_domes == 0
	
	def get_num_domes(self):
		return self._num_domes
	
	def enter_transition(self):
		if self._game_mode != LevelState.TRANSITION:
			self._old_game_mode = self._game_mode
			self._game_mode = LevelState.TRANSITION
	
	def enter_intex(self):
		if self._game_mode != LevelState.INTEX:
			#self._old_game_mode = self._game_mode
			self._game_mode = LevelState.INTEX
		
	def exit_intex(self):
		if self._game_mode == LevelState.INTEX or self._game_mode == LevelState.SCANNER or self._game_mode == LevelState.IN_GAME_MENU:
			self._game_mode = self._old_game_mode
			
	def enter_scanner(self):
		if self._game_mode != LevelState.SCANNER:
			#self._old_game_mode = self._game_mode
			self._game_mode = LevelState.SCANNER
		
	
	def enter_in_game_menu(self):
		if self._game_mode != LevelState.IN_GAME_MENU:
			self._old_game_mode = self._game_mode
			self._game_mode = LevelState.IN_GAME_MENU
		
