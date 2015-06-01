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

import wiidetect as detect
WII = detect.is_wii()

PALETTE_IMG="images/tileset1.bmp"

if not WII:
	
	DEPTH=16
#	DEPTH=8
#	SCREEN_X=800
#	SCREEN_Y=600
#	SCREEN_X=400
#	SCREEN_Y=300
	SCREEN_X=640
	SCREEN_Y=480

	REFRESH_RATE = 20
#	REFRESH_RATE = 15
	FREQ=22050

	#Resize all images and rectangle dimensions...
	RESIZE = True
#	RESIZE = False
	RESIZE_FACTOR = 1.5
	HUD_RESIZE_FACTOR = 1.6
#	RESIZE_FACTOR = 2
#	HUD_RESIZE_FACTOR = 2


else:
	""" Wii Python does not have os module, fixed audio frequency and lower resolution """
	
#	DEPTH=16
	DEPTH=8
	SCREEN_X=640
	SCREEN_Y=480
	REFRESH_RATE = 25
	FREQ=32000

	RESIZE = True
	RESIZE_FACTOR = 1.5
	HUD_RESIZE_FACTOR = 1.6


if not WII:
	import os
	
DEBUG_LEVEL=0
VERSION_STRING="Public beta release - Build 18 - 261010"

DEBUG_COLLISIONS=False

class Cheats:

	CHEAT_NO_ALIENS=False
	CHEAT_WALK_THROUGH_WALLS=False
	CHEAT_NO_UNIT_COLLIDES=False
	CHEAT_PLOT_INVISIBLE=False	
	CHEAT_NO_COLLISIONS=False
	CHEAT_NO_MAP_PLOT=False
	CHEAT_NO_HURT=False
	CHEAT_NO_TRANSPARENCY=False
	CHEAT_INTEX_ANYWHERE=False
	CHEAT_QUICK_QUIT=False
	CHEAT_NO_MOVE_BOSS=False
	CHEAT_NO_HURT_BOSS=False
	CHEAT_PLOT_SPECIAL_TILES=False
	CHEAT_NO_AUDIO=False
	CHEAT_NO_COUNTDOWN=False
	CHEAT_LOG_COLLISIONS=False
	#An eperiment with a different tile plotter ('display2.py')
	#Doesn't work on WII. Has no effect unless display2 imported in scene.py
	CHEAT_QUICK_BG=True
	CHEAT_BUTTON=False
	CHEAT_NEXT_LEVEL=False
	
	@staticmethod
	def getCheatNextLevelMenu():
		return Cheats.CHEAT_NEXT_LEVEL
	@staticmethod
	def getCheatButtonEnabled():
		return Cheats.CHEAT_BUTTON
	
	@staticmethod
	def getNoTransparency():
		return Cheats.CHEAT_NO_TRANSPARENCY
	
	@staticmethod
	def toggleNoHurt():
		Cheats.CHEAT_NO_HURT = not Cheats.CHEAT_NO_HURT
	
	@staticmethod
	def getNoHurt():
		return Cheats.CHEAT_NO_HURT
	
	@staticmethod
	def toggleNoMapPlot():
		Cheats.CHEAT_NO_MAP_PLOT=not Cheats.CHEAT_NO_MAP_PLOT
	
	@staticmethod
	def getNoMapPlot():
		return Cheats.CHEAT_NO_MAP_PLOT
	
	@staticmethod
	def getNoCollisions():
		return Cheats.CHEAT_NO_COLLISIONS
	
	@staticmethod
	def toggleNoCollisions():
		Cheats.CHEAT_NO_COLLISIONS = not Cheats.CHEAT_NO_COLLISIONS
	
	@staticmethod
	def toggleWalkThroughWalls():
		Cheats.CHEAT_WALK_THROUGH_WALLS= not Cheats.CHEAT_WALK_THROUGH_WALLS

	@staticmethod
	def getWalkThroughWalls():
		return Cheats.CHEAT_WALK_THROUGH_WALLS
	
	@staticmethod
	def getNoAliens():
		return Cheats.CHEAT_NO_ALIENS
	
	@staticmethod
	def getNoUnitCollides():
		return Cheats.CHEAT_NO_UNIT_COLLIDES
	
	@staticmethod
	def getPlotInvisible():
		return Cheats.CHEAT_PLOT_INVISIBLE
	
	@staticmethod
	def togglePlotInvisible():
		Cheats.CHEAT_PLOT_INVISIBLE = not Cheats.CHEAT_PLOT_INVISIBLE
	
	@staticmethod
	def toggleNoCountdown():
		Cheats.CHEAT_NO_COUNTDOWN = not Cheats.CHEAT_NO_COUNTDOWN
	
	@staticmethod
	def toggleNoAudio():
		Cheats.CHEAT_NO_AUDIO = not Cheats.CHEAT_NO_AUDIO
	
	
	@staticmethod
	def getIntexAnywhere():
		return Cheats.CHEAT_INTEX_ANYWHERE
	
	@staticmethod
	def get_quick_quit():
		return Cheats.CHEAT_QUICK_QUIT

	@staticmethod
	def getNoMoveBoss():
		return Cheats.CHEAT_NO_MOVE_BOSS
	
	@staticmethod
	def getNoHurtBoss():
		return Cheats.CHEAT_NO_HURT_BOSS
	
	@staticmethod
	def getPlotSpecialTiles():
		return Cheats.CHEAT_PLOT_SPECIAL_TILES

	@staticmethod
	def getNoAudio():
		return Cheats.CHEAT_NO_AUDIO

	@staticmethod
	def getNoCountdown():
		return Cheats.CHEAT_NO_COUNTDOWN

	@staticmethod
	def getLogCollisionsInfo():
		return Cheats.CHEAT_LOG_COLLISIONS
	
	@staticmethod
	def toggleLogCollisionsInfo():
		Cheats.CHEAT_LOG_COLLISIONS = not Cheats.CHEAT_LOG_COLLISIONS
	
        @staticmethod
        def getQuickBg():
                return Cheats.CHEAT_QUICK_BG

        @staticmethod
        def toggleQuickBg():
                Cheats.CHEAT_QUICK_BG = not Cheats.CHEAT_QUICK_BG

