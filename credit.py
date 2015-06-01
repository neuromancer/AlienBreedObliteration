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
from text import *

SITE = "http://sourceforge.net/projects/wiiab"

class SolidText:
	def __init__(self, my_game, text, delay):
		self.menu_font = BreedFont(my_game.get_mixer())
		self.lines = text.split('\n')	
		self.delay = delay
		self.my_game = my_game
		self.last_update = 0

	def update(self, time):
		if time - self.last_update > self.delay:
			if self.last_update ==0:
				self.last_update = time
			else:
				return True
			
		
		return False
			
	def draw(self, screen):
		sw = screen.get_width()
		sh = screen.get_height()
		y = sh/2 - (len(self.lines) * self.menu_font.large_font_height) /2
		for line in self.lines:
			self.menu_font.draw_line_centered(line, y, screen)
			y+= self.menu_font.large_font_height

class FadeInText:
	def __init__(self, my_game, text, fade_delay):
		self.menu_font = BreedFont(my_game.get_mixer())
		self.lines = text.split('\n')	
		self.fade_delay = fade_delay
		self.my_game = my_game
		self.fade_val = 255
		self.last_update = 0

	def update(self, time):
		if time - self.last_update > self.fade_delay:
			self.increment()
			self.last_update = time
		
		return self.finished()
			
	def finished(self):
		return self.fade_val == 0
	
	def increment(self):
		self.fade_val -=10
		if self.fade_val < 0:
			self.fade_val = 0
	
	def draw(self, screen):
		sw = screen.get_width()
		sh = screen.get_height()
		y = sh/2 - (len(self.lines) * self.menu_font.large_font_height) /2
		for line in self.lines:
			self.menu_font.draw_line_centered(line, y, screen)
			y+= self.menu_font.large_font_height
			
		#Overlays not supported in 8bit mode	
		if DEPTH != 8:
			overlay = self.my_game.create_blank((sw,sh))
			overlay.fill(mygame.Colour(0, 0, 0))
			overlay.set_alpha(self.fade_val)
			screen.blit(overlay, (0,0))
			

class FadeOutText(FadeInText):
	def __init__(self, my_game, text, fade_delay):
		FadeInText.__init__(self, my_game, text, fade_delay)
		self.fade_val = 0

	def increment(self):
		self.fade_val +=10
		if self.fade_val > 255:
			self.fade_val = 255
	
	def finished(self):
		return self.fade_val == 255


class FadeInSprite:
	def __init__(self, my_game, img, caption, fade_delay):
		self.img = mygame.load_image(get_image_pathname(img))
		if RESIZE:
			self.img = self.img.scale((int(self.img.get_width()*RESIZE_FACTOR),int(self.img.get_height() *RESIZE_FACTOR)))
		trans = mygame.Colour(255, 0, 255)
		self.img.set_colorkey(trans)

		self.fade_delay = fade_delay
		self.my_game = my_game
		self.fade_val = 255
		self.last_update = 0
		self.caption = caption
		if self.caption:
			self.menu_font = BreedFont(my_game.get_mixer())

	def update(self, time):
		if time - self.last_update > self.fade_delay:
			self.increment()
			self.last_update = time
		
		return self.finished()
			
	def finished(self):
		return self.fade_val == 0
	
	def increment(self):
		self.fade_val -=10
		if self.fade_val < 0:
			self.fade_val = 0
	
	def draw(self, screen):
		sw = screen.get_width()
		sh = screen.get_height()
		x = sw/2 - self.img.get_width() / 2
		y = sh/2 - self.img.get_height() /2
		self.my_game.get_screen().blit(self.img,(x, y))
		if self.caption:
			y+= self.menu_font.large_font_height + self.img.get_height()
			self.menu_font.draw_line_centered(self.caption, y, screen)
			
		#Overlay not supported in 8bit mode
		if DEPTH != 8:
			overlay = self.my_game.create_blank((sw,sh))
			overlay.fill(mygame.Colour(0, 0, 0))
			overlay.set_alpha(self.fade_val)
			screen.blit(overlay, (0,0))
		
