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
import math

DELAY = 100

class Star:

	WHITE =mygame.Colour(255, 255, 255)
	BLACK =mygame.Colour(20, 20, 40)
	LIGHTGREY =mygame.Colour(180, 180, 180)
	DARKGREY = mygame.Colour(120, 120, 120)

	def __init__(self, x, y, speed, size):
		self.x = x
		self.y = y
		self.speed = speed
		self.last_update = 0
		self.size = size
	

	def update(self, time):
		if time > self.last_update - DELAY:
			self.x += self.speed[0]
			self.y += self.speed[1]
			self.colour = mygame.randint(0,16)
			self.last_update = time	

	def draw(self, screen):
		if self.colour<4:
			colour = Star.BLACK
		elif self.colour<10:
			colour = Star.DARKGREY
		elif self.colour<13:
			colour = Star.LIGHTGREY
		else:
			colour = Star.WHITE
			
		if self.size==1:
			screen.set_at((self.x, self.y), colour)
		if self.size==2:
			screen.set_at((self.x, self.y), colour)
			screen.set_at((self.x+1, self.y), colour)
			screen.set_at((self.x, self.y+1), colour)
			screen.set_at((self.x+1, self.y+1), colour)
		if self.size>3:
			screen.set_at((self.x, self.y), colour)
			screen.set_at((self.x+1, self.y), colour)
			screen.set_at((self.x, self.y+1), colour)
			screen.set_at((self.x+1, self.y+1), colour)
			screen.set_at((self.x+2, self.y), colour)
			screen.set_at((self.x+2, self.y+1), colour)
			
			
			
	
class StarField:

	def __init__(self, view):
		self.view = view
	
		
	def start(self):
		self.star_planes = []
	
		for plane in range(0,3):
			star_plane = []
			self.star_planes.append(star_plane)
				
			for star in range(0,10):
				s = self.random_star(3-plane*20)
				star_plane.append(s)
			
	def update(self, time):
		for plane in self.star_planes:
			for star in plane:
				star.update(time)
				if self.offscreen(star):
					self.restart_star(star)
					
	def draw(self, screen):
		for plane in self.star_planes:
			for star in plane:
				star.draw(screen)
		
	def offscreen(self, star):
		return star.x > (self.view.x + self.view.w) or star.x < self.view.x or star.y > (self.view.y + self.view.w) or star.y < self.view.y

	def random_star(self, speed):
		x,y = self.get_rand_pos()
		s = int(math.sqrt(math.pow(speed,2) / 2))
		ss = (-s,s)			
		size = mygame.randint(0,4)
		return Star(x,y, ss, size)
	
	def get_rand_pos(self):
		r = mygame.randint(0,1)
		if r:
			x = mygame.randint(self.view.x, self.view.x+self.view.w)
			y = mygame.randint(self.view.y-100, self.view.y)
		else:
			x = mygame.randint(self.view.x+self.view.w, self.view.x+self.view.w+100)
			y = mygame.randint(self.view.y, self.view.y+self.view.h)
		
		return x,y
	
	def restart_star(self, star):
		star.x,star.y = self.get_rand_pos()
		
