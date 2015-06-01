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

BLIP_SOUND='blip.ogg'

class TickerFont:
	INSTANT = 1
	CHARACTER = 2
	DELAY = 30
	
	def __init__(self, mixer, play_blip):
		self.large_font_width= 0
		self.large_font_height = 0
		self.small_font_width = 0
		self.small_font_height = 0
		self.small_font_voffset = 0
		
		self.large_images = []
		self.large_index = []
		self.small_images = []
		self.small_index = []
		
		self.x = 0
		self.y = 0
		self.text = None
		self.mode = BreedFont.INSTANT
		self.full_text = None
		self.char_index = 0

		if play_blip:
			self.blip_sound = mixer.Sound(get_sound_pathname(BLIP_SOUND))
			self.blip_sound.set_volume(32)
		else:
			self.blip_sound = None
			
		self.char_increment = 1

	def set_text(self, text, rect):
		self.full_text = text
		self.rect = rect
		self.mode = BreedFont.INSTANT
		self.char_index = len(self.full_text)-1
	
	def set_ticker_text(self, text, rect):
		self.full_text = text
		self.rect = rect
		self.mode = BreedFont.CHARACTER
		self.delay = BreedFont.DELAY
		self.char_index = 0
		self.__last_update = 0
		
	def update(self, time):
		if self.full_text:
			if self.mode == BreedFont.INSTANT:
				self.char_index = len(self.full_text)-1
				
			elif self.mode == BreedFont.CHARACTER:
				if time - self.__last_update > self.delay:
					self.__last_update = time
					self.char_index += self.char_increment
					if self.char_index >= len(self.full_text):
						self.char_index = len(self.full_text)-1
						
					else:
						if self.blip_sound:
							if not Cheats.getNoAudio():
								self.blip_sound.play()

		return
	
	def draw(self, screen):
		if self.full_text:
		
			h = self.large_font_height
			w = self.large_font_width
			
			x = self.rect.x
			y = self.rect.y
			
			words = self.full_text.split(' ')
			
			curr_index = 0
			for word in words:
				if curr_index > self.char_index:
					break;
				
				l = self.__word_length(word)
								
				if x+l > self.rect.x + self.rect.w:
					x = self.rect.x
					y += h
					
				x,y,curr_index = self.__plot_word(word + " ", x, y, h, curr_index, screen)
				
				
					
	def __word_length(self, w):
		x=0
		for c in w:
			if c in self.large_index:
				x+= self.large_font_width
			elif c in self.small_index:
				x+= self.small_font_width
		return x
						
	def __plot_word(self, w, x, y, h, curr_index, screen):
		i = curr_index
		for c in w:
			if i>self.char_index:
				break
			
			if c in self.large_index:
				index = self.large_index.index(c)
			
				img = self.large_images[index]
				screen.blit(img, (x, y))
				x+= self.large_font_width
				
			elif c in self.small_index:
				index = self.small_index.index(c)
			
				img = self.small_images[index]
				screen.blit(img, (x, y + self.small_font_voffset))
				x+= self.small_font_width
				
			if c == '\n':
				x = self.rect.x
				y += h
			i+= 1
			
			
		return x,y,i
			
	def finished(self):
		return self.char_index == len(self.full_text) -1
	
	def draw_line_centered(self, text, y, screen):
		w = self.__word_length(text)
		indent = SCREEN_X /2 - w /2
		my_rect = mygame.Rect(indent, y, SCREEN_X - indent, self.large_font_height)
		self.set_text(text, my_rect)
		self.draw(screen)

	
class BreedFont(TickerFont):
	INSTANT = 1
	CHARACTER = 2
	DELAY = 30
	
	def __init__(self, mixer):
		TickerFont.__init__(self, mixer, True)
		self.large_font_width= 9
		self.large_font_height = 12
		
		self.small_font_width = 7
		self.small_font_height = 11
		self.small_font_voffset = 1
		
		large_rows = []
		large_rows.append(' !,.0123456789')
		large_rows.append(':<>\'+&?/')
		large_rows.append('ABCDEFGHIJKLMN')
		large_rows.append('OPQRSTUVWXYZ-@')
				
		self.large_images, self.large_index = CompositeTileLoader.load_indexed_tiles(0,0,self.large_font_width,self.large_font_height, large_rows, 'breedfont.bmp', mygame.Colour(0xff, 0, 0xff))

		small_rows = []
		small_rows.append(' !,.0123456789')
		small_rows.append(':<>\'+&?/')
		small_rows.append('abcdefghijklmn')
		small_rows.append('opqrstuvwxyz-@')
		
		self.small_images, self.small_index = CompositeTileLoader.load_indexed_tiles(0,48,self.small_font_width, self.small_font_height, small_rows, 'breedfont.bmp', mygame.Colour(0xff, 0, 0xff))

		self.x = 0
		self.y = 0
		self.text = None
		self.mode = BreedFont.INSTANT
		self.full_text = None

		if RESIZE:
			self.large_font_width= int(self.large_font_width * RESIZE_FACTOR)
			self.large_font_height = int(self.large_font_height * RESIZE_FACTOR)
			
			self.small_font_width = int(self.small_font_width * RESIZE_FACTOR)
			self.small_font_height = int(self.small_font_height * RESIZE_FACTOR)
			self.small_font_voffset = int(self.small_font_voffset * RESIZE_FACTOR)
	
	
	
