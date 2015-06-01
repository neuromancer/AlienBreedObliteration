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
#from collision2 import *
from tileloader import *
from text import *
from palette import *

MAP_BITS='mapbits.bmp'
CURSOR_FILE='cursor.bmp'
INTEX_START_SOUND='compstart.ogg'

class MenuBackground:
	
	def __init__(self):
		return
	
	def start(self):
		self.img = mygame.load_image(get_image_pathname('IntexBG.bmp'))
		self.img.set_colorkey(mygame.Colour(0xff, 0, 0xff))
		if RESIZE:
			self.img = self.img.scale((int(self.img.get_width()*HUD_RESIZE_FACTOR),int(self.img.get_height() *HUD_RESIZE_FACTOR)))

	def draw(self, screen):
		screen.blit(self.img, (0,0))



CURSOR_BLINK_RATE=100

class MenuCursor:
		
	def __init__(self):
		self._last_update = None
		self.fname = CURSOR_FILE		
		self.current_frame = 0	

	def start(self):
		self.tile_width = 8
		self.tile_height = 10
		self.load_tiles()
		
	def update(self, time):
		if self._last_update:
			if time - self._last_update > CURSOR_BLINK_RATE:
				self._last_update = time
				self.current_frame +=1
				if self.current_frame > 3:
					self.current_frame = 0	
		else:
			self._last_update = time

	def load_tiles(self):
		self.images, self.tile_width, self.tile_height = CompositeTileLoader.load_tiles(self.fname, self.tile_width, self.tile_height, None)
		

	def draw(self, screen, x, y):
		img = self.images[self.current_frame]
		screen.blit(img, (x, y))

	def get_green_tile(self):
		return self.images[0]
	
	def get_height(self):
		return self.images[0].get_height()
	
	def get_width(self):
		return self.images[0].get_width()
	
class MenuItem:
	
	def __init__(self, text, action, value = None):
		self.text = text
		self.action = action
		self.value = value
			
	def draw(self):
		return


class AbstractMenu:
		
	def up(self):
		return
	
	def down(self):
		return
	
	def left(self):
		return
	
	def right(self):
		return
	
	def select(self):
		return

	def update(self, time):
		return
	
	def start(self):
		return

class MainMenu(AbstractMenu):

	START_Y = 50
	LINE_HEIGHT = 15
	LINE_INDENT = 50
	CURSOR_INDENT = 100

	def __init__(self, menu_controller):
		self.menu_controller = menu_controller
		
		self.title = "INTEX MAIN MENU"
	
		self.menu_items = []
		self.menu_items.append(MenuItem("INTEX WEAPON SUPPLIES", Menu.ACTION_WEAPONS_MENU))
		self.menu_items.append(MenuItem("INTEX TOOL SUPPLIES", Menu.ACTION_TOOLS_MENU))
		self.menu_items.append(MenuItem("INTEX RADAR SERVICE", Menu.ACTION_RADAR_MENU))
		self.menu_items.append(MenuItem("MISSION OBJECTVE", Menu.ACTION_MISSION_MENU))
		self.menu_items.append(MenuItem("INTEX ENTERTAINING", Menu.ACTION_ENT_MENU))
		self.menu_items.append(MenuItem("GAME STATISTICS", Menu.ACTION_STATS_MENU))
		self.menu_items.append(MenuItem("INFORMATION DATABASE", Menu.ACTION_INFO_MENU))
		self.menu_items.append(MenuItem("ABORT INTEX NETWORK", Menu.ACTION_EXIT_MENU))

		self.current_row = 0
		self.menu_cursor = menu_controller.get_cursor()
		

	def draw(self, screen):
		y=MainMenu.START_Y
		x=MainMenu.LINE_INDENT
		menu_font = self.menu_controller.menu_font
		menu_font.draw_line_centered(self.title,y, screen)
		y+= MainMenu.LINE_HEIGHT * 2
		
		menu_items_start_y = y
		
		for mi in self.menu_items:
			menu_font.draw_line_centered(mi.text, y, screen)
			y += MainMenu.LINE_HEIGHT
			x = 0
			
		cursor_y = menu_items_start_y + self.current_row * MainMenu.LINE_HEIGHT
		self.menu_cursor.draw(screen, MainMenu.CURSOR_INDENT, cursor_y)
	
	def update(self, time):
		self.menu_cursor.update(time)
		
	def up(self):
		self.current_row -=1
		if self.current_row < 0:
			self.current_row = len(self.menu_items) -1
	
	def down(self):
		self.current_row +=1
		if self.current_row == len(self.menu_items):
			self.current_row = 0
	def select(self):
		menu_item = self.menu_items[self.current_row]
		return self.menu_controller.do_action(menu_item.action)

if RESIZE:
	MainMenu.START_Y = int(MainMenu.START_Y * RESIZE_FACTOR)
	MainMenu.LINE_HEIGHT = int(MainMenu.LINE_HEIGHT * RESIZE_FACTOR)
	MainMenu.LINE_INDENT = int(MainMenu.LINE_INDENT * RESIZE_FACTOR)
	MainMenu.CURSOR_INDENT = int(MainMenu.CURSOR_INDENT * RESIZE_FACTOR)


