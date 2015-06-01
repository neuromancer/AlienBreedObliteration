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
 
import re,gc
import mygame as mygame
from level import *
from weapons import *
from utils import *
from text import *
from level_text import *
from gamemenu import *
from star import *
from credit import *
from display import *
#from display2 import *
from palette import *

if not WII:
	import time as _time

MENU_BACKGROUND_SOUND='menu.xm'
LEVEL_BACKGROUND_SOUND='background.ogg'
END_GAME_SOUND ='end.xm'

DEBUG_TIMINGS=False
 
class Scene:
			
	SCENE_CONTINUE = 1
	SCENE_END_SUCCESS = 2
	SCENE_END_FAILURE = 3
	SCENE_LOAD_GAME = 4
	SCENE_CREDITS = 5
	SCENE_DEMO = 6
	
	def update_and_draw(self, time):
		return
	
	def __init__(self, name):
		self.name = name

	def start(self):
		return
		
	def stop(self):
		return


class MenuBackground:
	def __init__(self, my_game):
		self.background_sound = my_game.get_mixer().Music(get_sound_pathname(MENU_BACKGROUND_SOUND))
		self.star = StarField(mygame.Rect(0,0,SCREEN_X, SCREEN_Y))
		self.my_game=my_game
		self.playing = False
		
	def start(self):
		if not self.playing:
			self.background_sound = self.my_game.get_mixer().Music(get_sound_pathname(MENU_BACKGROUND_SOUND))
			if not Cheats.getNoAudio():
				self.background_sound.play(-1)
			self.star.start()
			self.playing = True

	def stop(self):
		if self.background_sound:
			self.background_sound.stop()
		self.playing = False
		self.background_sound = None

	def update_and_draw(self, time):
		self.star.update(time)
		self.star.draw(self.my_game.get_screen())

class MenuScene(Scene):
		
	def __init__(self, my_game, menu_background):
		Scene.__init__(self, 'menu')
		self.my_game = my_game
		self.menu_background = menu_background
		self.img = mygame.load_image(get_image_pathname('alienhead.bmp'))
		
		if RESIZE:
			self.img = self.img.scale((int(self.img.get_width()*RESIZE_FACTOR),int(self.img.get_height() *RESIZE_FACTOR)))
		trans = mygame.Colour(255, 0, 255)
		self.img.set_colorkey(trans)
				
		self.x=(SCREEN_X - self.img.get_height()) /2
		self.y= SCREEN_Y +100
		
		key_set = KeySet.load_key_set()
		self.proceed_button = key_set.fire
		self.df = DebugFont()
		self.menu = GameMenu(my_game)
	
	def start(self):
		self.initial_skip_delay = 4000
		self.demo_start_delay = 10000
		self.start_time = None
		self.last_key_press_time = None
		self.menu.start()
		
	def stop(self):
		return
				
	def update_and_draw(self, time):
		
		if self.y > 0:
			self.y -= 20

		self.my_game.get_screen().fill(mygame.Colour(0,0,0))
		self.menu_background.update_and_draw(time)
		
		self.df.draw_text(VERSION_STRING,10,10, self.my_game.get_screen())
		self.my_game.get_screen().blit(self.img,(self.x, self.y))
		
		if self.check_for_starting_demo(time):
			return (Scene.SCENE_DEMO,0)
		
		if not self.start_time:
			self.start_time = time
		
		if time - self.start_time > self.initial_skip_delay:
			
			self.menu.update(time)
			self.menu.draw(self.my_game.get_screen())
			
			if self.menu.is_finished():
				if self.menu.action == AbstractMenuController.ACTION_START_GAME:
					return (Scene.SCENE_END_SUCCESS, 0)
				elif self.menu.action == AbstractMenuController.ACTION_LOAD_GAME:
					additional_data = self.menu.additional_data
					return (Scene.SCENE_LOAD_GAME, additional_data)
				elif self.menu.action == AbstractMenuController.ACTION_CREDITS:
					return (Scene.SCENE_CREDITS, 0)
				else:
					return (Scene.SCENE_END_FAILURE, 0)
		
		return (Scene.SCENE_CONTINUE, 0)

	def check_for_starting_demo(self, time):
		keystate = self.my_game.get_key_pressed()
		if keystate > 0:
			self.last_key_press_time = time
		if not self.last_key_press_time:
			self.last_key_press_time = time
		if time - self.last_key_press_time > self.demo_start_delay:
			return True
		


LIFT_SOUND='lift.ogg'


