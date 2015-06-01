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
import mygame

import unit as U
from utils import *
from playerstats import *
import charactermovement as CM
#import numpy_levelloader as LL
import array_levelloader as LL
from countdown import *
from levelstate import *
from level_text import *
import intex as intex
from delayedcommands import *
from gamemenu import *
from palette import *
#for debug stats
from collision2 import *

END_LEV_MUSIC=get_sound_pathname('endlev.xm')

class LevelUnitSetRect:
	
	def __init__(self, rect):
		self.units = []
		self.rect = rect
	
	def add_unit(self, unit):
		self.units.append(unit)
	
	def collides(self, rect):
		return rect.colliderect(self.rect)
	
UNIT_SCENE_SIZE=SCREEN_X/2
MOVEABLE_SET = True
CHOP_VERTICALLY=True

class LevelUnitSet:
	
	def __init__(self, map_max_x, map_max_y):
		self.static_columns = []
		#Split the map up into sections and keep units in these columns
		#reduces the aamount of searching we must do when testing for collisions
		
		self.num_rows = 0
		num_sections = 0
		if CHOP_VERTICALLY:
			step = UNIT_SCENE_SIZE
		else:
			step = int(map_max_y)
		
		for y in range(0, int(map_max_y), step):
			y_width = step
			self.num_columns = 0
			for x in range(0, int(map_max_x), UNIT_SCENE_SIZE):
				r = mygame.Rect(x, y, UNIT_SCENE_SIZE, y_width)
				s = LevelUnitSetRect(r)
				self.static_columns.append(s)
				print_debug("Created column %d,%d,%d,%d" %(r.x, r.y, r.w, r.h),3)
				self.num_columns+=1
				num_sections +=1
		print_debug("Number of sections for unit sets %d (%d,%d,%d)" %(num_sections, self.num_columns, self.num_rows, map_max_x),3)
		
		self.static_units = [] #complete list
		self.moveable_units = [] #complete list
		self.alien_prototypes = dict({})
		self.gun_flare_unit = None
		self.player = None
		self.bullet_prototypes = dict({})
		self.small_explosion_prototype = None
		self.units_by_name = dict({})
		self.lifts = []
		self.doors = []
		
	def add_unit(self, unit):
		self.static_units.append(unit)
		self.__add_to_set(unit)
	
	def __add_to_set(self, unit):
		added = False
		rect = unit.get_rect()
		#for s in self.static_columns:
		possibles = self.get_possible_sections(rect)
		for s in possibles:
			if s.collides(rect):
				s.add_unit(unit)
				added =True
		unit.set_observer(self)
		if unit.get_name():
			self.units_by_name[unit.get_name()] = unit
		
		if not added:
			print_debug("Couldnt add %d, %d, %d, %d" % (unit.get_rect().x,unit.get_rect().y,unit.get_rect().w,unit.get_rect().h), 3)
		
	def add_alien_prototype(self, file, unit):
		self.alien_prototypes[file] = unit
	
	def get_alien_prototype(self, file):
		return self.alien_prototypes[file]
	
	def add_alien(self, unit):
		unit.set_observer(self)
		self.moveable_units.append(unit)
		if MOVEABLE_SET:
			self.__add_to_set(unit)
		
	def set_player_unit(self, player):
		self.player = player
		self.moveable_units.append(player)
		if MOVEABLE_SET:
			self.__add_to_set(player)
	
	def get_player_unit(self):
		return self.player
	
	def set_gun_flare_unit(self, unit):
		self.gun_flare_unit = unit
	
	def get_gun_flare_unit(self):
		return self.gun_flare_unit
	
	def add_bullet_prototype(self, file, unit):
		self.bullet_prototypes[file] = unit
	
	def get_bullet_prototype(self, file):
		return self.bullet_prototypes[file]
	
	def add_bullet(self, unit):
		unit.set_observer(self)
		self.moveable_units.append(unit)
		if MOVEABLE_SET:
			self.__add_to_set(unit)
		
	def get_all_units(self):
		l = []
		l.extend(self.static_units)
		l.extend(self.moveable_units)
		return l
		
	def get_units_for_collision_detection(self, rect):
		l = []
		#may return duplicates
		#for s in self.static_columns:
		possibles = self.get_possible_sections(rect)
		for s in possibles:
			if s.collides(rect):
				l.extend(s.units)
				
		if not MOVEABLE_SET:
			l.extend(self.moveable_units)
		return l
	
	def unit_position_updated(self, unit, old_pos_rect):
		if MOVEABLE_SET:
			#the unit may have changed 'set' s re-add
			remove = self.__remove_from_set(unit, old_pos_rect)
			#if not remove:
			#	print "Unable to remove"
			if remove:
				self.__add_to_set(unit)
		return
	
	def __remove_from_set(self, unit, old_pos_rect):
		removed = False
		
		possibles = self.get_possible_sections(old_pos_rect)
		
		#for s in self.static_columns:
		for s in possibles:
			if s.collides(old_pos_rect):
				if unit in s.units:
					s.units.remove(unit)
					removed = True
		return removed
		
	def unit_removed(self, unit):
		removed = self.__remove_from_set(unit, unit.get_rect())
		
		if unit in self.static_units:
			self.static_units.remove(unit)
			removed = True
			
		if unit in self.moveable_units:
			self.moveable_units.remove(unit)
			removed = True
		
		if not removed:
			print_debug("Unable to remove %s" %( unit.get_uni_filename()), 3)
		
		return
	
	def set_small_explosion_unit(self, unit):
		self.small_explosion_unit = unit
	
	def get_small_explosion_unit(self):
		return self.small_explosion_unit
	
	def add_small_explosion(self, explosion):
		explosion.set_observer(self)
		self.moveable_units.append(explosion)
	
	def set_big_explosion_unit(self, unit):
		self.big_explosion_unit = unit
	
	def get_big_explosion_unit(self):
		return self.big_explosion_unit
	
	def add_big_explosion(self, explosion):
		explosion.set_observer(self)
		self.moveable_units.append(explosion)
	
	def get_unit_by_name(self, name):
		if name in self.units_by_name:
			return self.units_by_name[name]
		else:
			return None
	
	def get_possible_sections(self, rect):
		#find unit sets which may collide with rect
		
		x_start = int(rect.x / UNIT_SCENE_SIZE)
		x_end = int((rect.x + rect.w) / UNIT_SCENE_SIZE)
		y_start = int(rect.y / UNIT_SCENE_SIZE)
		y_end = int((rect.y + rect.h) / UNIT_SCENE_SIZE)
		
		if not CHOP_VERTICALLY:
			y_start = 1
			y_end =1
		
		rects = []
		for y in range(y_start, y_end+1):
			for x in range(x_start, x_end+1):
				if CHOP_VERTICALLY:
					index = self.num_columns * y + x
				else:
					index = x
				if index < len(self.static_columns):
					rects.append(self.static_columns[index])
	
		#print "returning %d rects " % len(rects)
		return rects
				
	def add_lift(self, lift):
		self.lifts.append(lift)
		self.add_unit(lift)
		
	def get_lifts(self):
		return self.lifts
		
	def add_door(self, door):
		self.doors.append(door)
		self.add_unit(door)
		
	def get_doors(self):
		return self.doors
	
		
