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
from tileloader import *
from levelstate import *

COUNTDOWN_FILE='countdown.bmp'

class CountDownFont:

	def __init__(self):
		self.tile_width= 12
		self.tile_height = 32
		self.trans = mygame.Colour(0xff, 0, 0xff)
						
		self.load_tiles()
		
		self.x = 0
		self.y = 0
		self.count = 0

		if RESIZE:
			self.tile_width= int(self.tile_width * RESIZE_FACTOR)
			self.tile_height = int(self.tile_height * RESIZE_FACTOR)

	def load_tiles(self):
		
		self.images, self.tile_width, self.tile_height = CompositeTileLoader.load_tiles(COUNTDOWN_FILE, self.tile_width, self.tile_height, self.trans)
		


	def set_count(self, count, x, y):
		self.count = count
		self.x = x
		self.y = y

	def draw(self, screen):
		a = self.count / 10
		b = self.count % 10
		a_img = self.images[int(a)]
		b_img = self.images[b] 
		screen.blit(a_img, (self.x, self.y))
		screen.blit(b_img, (self.x + self.tile_width + 2, self.y))
	
class Jolt:
	def __init__(self):
		self._last_update = None
		self._direction = -1
		self._count = 0
		
	def update(self, time, display):
		if not self.finished():
			if self._last_update:
				if time - self._last_update > 50:
					display.scroll(-10 * self._direction, 0)
					self._last_update = time
					self._direction = -1 * self._direction
					self._count += 1
			else:
				self._last_update = time
			
	def finished(self):
		return self._count == 8

	def start(self):
		self._count = 0

SIREN_SOUND=get_sound_pathname('siren.ogg')
WARN_DESTR_SOUND=get_sound_pathname('vocdestruction.ogg')
DESTR_SOUND=get_sound_pathname('vocdestruction2.ogg')

class Countdown:
	
	def __init__(self, delay, count, fade, shake, mixer, level):
		self._delay_timer = delay / 1000
		self._timer = count / 1000
		self._fadered = fade
		self._shake = shake
		self._start_timer = count
		self._last_update = None
		self._x = 20
		self._y = 20
		self._font = CountDownFont()
		self._font.set_count(self.get_timer(), self._x, self._y)
		self.mixer = mixer
		self.level = level
		self.siren_sound = mixer.Sound(SIREN_SOUND)
		self.siren_sound.set_volume(100)
		self.warning_sound = mixer.Sound(WARN_DESTR_SOUND)
		self.destruction_sound = mixer.Sound(DESTR_SOUND)
		self._jolt = Jolt()
		self._countdown_started = False
		
	def update(self, time, display):
		if not self._last_update:
			self._last_update = time
			
			
		if self._countdown_started:
			self.handle_countdown(time, display)
		else:
			if self._delay_timer > 0:
				if time - self._last_update > 1000:
					self._last_update = time
					if self._delay_timer > 1:
						self._delay_timer -=1
					else:
						self.start_countdown()
		if self._timer <= 0 :
			self.level.game_over()
	
	def start_countdown(self):
		level_state = self.level.get_level_state()
		level_state.set_game_mode(LevelState.COUNTDOWN)
		if not Cheats.getNoAudio():
			self.siren_sound.play(-1)
		self._countdown_started = True
	
	def handle_countdown(self, time, display):
		if time - self._last_update > 1000 and self._timer > 0:
			self._timer -= 1
			self._last_update = time
			self._font.set_count(self.get_timer(), self._x, self._y)	
			
			if self._shake:
				if self._timer > 10:
					if (self._start_timer - self._timer) == 5:
						if not Cheats.getNoAudio():
							self.warning_sound.play()
				
					if (self._timer - self._start_timer) % 10 == 0:
						self._jolt.start()
						if not Cheats.getNoAudio():
							self.warning_sound.play()
						self.add_random_explosions(display, 4)
							
				else:
					if (self._timer - self._start_timer) % 2 == 0:
						if not Cheats.getNoAudio():
							self.destruction_sound.play()
						display.scroll(-5, 0)
						self._jolt.start()
						self.add_random_explosions(display, 10)
					
		if self._shake:
			self._jolt.update(time, display)
	
	def add_random_explosions(self, display, num):
		self.level.add_random_explosions(display.view, num, 3000)
		
	def get_timer(self):
		return self._timer

	def draw(self, screen):
		self._font.draw(screen)
		
	def stop(self):
		self.siren_sound.stop()
	