CURSOR_KEY_RATE = 400

class MenuKeyHandler:
	def __init__(self, my_game):
		self._last_update = None
		self._last_key_pressed = None
		self.my_game = my_game
		
	def update(self, time):
		self.key = None
		update = False
		if self._last_update:
			key_pressed = self.my_game.get_key_pressed()
			if self._last_key_pressed == key_pressed:	
				if time - self._last_update > CURSOR_KEY_RATE:
					update = True
			else:
				update = True
		else:
			update = True
			
		if update:		
			self._last_key_pressed = self.my_game.get_key_pressed()
			self._last_update = time
			
			if self.my_game.get_key_pressed() & mygame.MY_K_DOWN > 0:
				self.key = mygame.MY_K_DOWN
	
			if self.my_game.get_key_pressed() & mygame.MY_K_UP > 0:
				self.key = mygame.MY_K_UP
			
			if self.my_game.get_key_pressed() & mygame.MY_K_FIRE > 0:
				self.key = mygame.MY_K_FIRE
		
			if self.my_game.get_key_pressed() & mygame.MY_K_LEFT > 0:
				self.key = mygame.MY_K_LEFT
	
			if self.my_game.get_key_pressed() & mygame.MY_K_RIGHT > 0:
				self.key = mygame.MY_K_RIGHT
	

ENT_MENU_TEXT='gamemenuentertainment.txt'
INFO_MENU_TEXT='gamemenuinfo.txt'

class Menu:
	MAIN_MENU = 0
	ENT_MENU = 1
	MISSION_MENU=2
	RADAR_MENU=3
	INFO_MENU=4
	TOOLS_MENU=5
	STATS_MENU=6
	WEAPONS_MENU=7
	INTRO_MENU = 8
	OUTRO_MENU = 9
	
	ACTION_ENT_MENU=1
	ACTION_NONE=0
	ACTION_MAIN_MENU=2
	ACTION_MISSION_MENU=3
	ACTION_RADAR_MENU = 4
	ACTION_INFO_MENU = 5
	ACTION_TOOLS_MENU = 6
	ACTION_STATS_MENU = 7
	ACTION_WEAPONS_MENU = 8
	ACTION_EXIT_MENU = 9
	ACTION_QUIT = 10
	
	def __init__(self, my_game, level):
		self.my_game = my_game
		self.level = level
		self.menu_font = IntextMenuFont(my_game.get_mixer())
		self.menu_cursor = MenuCursor()
		self.intro_menu = IntexIntro(self)
		self.outro_menu = IntexOutro(self)
		self.main_menu = MainMenu(self)
		self.ent_menu = PageTextMenu(self)
		self.ent_menu.set_text_lines(load_text_file_as_string_array(get_config_pathname(ENT_MENU_TEXT)))
		self.mission_menu = PageTextMenu(self)
		self.mission_text = level.text_loader.get_mission_text()
		self.radar_menu = RadarMenu(self)
		self.info_menu = PageTextMenu(self)
		self.info_menu.set_text_lines(load_text_file_as_string_array(get_config_pathname(INFO_MENU_TEXT)))
		self.tools_menu = ToolsMenu(self)
		self.stats_menu = StatsMenu(self)
		self.weapons_menu = WeaponsMenu(self)
		self.menu_background = MenuBackground()
		self.key_handler = MenuKeyHandler(my_game)
		self.purchase_handler = PurchaseHandler(self)
		self.finished = False
	
	def get_cursor(self):
		return self.menu_cursor
	
	def update(self, time):
		self.key_handler.update(time)
		menu = self.get_current_menu()	
		if self.key_handler.key == mygame.MY_K_DOWN:
			menu.down()
		
		if self.key_handler.key == mygame.MY_K_UP > 0:
			menu.up()
		
		if self.key_handler.key == mygame.MY_K_LEFT:
			menu.left()
		
		if self.key_handler.key == mygame.MY_K_RIGHT:
			menu.right()
		
		if self.key_handler.key == mygame.MY_K_FIRE > 0:
			menu.select()
						
		menu.update(time)
	
	def get_current_menu(self):
		menu = None
		if self.current_menu == Menu.MAIN_MENU:
			menu = self.main_menu
		elif self.current_menu == Menu.ENT_MENU:
			menu = self.ent_menu
		elif self.current_menu ==  Menu.MISSION_MENU:
			menu = self.mission_menu
		elif self.current_menu ==  Menu.RADAR_MENU:
			menu = self.radar_menu
		elif self.current_menu ==  Menu.INFO_MENU:
			menu = self.info_menu
		elif self.current_menu ==  Menu.TOOLS_MENU:
			menu = self.tools_menu
		elif self.current_menu ==  Menu.STATS_MENU:
			menu = self.stats_menu
		elif self.current_menu ==  Menu.WEAPONS_MENU:
			menu = self.weapons_menu
		elif self.current_menu == Menu.INTRO_MENU:
			menu = self.intro_menu
		elif self.current_menu == Menu.OUTRO_MENU:
			menu = self.outro_menu
	
		return menu
	
	def draw(self, screen):
		screen.fill(mygame.Colour(0,0,0))
		self.menu_background.draw(screen)
		menu = self.get_current_menu()
		menu.draw(screen)
	
	def do_action(self, action):
		if action == Menu.ACTION_QUIT:
			self.finished = True
		else:
			if action == Menu.ACTION_ENT_MENU:
				self.current_menu = Menu.ENT_MENU
			elif action == Menu.ACTION_MAIN_MENU:
				if self.in_sanner_only:
					self.finished = True
				else:
					self.current_menu = Menu.MAIN_MENU
			elif action == Menu.ACTION_MISSION_MENU:
				self.current_menu = Menu.MISSION_MENU
			elif action == Menu.ACTION_RADAR_MENU:
				self.current_menu = Menu.RADAR_MENU
			elif action == Menu.ACTION_INFO_MENU:
				self.current_menu = Menu.INFO_MENU
			elif action == Menu.ACTION_TOOLS_MENU:
				self.current_menu = Menu.TOOLS_MENU
			elif action == Menu.ACTION_STATS_MENU:
				self.current_menu = Menu.STATS_MENU
			elif action == Menu.ACTION_WEAPONS_MENU:
				self.current_menu = Menu.WEAPONS_MENU
			elif action == Menu.ACTION_EXIT_MENU:
				self.current_menu = Menu.OUTRO_MENU
				
			self.get_current_menu().start()

	def is_finished(self):
		return self.finished
	
	def start(self):
		self.init_components()
		self.finished = False
		self.current_menu = Menu.INTRO_MENU
		self.get_current_menu().start()
		self.in_sanner_only = False
		
		
	def init_components(self):
		#Set correct palette and force image load...
		set_intex_palette(self.my_game)
		self.menu_font.start()
		self.weapons_menu.start()
		self.menu_background.start()
		self.intro_menu.start()
		self.menu_cursor.start()
		#Force formatting of text now tiles have been loaded
		self.mission_menu.set_text(self.mission_text)
		
	def finish(self):
		set_game_palette(self.my_game)
		
				
	def start_scanner(self):
		self.init_components()
		self.finished = False
		self.current_menu = Menu.RADAR_MENU
		self.get_current_menu().start()
		self.in_sanner_only = True
		
	
		
