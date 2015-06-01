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

from utils import *
from weapons import *

HUD_IMAGE='hud.bmp'
HUD_GOLD_IMAGE = 'hudgold.bmp'  #64 x 8 
HUD_GOLD_PLUS = 'hudgoldplus.bmp'


class PlayerStats:
	
	MAX_HEALTH=50
	
	def __init__(self,ammo, lives, weapon_index, weapons):
		self.ammo = ammo
		self.lives = lives
		#self.lives = 1
		self.current_weapon_index = weapon_index
		
		self.money = 0
		self.__keys = 0
		self.__health = 0
		self.weapons = weapons
		self.setup_weapons()
		#Player X requries keys warning given...
		self.key_warning = False
		self.blue_pass = False
		self.scanner = False
	
	def setup_weapons(self):
		self.has_weapons = []
		for w in self.weapons.get_all_weapons():
			self.has_weapons.append(False)
		self.has_weapons[self.current_weapon_index] = True
		
	def get_health(self):
		if self.__health >0:
			return self.__health
		else:
			return 0
	
	def set_health(self, health):
		self.__health = health
	
	def keys(self):
		return self.__keys
	
	def add_key(self, k=1):
		self.__keys +=k
		#clear this so next time we need a key we hear the warning
		self.key_warning = False  
		
	def use_key(self):
		self.__keys -=1
	def get_weapon(self):
		return self.weapons.get_weapon(self.current_weapon_index)
		
	def increment_current_weapon(self):
		has = False
		while not has:
			self.current_weapon_index += 1
			total = self.weapons.get_num_weapons()
			if self.current_weapon_index >= total :
				self.current_weapon_index = 0
			has = self.has_weapon(self.current_weapon_index)
			
	def next_life(self):
		if self.lives > 0:
			self.lives -= 1
			self.__health =PlayerStats.MAX_HEALTH
			return True
		return False
		
			
	def has_scanner(self):
		return self.scanner
	
	def set_scanner(self, scanner):
		self.scanner = scanner
		
	def add_life(self):
		self.lives += 1
		
	def add_ammo_pack(self):
		 self.ammo += 50
		 
	def add_energy_pack(self):
		self.set_health(50)
	
	def has_weapon(self, weapon_index):
		return self.has_weapons[weapon_index]
	
	def set_has_weapon(self, weapon_index):
		self.has_weapons[weapon_index] = True
	
	def clone(self):
		ps = PlayerStats(self.ammo, self.lives, self.current_weapon_index, self.weapons)
		ps.money = self.money
		ps.add_key(self.keys())
		ps.set_health(self.get_health())
		ps.key_warning = self.key_warning
		ps.blue_pass = self.blue_pass
		ps.scanner = self.scanner
		for i in range(0, len(self.weapons.get_all_weapons())):
			if self.has_weapon(i):
				ps.set_has_weapon(i)
		return ps