class DeckMan:
	FLASH_DELAY=50
	MOVE_DELAY=10
	INCR=8
	def __init__(self, x, y, mixer):
		trans = mygame.Colour(255, 0, 255)
		self.images, self.tile_width, self.tile_height = CompositeTileLoader.load_tiles("deckman.bmp", 64, 96, trans)
		
		self.last_flash_update = 0
		self.last_move_update = 0
		self.increment = DeckMan.INCR
		if RESIZE:
			self.increment = int(self.increment * HUD_RESIZE_FACTOR)
		self.x =x
		self.y = y - self.tile_height
		
		self.lift_sound = mixer.Sound(get_sound_pathname(LIFT_SOUND))
		self.lift_sound.set_volume(32)
		if not Cheats.getNoAudio():
			self.lift_sound.play()
		self.current_frame = 0

	def update(self, time):
		if time > (self.last_flash_update + DeckMan.FLASH_DELAY):
			self.current_frame +=1
			if self.current_frame == 2:
				self.current_frame = 0
			self.last_flash_update = time
		if time > (self.last_move_update + DeckMan.MOVE_DELAY):
			self.y += self.increment
			self.last_move_update = time
			
	def draw(self, screen):
		if self.y < screen.get_height():
			screen.blit(self.images[self.current_frame], (self.x, self.y))
		
class LevelIntroScene(Scene):
					
	def __init__(self, level_num, mygame):
		Scene.__init__(self, 'levelintro')
		self.my_game = mygame
		self.level_filename = get_level_filename(level_num)
		self.text_loader = LevelTextLoader(self.level_filename)
		self.font = BreedFont(self.my_game.get_mixer())
		key_set = KeySet.load_key_set()
		self.proceed_button = key_set.fire
		self.menu = ContinueMenu(mygame)
		

	def start(self):
		self.ticker = True
		
		self.img, self.x,self.y,TEXT_X,TEXT_Y,TEXT_W,TEXT_H,LIFT_X = self.__get_screen_data()
		
		self.font_rect = mygame.Rect(TEXT_X, TEXT_Y, TEXT_W, TEXT_H)
		
		self.font.set_ticker_text(self.text_loader.get_mission_text(), self.font_rect)
		self.delay = 2000
		self.pause_time = 0
		self.initial_skip_delay = 4000
		self.start_time = None
		self.menu.start()
		
		if not self.__is_first_level():
			self.deck_man = DeckMan(LIFT_X, self.y, self.my_game.get_mixer())
		else:
			self.deck_man = None
		
	def stop(self):
		self.text_loader = None
		self.font = None
		self.menu = None
		# The Wii is very short on memory so freeing as much as possible before starting level is a good idea
		gc.collect()
		gc.collect()
		gc.collect()
				
	def update_and_draw(self, time):
		
		if not self.start_time:
			self.start_time = time
			
		keystate = self.my_game.get_key_pressed()
		proceed = keystate & self.proceed_button > 0
		
		if proceed and time - self.start_time > self.initial_skip_delay:
			if self.ticker:
				self.font.set_text(self.text_loader.get_mission_text(), self.font_rect)
				self.ticker = False
				self.pause_time = time 
							
		self.my_game.get_screen().fill(mygame.Colour(0,0,0))
		self.my_game.get_screen().blit(self.img,(self.x, self.y))
		self.font.update(time)
		self.font.draw(self.my_game.get_screen())
		if self.deck_man:
			self.deck_man.update(time)
			self.deck_man.draw(self.my_game.get_screen())
		if self.font.finished():
			self.menu.update(time)
			self.menu.draw(self.my_game.get_screen())
		
		if (time - self.pause_time) > self.delay: 
			if self.menu.is_finished():
				return (Scene.SCENE_END_SUCCESS, 0)
		else:
			#need to clear the finished flag
			self.menu.start()
		return (Scene.SCENE_CONTINUE, 0)
				
	def __is_first_level(self):
		return self.level_filename == 'level1.lev'

	def __get_screen_data(self):
		
		if self.__is_first_level():
			img = mygame.load_image(get_image_pathname('deckstart.bmp'))
			if RESIZE:
				img = img.scale((int(img.get_width()*HUD_RESIZE_FACTOR),int(img.get_height() *HUD_RESIZE_FACTOR)))
			x=0
			y=(SCREEN_Y - img.get_height()) /2
			
			TEXT_Y = SCREEN_Y * 0.2
			TEXT_X = SCREEN_X * 0.1 
			TEXT_W = SCREEN_X * 0.85
			TEXT_H = SCREEN_Y * 0.8
			
			
			return img,x,y,TEXT_X,TEXT_Y,TEXT_W,TEXT_H,0

		else:
			
			img = mygame.load_image(get_image_pathname('decklift.bmp'))
			if RESIZE:
				img = img.scale((int(img.get_width()*HUD_RESIZE_FACTOR),int(img.get_height() *HUD_RESIZE_FACTOR)))
			x=0
			y=(SCREEN_Y - img.get_height()) /2
			
			TEXT_Y = SCREEN_Y * 0.1
			TEXT_X = SCREEN_X * 0.3 
			TEXT_W = SCREEN_X * 0.6
			TEXT_H = SCREEN_Y * 0.8
			
			LIFT_X = 30
			if RESIZE:
				LIFT_X = int(LIFT_X * RESIZE_FACTOR)
			
			return img,x,y,TEXT_X,TEXT_Y,TEXT_W,TEXT_H,LIFT_X
			