class LevelUnitInstance:
	def __init__(self,name, file, tileposx, tileposy, state, action, triggerable, health):
		self.name = name
		self.file = file
		self.tileposx = tileposx
		self.tileposy = tileposy
		self.state = state
		self.trigger_action = action
		self.triggerable = triggerable
		self.health = health
		
		print_debug('LevelUnitInstance %s %s %f %f %s %s %d' %(self.name, self.file, self.tileposx, self.tileposy, self.state, self.trigger_action, self.triggerable), 5)

class Tile:
    	def __init__(self,image=None):
        	self.image = image
		self.tile_type = None
		self.frequency = None
					

class TileSet:
	
	def __init__(self):		
		self.trans_set2 = mygame.Colour(0xff,0,0xff)
	
	BLACK_TILE=0
	

	def load_tiles(self, fname, TW, TH):
		
		images, self.tile_width, self.tile_height = CompositeTileLoader.load_tiles(fname, TW, TH, self.trans_set2)
		
		NUM = len(images)
		self.tiles = [Tile for x in xrange(0, NUM)]
		
		n = 0
		for i in images:
			tile = Tile(i)
			self.tiles[n] = tile
			n+=1
		
		
	def __getitem__(self,index):
		return self.tiles[index]


	def size(self):
		return len(self.tiles)

