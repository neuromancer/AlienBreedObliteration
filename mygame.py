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


"""

This file represents a 'mygame' API implementation backed by Pygame (SDL).
This is useful for development and running on desktop machines.

The WII version doesn't use this implementation. Instead a Pyrex SDL wrapper
is used to interface directly to the WII SDL port.

Pygame will not run on the WII due to missing Python dependencies.
"""
import pygame as pygame
	
KEYDOWN = pygame.KEYDOWN

WPAD_BUTTON_2=0x0001
WPAD_BUTTON_1=0x0002
WPAD_BUTTON_B=0x0004
WPAD_BUTTON_A=0x0008
WPAD_BUTTON_MINUS=0x0010
WPAD_BUTTON_HOME=0x0080
WPAD_BUTTON_LEFT=0x0100
WPAD_BUTTON_RIGHT=0x0200
WPAD_BUTTON_DOWN=0x0400
WPAD_BUTTON_UP=0x0800
WPAD_BUTTON_PLUS=0x1000

MY_K_LEFT=WPAD_BUTTON_LEFT
MY_K_UP=WPAD_BUTTON_UP
MY_K_DOWN=WPAD_BUTTON_DOWN
MY_K_RIGHT=WPAD_BUTTON_RIGHT
MY_K_FIRE=WPAD_BUTTON_A
MY_K_CYCLE_WEAPON=WPAD_BUTTON_1
MY_K_QUIT=WPAD_BUTTON_HOME
MY_K_CHEAT=WPAD_BUTTON_PLUS
MY_K_FPS=WPAD_BUTTON_MINUS
MY_K_INTEX=WPAD_BUTTON_B
MY_K_RUN=WPAD_BUTTON_2

THROTTLE = False

class Clock:
	def __init__(self):
		self.last_tick = 0
		self.ticks = []
		for i in range(0,10):
			self.ticks.append(0)
		self.current_index = -1
		self._clock = pygame.time.Clock()

	def get_fps(self):
		count = 0
		sum = 0
		
		for t in self.ticks:
			count+=1
			sum += t
		if sum>0 and count >0 :
			fps = 1000/ (sum / count)
		else:
			fps = 0
		return fps

	def tick(self, framerate=0):
		tick = pygame.time.get_ticks()
		if self.last_tick == 0:
			self.last_tick = tick
		else:
			elapsed = tick - self.last_tick
			
			if THROTTLE:
				#Check if we must delay a little bit to throttle FPS
				desired_elapsed = 1000/framerate
				
				if desired_elapsed > elapsed:
					delay = desired_elapsed - elapsed
					p = pygame.time.delay(delay)
					elapsed += p
				
			self.current_index +=1
			if self.current_index > 9 :
				self.current_index = 0
			self.ticks[self.current_index] = elapsed
			self.last_tick = tick
		
			
		self._clock.tick(framerate)


class Event:	

	def __init__(self):
		self.event_type = None
		self.key = None
	
	def get_event_type(self):
		return self.event_type

	def set_event_type(self, t):
		self.event_type = t

	def get_key(self):
		return self.key

	def set_key(self, k):
		self.key = k
	
class MyScreen:
	
	def __init__(self, fullscreen, config):
		options = pygame.SRCALPHA
		if fullscreen:
			options |= pygame.FULLSCREEN
		else:
			options |= pygame.NOFRAME
			
		if 'hardware' in config:
			options |= pygame.DOUBLEBUF | pygame.HWSURFACE
		
		self.bpp = config['depth']
		
		self.screen = pygame.display.set_mode((config['width'], config['height']), options, config['depth'])
		
		if config['depth'] == 8:
			self.configure_palette(config['paletteimage'])
		
		if 'hardware' in config:
			inf = pygame.display.Info()
			print "Hardware accelerated %d" % inf.hw
			print "Hardware blit accelerated %d" % inf.blit_hw
			
			
	def configure_palette(self, palette_img):
		self.set_palette_from_image(palette_img)
	
			
	def get_width(self):
		return self.screen.get_width()
	
	def get_height(self):
		return self.screen.get_height()

	def fill(self, colour):
		self.screen.fill(colour.colour)

	def blit(self, img, location):
		self.screen.blit(img._img, location)
		
	def blit_part(self, img, location, src_rect):
		pyrect = pygame.Rect(src_rect.x, src_rect.y, src_rect.w, src_rect.h)
		self.screen.blit(img._img, location, pyrect)

	def set_at(self, pos, colour):
		self.screen.set_at(pos, colour.colour)
		
	def set_palette_from_image(self, palette_img_fname):
		if self.bpp ==8:
			i = pygame.image.load(palette_img_fname)
			self.screen.set_palette(i.get_palette())
	
	def get_display_palette(self):
		if self.bpp == 8:
			return pygame.display.get_surface().get_palette()
		else:
			return None
	
	def set_display_palette(self, palette):
		if self.bpp == 8:
			pygame.display.set_palette(palette)
	