class Hud:
	def __init__(self, player_stats, my_game):
		self.player_stats = player_stats
		self.my_game = my_game
		self.hud_img = mygame.load_image(get_image_pathname(HUD_IMAGE))
		
		self.hud_gold = mygame.load_image(get_image_pathname(HUD_GOLD_IMAGE))
		
		self.hud_gold_big_blip = my_game.create_blank((2, self.hud_gold.get_height()))
		self.hud_gold_big_blip.blit(self.hud_gold, self.hud_gold_big_blip.get_rect(), self.hud_gold_big_blip.get_rect())
		
		self.hud_gold_plus = mygame.load_image(get_image_pathname(HUD_GOLD_PLUS))
		self.hud_gold_plus.set_colorkey(mygame.Colour(0xff,0,0xff))
		
		self.hud_gold_small_blip = my_game.create_blank((1, self.hud_gold.get_height()))
		self.hud_gold_small_blip.blit(self.hud_gold, self.hud_gold_small_blip.get_rect(), self.hud_gold_small_blip.get_rect())

		self.health_bar_x = 32
		self.lives_x = 134
		self.big_tick_x_increment = 4
		self.small_tick_x_increment = 2
		self.ammo_x = 206
		self.small_ammo_x = 250
		self.keys_x = 337
		
		self.health_bars = dict()
		
		if RESIZE:
			self.hud_img = self.hud_img.scale((int(self.hud_img.get_width() *HUD_RESIZE_FACTOR),int(self.hud_img.get_height() *HUD_RESIZE_FACTOR)))
			
			self.hud_gold = self.hud_gold.scale((int(self.hud_gold.get_width() *HUD_RESIZE_FACTOR),int(self.hud_gold.get_height() *HUD_RESIZE_FACTOR)))
			
			
			self.hud_gold_big_blip = self.hud_gold_big_blip.scale((int(self.hud_gold_big_blip.get_width() *HUD_RESIZE_FACTOR),int(self.hud_gold_big_blip.get_height() *HUD_RESIZE_FACTOR)))
			
			self.hud_gold_small_blip = self.hud_gold_small_blip.scale((int(self.hud_gold_small_blip.get_width() *HUD_RESIZE_FACTOR),int(self.hud_gold_small_blip.get_height() *HUD_RESIZE_FACTOR)))
			
			self.hud_gold_plus = self.hud_gold_plus.scale((int(self.hud_gold_plus.get_width() *HUD_RESIZE_FACTOR),int(self.hud_gold_plus.get_height() *HUD_RESIZE_FACTOR)))
			
			self.health_bar_x = int(self.health_bar_x * HUD_RESIZE_FACTOR)
			self.lives_x = int(self.lives_x * HUD_RESIZE_FACTOR)
			self.big_tick_x_increment = int(self.big_tick_x_increment * HUD_RESIZE_FACTOR)
			self.ammo_x = int(self.ammo_x * HUD_RESIZE_FACTOR)
			self.keys_x = int(self.keys_x * HUD_RESIZE_FACTOR)
			self.small_tick_x_increment = int(self.small_tick_x_increment * HUD_RESIZE_FACTOR)
			self.small_ammo_x = int(self.small_ammo_x * HUD_RESIZE_FACTOR)
		
	def paint(self, view, s):
		hud_x = 0
		hud_y = view.h - self.hud_img.get_height()
		
		s.blit(self.hud_img,(hud_x,hud_y))
		self.plot_health(s, hud_y)
		self.plot_lives(s, hud_y)
		self.plot_ammo(s, hud_y)
		self.plot_keys(s, hud_y)
	
	def plot_health(self, s, hud_y):
		health_bar_w = self.hud_gold.get_width() *  self.player_stats.get_health() / 50
		  
		health_bar_h = self.hud_gold.get_height()
		
		#Cache health bars...
		if health_bar_w in self.health_bars:
			health_bar = self.health_bars[health_bar_w]
		else:
			health_bar = self.my_game.create_blank((int(health_bar_w), int(health_bar_h)))
			self.health_bars[health_bar_w] = health_bar
		
		health_bar.blit(self.hud_gold, health_bar.get_rect(), health_bar.get_rect())
		
		s.blit(health_bar,(self.health_bar_x,hud_y))

	def plot_lives(self, s, hud_y):
		self.plot_big_ticks(s, hud_y, self.lives_x, self.player_stats.lives, 7)
	
	def plot_ammo(self, s, hud_y):
		self.plot_big_ticks(s, hud_y, self.ammo_x, self.player_stats.ammo / 50, 7)
		self.plot_little_ticks(s, hud_y, self.small_ammo_x, self.player_stats.ammo % 50, 24)
	
	def plot_keys(self, s, hud_y):
		self.plot_big_ticks(s, hud_y, self.keys_x, self.player_stats.keys(), 13)
		
	
	def plot_big_ticks(self, s, hud_y, start_x, num, max):
		x = start_x
		num_ticks = num
		plot_plus = False
		if num_ticks > max:
			num_ticks = max
			plot_plus = True
			
		for l in range(0, num_ticks):
			s.blit(self.hud_gold_big_blip, (x, hud_y))
			x += self.big_tick_x_increment
			
		if plot_plus:
			#this image is too wide - it has white space in second half...
			s.blit_part(self.hud_gold_plus, (x,hud_y), mygame.Rect(0, self.hud_gold_plus.get_rect().y, self.hud_gold_plus.get_rect().w/2, self.hud_gold_plus.get_rect().h))
			
	def plot_little_ticks(self, s, hud_y, start_x, num, max):
		x = start_x
		num_ticks = num / 2 # each tick is two counts
		if num_ticks > max:
			num_ticks = max
			
		for l in range(0, num_ticks):
			s.blit(self.hud_gold_small_blip, (x, hud_y))
			x += self.small_tick_x_increment