class PageTextMenu(AbstractMenu):
	PAGE_HEIGHT = 14
	PAGE_WIDTH = 250
	MODE_CENTRE = 0
	MODE_LEFT = 1
	LEFT_INDENT=50
	CURSOR_INDENT=50
	
	def __init__(self, menu_controller):
		self.current_row = 0
		self.menu_controller = menu_controller
		self.font = self.menu_controller.menu_font
		self.menu_cursor = menu_controller.get_cursor()
			
	def set_text_lines(self, text_lines):
		self.text_lines = text_lines
		self.mode = PageTextMenu.MODE_CENTRE
		
	
	def set_text(self, text):
		self.text_lines = self.font.format_string(text.upper(), PageTextMenu.PAGE_WIDTH)
		self.mode = PageTextMenu.MODE_LEFT
	
	
	def draw(self, screen):
		menu_font = self.menu_controller.menu_font
		ti = self.current_row
		y = MainMenu.START_Y
		for r in range(ti, ti + PageTextMenu.PAGE_HEIGHT):
			if r < len(self.text_lines):
				text = self.text_lines[r]
				if self.mode == PageTextMenu.MODE_CENTRE:
					menu_font.draw_line_centered(text.upper().strip(), y, screen)
				else:
					menu_font.draw_line(text.upper().strip(), PageTextMenu.LEFT_INDENT, y, screen)
					
			y+= MainMenu.LINE_HEIGHT
		self.menu_cursor.draw(screen, PageTextMenu.CURSOR_INDENT, y)
		
	def update(self, time):
		self.menu_cursor.update(time)
	
	def select(self):
		self.menu_controller.do_action(Menu.ACTION_MAIN_MENU)

	def down(self):
		self.current_row+=1
	
	def up(self):
		if self.current_row > 0:
			self.current_row-=1

	def start(self):
		self.current_row = 0


if RESIZE:
	PageTextMenu.PAGE_WIDTH = int(PageTextMenu.PAGE_WIDTH * RESIZE_FACTOR)
	PageTextMenu.LEFT_INDENT = int(PageTextMenu.LEFT_INDENT * RESIZE_FACTOR)
	PageTextMenu.CURSOR_INDENT = int(PageTextMenu.CURSOR_INDENT * RESIZE_FACTOR)