class FadeOutSprite(FadeInSprite):
	def __init__(self, my_game, img, caption, fade_delay):
		FadeInSprite.__init__(self, my_game, img, caption, fade_delay)
		self.fade_val = 0

	def increment(self):
		self.fade_val +=10
		if self.fade_val > 255:
			self.fade_val = 255
	
	def finished(self):
		return self.fade_val == 255
		
class SolidSprite(FadeOutSprite):
	def __init__(self, my_game, img, caption, fade_delay):
		FadeOutSprite.__init__(self, my_game, img, caption, fade_delay)
		self._finished = False

	def increment(self):
		if self.last_update !=0:
			self._finished = True
		return
	
	def finished(self):
		return self._finished



class CreditsMenu:

	def __init__(self, my_game):
		self.commands = []
		self.setup_commands(my_game)
		self.current_command = 0
	
	def add_text(self, my_game, text, hold=1000):
		self.commands.append(FadeInText(my_game,text, 10))
		self.commands.append(SolidText(my_game,text, hold))
		self.commands.append(FadeOutText(my_game,text, 10))
		
	def add_image(self, img, caption, my_game, hold=1000):
		self.commands.append(FadeInSprite(my_game,img, caption, 10))
		self.commands.append(SolidSprite(my_game,img, caption, hold))
		self.commands.append(FadeOutSprite(my_game,img, caption, 10))
		
	
	def setup_commands(self, my_game):
		self.add_text(my_game, "Alien Breed Obliteration - Wii Edition")
		
		self.add_text(my_game,"Written by HabitualCoder")
		
		self.add_text(my_game,"A homage to the Alien Breed series by")
		
		self.add_image("t17logo.bmp", None,my_game)
		
		self.add_text(my_game, "A clone of the retro remake by")
		
		self.add_image("developer.bmp", None, my_game)
		
		self.add_text(my_game, "Thanks to")
		
		self.add_text(my_game, "Everybody behind\n\nDevkitpro, libogc and SDL-Wii\nWii-Brew, Team Twiizers\ngc-linux, python and pygame", 4000)
		
		self.add_text(my_game, "Tested by The don")
		
		self.add_text(my_game, "The program and installation scripts\nare Free Software, GNU v3\nSee LICENSE for more details.\nGraphics, sounds and level data\nretrieved as part of installation\nare not covered by the GNU license.", 8000)
		
		#self.add_text(my_game, "Want to get involved...\n\n" + SITE, 2000)
		self.add_image("website.bmp", None,my_game)
		
	def update(self, time):
		if self.current_command < len(self.commands):
			finished = self.commands[self.current_command].update(time)
			if finished:
				if self.current_command < len(self.commands) -1:
					self.current_command +=1
				else:	
					return True
		return False
	
	def draw(self, screen):
		if self.current_command < len(self.commands):
			self.commands[self.current_command].draw(screen)
		
	def start(self):
		self.current_command = 0
		
class DemoMenu(CreditsMenu):
		
	def __init__(self, my_game):
		CreditsMenu.__init__(self, my_game)
		
	def setup_commands(self, my_game):
		self.add_image("demoScreen5.bmp", 'CLASSIC ALIEN BREED GAMEPLAY', my_game, 4000)
		self.add_image("demoScreen4.bmp", 'ORIGINAL GFX AND MUSIC', my_game, 4000)

		self.add_image("demoScreen2.bmp", '15 NEW LEVELS TO EXPLORE', my_game, 4000)
		self.add_image("demoScreen1.bmp", 'EVOLVED ALIEN AI', my_game, 4000)
		self.add_image("demoScreen3.bmp", 'IMPROVED BOSS FIGHTS', my_game, 4000)
		
		

		
