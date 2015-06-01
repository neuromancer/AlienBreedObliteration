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
import intex
from text import *
from savedgameutils import *

BIG_CURSOR_FILE='bigmenuselector.bmp'
CURSOR_FILE='menuselect.bmp'
SMALL_CURSOR_FILE='tinymenuselect.bmp'

class GameMenuCursor:
		
	def __init__(self):
		self.set_tile_info()
		self._last_update = None
		self.load_tiles()
		self.current_frame = 0	
	
	def set_tile_info(self):
		self.tile_width = 128
		self.tile_height = 16
		self.fname = CURSOR_FILE
		
	
	def update(self, time):
		if self._last_update:
			if time - self._last_update > intex.CURSOR_BLINK_RATE:
				self._last_update = time
				self.current_frame +=1
				if self.current_frame > 3:
					self.current_frame = 0	
		else:
			self._last_update = time

	def load_tiles(self):
		self.images, self.tile_width, self.tile_height = CompositeTileLoader.load_tiles(self.fname, self.tile_width, self.tile_height, mygame.Colour(0xff,0,0xff))

	def draw(self, screen, x, y):
		img = self.images[self.current_frame]
		screen.blit(img, (x, y))

	def get_green_tile(self):
		return self.images[0]
	
	def get_height(self):
		return self.images[0].get_height()
	
	def get_width(self):
		return self.images[0].get_width()


class GameMenuBigCursor(GameMenuCursor):
		
	def __init__(self):
		GameMenuCursor.__init__(self)
			
	def set_tile_info(self):
		self.tile_width = 380
		self.tile_height = 16
		self.fname = BIG_CURSOR_FILE


class AbstractMenuController:
	MAIN_MENU = 0
	SAVE_MENU = 1
	LOAD_MENU=2
	
	ACTION_MAIN_MENU=1
	ACTION_NONE=0
	ACTION_SAVE_MENU=2
	ACTION_LOAD_MENU=3
	ACTION_QUIT = 5
	ACTION_START_GAME = 6
	ACTION_LOAD_GAME = 7
	ACTION_BACK_TO_GAME = 8
	ACTION_SAVE_GAME = 9
	ACTION_CREDITS = 10
	ACTION_NEXT_LEVEL = 11
	
	def __init__(self, my_game):
		self.my_game = my_game
		self.key_handler = intex.MenuKeyHandler(my_game)
		self.finished = False
		self.menu_font = BreedFont(my_game.get_mixer())
		self.menu_cursor = GameMenuCursor()
		self.big_menu_cursor = GameMenuBigCursor()
		self.initialise_menus()
		
	def get_cursor(self):
		return self.menu_cursor
	
	def get_big_cursor(self):
		return self.big_menu_cursor
	
	
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
		if self.current_menu == AbstractMenuController.MAIN_MENU:
			menu = self.main_menu
		elif self.current_menu == AbstractMenuController.LOAD_MENU:
			menu = self.load_menu
		return menu
	
	def get_selected_menu_item(self):
		menu = self.get_current_menu()
		items = menu.menu_items
		return items[menu.current_row]
	
	def draw(self, screen):
		menu = self.get_current_menu()
		menu.draw(screen)
	
	def do_action(self, action):
		if action == AbstractMenuController.ACTION_QUIT:
			self.finished = True
			self.action = AbstractMenuController.ACTION_QUIT
		elif action == AbstractMenuController.ACTION_NEXT_LEVEL:
			self.finished = True
			self.action = AbstractMenuController.ACTION_NEXT_LEVEL
		elif action == AbstractMenuController.ACTION_START_GAME:
			self.finished = True
			self.action = AbstractMenuController.ACTION_START_GAME
		elif action == AbstractMenuController.ACTION_LOAD_GAME:
			self.finished = True
			self.action = AbstractMenuController.ACTION_LOAD_GAME
			self.additional_data = self.get_selected_menu_item().value
		elif action == AbstractMenuController.ACTION_BACK_TO_GAME:
			self.finished = True
			self.action = AbstractMenuController.ACTION_BACK_TO_GAME
		elif action == AbstractMenuController.ACTION_SAVE_GAME:
			self.finished = True
			self.action = AbstractMenuController.ACTION_SAVE_GAME
		elif action == AbstractMenuController.ACTION_CREDITS:
			self.finished = True
			self.action = AbstractMenuController.ACTION_CREDITS
			
		else:
			if action == AbstractMenuController.ACTION_MAIN_MENU:
				self.current_menu = AbstractMenuController.MAIN_MENU
			elif action == AbstractMenuController.ACTION_LOAD_MENU:
				self.current_menu = AbstractMenuController.LOAD_MENU
				
			
				
			self.get_current_menu().start()

	def is_finished(self):
		return self.finished
	
	def start(self):
		self.finished = False
		self.current_menu = AbstractMenuController.MAIN_MENU
		self.get_current_menu().start()
		self.additional_data =  None


class GameMenu(AbstractMenuController):
	def __init__(self, my_game):
		AbstractMenuController.__init__(self, my_game)
		
	def initialise_menus(self):	
		self.main_menu = GameMainMenuContent(self)
		self.load_menu = LoadGameMenuContent(self)
	
class ContinueMenu(AbstractMenuController):
	def __init__(self, my_game):
		AbstractMenuController.__init__(self, my_game)
		
	def initialise_menus(self):	
		self.main_menu = ContinueMenuContent(self)