class RadarMenu(AbstractMenu):
	
	X_START = 75
	Y_START = 50
	TITLE_Y = 25
	TILE_X_RATIO = 3
	TILE_Y_RATIO = 4
	
	NOTHING = 0
	WALL = 1
	DOOR = 2
	LIFT = 3
	INTEX = 4
	
	def __init__(self, menu_controller):
		self.level = menu_controller.level
		self.scanner_not_available = self.level.no_scanner
		self.menu_controller = menu_controller
		
	def start(self):
		self.menu_cursor = self.menu_controller.get_cursor()
		self.menu_font = self.menu_controller.menu_font
		self.__configure_block_tile()
		
	def __configure_block_tile(self):
		green_tile = self.menu_cursor.get_green_tile()
		self.wall_tile = green_tile.scale((green_tile.get_width()/RadarMenu.TILE_X_RATIO,green_tile.get_height()/RadarMenu.TILE_Y_RATIO))

		self.wall_tile_width = self.wall_tile.get_width()
		self.wall_tile_height = self.wall_tile.get_height()
		
		self.images, self.tile_width, self.tile_height = CompositeTileLoader.load_tiles(MAP_BITS, 2, 2, None)
		
		self.intex_tile = self.images[3].scale((green_tile.get_width()/RadarMenu.TILE_X_RATIO,green_tile.get_height()/RadarMenu.TILE_Y_RATIO))
		
		self.door_tile = None
		self.lift_tile = None 
				
	def draw(self, screen):
		self.menu_font.draw_line_centered("INTEX RADAR", RadarMenu.TITLE_Y, screen)
		
		if self.scanner_not_available:
			self.draw_radar_not_available(screen)
		else:
			self.draw_radar(screen)
	
	def draw_radar_not_available(self, screen):
		yy = screen.get_height() / 2
		self.menu_font.draw_line_centered("UNABLE TO REMOTE SCAN IMMEDIATE AREA", yy, screen)
		
		
	
	def draw_radar(self, screen):		
		xx = RadarMenu.X_START
		yy = RadarMenu.Y_START
		for y in range(0, self.level.level_height):
			for x in range(0,self.level.level_width):
				tile_type = self._get_tile_type(x,y)
				 
				if tile_type == RadarMenu.WALL:
					#plot a block
					screen.blit(self.wall_tile, (xx, yy))
					
				elif tile_type == RadarMenu.INTEX:
					#plot an intex block
					screen.blit(self.intex_tile, (xx, yy))
								
				xx+= self.wall_tile_width
			xx = RadarMenu.X_START
			yy += self.wall_tile_height
		
		self.draw_doors(screen)
		self.draw_lifts(screen)
		self.draw_player(screen)
		
	def _get_tile_type(self, x, y):
		lower_tile = int(self.level.level_map_lower[y][x])
		upper_tile = int(self.level.level_map_upper[y][x])
		
		lower_type = self.level.tile_set[lower_tile].tile_type
		upper_type = self.level.tile_set[upper_tile].tile_type
		
		if (lower_type == 'obstruction' or upper_type == 'obstruction'):
			return RadarMenu.WALL
		
		elif (lower_type == 'computer' or upper_type == 'computer'):
			return RadarMenu.INTEX
		
		else:
			return RadarMenu.NOTHING

	
	def draw_player(self, screen):
		pu = self.level.get_player()
		rx,ry,w,h = self._calc_unit_position(pu)
		self.menu_cursor.draw(screen, rx, ry)
		
	def _calc_unit_position(self, pu):
		r = pu.get_rect()
		p_x = pos = r.x
		p_y = pos = r.y
		mw,mh = self.level.get_map_tile_size()
		rx= p_x/mw*self.wall_tile_width + RadarMenu.X_START 
		ry=p_y/mh*self.wall_tile_height + RadarMenu.Y_START 
		w = r.w/mw*self.wall_tile_width
		h = r.h/mw*self.wall_tile_width
		
		return rx,ry,w,h
	
	def draw_lifts(self, screen):
		pus = self.level.get_lifts()
		for lift in pus:
			rx,ry,w,h = self._calc_unit_position(lift)
			if not self.lift_tile:
				self.lift_tile = self.images[1].scale((w,h))
				
			screen.blit(self.lift_tile, (rx, ry))
		
	def draw_doors(self, screen):
		doors = self.level.get_doors()
		for door in doors:
			if door.current_state() != 'open':
				rx,ry,w,h = self._calc_unit_position(door)
				if not self.door_tile:
					self.door_tile = self.images[2].scale((w,h))
				screen.blit(self.door_tile, (rx, ry))
		
	
		
	def update(self, time):
		self.menu_cursor.update(time)
		
	def select(self):
		self.menu_controller.do_action(Menu.ACTION_MAIN_MENU)


if RESIZE:
	RadarMenu.X_START = int(RadarMenu.X_START * RESIZE_FACTOR)
	RadarMenu.Y_START = int(RadarMenu.Y_START * RESIZE_FACTOR)
	RadarMenu.TITLE_Y = int(RadarMenu.TITLE_Y * RESIZE_FACTOR)