class MyGame:

	def __init__(self, fullscreen, config = {}):
		self._initialise_mygame(fullscreen, config)
		return
	
	def _initialise_mygame(self, fullscreen, config):
		self.screen = MyScreen(fullscreen, config)	
			
		freq = config['freq']
		format = config['format']
		channels = 2
		chunksize = 1024

		if 'freq' in config:
			freq = config['freq']

		if 'format' in config:
			format = config['format']
		
		if 'channels' in config:
			channels = config['channels']

		if 'chunksize' in config:
			chunksize = config['chunksize']
		
		
		#setting for laptop FREQ, -8, 1, 256
		#settings for desktop pc FREQ, 8, 2, 1024
		self.mixer = Mixer(freq, format, channels, chunksize) #raises exception on fail
		return
		
	def get_screen(self):
		return self.screen
	
	def get_mixer(self):
		return self.mixer

	def display_flip(self):
		pygame.display.flip()
	
	def get_ticks(self):
		return pygame.time.get_ticks()

	def get_key_pressed(self):
		pressed = pygame.key.get_pressed()
		result = 0
		if pressed[pygame.K_LEFT]:
			result |= WPAD_BUTTON_LEFT
		if pressed[pygame.K_RIGHT]:
			result |= WPAD_BUTTON_RIGHT
		if pressed[pygame.K_UP]:
			result |= WPAD_BUTTON_UP
		if pressed[pygame.K_DOWN]:
			result |= WPAD_BUTTON_DOWN
		if pressed[pygame.K_ESCAPE]:
			result |= WPAD_BUTTON_HOME
		if pressed[pygame.K_c]:
			result |= WPAD_BUTTON_A
		if pressed[pygame.K_SPACE]:
			result |= WPAD_BUTTON_B
		if pressed[pygame.K_f]:
			result |= WPAD_BUTTON_MINUS
		if pressed[pygame.K_w]:
			result |= WPAD_BUTTON_PLUS
		if pressed[pygame.K_p]:
			result |= WPAD_BUTTON_1
		if pressed[pygame.K_LSHIFT]:
			result |= WPAD_BUTTON_2

		return result


	def get_event(self):
		pes = pygame.event.get()
		events = []
		for pe in pes:
			if pe.type == pygame.KEYDOWN:
				if pe.key == pygame.K_ESCAPE:
					e = Event()
					e.set_event_type(pe.type)
					e.set_key(MY_K_QUIT)
					events.append(e)
				elif pe.key == pygame.K_f:
					e = Event()
					e.set_event_type(pe.type)
					e.set_key(WPAD_BUTTON_MINUS)
					events.append(e)
			
		return events
	
	def quit(self):
		pygame.quit()

	def create_blank(self, size):
		s = pygame.Surface(size)
		img = Image()
		img._img = s
		return img


class Image:
		
	def __init__(self):
		self._img = None
		return
	
	def load(self, filename):
		i = pygame.image.load(filename)
		self._img = i.convert()		

	def load_without_reformat(self, filename):
		self._img = pygame.image.load(filename)
		
	def get_width(self):
		return self._img.get_width()
	
	
	def get_height(self):
		return self._img.get_height()
	
	def subsurface(self, rect):
		pyrect = pygame.Rect(rect.x, rect.y, rect.w, rect.h)
		sub = self._img.subsurface(pyrect)
		i = Image()
		i._img = sub
		return i
	
	def set_colorkey(self, colour):
		self._img.set_colorkey(colour.colour)
		
	def scale(self, s):
		i = pygame.transform.scale(self._img, s)
		sc = Image()
		sc._img = i
		return sc
	

	def blit(self, src, src_rect, dest_rect):
		#I think the rects here are pygame rects
		self._img.blit(src._img, src_rect, dest_rect)

	def blit_loc(self, src, location):
		self._img.blit(src._img, location)

	def blit_part(self, img, location, src_rect):
		pyrect = pygame.Rect(src_rect.x, src_rect.y, src_rect.w, src_rect.h)
		self._img.blit(img._img, location, pyrect)

	def get_rect(self):
		return self._img.get_rect()
	
	def fill(self, colour):
		self._img.fill(colour.colour)

	def set_alpha(self, alpha):
		self._img.set_alpha(alpha)
		
	"""
	def get_at(self,x,y):
		#TODO this will probably fail in new pygame versions
		tup = self._img.get_at((x,y))
		r = tup[0]
		g = tup[1]
		b = tup[2]
		return Colour(r,g,b) 
	"""
		