class AbstractMenuContent(intex.AbstractMenu):
	LINE_HEIGHT = 15

	def __init__(self, menu_controller):
		self.menu_controller = menu_controller
	
		self.menu_items = self.define_menu_items()
		
		self.current_row = 0
		if self.cursor_type() == BIG_CURSOR_FILE:
			self.menu_cursor = menu_controller.get_big_cursor()
		else:
			self.menu_cursor = menu_controller.get_cursor()
		self.line_indent = -1

	def cursor_type(self):
		return CURSOR_FILE

	
	def draw(self, screen):
		if self.line_indent <0:
			self.line_indent = (SCREEN_X - self.menu_cursor.get_width()) /2 
			self.cursor_y_offset = -self.menu_cursor.get_height() /8
			
		y=self.get_start_y()
		x=self.line_indent
		menu_font = self.menu_controller.menu_font
		y+= AbstractMenuContent.LINE_HEIGHT * 2
		
		menu_items_start_y = y
		
		if self.should_fade_background():
			self.fade_background(y, screen)
		
		for mi in self.menu_items:
			menu_font.draw_line_centered(mi.text, y, screen)
			y += AbstractMenuContent.LINE_HEIGHT
			x = 0
			
		cursor_y = menu_items_start_y + self.current_row * AbstractMenuContent.LINE_HEIGHT
		self.menu_cursor.draw(screen, self.line_indent, cursor_y + self.cursor_y_offset)
	
	def should_fade_background(self):
		return False
	
	def fade_background(self,y, screen):
		if DEPTH != 8:
			#overlays not supported in 8 bit mode
			overlay = self.menu_controller.my_game.create_blank((SCREEN_X, SCREEN_Y-y))
			overlay.fill(mygame.Colour(0, 0, 0))
			overlay.set_alpha(164)
			screen.blit(overlay, (0,y))
	
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

	def set_menu_items(self, items):
		self.menu_items = items

if RESIZE:
	AbstractMenuContent.LINE_HEIGHT = int(AbstractMenuContent.LINE_HEIGHT * RESIZE_FACTOR)
	

class GameMainMenuContent(AbstractMenuContent):
	START_Y = 200
	
	def __init__(self, menu_controller):
		AbstractMenuContent.__init__(self, menu_controller)

	def define_menu_items(self):
		menu_items = []
		menu_items.append(intex.MenuItem("START GAME", AbstractMenuController.ACTION_START_GAME))
		menu_items.append(intex.MenuItem("LOAD GAME", AbstractMenuController.ACTION_LOAD_MENU))
		menu_items.append(intex.MenuItem("CREDITS", AbstractMenuController.ACTION_CREDITS))
		menu_items.append(intex.MenuItem("EXIT", AbstractMenuController.ACTION_QUIT))
		return menu_items

	def get_start_y(self):
		return GameMainMenuContent.START_Y

if RESIZE:
	GameMainMenuContent.START_Y = int(GameMainMenuContent.START_Y * RESIZE_FACTOR)


class ContinueMenuContent(AbstractMenuContent):
	START_Y = 250
		
	def __init__(self, menu_controller):
		AbstractMenuContent.__init__(self, menu_controller)

	def define_menu_items(self):
		menu_items = []
		menu_items.append(intex.MenuItem("CONTINUE", AbstractMenuController.ACTION_START_GAME))
		return menu_items
	
	def get_start_y(self):
		return ContinueMenuContent.START_Y

if RESIZE:
	ContinueMenuContent.START_Y = int(ContinueMenuContent.START_Y * RESIZE_FACTOR)
	
class LoadGameMenuContent(AbstractMenuContent):
	START_Y = 50
		
	def __init__(self, menu_controller):
		AbstractMenuContent.__init__(self, menu_controller)


	def cursor_type(self):
		return BIG_CURSOR_FILE

	def should_fade_background(self):
		return True
	

	def define_menu_items(self):
		menu_items =  []
		menu_items.append(intex.MenuItem("BACK", AbstractMenuController.ACTION_MAIN_MENU))
		return menu_items

	def get_start_y(self):
		return LoadGameMenuContent.START_Y

	def start(self):
		games = SaveGameUtil.get_saved_game_list()
		menu_items = []
		
		for g in games:
			menu_items.append(intex.MenuItem(g.name, AbstractMenuController.ACTION_LOAD_GAME, g))
				
		menu_items.append(intex.MenuItem("BACK", AbstractMenuController.ACTION_MAIN_MENU))
		
		self.set_menu_items(menu_items)

if RESIZE:
	LoadGameMenuContent.START_Y = int(LoadGameMenuContent.START_Y * RESIZE_FACTOR)
	
	
class InGameMenuContent(AbstractMenuContent):
	START_Y = SCREEN_Y / 2
		
	def __init__(self, menu_controller):
		AbstractMenuContent.__init__(self, menu_controller)

	def define_menu_items(self):
		menu_items = []
		menu_items.append(intex.MenuItem("BACK TO GAME", AbstractMenuController.ACTION_BACK_TO_GAME))
		menu_items.append(intex.MenuItem("SAVE GAME", AbstractMenuController.ACTION_SAVE_GAME))
		if Cheats.getCheatNextLevelMenu():
			menu_items.append(intex.MenuItem("NEXT LEVEL", AbstractMenuController.ACTION_NEXT_LEVEL))
		menu_items.append(intex.MenuItem("QUIT", AbstractMenuController.ACTION_QUIT))
		return menu_items
	
	def get_start_y(self):
		return InGameMenuContent.START_Y


	def start(self):
		self.current_row = 0
		
class InGameMenu(AbstractMenuController):
	def __init__(self, my_game):
		AbstractMenuController.__init__(self, my_game)
		
	def initialise_menus(self):	
		self.main_menu = InGameMenuContent(self)