class ToolsMenu(AbstractMenu):
	TITLE_Y = 25
	START_Y = 50
	LINE_HEIGHT = 15
	LINE_INDENT = 65
	CURSOR_INDENT = 50
	MSG_DELAY = 2000
	
	def __init__(self, menu_controller):
		self.menu_controller = menu_controller
		self.menu_cursor = menu_controller.get_cursor()
		self.menu_font = menu_controller.menu_font
		self.weapons = self.menu_controller.level.weapons
		
		self.current_row = 0
		self.last_tool_row = len(self.weapons.get_all_tools()) - 1
		self.exit_row = self.last_tool_row + 2
		self.credit_row = self.exit_row + 2
		self.msg = None
		self.msg_time = None
		
	def draw(self, screen):
		stats = self.menu_controller.level.get_player().get_player_stats()
		self.menu_font.draw_line_centered("INTEX TOOL SUPPLIES", ToolsMenu.TITLE_Y, screen)
		self.menu_cursor.draw(screen, ToolsMenu.CURSOR_INDENT, ToolsMenu.START_Y + self.current_row * ToolsMenu.LINE_HEIGHT)
		
		y = ToolsMenu.START_Y
		for tool in self.weapons.get_all_tools():
			self.menu_font.draw_line(tool.desc.upper(), ToolsMenu.LINE_INDENT, y, screen)
			y+= ToolsMenu.LINE_HEIGHT
	
	
		
		self.menu_font.draw_line_centered("EXIT", ToolsMenu.START_Y + self.exit_row * ToolsMenu.LINE_HEIGHT, screen)
	
		if self.msg:
			text = self.msg
		else:
			text = "CREDIT LIMT : %d CR" % stats.money
		self.menu_font.draw_line(text, ToolsMenu.LINE_INDENT, ToolsMenu.START_Y + self.credit_row * ToolsMenu.LINE_HEIGHT, screen)
	
	def update(self, time):
		self.menu_cursor.update(time)
		if self.msg:
			if not self.msg_time:
				self.msg_time = time
			else:
				if time > self.msg_time + ToolsMenu.MSG_DELAY:
					self.msg = None
					self.msg_time = None
		
	def down(self):
		self.current_row+=1
		if self.current_row == self.last_tool_row + 1:
			self.current_row = self.exit_row
		elif self.current_row > self.exit_row:
			self.current_row = 0
	
	def up(self):
		self.current_row-=1
		if self.current_row < 0:
			self.current_row = self.exit_row

		if self.current_row == self.exit_row -1:
			self.current_row = self.last_tool_row
			
	def select(self):
		if self.current_row == self.exit_row:
			self.menu_controller.do_action(Menu.ACTION_MAIN_MENU)
		else:
			
			result = self.menu_controller.purchase_handler.check_and_purchase(self.current_row)
			if result == PurchaseHandler.ALREADY_PURCHASED:
				self.display_already_has()
			elif result == PurchaseHandler.NO_CREDITS:
				self.display_no_credit()
			elif result == PurchaseHandler.PURCHASED:
				self.display_purchased()
	
	def display_purchased(self):
		self.msg = "TOOL PURCHASED"
	def display_no_credit(self):
		self.msg = "NOT ENOUGH CREDITS"
	
	def display_already_has(self):
		self.msg = "ALREADY PURCHASED"

	def start(self):
		self.current_row = self.exit_row

if RESIZE:
	ToolsMenu.TITLE_Y = int(ToolsMenu.TITLE_Y * RESIZE_FACTOR)
	ToolsMenu.START_Y = int(ToolsMenu.START_Y * RESIZE_FACTOR)
	ToolsMenu.LINE_HEIGHT = int(ToolsMenu.LINE_HEIGHT * RESIZE_FACTOR)
	ToolsMenu.LINE_INDENT = int(ToolsMenu.LINE_INDENT * RESIZE_FACTOR)
	ToolsMenu.CURSOR_INDENT = int(ToolsMenu.CURSOR_INDENT * RESIZE_FACTOR)



PURCHASE_WEAPON_SOUND=INTEX_START_SOUND
PURCHASE_AMMO_SOUND='ammo.ogg'
PURCHASE_KEY_SOUND='key.ogg'
PURCHASE_HEALTH_SOUND='money.ogg'
PURCHASE_LIFE_SOUND='life.ogg'

