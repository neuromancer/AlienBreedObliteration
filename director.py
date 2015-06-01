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

import traceback,sys
from utils import *
from scene import *
#Used for the font plotting in error handler
from text import *
from savedgameutils import *
from palette import *

class Director:
	
	def __init__(self, game_args, my_game_config):
		self.game_args = game_args
		self.initialise_engine(my_game_config)
		self.previous_player_stats = None
		self.finished = False
		self.loaded_game = None
		self.current_level = self.game_args.level
		self.menu_background = MenuBackground(self.my_game)
		
	def initialise_engine(self, my_game_config):
		self.my_game = mygame.MyGame(self.game_args.fullscreen, my_game_config)
		set_game_palette(self.my_game)
		load_cheats()
		
	def play(self):

		if self.game_args.show_menu:
			self.go_to_menu_scene()
		else:
			self.go_to_level_scene()
		
		
		#Python2.4 can't have finally and catch together.
		try:
			#For the WII we have no console so must display errors on the screen using SDL.
			if WII:
				try:
					self._main_loop()
				except:	
					self.display_error()
			else:
				#For other environments we will let the interpretter handle the error
				self._main_loop()
		
		finally:
			self.my_game.quit()	
	
	def display_error(self):
		exctype, value, tb = sys.exc_info()
		strings = traceback.format_exception(exctype, value,tb)
		del tb
		font = DebugFont()
		self.my_game.get_screen().fill(mygame.Colour(0,0,0))
		font.draw_text_lines(strings, 10,10,self.my_game.get_screen())
		self.my_game.display_flip()
        	mygame.pause(50000)
	
	def next_scene(self, scene_result, additional_data):
		if self.current_scene.name == 'menu':
			if scene_result == Scene.SCENE_END_SUCCESS:
				self.current_scene.stop()
				self.current_scene = None
				self.current_level = self.game_args.level
				self.go_to_level_intro_scene()
				
			elif scene_result == Scene.SCENE_LOAD_GAME:
				self.current_scene.stop()
				self.load_game(additional_data)
				self.current_scene = None
				self.go_to_level_intro_scene()
				
			elif scene_result == Scene.SCENE_CREDITS:
				self.current_scene.stop()
				self.current_scene = None
				self.go_to_credit_scene()	
				
			elif scene_result == Scene.SCENE_DEMO:
				self.current_scene.stop()
				self.current_scene = None
				self.go_to_demo_scene()	

			else:
				self.current_scene.stop()
				self.menu_background.stop()
				self.finished = True
				
		elif self.current_scene.name == 'levelintro':
			self.current_scene.stop()
			self.go_to_level_scene()
		
		elif self.current_scene.name == 'level':
			if scene_result == Scene.SCENE_END_SUCCESS:
				#remember the player stats for the next level...
				self.previous_player_stats = self.level_play_scene.get_player_stats()
			self.current_scene.stop()
			self.level_play_scene = None
			if scene_result == Scene.SCENE_END_SUCCESS:
				if self.current_level == 15:
					self.go_to_end_game_scene()
				else:
					self.current_level += 1
					self.go_to_level_intro_scene()
			else:
				self.go_to_game_over_scene()
		
		elif self.current_scene.name =='gameover' or self.current_scene.name =='endgame' or self.current_scene.name =='credits' or self.current_scene.name =='demo':
			self.current_scene.stop()
			self.go_to_menu_scene()
				
	def go_to_menu_scene(self):
		self.current_scene = MenuScene(self.my_game, self.menu_background)
		self.menu_background.start()
		self.current_scene.start()
	
	def go_to_level_intro_scene(self):
		self.menu_background.stop()
		self.current_scene = LevelIntroScene(self.current_level, self.my_game)
		self.current_scene.start()
		
		
	def go_to_level_scene(self):
		self.menu_background.stop()
		self.level_play_scene = LevelPlayScene(self.current_level, self.my_game, self.previous_player_stats, self.loaded_game)
		self.loaded_game = None
		self.previous_player_stats = None
		self.current_scene = self.level_play_scene
		self.current_scene.start()
	
	def go_to_end_game_scene(self):
		self.current_scene = EndGameScene(self.my_game)
		self.current_scene.start()
	
	def go_to_game_over_scene(self):
		self.current_scene = GameOverScene(self.my_game)
		self.current_scene.start()
	
	def go_to_credit_scene(self):
		self.current_scene = CreditsScene(self.my_game, self.menu_background)
		self.current_scene.start()
	
	def go_to_demo_scene(self):
		self.current_scene = DemoScene(self.my_game, self.menu_background)
		self.current_scene.start()

	def load_game(self, saved_game_id):
		self.loaded_game = SavedGame.load_by_id(saved_game_id)
		self.current_level = self.loaded_game.level
			
	
	def _main_loop(self):
		
		clock = mygame.Clock()
		key_set = KeySet.load_key_set()
		
		while not self.finished:
			time = self.my_game.get_ticks() 
			
			deltat = clock.tick(REFRESH_RATE)
			
			for event in self.my_game.get_event():
				
				if event.get_event_type() is mygame.KEYDOWN:
					
					if Cheats.get_quick_quit():
						if event.get_key() == key_set.escape:
							self.finished = True
						
					if event.get_key() == key_set.fps:
						fps = clock.get_fps()
						print fps
						
				elif event.get_event_type() is mygame.QUIT:
					self.finished = True
				
			result, additional_data = self.current_scene.update_and_draw(time)
			
			if result != Scene.SCENE_CONTINUE:
				self.next_scene(result, additional_data)
			
			
			self.my_game.display_flip()
		
