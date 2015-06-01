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

from playerstats import *
from levelstate import *

class Display:
		
	def __init__(self,level, refresh_rate, my_game):
        	self.view = mygame.Rect(0,0,0,0)
		self.level = level
		self.border_ratio = 5
		self.hud = Hud(level.get_player().get_player_stats(), level.my_game)
		self.refresh_rate = refresh_rate
		self.countdown_overlay = None
		self.debug_alien_path = None
		self.palette_switched = False
		self.my_game = my_game
		
	def paint(self,s):
		sw,sh = s.get_width(),s.get_height()
		self.view.w,self.view.h = sw,sh
		
		if self.level.get_level_state().get_game_mode() == LevelState.INTEX or self.level.get_level_state().get_game_mode() == LevelState.SCANNER:
			self.level.intex_menu.draw(s)
		elif self.level.get_level_state().get_game_mode() == LevelState.TRANSITION:
			self.clear_background(s)
		else:
			self.clear_background(s)
			if not Cheats.getNoMapPlot():
				self.draw_level_tiles(s, self.view.w, self.view.h)
			self.draw_units(s, self.view.w, self.view.h)
			self.draw_countdown(s, self.view.w, self.view.h)	
			self.hud.paint(self.view, s)
			
			if self.level.get_level_state().get_game_mode() == LevelState.IN_GAME_MENU:
				self.level.in_game_menu.draw(s)
				
			if self.debug_alien_path:
				self.plot_debug_alien_path(s)
	def close(self):
		return
		
	def clear_background(self, s):
		s.fill(mygame.Colour(0,0,0))
		
	def draw_level_tiles(self, s, sw, sh):
		tiles = self.level.tile_set
		tw,th = tiles[0].image.get_width(),tiles[0].image.get_height()
		w = sw
		h = sh
		plot_special = Cheats.getPlotSpecialTiles()
		
		ox,oy = self.view.x,self.view.y
		yy = - (self.view.y%th) 
		my = (oy+sh)/th
		if (oy+sh)%th: my += 1
				
		level_height = self.level.level_height
		for y in xrange(oy/th,my):
			if y < h:
				xx= - (self.view.x%tw)
				mx = (ox+sw)/tw
				if y>=0 and y <level_height:
					map_lower = self.level.level_map_lower[y]
					map_upper = self.level.level_map_upper[y]
				for x in xrange(ox/tw,mx+1):
					if x<w:
						
						if y<0 or y >= level_height:
							#off map (y) so plot blank tile
							lower_tile = tiles.BLACK_TILE
							upper_tile = tiles.BLACK_TILE
						elif x<0 or x >= self.level.level_width:
							#off map (x) so plot blank tile
							lower_tile = tiles.BLACK_TILE
							upper_tile = tiles.BLACK_TILE
						else:
							#within map bounds so read tile
							lower_tile = int(map_lower[x])
							upper_tile = int(map_upper[x])
						
						
						#tile 0 is used for plotting black background so is not special
						
						special_lower_tile = False
						if lower_tile > 0 and lower_tile <16:
							#Special tile
							special_lower_tile = True
							
						#Plot the lower tile if not special or we have show special enabled
						if not special_lower_tile or plot_special:
							#Plot lower tile
							img = tiles[lower_tile].image 
							s.blit(img,(xx,yy))
								
						#If the lower tile is special and our
						#cheats specify show special then dont
						#show upper tile over the top
						plot_upper = True
						if plot_special and special_lower_tile:
							plot_upper = False
							
						if plot_upper:
							#Tiles 0- 15 are used as invisible items
							if upper_tile >0 and upper_tile < 16:
								#Special tile
								if plot_special:
									plot_upper = True
								else:
									plot_upper = False
								
							if plot_upper:
								img = tiles[upper_tile].image 
								s.blit(img,(xx,yy))
						
							
					xx += tw
					
			yy+=th
				
		
	def draw_units(self, s, sw, sh):
		for u in self.level.get_all_units():
			#print_debug("Unit pos %f %f" %(u.get_pos()), 5)
			#print_debug("View pos %d %d" % (self.view.x,self.view.y),5)
			u.draw(s, self.view)
			
	def draw_countdown(self, s, sw, sh):
		countdown = self.level.get_countdown()
		if self.level.get_level_state().get_game_mode() == LevelState.COUNTDOWN:
			self.fade_red()
			countdown.draw(s)
	
	def fade_red(self):
		#Different strategy for 8bit palette mode
		#and 16 bit RGB mode
		if DEPTH == 8:
			self.fade_red_8bit()
		else:
			self.fade_red_16bit()
	
	def fade_red_8bit(self):
		#8bit palette mode allows us to teak the palette in use
		if not self.palette_switched:
			palette = self.my_game.get_screen().get_display_palette()
			new_palette=[]
			for c in palette:
				new_palette.append((c[0], 0, 0))
			self.my_game.get_screen().set_display_palette(new_palette)
			self.palette_switched = True
	
	def fade_red_16bit(self):
		#For bpp >8 we can't use palette switches so must use an alpha overlay
		s = self.my_game.get_screen()
		if not self.countdown_overlay:	
			sw,sh = s.get_width(),s.get_height()
			self.countdown_overlay = self.level.my_game.create_blank((sw,sh))
			self.countdown_overlay.fill(mygame.Colour(0xff, 0, 0))
			self.countdown_overlay.set_alpha(128)
		if not Cheats.getNoCountdown():	
			s.blit(self.countdown_overlay, (0,0))
					
				
	def scroll(self,x,y):
		self.view.x += x
		self.view.y += y
	

    	""" Convert a view position to a tile position
	"""
	def view_to_tile(self,pos):
		x,y = pos
		tiles = self.level.tile_set
		tw,th = tiles[0].image.get_width(),tiles[0].image.get_height()
		return x/tw,y/th
        
	""" Convert a tile position to a view position
	"""
    	def tile_to_view(self,pos):
		x,y = pos
		tiles = self.level.tile_set
		tw,th = tiles[0].image.get_width(),tiles[0].image.get_height()
		x,y = x*tw, y*th 
		return x,y

	def rect_at_edge(self, rect):
		xborder = self.view.w / self.border_ratio
		yborder = self.view.h / self.border_ratio
		#calc rec within center of screen excluding border
		vrect = Rect(self.view)
		vrect.x += xborder
		vrect.y += yborder
		vrect.w -= xborder*2
		vrect.h -= yborder*2 
		
		return not vrect.contains(rect)	
	
	def rect_just_off_screen(self, rect):
		xborder = self.view.w / self.border_ratio
		yborder = self.view.h / self.border_ratio
		#calc rec encompasing the current view plus border on every edge
		vrect = self.view.copy()
		vrect.x -= xborder
		vrect.y -= yborder
		vrect.w += xborder*2
		vrect.h += yborder*2 
		
		if vrect.contains(rect):
			#within screen + borders
			#verify not on screen (i.e. within borders)...
			return not self.view.colliderect(rect)
		
		return False
	
	def rect_just_off_and_on_screen(self, rect):
		xborder = self.view.w / self.border_ratio
		yborder = self.view.h / self.border_ratio
		#calc rec encompasing the current view plus border on every edge
		vrect = self.view.copy()
		vrect.x -= xborder
		vrect.y -= yborder
		vrect.w += xborder*2
		vrect.h += yborder*2 
		
		return vrect.contains(rect)
	
	def center_on_player(self, screen):
		player_x = self.level.get_player().get_rect().x
		player_y = self.level.get_player().get_rect().y
	
		scroll_to_x = player_x - screen.get_width() / 2
		scroll_to_y = player_y - screen.get_height() / 2
		self.scroll(scroll_to_x, scroll_to_y)
		
		
	#For debugging alien AI path finding we'll plot one path	
	def add_debug_alien_path(self, path):
		self.debug_alien_path = path
		
	#For debugging alien AI path finding we'll plot one path	
	def plot_debug_alien_path(self, screen):
		tiles = self.level.tile_set
		for pi in range(0,self.debug_alien_path.length()):
			s = self.debug_alien_path.get_step(pi)
			
			img = tiles[14].image 
			xx,yy = self.tile_to_view((s.x, s.y))
			ox,oy = self.view.x,self.view.y
			screen.blit(img,(xx-ox,yy-oy))