class LevelPlayScene(Scene):
		
	def __init__(self, level_num, mygame, prev_level_player_stats, loaded_game):
		Scene.__init__(self, 'level')
		self.my_game = mygame
		self.screen = mygame.get_screen()
		self.mixer = mygame.get_mixer()
		self.background_sound = self.mixer.Sound(get_sound_pathname(LEVEL_BACKGROUND_SOUND))
		self.background_sound.set_volume(100)
	
		self.weapons = ToolsAndWeapons(self.mixer)	
		
		starting_player_stats = self.calculate_starting_player_stats(prev_level_player_stats, loaded_game)
		self.l = Level(level_num, self.weapons, starting_player_stats, mygame)
		
		self.display = Display(self.l, REFRESH_RATE, mygame)
		self.display.center_on_player(self.screen)
		self.l.construct_shared_movers(self.display)
		
		self.debug_display_time = 0
		self.debug_update_time = 0

	def calculate_starting_player_stats(self, starting_player_stats, loaded_game):
		#If we have a loaded game then load the starting 
		#player stats from there...
		if loaded_game:
			l, starting_player_stats = loaded_game.convert(self.weapons)
		
		if not starting_player_stats:
			starting_player_stats = self.debug_starting_stats()	
		return starting_player_stats
			
	def debug_starting_stats(self):
		#if using development command line arguments to start at a different level to level 1 then need to create player stats...
		ps = PlayerStats(800, 1, 0, self.weapons)
		ps.add_key(10)
		ps.set_has_weapon(2)
		ps.money += 100000
		#ps.scanner = True
		
		return ps
	
	def get_player_stats(self):
		return self.l.get_player().get_player_stats()
			
	def start(self):
		if not Cheats.getNoAudio():
			self.background_sound.play(-1)
		
	def stop(self):
		self.background_sound.stop()
		self.background_sound = None
		self.display.close()
		self.display = None
		self.l = None
		self.weapons = None
		set_game_palette(self.my_game)
		# The Wii is very short on memory so clearing all the memory used by the level here is a good idea
		gc.collect()
		gc.collect()
		gc.collect()
		
	def debug_timing_A(self) :
		if not WII and DEBUG_TIMINGS:
			self._display_start_time = _time.time()
			
	def debug_timing_B(self) :
		if not WII and DEBUG_TIMINGS:
			self._display_end_time = _time.time()
		
	def debug_timing_C(self) :
		if not WII and DEBUG_TIMINGS:
			update_end_time = _time.time()
			display_time = self._display_end_time - self._display_start_time
			if display_time > self.debug_display_time:
				self.debug_display_time = display_time
			#print "Display time %f" % display_time
				
			update_time = update_end_time - self._display_end_time
			if update_time > self.debug_update_time:
				self.debug_update_time = update_time
			#print "Update time %f" % update_time

			print "Display %f Update %f Collisions %d" % (display_time, update_time, not Cheats.getNoCollisions())

	def update_and_draw(self, time):
		self.debug_timing_A()
		self.display.paint(self.screen)
		self.debug_timing_B()
		self.l.update(time, self.display)
		self.debug_timing_C()
			
		level_state = self.l.get_level_state()
		if level_state.get_game_over():
			if level_state.get_level_complete():
				return (Scene.SCENE_END_SUCCESS, 0)
			else:
				return (Scene.SCENE_END_FAILURE, 0)
		else:
			return (Scene.SCENE_CONTINUE, 0)


