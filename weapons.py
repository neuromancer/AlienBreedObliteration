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
 
import re

from utils import *

TOOLS_AND_WEAPONS='toolsandweapons.wep'
GUN_NO_AMMO='shotnoammo.ogg'

class ToolsAndWeapons:

	def __init__(self, mixer):
		self.weapons = []
		self.tools = []
		self.load_weapons(get_config_pathname(TOOLS_AND_WEAPONS), mixer)
		self.no_ammo_sound = mixer.Sound(get_sound_pathname(GUN_NO_AMMO))

	def load_weapons(self, filename, mixer): 
		WEAPONS = re.compile('WEAPONS total=(\d*)')
		WEAPON = re.compile('WEAPON name="([^"]*)"\s*description="([^"]*)"\s*tileimage=(\d*)\s*projectile="([^"]*)"\s*firesound="([^"]*)"\s*cost=(\d*)\s*firetime=(\d*)\s*repeattime=(\d*)\s*nozzelflash=(\S*)\s*pitchvary=(\S*)\s*arc=(\S*)\s*bounce=(\S*)')

		TOOLS = re.compile('TOOLS total=(\d*)')
		TOOL = re.compile('TOOL name="([^"]*)"\s*description="([^"]*)"\scost=(\d*)')
		
		num_weapons_read = 0
		num_tools_read = 0
    		a = open(filename, "r")
		try:
			line = a.readline()
			while line:
				print_debug(line,5)
				m = WEAPONS.match(line)
				if m:
					self.total_weapons = int(m.group(1))
					print_debug("Total weapons%d" % (self.total_weapons), 5)
				m = WEAPON.match(line)
				if m:
					name = m.group(1)
					desc = m.group(2)
					tile = int(m.group(3))
					projectile = m.group(4)
					fire_sound = m.group(5)
					cost= int(m.group(6))
					fire_time = int(m.group(7))
					repeat_time= int(m.group(8))
					nozzel_flash=m.group(9)=='true'
					pitch_vary = m.group(10)=='true'
					arc = m.group(11)=='true'
					bounce = m.group(12)=='true'
					weapon = Weapon(name, desc, tile, projectile, fire_sound, cost, fire_time, repeat_time, nozzel_flash, pitch_vary, arc, bounce, mixer)
					
					num_weapons_read +=1
					self.add_weapon(weapon)
					
				m = TOOLS.match(line)
				if m:
					self.total_tools = int(m.group(1))
					
				m = TOOL.match(line)
				if m:
					name = m.group(1)
					desc =m.group(2)
					cost = int(m.group(3))
					
					tool = Tool(name, desc, cost)
					self.add_tool(tool)
					
					num_tools_read +=1
					
				line = a.readline()
		finally:
			a.close() 
			
		print_debug("num weapons read %d" % num_weapons_read, 5)
		print_debug("num tools read %d" % num_tools_read, 5)

	def add_tool(self, tool):
		self.tools.append(tool)
		
	def add_weapon(self, weapon):
		self.weapons.append(weapon)

	def get_weapon(self, weapon_index):
		return self.weapons[weapon_index]

	def get_all_weapons(self):
		return self.weapons

	def get_num_weapons(self):
		return len(self.weapons)
		
	def play_no_ammo_sound(self):
		if not Cheats.getNoAudio():
			self.no_ammo_sound.play()

	def get_all_tools(self):
		return self.tools
		
class Weapon:
	def __init__(self, name, desc, tile, projectile, fire_sound, cost, fire_time, repeat_time, nozzel_flash, pitch_vary,  arc, bounce, mixer):
		self.name = name
		self.desc = desc
		self.tile = tile
		self.projectile = projectile
		self.fire_sound = fire_sound
		self.cost = cost
		self.fire_time = fire_time
		self.repeat_time =  repeat_time
		self.nozzel_flash = nozzel_flash
		self.pitch_vary = pitch_vary
		self.fire_sound = mixer.Sound(get_sound_pathname(fire_sound))
		self.arc = arc
		self.bounce = bounce
		
		print_debug("Weapon %s %s %d %s %s %d %d %d %d %d %d %d" % (name, desc, tile, projectile, fire_sound, cost, fire_time, repeat_time, nozzel_flash, pitch_vary, arc,  bounce),5)


	def play_fire_sound(self):
		if not Cheats.getNoAudio():
			self.fire_sound.play()

class Tool:
	def __init__(self, name, desc, cost):
		self.name = name
		self.desc = desc
		self.cost = cost
		
		print_debug("Tool %s %s %d" % (name, desc, cost),5)