class PurchaseHandler:
	
	ALREADY_PURCHASED = 1
	NO_CREDITS = 2
	PURCHASED = 3
	
	def __init__(self, menu_controller):
		self.menu_controller = menu_controller
		self.weapons = self.menu_controller.level.weapons
		mixer = self.menu_controller.my_game.get_mixer()
		self.weapon_sound = mixer.Sound(get_sound_pathname(PURCHASE_WEAPON_SOUND))
		self.ammo_sound = mixer.Sound(get_sound_pathname(PURCHASE_AMMO_SOUND))
		self.key_sound = mixer.Sound(get_sound_pathname(PURCHASE_KEY_SOUND))
		self.health_sound = mixer.Sound(get_sound_pathname(PURCHASE_HEALTH_SOUND))
		self.life_sound = mixer.Sound(get_sound_pathname(PURCHASE_LIFE_SOUND))
		
		
	def check_and_purchase(self, selected_row):
		stats = self.menu_controller.level.get_player().get_player_stats()
		weapon = self.weapons.get_all_tools()[selected_row]
		
		if weapon.name == 'scanner':
			if not stats.has_scanner():
				if stats.money >= weapon.cost:
					stats.money -= weapon.cost
					stats.set_scanner(True)
					if not Cheats.getNoAudio():
						self.weapon_sound.play()
					return PurchaseHandler.PURCHASED
				else:
					return PurchaseHandler.NO_CREDITS	
			else:
				return PurchaseHandler.ALREADY_PURCHASED
				
		else:
			if stats.money >= weapon.cost:
				stats.money -= weapon.cost
				if weapon.name == 'additionallife':
					stats.add_life()
					if not Cheats.getNoAudio():
						self.life_sound.play()
					
				elif weapon.name == 'ammopack':
					stats.add_ammo_pack()
					if not Cheats.getNoAudio():
						self.ammo_sound.play()
					
				elif weapon.name == 'energypack':
					stats.add_energy_pack()
					if not Cheats.getNoAudio():
						self.health_sound.play()
					
				elif weapon.name == 'keypack':
					stats.add_key(10)
					if not Cheats.getNoAudio():
						self.key_sound.play()
					
				return PurchaseHandler.PURCHASED
				
			else:
				return PurchaseHandler.NO_CREDITS


	def check_and_purchase_weapon(self, selected_weapon):
		stats = self.menu_controller.level.get_player().get_player_stats()
		weapon = self.weapons.get_all_weapons()[selected_weapon]
		if not stats.has_weapon(selected_weapon):
			if stats.money >= weapon.cost:
				stats.money -= weapon.cost
				stats.set_has_weapon(selected_weapon)
				if not Cheats.getNoAudio():
					self.weapon_sound.play()
				return PurchaseHandler.PURCHASED
			else:
				return PurchaseHandler.NO_CREDITS
		

class StatsMenu(AbstractMenu):
	TITLE_Y = 25
	START_Y = 50
	LINE_HEIGHT = 15
	LINE_INDENT = 50
	
	def __init__(self, menu_controller):
		self.menu_controller = menu_controller
		self.menu_cursor = menu_controller.get_cursor()
		self.menu_font = menu_controller.menu_font
		self.current_row = 0
		
	def draw(self, screen):
		stats = self.menu_controller.level.get_player().get_player_stats()
		self.menu_font.draw_line_centered("PLAYER STATISTICS", StatsMenu.TITLE_Y, screen)
	
		self.display(ToolsMenu.LINE_INDENT, 2, "LIVES            %d" % stats.lives,screen)
		
		self.display(ToolsMenu.LINE_INDENT, 3, "HEALTH           %d" % stats.get_health(),screen)
	
		self.display(ToolsMenu.LINE_INDENT, 4, "AMMO             %d" % stats.ammo, screen)
		
		self.display(ToolsMenu.LINE_INDENT, 5, "KEYS             %d" % stats.keys(),screen)
	
		if stats.has_scanner():
			self.display(ToolsMenu.LINE_INDENT, 6, "SCANNER          YES",screen)
		else:
			self.display(ToolsMenu.LINE_INDENT, 6, "SCANNER          NO",screen)
	
		self.display(ToolsMenu.LINE_INDENT, 7, "CREDITS          %d" % stats.money,screen)
	
		row = 8
		weapon_index = 0
		for w in stats.weapons.get_all_weapons():
			
			if stats.has_weapon(weapon_index):
				self.display(ToolsMenu.LINE_INDENT, row, "                 YES",screen)
			else:
				self.display(ToolsMenu.LINE_INDENT, row, "                 NO",screen)
				
			self.display(ToolsMenu.LINE_INDENT, row, w.name.upper(),screen)	
			weapon_index+=1
			row+=1
	
	
	def display(self, x, y, msg, screen):
		self.menu_font.draw_line(msg, x, ToolsMenu.START_Y + y * ToolsMenu.LINE_HEIGHT, screen)
	

	def select(self):
		self.menu_controller.do_action(Menu.ACTION_MAIN_MENU)
	
	def update(self, time):
		return 

if RESIZE:
	StatsMenu.TITLE_Y = int(StatsMenu.TITLE_Y * RESIZE_FACTOR)
	StatsMenu.START_Y = int(StatsMenu.START_Y * RESIZE_FACTOR)
	StatsMenu.LINE_HEIGHT = int(StatsMenu.LINE_HEIGHT * RESIZE_FACTOR)
	StatsMenu.LINE_INDENT = int(StatsMenu.LINE_INDENT * RESIZE_FACTOR)



WEAPON_IMAGES='allweaps.bmp'

