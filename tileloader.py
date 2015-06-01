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

class CompositeTileLoader:

	@staticmethod
	def load_tiles(fname, TW, TH, trans, resize=RESIZE_FACTOR):
		
		f = get_image_pathname(fname)
		img = mygame.load_image(f)
		
		#trans = img.get_at((0,0))
		#print trans
		
		w,h = img.get_width(),img.get_height()
		#calculate total number of tiles in image
		NUM = (w/TW) * (h/TH)
		
		print_debug("Num tiles # %d" % NUM, 5)
		images = [mygame.Image for x in xrange(0,NUM)]
		
		#read tiles into list
		n = 0
		
		for y in range(0,h,TH):
			for x in range(0,w,TW):
				if x + TW > w:
					break;

				print_debug("tile subsurface : %d %d %d %d" %(x,y,TW,TH),5)
				i = img.subsurface(mygame.Rect(x,y,TW,TH))
				
				if RESIZE:
					i = i.scale((int(TW *resize),int(TH *resize)))
				#set the transparent colour
				if not Cheats.getNoTransparency() and trans:
					i.set_colorkey(trans)
				images[n] = i
				n += 1
			#for some reason some imgs have borders which confuse this code
			#which assumes perfect tescellation of images
			#so we will break out of the loop if we have loaded all the tiles
			if n >= NUM:
				break
			
		if RESIZE:
			TW = int(TW *resize)
			TH = int(TH *resize)

		return images, TW, TH
		
		
	@staticmethod
	def load_indexed_tiles(start_x,start_y,width,height, rows, filename, trans):
	
		x= start_x
		y= start_y
		w= width
		h= height
		
		img = mygame.load_image(get_image_pathname(filename))
		img.set_colorkey(trans)
	
		NUM = 0
		for r in rows:
			NUM += len(r)
			
		index = []
		images = [mygame.Image for xx in xrange(0,NUM)]
		
		n = 0
		for r in rows:
			for c in r:
				if c not in index:
					index.append(c)
					i = img.subsurface(mygame.Rect(x,y,w,h))
					if RESIZE:
						i = i.scale((int(w *RESIZE_FACTOR),int(h *RESIZE_FACTOR)))
					images[n] = i
					n+=1
				x += w
	
			y+= h
			x=0
		
		return images, index