def load_cheats():
	try:
		cheats = load_text_file_as_string_array('cheat.txt')
		if len(cheats)>0:
			cheat_button = cheats[0].rstrip() == 'cheatbutton=true'
			Cheats.CHEAT_BUTTON = cheat_button
		if len(cheats)>1:
			no_aliens = cheats[1].rstrip() == 'noaliens=true'
			Cheats.CHEAT_NO_ALIENS = no_aliens
		if len(cheats)>2:
			quick_quit=cheats[2].rstrip() == 'quickquit=true'
			Cheats.CHEAT_QUICK_QUIT=quick_quit
		if len(cheats)>3:
			no_hurt=cheats[3].rstrip() == 'nohurt=true'
			Cheats.CHEAT_NO_HURT=no_hurt
		if len(cheats)>4:
			intex=cheats[4].rstrip() == 'intexanywhere=true'
			Cheats.CHEAT_INTEX_ANYWHERE=intex
		if len(cheats)>5:
			next_level=cheats[5].rstrip() == 'nextlevel=true'
			Cheats.CHEAT_NEXT_LEVEL=next_level
	except IOError:
		#Ignore - means there is no cheat file
		return

def print_debug(m,level):
	if DEBUG_LEVEL >= level:
		print m
	return
	
		
def get_sound_pathname(soundname):
	#The PC version will play the oggs...
	#Convert all wavs to oggs (they are oggs but the config says wav)
	s = soundname.replace('.wav','.ogg')
	if not WII:
		return os.path.join('sounds', s)
	else:
		#The WII version can only play WAVs...
		s = soundname.replace('.ogg','.wav')
		return 'sounds/' + s
	
def get_image_pathname(imgname):
	if not WII:
		return os.path.join('images', imgname)
	else:
		return 'images/' + imgname

def get_config_pathname(name):
	if not WII:
		return os.path.join('config', name)
	else:
		return 'config/' + name

def get_saved_game_directory():
	return 'savedgames'

def get_saved_game_pathname(name):
	if not WII:
		return os.path.join('savedgames', name)
	else:
		return 'savedgames/' + name

def get_level_filename(level_num):
	return 'level' + str(level_num) + '.lev'

import mygame

class KeySet:
	
	def __init__(self):
		self.left = mygame.MY_K_LEFT
		self.right = mygame.MY_K_RIGHT
		self.up = mygame.MY_K_UP
		self.down = mygame.MY_K_DOWN
		self.fire = mygame.MY_K_FIRE
		self.change_weapon = mygame.MY_K_CYCLE_WEAPON
		self.escape = mygame.MY_K_QUIT
		self.walls = mygame.MY_K_CHEAT
		self.fps = mygame.MY_K_FPS
		self.intex = mygame.MY_K_INTEX
		self.run = mygame.MY_K_RUN


	@staticmethod
	def load_key_set():
		return KeySet()

def load_text_file_as_string(filename): 
	a = open(filename, "r")
	try:
		text = ""
		line = a.readline()
		while line:
			text += line
			line = a.readline()
		return text
	finally:
		a.close() 

def load_text_file_as_string_array(filename): 
	a = open(filename, "r")
	try:
		lines = []	
		line = a.readline()
		while line:
			lines.append(line)
			line = a.readline()
		return lines
	finally:
		a.close() 


def get_random_int(start,end):
	return mygame.randint(start,end)


def get_saved_game_list():
	return mygame.get_dir_list(get_saved_game_directory())

