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
from playerstats import *

class SavedGameId:

	def __init__(self, name, file):
		self.name = name
		self.file = file

class SavedGame:
		
	def __init__(self):
		self.ammo = 0
		self.lives = 0
		self.current_weapon = 0
		self.weapons = 0
		self.money = 0
		self.keys = 0
		self.health = 0
		self.level = 0
		self.scanner = 0
		self.name = None
		self.file = None

	def create(self, player_stats, level):
		self.ammo = player_stats.ammo
		self.lives = player_stats.lives
		self.current_weapon = player_stats.current_weapon_index
		self.money = player_stats.money
		self.keys = player_stats.keys()
		self.health = player_stats.get_health()
		self.scanner = 0
		if player_stats.scanner:
			self.scanner = 1
		self.weapons = 0
		w = player_stats.has_weapons
		index = 0
		for i in w:
			self.weapons |= (i << index)
		self.level = level
		
	@staticmethod
	def load_by_id(saved_game_id):
		path = saved_game_id.file
		return SavedGame.load_by_path(path)
		
	@staticmethod
	def load_by_path(path):
		game = SavedGame()
		game.file = path
		a = open(path, "r")
		try:
			game.name = a.readline()
			data = a.readline()
			parts = data.split(',')
			game.ammo = int(parts[0])
			game.lives = int(parts[1])
			game.current_weapon = int(parts[2])
			game.money = int(parts[3])
			game.keys = int(parts[4])
			game.health = int(parts[5])
			game.scanner = int(parts[6])
			game.weapons = int(parts[7])
			game.level = int(parts[8])
		finally:
			a.close() 
		return game


	def save(self, saved_game_id):
		a = open(saved_game_id.file, "w")
		try:
			a.write(saved_game_id.name)
			a.write("\n")
			a.write(str(int(self.ammo)))
			a.write(",")
			a.write(str(int(self.lives)))
			a.write(",")
			a.write(str(self.current_weapon))
			a.write(",")
			a.write(str(int(self.money)))
			a.write(",")
			a.write(str(int(self.keys)))
			a.write(",")
			a.write(str(int(self.health)))
			a.write(",")
			a.write(str(self.scanner))
			a.write(",")
			a.write(str(self.weapons))
			a.write(",")
			a.write(str(self.level))
			a.write("\n")
			
		finally:
			a.close() 
		return


	def convert(self, weapons):
		ammo = self.ammo
		lives = self.lives
		current_weap = self.current_weapon
		ps = PlayerStats(ammo, lives, current_weap, weapons)
		
		ps.money = self.money
		ps.add_key(self.keys)
		ps.set_health(self.health)
		ps.scanner = self.scanner == 1
		
		for i in range(0,len(weapons.get_all_weapons())):
			have = self.weapons & (1 << i) > 0
			if have:
				ps.set_has_weapon(i)
			
		return self.level, ps


class SaveGameUtil:

	@staticmethod
	def get_saved_game_list():
		files = get_saved_game_list()
		files.sort()

		ids = []

		for f in files:
			path = get_saved_game_pathname(f)
			game = SavedGame.load_by_path(path)
			id = SavedGameId(game.name, game.file)
			ids.append(id)

		return ids
		
	@staticmethod
	def new_id(level_num, name):
		gname = 'Level ' + str(level_num) + " - " + name
		fname = 'level' + str(level_num)
		return SavedGameId(gname, get_saved_game_pathname(fname))
	