class WeaponsMenu(AbstractMenu):
	TITLE_Y = 25
	MSG_DELAY = 2000
	IMG_X = 84
	IMG_Y = 135
	LINE_HEIGHT = 15
	LINE_INDENT = 20
	PURCHASE_ROW = 15
	EXIT_ROW = 16
	CURSOR_INDENT = 100
	
	def __init__(self, menu_controller):
		self.menu_controller = menu_controller
		self.weapons = self.menu_controller.level.weapons
		self.current_weapon = 0
		self.msg = None
		self.current_row = 0
		self.msg_time = None
		
	def start(self):
		self.current_row = WeaponsMenu.EXIT_ROW
		#Reload image resources (to ensure correct palette)
		self.menu_cursor = self.menu_controller.get_cursor()
		self.menu_font = self.menu_controller.menu_font
		self.load_tiles()
		
	def load_tiles(self):
		self.trans = mygame.Colour(0xff,0,0xff)
		self.tile_width = 256
		self.tile_height = 128
		self.images, self.tile_width, self.tile_height = CompositeTileLoader.load_tiles(WEAPON_IMAGES, self.tile_width, self.tile_height, self.trans, HUD_RESIZE_FACTOR)
		
	def draw(self, screen):
		stats = self.menu_controller.level.get_player().get_player_stats()
		self.menu_font.draw_line_centered("INTEX WEAPON SUPPLIES", StatsMenu.TITLE_Y, screen)
		
		weapon = self.weapons.get_all_weapons()[self.current_weapon]
		img = self.images[weapon.tile]
		
		y = StatsMenu.TITLE_Y + WeaponsMenu.LINE_HEIGHT *2
		
		self.menu_font.draw_line_centered(weapon.desc.upper(), y, screen)
		
		y += WeaponsMenu.LINE_HEIGHT *2
		
		
		cost = "                     CREDIT LIMIT : %d CR" % stats.money
		self.menu_font.draw_line(cost, WeaponsMenu.LINE_INDENT, y, screen)
		
		cost = "COST : %d CR" % weapon.cost
		self.menu_font.draw_line(cost, WeaponsMenu.LINE_INDENT, y, screen)
		
		screen.blit(img, (WeaponsMenu.IMG_X, WeaponsMenu.IMG_Y))
	
		
			
		if self.msg:
			text = self.msg
		else:
			if stats.has_weapon(self.current_weapon):
				text = "ALREADY PURCHASED"
			else:
				text = "PURCHASE"
		
		y = WeaponsMenu.PURCHASE_ROW * WeaponsMenu.LINE_HEIGHT + WeaponsMenu.TITLE_Y
		self.menu_font.draw_line_centered(text, y, screen)
		y = WeaponsMenu.EXIT_ROW * WeaponsMenu.LINE_HEIGHT + WeaponsMenu.TITLE_Y
		self.menu_font.draw_line_centered("EXIT", y, screen)
	
		self.menu_cursor.draw(screen, WeaponsMenu.CURSOR_INDENT, WeaponsMenu.TITLE_Y + self.current_row * WeaponsMenu.LINE_HEIGHT)
		
	
	def update(self, time):
		self.menu_cursor.update(time)
		if self.msg:
			if not self.msg_time:
				self.msg_time = time
			else:
				if time > self.msg_time + ToolsMenu.MSG_DELAY:
					self.msg = None
					self.msg_time = None
	
	
	def select(self):
		if self.current_row == WeaponsMenu.EXIT_ROW:
			self.menu_controller.do_action(Menu.ACTION_MAIN_MENU)
		else:			
			result = self.menu_controller.purchase_handler.check_and_purchase_weapon(self.current_weapon)
			if result == PurchaseHandler.ALREADY_PURCHASED:
				self.display_already_has()
			elif result == PurchaseHandler.NO_CREDITS:
				self.display_no_credit()
			elif result == PurchaseHandler.PURCHASED:
				self.display_purchased()
	

	def display_purchased(self):
		self.msg = "WEAPON PURCHASED"
	def display_no_credit(self):
		self.msg = "NOT ENOUGH CREDITS"
	
	def left(self):
		if self.current_weapon > 0:
			self.current_weapon -= 1
		else:
			 self.current_weapon = len(self.weapons.get_all_weapons()) -1

	def right(self):
		if self.current_weapon < len(self.weapons.get_all_weapons()) -1:
			self.current_weapon += 1
		else:
			 self.current_weapon = 0

	def up(self):
		if self.current_row == WeaponsMenu.PURCHASE_ROW:
			self.current_row = WeaponsMenu.EXIT_ROW
		elif self.current_row == WeaponsMenu.EXIT_ROW:
			self.current_row = WeaponsMenu.PURCHASE_ROW

	def down(self):
		self.up()

	

#84,135
#width=256x128