class Level:
	
	MAX_AlIENS = 10
	
	def __init__(self, level_num, weapons, initial_player_stats, my_game):
		self.my_game = my_game
		self.level_unit_instances = []
		U.UnitFactory.empty()
		self.initial_player_stats = initial_player_stats
		self.initial_player_health = None
		self.weapons = weapons
		self.level_num = level_num
		lev_filename = get_level_filename(level_num)
		self.text_loader = LevelTextLoader(lev_filename)
		self.name = ''
		self._active_countdown = None
		self.no_scanner = False
		self.hardnessbias = 1.0
		self.load_lev(lev_filename)
		self.level_state = LevelState()
		self._delayed_commands = []
		
		self.num_aliens_on_screen = 0
		
		# load the background tile images
		self.tile_set = TileSet()
		self.tile_set.load_tiles(self.map_tile_bitmap, self.map_tile_width, self.map_tile_height)
		# load background tile meta info
		self.load_level_tile_meta(self.map_tile_define, self.tile_set)
		#  load level tile map
		loader = LL.LevelDataLoader(self)
		self.level_map_lower, self.level_map_upper = loader.load_level_tile_data(get_config_pathname(self.map_tile_data))
		
		#now load all the units defined in the level data
		max_map_x = self.level_width * self.map_tile_width
		max_map_y = self.level_height * self.map_tile_height
		if RESIZE:
			max_map_x = int(max_map_x *RESIZE_FACTOR)
			max_map_y = int(max_map_y *RESIZE_FACTOR)
			self.map_tile_width = int(self.map_tile_width * RESIZE_FACTOR)
			self.map_tile_height = int(self.map_tile_height * RESIZE_FACTOR)
			
		self.unit_set = LevelUnitSet(max_map_x, max_map_y)
		self.load_units(self.unit_set)
		self.intex_menu = intex.Menu(my_game, self)
		self.in_game_menu = InGameMenu(my_game)
		self.end_lev_sound = my_game.get_mixer().Music(END_LEV_MUSIC)
		print_debug("Level constructed",2)
	
	def load_lev(self, filename): 
		MAPTILEBITMAP = re.compile('MAPTILEBITMAP file=(\S*) tileheight=(\d*) tilewidth=(\d*)')
		MAPTILEDEFINE = re.compile('MAPTILEDEFINE file=(\S*)')
		MAPTILEDATA = re.compile('MAPTILEDATA file=(\S*)')
		UNIT = re.compile('<UNIT (?:name=(\S*)\s)?file=(\S*) tileposx=([\d\.]*) tileposy=([\d\.]*)(?:\sstate=(\S*))?(?:\saction="([^"]*)")?(?:\striggerable=(\d*))?(?:\shealth=(\d*))?>')
		
		HARDNESSBIAS = re.compile('HARDNESSBIAS health=([\d\.]*)(?:\sscanner=(\d*))?')
		
		PLAYERSTATS = re.compile('PLAYERSTATS Player=(\d*) Ammo=(\d*) Lives=(\d*) CountDownDelay=Normal HasFired=(\d*) MachineGun=(\d*)')
		
		NAME = re.compile('NAME name="([^"]*)"')
		
		COUNTDOWN = re.compile('COUNTDOWNDATA delay=(\d*) time=(\d*)(?:\sfadered=(\d*))?(?:\sshake=(\d*))?')
		
		num_units_read = 0
    		a = open(get_config_pathname(filename), "r")
		try:
			line = a.readline()
			while line:
				print_debug(line,5)
				m = MAPTILEBITMAP.match(line)
				if m:
					self.map_tile_bitmap = m.group(1)
					self.map_tile_height= int(m.group(2))
					self.map_tile_width = int(m.group(3))
					print_debug("Level %s %d %d" % (self.map_tile_bitmap, self.map_tile_height, self.map_tile_width), 5)
					
				m = MAPTILEDEFINE.match(line)
				if m:
					self.map_tile_define = m.group(1)
					print_debug("Map tile def %s" % self.map_tile_define, 5)
				
				m = MAPTILEDATA.match(line)
				if m:
					self.map_tile_data = m.group(1)
					print_debug("Map tile data %s" % self.map_tile_data, 5)
				
				m = UNIT.match(line)
				if m:
					name = m.group(1)
					file = m.group(2)
					tileposx = float(m.group(3))
					tileposy = float(m.group(4))
					state = m.group(5)
					action = m.group(6)
					if m.group(7):
						triggerable = int(m.group(7))
					else:
						triggerable = 0
					if m.group(8):
						initial_health = int(m.group(8))
					else:
						initial_health = None
						
					if RESIZE:
						tileposx = int(tileposx * RESIZE_FACTOR)
						tileposy = int(tileposy * RESIZE_FACTOR)
					
					unit_def = LevelUnitInstance(name, file, tileposx, tileposy, state, action, triggerable, initial_health)
					self.level_unit_instances.append(unit_def)
					
					num_units_read += 1
				
				m = HARDNESSBIAS.match(line)
				if m:
					self.hardnessbias = float(m.group(1))
					if m.group(2):
						self.no_scanner = m.group(2) == '0'

				m = PLAYERSTATS.match(line)
				if m:
					ammo = int(m.group(2))
					lives = int(m.group(3))
					weapon_index = int(m.group(5))
					self.initial_player_stats = PlayerStats(ammo, lives, weapon_index-1, self.weapons)
				m = NAME.match(line)
				if m:
					self.name = m.group(1)
				m = COUNTDOWN.match(line)
				if m:
					delay = int(m.group(1))
					time = int(m.group(2))
					if m.group(3):
						fade = int(m.group(3))==1
					else:
						fade = True
					if m.group(4):
						shake = int(m.group(4))==1
					else:
						shake = True
					
					self._active_countdown = Countdown(delay, time, fade, shake, self.my_game.get_mixer(), self)
					
				line = a.readline()
		finally:
			a.close() 
			
		print_debug("num units read %d" % num_units_read, 5)
        
	
	def load_level_tile_meta(self, filename, tile_set):
		DIMENSIONS = re.compile('DIMENSIONS mapwidth=(\d*) mapheight=(\d*)')
		TILE = re.compile('TILE number=(\d*) type=(\S*) frequency=(\S*)')
		
		num_tiles_read = 0
    		a = open(get_config_pathname(filename), "r")
		try:
			line = a.readline()
			while line:
				print_debug(line,5)
				m = DIMENSIONS.match(line)
				if m:
	
					self.level_width=int(m.group(1))
					self.level_height=int(m.group(2))
					print_debug("Level dimensions %d %d" % (self.level_width, self.level_height), 5)
				m = TILE.match(line)
				if m:
					tile_num = int(m.group(1))
					tile_type = m.group(2)
					frequency = m.group(3)
					
					
					tile = tile_set[tile_num]
					tile.tile_type = tile_type
					tile.frequency = frequency
					
					print_debug("Tile meta %d %s %s" % (tile_num, tile_type, frequency), 5)
					
				num_tiles_read += 1		
				line = a.readline()
		finally:
			a.close() 
			
		print_debug("num tiles meta read %d" % num_tiles_read, 5)
        

	def load_units(self, unit_set):
		print_debug("Unit load units", 5)
		time = self.my_game.get_ticks()
		mixer = self.my_game.get_mixer()
		
		#Load the alien units (not referenced by level data)...
		for file in ('enemy1.uni','enemy2.uni','enemy3.uni','enemy4.uni', 'enemy5.uni', 'enemy6.uni', 'enemy7.uni', 'enemy8.uni', 'enemy9.uni', 'firebossworm.uni'):
			unit = U.UnitFactory.create_unit(file, mygame.Colour(0xff, 0, 0xff), mixer, self, time)	
			unit_set.add_alien_prototype(file, unit)

		
		for u in self.level_unit_instances:
			unit = U.UnitFactory.create_level_unit(u, mygame.Colour(0xff, 0, 0xff), mixer, self, time)
			
			#Keep note of the special units...
			print_debug(u.name, 5)
			if u.name == 'Player':
				unit_set.set_player_unit(unit)
				unit.set_player_stats(self.initial_player_stats)
				#Use level configured starting health if set
				if self.initial_player_health:
					unit.get_player_stats().set_health(self.initial_player_health)
				#clear the bluepass as you loose this at start of level
				unit.get_player_stats().blue_pass = False
				
				print_debug("Player at %f,%f"%(u.tileposx, u.tileposy),2)
				
			elif u.name == 'GunFire' or u.file ==  'gunfire.uni':
				#not all levels have a name configured for gunfire
				unit_set.set_gun_flare_unit(unit)
		
			elif u.name == 'Boss':
				unit_set.add_alien(unit)
						
			#level6 seems to include an enemy so need to check for that here
			elif u.file == 'enemy5.uni':
				unit_set.add_alien(unit)
				
			elif u.file == 'lift.uni':
				unit_set.add_lift(unit)
			
			elif unit.unit_definition.object_type == 'door':
				unit_set.add_door(unit)
					
			else:
				#add as a static unit
				unit_set.add_unit(unit)
		
			# keep a count of every dome created
			if unit.unit_definition.ai_type == 'dome' or unit.unit_definition.ai_type == 'egg' or unit.unit_definition.ai_type == 'hostage':
				self.level_state.add_dome()
		
			
		#Load the bullet unit (not referenced directly by level data)...
		for weapon in self.weapons.get_all_weapons():
			file = weapon.projectile
			#pygame.Color("#0000FF")
			unit = U.UnitFactory.create_unit(file, mygame.Colour(0xff, 0, 0xff), mixer, self, time)
			unit.set_additional_profile(weapon)
			unit_set.add_bullet_prototype(file, unit)

		#Load the small explosions...
		unit = U.UnitFactory.create_unit('explosionsmall.uni', mygame.Colour(0xff, 0, 0xff), mixer, self, time)	
		unit_set.set_small_explosion_unit(unit)
		#Load the big explosions....
		unit = U.UnitFactory.create_unit('explosionbig.uni', mygame.Colour(0xff, 0, 0xff), mixer, self, time)	
		unit_set.set_big_explosion_unit(unit)
		
	def update(self, time, display):
		if self.get_level_state().get_game_mode() == LevelState.INTEX or  self.get_level_state().get_game_mode() == LevelState.SCANNER:
			self.update_in_intex(time, display)
		
		elif self.get_level_state().get_game_mode() == LevelState.IN_GAME_MENU:
			self.update_in_game_menu(time, display)
			
		else:
			CollisionStats.get_instance().reset()
			self.update_not_in_intex(time, display)
			if DEBUG_COLLISIONS:
				CollisionStats.get_instance().debug_print()
			
	def update_not_in_intex(self, time, display):
		num_aliens_on_screen = 0
		
		for u in self.get_all_units():
			updated = u.update(time, display)
			if u.unit_definition.ai_type == 'alien' and updated:		
				num_aliens_on_screen +=1
		
		for c in self._delayed_commands:
			if c.update(time):
				self._delayed_commands.remove(c)
				
		if self._active_countdown:
			self._active_countdown.update(time, display)			
			
		self.check_for_entering_intex(display)
		self.check_for_in_game_menu(display)
		self.num_aliens_on_screen = num_aliens_on_screen
	
	def check_for_in_game_menu(self, display):
		kh = self.player_mover.get_key_handler()
		if kh.is_quit():
			self.get_level_state().enter_in_game_menu()
			self.in_game_menu.start()
	
	def check_for_entering_intex(self, display):
		kh = self.player_mover.get_key_handler()
		if kh.is_intex():
			
			at_intex_terminal = False
			if Cheats.getIntexAnywhere():
				at_intex_terminal = True
			
			if self.at_computer(display):	
				at_intex_terminal = True
				
			if at_intex_terminal:
				self.delayed_enter_intex(False)
			else:
				#todo check if have scanner
				if self.get_player().get_player_stats().has_scanner():
					self.delayed_enter_intex(True)
	
	def delayed_enter_intex(self, enter_scanner):
		if self.level_state.get_game_mode() != LevelState.TRANSITION and self.level_state.get_game_mode() != LevelState.INTEX and self.level_state.get_game_mode() != LevelState.SCANNER:
			
			delay_command  = DelayedEnterIntexCommand(self, enter_scanner)
			self._delayed_commands.append(delay_command)
			self.get_level_state().enter_transition()
	
	def at_computer(self, display):
		rect = self.get_player().get_rect()
		pos = []
		pos.append((rect.x, rect.y))
		pos.append((rect.x + rect.w, rect.y))
		pos.append((rect.x + rect.w, rect.y+rect.h))
		pos.append((rect.x, rect.y+rect.h))
		for p in pos:
			tiles = display.view_to_tile(p)
			tile = self.level_map_lower[tiles[1]][tiles[0]]
			if self.tile_set[tile].tile_type == 'computer':
				return True
		return False
			
	
	def update_in_intex(self, time, display):
		if self.get_level_state().get_game_mode() == LevelState.INTEX or  self.get_level_state().get_game_mode() == LevelState.SCANNER:
			self.intex_menu.update(time)
			if self.intex_menu.is_finished():
				self.intex_menu.finish()
				self.get_level_state().exit_intex()
				set_game_palette(self.my_game)
				display.palette_switched = False
				

	def update_in_game_menu(self, time, display):
		self.in_game_menu.update(time)
		if self.in_game_menu.is_finished():
			if self.in_game_menu.action == AbstractMenuController.ACTION_SAVE_GAME:
				self.save_game()
			
			elif self.in_game_menu.action == AbstractMenuController.ACTION_QUIT:
				self.game_over()
				
			elif self.in_game_menu.action == AbstractMenuController.ACTION_NEXT_LEVEL:
				self.level_complete()
			self.get_level_state().exit_intex()
			

	def construct_shared_movers(self, display):
		#setup movement for enemies...
		self.alien_mover = CM.AlienMovement(display, self.unit_set.get_alien_prototype('enemy1.uni'))
		#todo should not be here

		#setup movement for player...
		self.player_mover = CM.PlayerMovement (display, self.get_player(), self.my_game)

		#setup movement for bullet...
		self.bullet_mover = CM.BulletMovement(display, self.unit_set.get_bullet_prototype('firemachinegun.uni'))


	def get_player(self):
		return self.unit_set.get_player_unit()
	
	def get_lifts(self):
		return self.unit_set.get_lifts()
	
	def get_doors(self):
		return self.unit_set.get_doors()
	
	def add_new_alien_unit(self, uni_name, x, y):
		alien = self.unit_set.get_alien_prototype(uni_name)
		new_alien = alien.clone_unit(self.my_game.get_mixer(), self, self.my_game.get_ticks())
		new_alien.set_pos(x,y)
		print_debug("Creating new alien %s, %d,%d" % (uni_name, x, y),2)
		self.unit_set.add_alien(new_alien)
		return new_alien
	
	def get_bullet_dimensions(self, weapon_type):
		bullet = self.unit_set.get_bullet_prototype(weapon_type)
		return bullet.current_image().get_rect()
	
	def add_bullet_unit(self, weapon, x, y, state):
		weapon_type = weapon.projectile
		bullet = self.unit_set.get_bullet_prototype(weapon_type)
		new_bullet = bullet.clone_unit(self.my_game.get_mixer(), self, self.my_game.get_ticks())
		new_bullet.set_pos(x,y)
		new_bullet.enter_state(state, self.my_game.get_ticks())
		data = new_bullet.get_behaviour_data()
		data['weapon'] = weapon
		print_debug("Creating new bullet %s, %d,%d %s" % (weapon_type, x, y, state),2)
		
		if not new_bullet.is_current_position_blocked():
			self.unit_set.add_bullet(new_bullet)
			return True
		else:
			return False
		
	def get_gunfire_dimensions(self):
		return self.unit_set.get_gun_flare_unit().get_rect()


	def get_all_units(self):
		return self.unit_set.get_all_units()

	def get_units_for_collision_detection(self, rect):
		return self.unit_set.get_units_for_collision_detection(rect)

	def get_gun_flare_unit(self):
		return self.unit_set.get_gun_flare_unit()
	
	def get_small_explosion_unit(self):
		return self.unit_set.get_small_explosion()
	
	def add_small_explosion(self, x, y):
		explosion = self.unit_set.get_small_explosion_unit()
		sx = explosion.clone_unit(self.my_game.get_mixer(), self, self.my_game.get_ticks())
		sx.set_pos(x,y)
		print_debug("Creating new explosion %d,%d" % (x, y),2)
		
		self.unit_set.add_small_explosion(sx)
		
	def add_big_explosion(self, x, y):
		explosion = self.unit_set.get_big_explosion_unit()
		sx = explosion.clone_unit(self.my_game.get_mixer(), self, self.my_game.get_ticks())
		sx.set_pos(x,y)
		print_debug("Creating new explosion %d,%d" % (x, y),2)
		
		self.unit_set.add_big_explosion(sx)


	def add_random_explosions(self, rect, num, delay):
		for x in range(0, num):
			x = rect.x + get_random_int(0, rect.w)
			y = rect.y + get_random_int(0, rect.h)
			delay = get_random_int(0, delay)
			self._delayed_commands.append(DelayedExplosion(x,y,delay,self))
	
	def add_delay_command(self, command):
		self._delayed_commands.append(command)


	def get_level_state(self):
		return self.level_state	
		
	def level_complete(self):
		self.end_lev_sound.stop()
		delay_command  = DelayedLevelCompleteCommand(self, True)
		self._delayed_commands.append(delay_command)
		
	def game_over(self):
		self.end_lev_sound.stop()
		delay_command  = DelayedLevelCompleteCommand(self, False)
		self._delayed_commands.append(delay_command)
	
	
	def start_countdown(self):
		self._active_countdown.start_countdown()
		if not Cheats.getNoAudio():
			self.end_lev_sound.play(-1)
		
		
	def get_countdown(self):
		return self._active_countdown
		
	def close_door_by_name(self, name, time):
		door = self.unit_set.get_unit_by_name(name)
		if door:
			if door.current_state() != 'closing' and door.current_state() != 'closed':
				door.enter_state('closing', time)
	
	def open_door_by_name(self, name, time):
		door = self.unit_set.get_unit_by_name(name)
		if door:
			if door.current_state() != 'opening' and door.current_state() != 'open':
				door.enter_state('opening', time)
	
	
	def get_map_tile_size(self):
		return self.map_tile_width, self.map_tile_height
	
	def save_game(self):
		#Use the player stats at the start of the level...
		ps = self.initial_player_stats
		game_id = SaveGameUtil.new_id(self.level_num, self.name)
		game = SavedGame()
		game.create(ps, self.level_num)
		game.save(game_id)

	def get_num_aliens_on_scrreen(self):
		return self.num_aliens_on_screen
	
	def at_max_aliens_on_screen(self):
		return self.num_aliens_on_screen >= Level.MAX_AlIENS
	
	def enter_boss_mode(self):
		if not Cheats.getNoAudio():
			self.end_lev_sound.play(-1)
		self.level_state.set_game_mode(LevelState.BOSS)
		