class EndGameScene(Scene):
					
	def __init__(self, mygame):
		Scene.__init__(self, 'endgame')
		self.my_game = mygame
		self.text = load_text_file_as_string(get_config_pathname('GameEndText.txt'))
		self.font = BreedFont(self.my_game.get_mixer())
		key_set = KeySet.load_key_set()
		self.proceed_button = key_set.fire
		self.background_sound = self.my_game.get_mixer().Music(get_sound_pathname(END_GAME_SOUND))
		self.background_sound.set_volume(100)
		
	def start(self):
		self.ticker = True
		
		self.img,self.x,self.y,TEXT_X,TEXT_Y,TEXT_W,TEXT_H = self.__get_screen_data()
		
		self.font_rect = mygame.Rect(TEXT_X, TEXT_Y, TEXT_W, TEXT_H)
		
		self.font.set_ticker_text(self.text, self.font_rect)
		self.delay = 500
		self.pause_time = 0
		self.start_time = None
		
		if not Cheats.getNoAudio():
			self.background_sound.play(-1)
	
	def stop(self):
		self.background_sound.stop()
	
	
	def update_and_draw(self, time):
		
		if not self.start_time:
			self.start_time = time
		
		keystate = self.my_game.get_key_pressed()
		proceed = keystate & self.proceed_button > 0
		
		
		if proceed:
					
			if self.font.finished():
				return (Scene.SCENE_END_SUCCESS, 0)
							
		self.my_game.get_screen().fill(mygame.Colour(0,0,0))
		self.my_game.get_screen().blit(self.img,(self.x, self.y))
		self.font.update(time)
		self.font.draw(self.my_game.get_screen())
			
		return (Scene.SCENE_CONTINUE, 0)

	def __get_screen_data(self):
		
		img = mygame.load_image(get_image_pathname('ending.bmp'))
		if RESIZE:
			img = img.scale((SCREEN_X, SCREEN_Y))
		x=0
		y=(SCREEN_Y - img.get_height()) /2
		
		TEXT_Y = SCREEN_Y * 0.1
		TEXT_X = SCREEN_X * 0.1 
		TEXT_W = SCREEN_X * 0.8
		TEXT_H = SCREEN_Y * 0.8
		
		return img,x,y,TEXT_X,TEXT_Y,TEXT_W,TEXT_H

class GameOverScene(Scene):
	DELAY = 50
	FINISHED_DELAY = 2000
		
	def __init__(self, mygame):
		Scene.__init__(self, 'gameover')
		self.my_game = mygame
		self.frames = []
		self.load_images()
		self.last_update = 0
		self.current_frame = 0
		self.finished = False
		
	def load_images(self):
		for i in range(1,10):
			img_name = 'gameover%d.bmp' % i
			img = mygame.load_image(get_image_pathname(img_name))
			if RESIZE:
				img = img.scale((int(img.get_width()*RESIZE_FACTOR),int(img.get_height() *RESIZE_FACTOR)))
			self.frames.append(img)
			
		w = self.frames[8].get_width()
		h = self.frames[8].get_height()
		
		self.x = (SCREEN_X - w) / 2
		self.y = (SCREEN_Y - h) / 2
		
			
	def start(self):
		self.current_frame = 0
		self.finished = False
		
	def stop(self):
		return
	
	
	def update_and_draw(self, time):
		if not self.finished:
			if time >= self.last_update + GameOverScene.DELAY:
				self.last_update = time
				self.current_frame += 1
				if self.current_frame > 8:
					self.current_frame = 8
					self.finished = True
		else:
			if time >= self.last_update + GameOverScene.FINISHED_DELAY:
				return (Scene.SCENE_END_SUCCESS, 0)
			
		self.my_game.get_screen().fill(mygame.Colour(0,0,0))
		self.my_game.get_screen().blit(self.frames[self.current_frame],(self.x, self.y))
		
		return (Scene.SCENE_CONTINUE, 0)
			
class SlideShowScene(Scene):
	def __init__(self, mygame, menu_background, name):
		Scene.__init__(self, name)
		self.my_game = mygame
		key_set = KeySet.load_key_set()
		self.proceed_button = key_set.fire
		self.menu_background = menu_background
		self.start_time = None
		self.delay = 2000
		self.init_content(mygame)
		
	def init_content(self, mygame):
		return
		
	def start(self):
		self.finished = False
		
	def stop(self):
		return
		
	def update_and_draw(self, time):
		self.my_game.get_screen().fill(mygame.Colour(0,0,0))
		finished = self.draw_content(self.my_game.get_screen(), time)
		self.menu_background.update_and_draw(time)
		proceed = False
		if not self.start_time:
			self.start_time = time
			
		if time - self.start_time > self.delay:
			keystate = self.my_game.get_key_pressed()
			proceed = keystate & self.proceed_button > 0
		
		if proceed or finished:
			return (Scene.SCENE_END_SUCCESS, 0)
		else:
			return (Scene.SCENE_CONTINUE, 0)
	
	def draw_content(self, screen, time):
		return
	
class CreditsScene(SlideShowScene):
	def __init__(self, mygame, menu_background):
		SlideShowScene.__init__(self, mygame, menu_background, 'credits')
	
	def init_content(self, mygame):
		self.cred = CreditsMenu(mygame)
	
	def draw_content(self, screen, time):
		finished = self.cred.update(time)
		self.cred.draw(screen)
		return finished

class DemoScene(SlideShowScene):
	def __init__(self, mygame, menu_background):
		SlideShowScene.__init__(self, mygame, menu_background, 'demo')
	
	def init_content(self, mygame):
		self.cred = DemoMenu(mygame)
	
	def draw_content(self, screen, time):
		finished = self.cred.update(time)
		self.cred.draw(screen)
		return finished