class IntexTickerFont(BreedFont):
		
		
	def __init__(self, mixer):
		TickerFont.__init__(self, mixer, False)	
		
		self.large_font_width= 8
		self.large_font_height = 12

		self.load_tiles()
			
		if RESIZE:
			self.large_font_width= int(self.large_font_width * RESIZE_FACTOR)
			self.large_font_height = int(self.large_font_height * RESIZE_FACTOR)
	
	def load_tiles(self):
		
		rows = []		
		rows.append(' ABCDEFGHIJKLMNO')
		rows.append('PQRSTUVWXYZ-+  ')
		rows.append("0123456789:.',& ")

		self.large_images, self.large_index = CompositeTileLoader.load_indexed_tiles(0,0,self.large_font_width,self.large_font_height, rows, 'greenfont.bmp', mygame.Colour(0xff, 0, 0xff))



class IntextMenuFont:
	
	def __init__(self, mixer):
		self.index = []
	
	""" Must reload images at point of use for 8bit palette
	modes to ensure corect display palette is used"""
	def start(self):
		self.font_width= 8
		self.font_height = 12
		
		self.load_tiles()
		
		if RESIZE:
			self.font_width= int(self.font_width * RESIZE_FACTOR)
			self.font_height = int(self.font_height * RESIZE_FACTOR)

	def load_tiles(self):
		
		rows = []		
		rows.append(' ABCDEFGHIJKLMNO')
		rows.append('PQRSTUVWXYZ-+  ')
		rows.append("0123456789:.',& ")

		self.images, self.index = CompositeTileLoader.load_indexed_tiles(0,0,self.font_width,self.font_height, rows, 'greenfont.bmp', mygame.Colour(0xff, 0, 0xff))


	def draw_line(self, text, x, y, screen):
		for c in text:
			if c in self.index:
				index = self.index.index(c)
			
				img = self.images[index]
				screen.blit(img, (x, y))
				x+= self.font_width
		return x,y,

	def draw_line_centered(self, text, y, screen):
		w = len(text) * self.font_width
		indent = SCREEN_X /2 - w /2
		self.draw_line(text, indent, y, screen)

	def __word_length(self, w):
		x=0
		for c in w:
			if c in self.index:
				x+= self.font_width
		return x

	def format_string(self, text, width):
		in_lines = text.split('\n')
		
		lines = []
		
		for in_line in in_lines:
			words = in_line.split(' ')
			x = 0	
		
			line = ""
			for word in words:
				l = self.__word_length(word)
				if x+l >= width:
					x = 0
					lines.append(line)
					line = ''
					
				
				line += word
				line += ' '
				x += (l+1)
			
			if len(line)>0:
				lines.append(line)
				
		return lines



class DebugFont:
	
	def __init__(self):
	
		self.font_width= 5
		self.font_height = 12
		
		self.load_tiles()
		
		if RESIZE:
			self.font_width= int(self.font_width * RESIZE_FACTOR)
			self.font_height = int(self.font_height * RESIZE_FACTOR)

	def load_tiles(self):
		
		rows = []
		rows.append(' !"`````()`+,-./0123456789:;{=}?`ABCDEFGHIJKLMNOPQR')
		rows.append('STUVWXYZ[\\]`````````````````````````````````       ')

		self.images, self.index = CompositeTileLoader.load_indexed_tiles(0,0,self.font_width,self.font_height, rows, 'tinyfont.bmp', mygame.Colour(0xff, 0, 0xff))


	def draw_text(self, text, x, y, screen):
		xx = x
		yy = y
		w = screen.get_width() - self.font_width
		for c in text.upper():
			if c in self.index:
				index = self.index.index(c)
				img = self.images[index]
				screen.blit(img, (xx, yy))
				
			xx+= self.font_width
			if xx > w:
				xx = x
				yy += self.font_height
		return yy
							
	def draw_text_lines(self, lines, x, y, screen):
		yy=y
		for l in lines:
			yy = self.draw_text(l, x, yy, screen)
			yy += self.font_height