if RESIZE:
	WeaponsMenu.TITLE_Y = int(WeaponsMenu.TITLE_Y * RESIZE_FACTOR)
	WeaponsMenu.IMG_X = int(WeaponsMenu.IMG_X * HUD_RESIZE_FACTOR)
	WeaponsMenu.IMG_Y = int(WeaponsMenu.IMG_Y * HUD_RESIZE_FACTOR)
	WeaponsMenu.LINE_HEIGHT = int(WeaponsMenu.LINE_HEIGHT * RESIZE_FACTOR)
	WeaponsMenu.LINE_INDENT = int(WeaponsMenu.LINE_INDENT * RESIZE_FACTOR)
	WeaponsMenu.CURSOR_INDENT = int(WeaponsMenu.CURSOR_INDENT *RESIZE_FACTOR)
	
	
INTEXT_INTRO_TEXT = 'gamemenuintro.txt'
WELCOME_SOUND = 'welcome.ogg'

class IntexIntro(AbstractMenu):
	TEXT_X = 25
	TEXT_Y = 25
	TEXT_W = 800  #so large auto font wrapping will not occur
	TEXT_H = 200
	DELAY = 1000
	
	def __init__(self, menu_controller):
		self.menu_controller = menu_controller		
		self.mixer = menu_controller.my_game.get_mixer()
		self.welcome_sound = self.mixer.Sound(get_sound_pathname(WELCOME_SOUND))
		self.comp_start_sound = self.mixer.Sound(get_sound_pathname(INTEX_START_SOUND))
		self.last_update = 0
		
		
	def start(self):
		#Reload image resources nw we are in correct palette
		self.menu_cursor = self.menu_controller.menu_cursor
		self.ticker_font = IntexTickerFont(self.mixer)
		self.menu_font = self.menu_controller.menu_font


		if not Cheats.getNoAudio():
			self.comp_start_sound.play()		
			
		self.font_rect = mygame.Rect(IntexIntro.TEXT_X, IntexIntro.TEXT_Y, IntexIntro.TEXT_W, IntexIntro.TEXT_H)
		
		text = load_text_file_as_string(get_config_pathname(INTEXT_INTRO_TEXT))
	
		self.ticker_font.set_ticker_text(text.upper(), self.font_rect)
		
		self.ticker_font.delay = 0
		self.ticker_font.char_increment = 8
		self.in_ticker = False
		
		
	def update(self, time):
		#show Intex text briefly and then resume ticker...
		
		if self.last_update == 0:
			self.last_update = time
		else:
			if time > self.last_update + IntexIntro.DELAY and not self.in_ticker:
				self.in_ticker = True
				if not Cheats.getNoAudio():
					self.welcome_sound.play()
			else:
				self.menu_cursor.update(time)
				
			if self.in_ticker:
				self.ticker_font.update(time)
				if self.ticker_font.finished():
					self.menu_controller.do_action(Menu.ACTION_MAIN_MENU)
		
	def draw(self, screen):
		if self.in_ticker:
			#display ticker text...
			self.ticker_font.draw(screen)
		else:
			#Display startix intex text
			self.menu_font.draw_line("INTEX", IntexIntro.TEXT_X, IntexIntro.TEXT_Y, screen)
			self.menu_cursor.draw(screen, IntexIntro.TEXT_X + 5 * self.menu_font.font_width, IntexIntro.TEXT_Y)
	

if RESIZE:
	IntexIntro.TEXT_X = int(IntexIntro.TEXT_X * RESIZE_FACTOR)
	IntexIntro.TEXT_Y = int(IntexIntro.TEXT_Y * RESIZE_FACTOR)
	IntexIntro.TEXT_W = int(IntexIntro.TEXT_W * RESIZE_FACTOR)
	IntexIntro.TEXT_H = int(IntexIntro.TEXT_H * RESIZE_FACTOR)
	
INTEXT_OUTRO_TEXT = 'gamemenuoutro.txt'	
INTEX_END_SOUND='compend.ogg'
class IntexOutro(AbstractMenu):
	
	def __init__(self, menu_controller):
		self.menu_controller = menu_controller
		self.menu_cursor = menu_controller.menu_cursor
		mixer = menu_controller.my_game.get_mixer()
		self.comp_end_sound = mixer.Sound(get_sound_pathname(INTEX_END_SOUND))
		self.menu_font = menu_controller.menu_font
		
	def start(self):
		self.text = load_text_file_as_string(get_config_pathname(INTEXT_OUTRO_TEXT))
		self.last_update = 0
		self.finished = False
		
	def update(self, time):
		if self.last_update == 0:
			self.last_update = time
		else:
			if time > self.last_update + IntexIntro.DELAY and not self.finished:
				if not Cheats.getNoAudio():
					self.comp_end_sound.play()
				self.finished = True
				self.menu_controller.do_action(Menu.ACTION_QUIT)
			else:
				self.menu_cursor.update(time)
					
		
	def draw(self, screen):
		self.menu_font.draw_line(self.text.upper(), IntexIntro.TEXT_X, IntexIntro.TEXT_Y, screen)
		self.menu_cursor.draw(screen, IntexIntro.TEXT_X +  len(self.text) * self.menu_font.font_width, IntexIntro.TEXT_Y)
	