class Rect:
	
	def __init__(self, x,y,w,h):
		self.x = int(x)
		self.y = int(y)
		self.w = int(w)
		self.h = int(h)
	
	def copy(self):
		r = Rect(self.x, self.y, self.w, self.h)
		return r
		
		
		
	def colliderect(self, r):
		other_rect = pygame.Rect(r.x, r.y, r.w, r.h)
		this_rect = pygame.Rect(self.x, self.y, self.w, self.h)
		return this_rect.colliderect(other_rect)
	
	def move(self, xd, yd):
		new_x = self.x + xd
		new_y = self.y + yd
		return Rect(new_x, new_y, self.w, self.h)
	
	def contains(self, r):
		other_rect = pygame.Rect(r.x, r.y, r.w, r.h)
		this_rect = pygame.Rect(self.x, self.y, self.w, self.h)
		return this_rect.contains(other_rect)
	
	def clip(self, r):
		"""
		other_rect = pygame.Rect(r.x, r.y, r.w, r.h)
		this_rect = pygame.Rect(self.x, self.y, self.w, self.h)
		clip = this_rect.clip(other_rect)
		return Rect(clip.x, clip.y, clip.w, clip.h)
		"""
		return self._my_clip(r)
	
	def _my_clip(self, b):
		ax1 = self.x
		ax2 = self.x + self.w
		bx1 = b.x
		bx2 = b.x + b.w
		ay1 = self.y
		ay2 = self.y + self.h
		by1 = b.y
		by2 = b.y + b.h
	
		my_clip = None
	
		if bx1 >= ax1:
			if bx1 < ax2 and bx2 >= ax2:
				x = bx1
				w = ax2 - bx1
			elif bx1 < ax2 and bx2 < ax2:
				x = bx1
				w = bx2 - bx1
		if bx1 < ax1:
			if bx2 > ax1 and bx2 <= ax2:
				x = ax1
				w = bx2 - ax1
			elif bx2 > ax2:
				x = ax1
				w = ax2 - ax1	
		if by1 >= ay1:
			if by1 < ay2 and by2 >= ay2:
				y = by1	
				h = ay2 - by1
			elif by2 < ay2:
				y = by1
				h = by2 - by1
		elif by1 < ay1:
			if by2 > ay1 and by2 <= ay2:
				y = ay1	
				h = by2 - ay1
			elif by2 > ay2:
				y = ay1
				h = ay2 - ay1
			
		return Rect(x,y,w,h)

	
	
	
class Colour:
	def __init__(self,r,g,b):
		if pygame.version.vernum[1] == 8:
			self.colour = pygame.Color(r,g,b)
		else:
			rs = "%2x" % r
			rs = rs.replace(' ', '0')
			gs = "%2x" % g
			gs = gs.replace(' ', '0')
			bs = "%2x" % b
			bs = bs.replace(' ', '0')
			x = "#" + rs + gs + bs
			self.colour = pygame.Color(x)
	
	def set_alpha(self, a):
		self.a = a

	"""
	def get_red(self):
		#This will no doubt fail on new pygame
		return self.colour[0]
	
	def get_green(self):
		#This will no doubt fail on new pygame
		return self.colour[1]
	
	def get_blue(self):
		#This will no doubt fail on new pygame
		return self.colour[2]
	"""
	
class Mixer:
	
	def __init__(self, freq, format, channels, chunksize):
		# open 44.1KHz, signed 16bit, system byte order,
		# stereo audio, using 1024 byte chunks
		pygame.mixer.init(freq, format, channels, chunksize)
		return

	def Sound(self, filename):
		return Sound(filename)

	def Music(self, filename):
		return Music(filename)

class Sound:
	def __init__(self, filename):
		self._sound = pygame.mixer.Sound(filename)
    	
	def play(self, i = 0):
		self._sound.play(i)

	# 0 - 128
	def set_volume(self, vol):
		f = vol/128.0
		self._sound.set_volume(f)

	def stop(self):
		self._sound.stop()

class Music:
	def __init__(self, filename):
		pygame.mixer.music.load(filename)

	def play(self, i = 0):
		pygame.mixer.music.play(i)

	# 0 - 128
	def set_volume(self, vol):
		f = vol/128.0
		pygame.mixer.music.set_volume(vol)

	def stop(self):
		pygame.mixer.music.stop()
		
def load_image(filename):
	img = Image()
	img.load(filename)
	return img

def load_image_without_reformat(filename):
	img = Image()
	img.load_without_reformat(filename)
	return img

def is_wii():
	#We don't use pygame on the WII
	return False


def is_big_endian(warning=False):
	if pygame.version.vernum[1] == 7:
		#byte ordering not available in this verion
		#so cheat and asume little endian
		if warning:
			print "Error: Pygame library too old to detect sdlendian. Assuming Little endian (Intel)."
		return False
	else:	
		return pygame.get_sdl_byteorder() == pygame.BIG_ENDIAN

def is_little_endian(warning=False):
	if pygame.version.vernum[1] == 7:
		#byte ordering not available in this verion
		#so cheat and asume little endian
		if warning:
			print "Error: Pygame library too old to detect sdlendian. Assuming Little endian (Intel)"
		return True
	else:
		return pygame.get_sdl_byteorder() == pygame.LIL_ENDIAN

	
def pause(ms):
	pygame.time.wait(ms)
	
def randint(start, end):
	import random
	return random.randint(start, end)

def get_version():
	return pygame.version.vernum

def get_dir_list(dir_name):
	import os
	return os.listdir(dir_name)
