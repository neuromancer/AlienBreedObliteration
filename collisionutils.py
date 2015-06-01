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

"""

For most units collisions will be calculated using a slightly smaller (80%)
rectangle than the visible sprite. 

Units track their position using a Rect object (x,y,w,h).
They also track their collision rectangle using a slightly smaller rectangle.
These rectangles are recalculated every time the unit moves position using the
calc_collision_rect(sprite rectangle) method

As pixel perfect collisions are very slow in SDL we approximate this for the 
large boss units by using multiple collision rectangles. In that case the 
calc_bossX_collision_rect(sprite rectangle) are used.

The boss method's rectangle dimensions are determined to approximate the 
non-transparent parts of the boss' sprite.

Which method to use is determined by the Unit's behaviour code.

"""

def calc_collision_rect(player_rect):
	f = .8
	o = .1
	
	w = player_rect.w *f
	h = player_rect.h *f
	x = player_rect.x + player_rect.w*o
	y = player_rect.y + player_rect.h*o
	return mygame.Rect(x,y,w,h)

def calc_boss2_collision_rect(player_rect):
	rects = []
	
	
	w = player_rect.w * .6
	h = player_rect.h * .6
	x = player_rect.x + player_rect.w *.2
	y = player_rect.y
	rects.append(mygame.Rect(x,y,w,h))
	
	w = player_rect.w * .2
	h = player_rect.h * .2
	x = player_rect.x + player_rect.w *.4
	y = player_rect.y + player_rect.h * .7

	rects.append(mygame.Rect(x,y,w,h))
	return rects

def calc_boss3_collision_rect(player_rect):
	rects = []
	
	
	w = player_rect.w * .6
	h = player_rect.h * .3
	x = player_rect.x + player_rect.w *.2
	y = player_rect.y + player_rect.h * 0.6
	rects.append(mygame.Rect(x,y,w,h))
	
	w = player_rect.w * .4
	h = player_rect.h * .6
	x = player_rect.x + player_rect.w *.3
	y = player_rect.y

	rects.append(mygame.Rect(x,y,w,h))
	return rects


def calc_boss4_collision_rect(player_rect):
	rects = []
	
	
	w = player_rect.w * .8
	h = player_rect.h * .4
	x = player_rect.x + player_rect.w *.2
	y = player_rect.y + player_rect.h * 0.6
	rects.append(mygame.Rect(x,y,w,h))
	
	w = player_rect.w * .5
	h = player_rect.h * .6
	x = player_rect.x + player_rect.w *.2
	y = player_rect.y

	rects.append(mygame.Rect(x,y,w,h))
	return rects


def calc_boss1_collision_rect(player_rect):
	rects = []
	
	
	w = player_rect.w * .8
	h = player_rect.h * .3
	x = player_rect.x + player_rect.w *.1
	y = player_rect.y + player_rect.h * 0.3
	rects.append(mygame.Rect(x,y,w,h))
	
	
	w = player_rect.w * .4
	h = player_rect.h * .3
	x = player_rect.x + player_rect.w *.3
	y = player_rect.y
	rects.append(mygame.Rect(x,y,w,h))
	
	
	w = player_rect.w * .6
	h = player_rect.h * .3
	x = player_rect.x + player_rect.w *.2
	y = player_rect.y + player_rect.h * 0.6
	rects.append(mygame.Rect(x,y,w,h))
	
	
	return rects
