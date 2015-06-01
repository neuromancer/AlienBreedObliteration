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
import mygame

from utils import *
from movement import *
from behaviour import *
from tileloader import *
from playerstats import *
from collisionutils import *

class Frame:

	def __init__(self,tile,time,randomtime, soundname,mixer):
		self.tile = tile
		self.time = time
		self.random_time = randomtime
		self.soundname = soundname
		
		if soundname:
			s = get_sound_pathname(soundname)
			self.sound = mixer.Sound(s)
		else:
			self.sound = None
			
		print_debug("Frame: %s %d %d, %s" % (self.tile, self.time, self.random_time, self.soundname),5)

class AnimationState:
			
	def __init__(self, animation, unit):
		self.current_frame_index = 0
		self._last_update = 0
		self.animating = False
		self.animation = animation
		self.unit = unit
		
	def current_frame(self):
		return self.animation.frames[self.current_frame_index]

	def stop(self):
		self.animating = False


	def enter_state(self, time):
		self.animating = True
		self._start = time
		self._last_update = self._start
		self.animation.handle_enter_frame(self)

	def update(self, t):
		self.animation.update(self, t)

class Animation:		

	def __init__(self, unit_def, state, num_frames, fire_tile, fire_x, fire_y, finish_state):
		self.unit_def = unit_def
		self.fire_tile = fire_tile
		self.frames = []
		self.state = state
		self.fire_x = fire_x
		self.fire_y = fire_y
		self.finish_state = finish_state
		self.num_frames = num_frames
		
		print_debug("Animation: %s %s %d %d %d %s" % (self.unit_def.uni_filename, self.state, self.fire_tile, self.fire_x, self.fire_y, self.finish_state),5)

	
	
	def update(self, animation_state, t):
		if animation_state.animating:
			#only automatically cycle the frames if the frame has a time attribute
			if self.current_frame_delay(animation_state) > 0:
				if t - animation_state._last_update > self.current_frame_delay(animation_state):
					print_debug("%s, l:%d delay:%d" %(self.unit_def.uni_filename, animation_state._last_update, self.current_frame_delay(animation_state)), 4)
					animation_state.current_frame_index += 1
					if animation_state.current_frame_index >= self.num_frames:
						animation_state.current_frame_index = 0
						self.handle_end_animation(animation_state, t)
					else:
						self.handle_enter_frame(animation_state)
					animation_state._last_update = t

	def current_frame_delay(self, animation_state):
		t = animation_state.current_frame().time
		if animation_state.current_frame().random_time > -1:
			r = get_random_int(0, animation_state.current_frame().random_time)
			t += r
		return t

	

	def handle_enter_frame(self, animation_state):
		#check if there is a sound to play for this frame
		print_debug("Entering %s Frame %d tile %d" % (self.unit_def.uni_filename, animation_state.current_frame_index, animation_state.current_frame().tile),4)
		if animation_state.current_frame().sound:
			if not Cheats.getNoAudio():
            			channel = animation_state.current_frame().sound.play()
		
	def handle_end_animation(self, animation_state, time):
		#called when about to loop animation back to beginning
		#check for finishstate attribute
		if self.finish_state:
			if self.finish_state == 'remove':
				animation_state.unit.remove(time)
				print_debug("%s removed" % self.unit_def.uni_filename,1)
			
			elif self.finish_state:
				print_debug("Automatically entering state %s" % self.finish_state, 3)
				animation_state.unit.enter_state(self.finish_state, time)
				
class Unit:
	
	def __init__(self, unit_definition, time):
		self.unit_definition = unit_definition
		self.unit_state = UnitState(unit_definition, self)
		self.enter_spawn_state(time)
		# in order to provide some optimisation, the master set of units would like to know about movement and removal of this unit. We'll notify it through this observer..
		self.observer = None
		self.set_health(unit_definition.health) # the def includes the starting health
		
	def enter_spawn_state(self, time):
		if self.unit_definition.spawn_state == 'random':
			#choose a random state
			num_states = len(self.unit_definition.animations.values())
			r = get_random_int(0, num_states-1)
			state = self.unit_definition.animations.values()[r]
			self.enter_state(state.state, time)
		else:
						
			self.enter_state(self.unit_definition.spawn_state, time)
		
	
	def clone_unit(self, mixer, level, time):
		return  UnitFactory.create_unit(self.get_uni_filename(), self.unit_definition.trans, mixer, level, time)
		
	def set_observer(self, observer):
		self.observer = observer
		
	def set_pos(self, x,y):
		self.unit_definition.set_pos(x,y,self)
		if self.observer:
			self.observer.unit_position_updated(self)
	
	def get_pos(self):
		return self.unit_definition.get_pos(self.unit_state)
	
	def get_speed(self):
		return self.unit_definition.speed
	
	def draw(self, screen, view):
		self.unit_definition.draw(screen, view, self.unit_state)
		
	def get_rect(self):
		return self.unit_state.rect
	
	def get_collision_rects(self):		
		return self.unit_state.collision_rects
	
	def update(self, time, display):
		return self.unit_definition.update(time, display, self.unit_state, self)
		
	def current_state(self):
		return self.unit_state.current_state
		
	""" Useful when returning from dying. set by enter_state"""
	def previous_state(self):
		return self.unit_state.previous_state
	
		
	def stop(self):
		self.unit_definition.stop(self.unit_state)
		
	
	def collide_with(self, rect):
		return self.unit_definition.collide_with(rect, self.unit_state)
		
	def move(self, x, y):
		old_pos = self.unit_state.rect.copy()
		self.unit_state.rect = self.unit_state.rect.move(x,y)
		self.unit_state.collision_rects = self.unit_definition.calc_collision_rects(self)
		
		if self.observer:
			self.observer.unit_position_updated(self, old_pos)
		
	

	def enter_state(self, statename, time):
		if self.unit_state.current_state != statename or not self.currently_animating():
			print_debug("%s entering state %s" % (self.unit_definition.uni_filename,statename), 5)
			self.unit_state.previous_state = self.unit_state.current_state
			self.unit_state.current_state = statename
			self.current_animation_state().enter_state(time)
			
			if self.unit_definition.behaviour:
				#it will be set except during init
				self.unit_definition.behaviour.enter_state(statename, self)

	def current_animation(self):
		return self.unit_definition.animations[self.unit_state.current_state]


	def current_animation_state(self):
		return self.unit_state.current_animation_state()

	def currently_animating(self):
		s = self.current_animation_state()
		if s:
			return s.animating
		else:
			return False

	def get_uni_filename(self):
		return self.unit_definition.uni_filename

	def fire(self):
		self.unit_state.firing=True

	def current_image(self):
		return self.unit_definition.current_image(self.unit_state)

	def collide_map(self, horizontalOrVertical, pos_x, pos_y, time):
		self.unit_definition.behaviour.collide_map(self, horizontalOrVertical, pos_x, pos_y, time)
		
	def remove(self, time):
		if self.unit_definition.behaviour.on_remove(self, time):
			self.unit_state.removed = True
			if self.observer:		
				self.observer.unit_removed(self)
	
	
	def get_center_pos(self):
		return (self.unit_state.rect.x + self.unit_definition.tile_width/2, self.unit_state.rect.y + self.unit_definition.tile_height/2)
	
	def collide_unit(self, unit, intersection_rect, time):
		self.unit_definition.collide_unit(self, unit, intersection_rect, time)

	def get_object_type(self):
		return self.unit_definition.object_type

	def get_player_stats(self):
		return self.unit_state.player_stats
	
	def set_player_stats(self, player_stats):
		health = self.get_health()
		#clone the stats so that they can change without affecting any initial player stats records...
		self.unit_state.player_stats = PlayerStats.clone(player_stats)
		self.unit_state.set_health(health)

	def is_blocking_collision(self, them):
		return self.unit_definition.is_blocking_collision(self, them)
	
	def is_current_position_blocked(self):
		return self.unit_definition.is_current_position_blocked(self)
	
	def set_additional_profile(self, profile):
		self.unit_state.set_additional_profile(profile)
	
	def get_additional_profile(self):
		return self.unit_state.get_additional_profile()

	""" Only makes sense for player units"""
	def get_current_weapon(self):
		return self.unit_state.player_stats.get_weapon()

	""" Only makes sense for player units"""
	def toggle_current_weapon_up(self):
		return self.unit_state.player_stats.increment_current_weapon()

	def do_action(self, action, time):
		self.unit_definition.do_action(action, self, time)

	def get_health(self):
		return self.unit_state.get_health()

	def set_health(self, health):
		self.unit_state.set_health(health)
		
	def decrease_health(self, amount):
		return self.unit_state.decrease_health(amount)
		
	def firing(self):
		return self.unit_state.firing
	
	def start_new_life(self):
		return self.unit_state.start_new_life()
		
	def has_state(self, statename):
		return self.unit_definition.has_state(statename)
	
	def set_trigger_action(self, action):
		self.unit_state.trigger_action = action
		
	def get_collision_action(self):
		if self.unit_definition.collision_action:
			return self.unit_definition.collision_action
		else:
			return None
		
	def get_trigger_action(self):
		if self.unit_state.trigger_action:
			return self.unit_state.trigger_action
		else:
			return None
		
	def set_triggerable(self, trig):
		self.unit_state.triggerable = trig
		
	def get_triggerable(self, trig):
		#triggerable can be set on he unit_defintions (shared by all instaces)
		#or on the unit_state (unique to this instance)
		if self.unit_state.triggerable:
			return self.unit_state.triggerable
		else:
			return self.unit_definition.triggerable

	def get_current_state(self):
		return self.unit_state.get_current_state()
		
	def set_name(self, name):
		self.unit_state.set_name(name)
		
	def get_name(self):
		return self.unit_state.get_name()
	
	def get_behaviour_data(self):
		return self.unit_state.behaviour_data
	
	def collideable(self):
		return self.unit_definition.collideable
	
	def removed(self):
		return self.unit_state.removed
		
	
class UnitFactory:
		
	unit_map = dict({})
		
		
	@staticmethod
	def create_level_unit(unit_level_instance, trans, mixer, level, time):
		unit_def = UnitFactory._get_unit_definiton(unit_level_instance.file, trans, mixer, level)
		unit = Unit(unit_def, time)
		unit.set_pos(unit_level_instance.tileposx,unit_level_instance.tileposy)
		if unit_level_instance.name:
			unit.set_name(unit_level_instance.name)
		if unit_level_instance.trigger_action:
			unit.set_trigger_action(unit_level_instance.trigger_action)
		
		if unit_level_instance.state:
			unit.enter_state(unit_level_instance.state, time)
		if unit_level_instance.triggerable:
			unit.set_triggerable(unit_level_instance.triggerable)
		if unit_level_instance.health:
			unit.set_health(unit_level_instance.health)
			
		return unit
	
	@staticmethod
	def create_unit(uni_filename, trans, mixer, level, time):
		unit_def = UnitFactory._get_unit_definiton(uni_filename, trans, mixer, level)
		return Unit(unit_def, time)
	
	@staticmethod
	def _get_unit_definiton(uni_filename, trans, mixer, level):
		unit_def = None
		if uni_filename in UnitFactory.unit_map:
			unit_def = UnitFactory.unit_map[uni_filename]
		else:
			unit_def = UnitDefinition.create_unit_definition(uni_filename, trans, mixer, level)
			UnitFactory.unit_map[uni_filename] = unit_def
		return unit_def
		
	@staticmethod
	def empty():
		UnitFactory.unit_map.clear()
		
class UnitState:
		
	def __init__(self, unit_definition, unit):
		self.removed = False
		self.current_state = None
		self.firing = False
		self.animation_states = dict({})
		self.additional_profile = None
		self.health = None
		self.player_stats = None
		self.last_fire_time = 0
		self.trigger_action = None
		self.triggerable = None
		self.name = None
		self.behaviour_data = dict({})
		
		#initialise animation states for each animation
		for state in unit_definition.animations.keys():
			animation = unit_definition.animations[state]
			self.animation_states[state] = AnimationState(animation, unit)
	
	def current_animation_state(self):
		if self.current_state:
			return self.animation_states[self.current_state]
		else:
			return None

	def set_additional_profile(self, profile):
		self.additional_profile = profile

	def get_additional_profile(self):
		return self.additional_profile

	def set_health(self, health):
		"""For players health is stored on player stats. for other units it is 
		stored on the unit"""
		if self.player_stats:
			self.player_stats.set_health(health)

		else:
			self.health = health
		
	def get_health(self):
		"""For players health is stored on player stats. for other units it is 
		stored on the unit"""
		if self.player_stats:
			return self.player_stats.get_health()

		else:
			return self.health
		
	def decrease_health(self, amount):
		self.set_health(self.get_health() - amount)
		return self.get_health() <= 0
		
		
	def start_new_life(self):
		if self.player_stats:
			return self.player_stats.next_life()
		return False
	
	def get_current_state(self):
		return self.current_state
	
	def set_name(self, name):
		self.name = name
		
	def get_name(self):
		return self.name
	
class UnitDefinition:

	def __init__(self, uni_filename, trans, mixer):
		self.uni_filename = uni_filename
		print_debug("Reading Unit : %s" % self.uni_filename, 5)
		self.animations = dict({})
		self.trans = trans
		self.object_type = None
 		self.collideable = False
		self.spawn_state = None
		self.health = 0
		self.speed = 0
		self.invisible = False
		self.collision_action = None
		self.opens_with_key = False
		self.decode_uni(get_config_pathname(self.uni_filename), mixer)
		self.load_tiles()
		self.behaviour = None
		
		
		if not self.spawn_state:
			print_debug("Unit %s does not have spawn_state defined. Taking first animation"%uni_filename,4)
			v = self.animations.values()[0].state
			self.spawn_state = v
			
		
		print_debug("Finished reading Unit : %s" % self.uni_filename, 5)
		

	def decode_uni(self, filename, mixer):
		 
		BITMAP = re.compile('BITMAP file=(\S*) tileheight=(\d*) tilewidth=(\d*)')
		
		STAT_A = re.compile('STATS .*health=(\d*)')
		
		STAT_B = re.compile('STATS .*collideable=(\d*)')
		
		STAT_C = re.compile('STATS .*invisible=(\d)*')
		
		STAT_D = re.compile('STATS .*openswithkey=(\d)*')
		
		STAT_E = re.compile('STATS .*speed=(\d*)')
		
		SPAWN_OBJ = re.compile('SPAWNOBJECT file=(\S*)')
		
		SPAWN = re.compile('SPAWN state=(\S*)')
		
		ANIMATION = re.compile('ANIMATION state=(\S*) numframes=(\d*)(?:\sfiretile=(\d*))?(?:\sfirex=([\d-]*) firey=([\d\-]*))?(?:\sfinishstate=(\S*))?')

		FRAME = re.compile('FRAME tile=(\d*)(?:\stime=(\d*))?(?:\ssound=(\S*))?(?:\srandomtime=(\d*))?')
		
		OBJECTTYPE = re.compile('OBJECTTYPE type=(\S*)(?:\saitype=(\S*))?')
		
		COLLISION = re.compile('COLLISION action=(\S*)')
		BLAST = re.compile('BLAST action=(\S*)')
		
		current_anim = None
		
    		a = open(filename, "r")
		try:
			line = a.readline()
			while line:
				print_debug(line,5)
				m = BITMAP.match(line)
				if m:
					self.filename = m.group(1)
					self.tile_height = int(m.group(2))
					self.tile_width = int(m.group(3))
				m = STAT_A.match(line)
				if m:
					if m.group(1):
						self.health = int(m.group(1))
							
				m = STAT_E.match(line)
				if m:
					if m.group(1):
						self.speed = int(m.group(1))
					
				m = STAT_B.match(line)
				if m:
					c  = int(m.group(1))
					self.collideable = c == 1
				m = STAT_C.match(line)
				if m:
					i = int(m.group(1))
					self.invisible = (i == 1)
				m = STAT_D.match(line)
				if m:
					i = int(m.group(1))
					if i ==1:
						self.opens_with_key = True
						
					
				m = SPAWN_OBJ.match(line)
				if m:
					self.spawn_object = m.group(1)
				m = SPAWN.match(line)
				if m:
					self.spawn_state = m.group(1)
				m = ANIMATION.match(line)
				if m:
					state = m.group(1)
					num_frames = int(m.group(2))
					if m.group(3):
						fire_tile = int(m.group(3))
					else:
						fire_tile = -1
					if m.group(4):
						fire_x = int(m.group(4))
						if RESIZE:
							fire_x = int(fire_x * RESIZE_FACTOR)
					else:
						fire_x = -1
					if m.group(5):
						fire_y = int(m.group(5))
						if RESIZE:
							fire_y = int(fire_y *RESIZE_FACTOR)
					else:
						fire_y = -1
						
					finish_state = m.group(6)
					
					current_anim = Animation(self, state, num_frames, fire_tile, fire_x, fire_y, finish_state)
				
					self.animations[state] = current_anim
					
				m = FRAME.match(line)
				if m:
					tile = int(m.group(1))
					if m.group(2):
						time = int(m.group(2))
					else:
						time = -1
					sound = m.group(3)
					if m.group(4):
						randomtime = int(m.group(4))
					else:
						randomtime = -1
					frame = Frame(tile, time, randomtime, sound, mixer)
					
					current_anim.frames.append(frame)
					
				m = OBJECTTYPE.match(line)
				if m:
					self.object_type = m.group(1)
					self.ai_type = m.group(2)
					
				m = COLLISION.match(line)
				if m:
					self.collision_action = m.group(1)
			
				m = BLAST.match(line)
				if m:
					self.collision_action = m.group(1)


				line = a.readline()
		finally:
			a.close() 
        		
	def load_tiles(self):
		self.images, self.tile_width, self.tile_height = CompositeTileLoader.load_tiles(self.filename, self.tile_width, self.tile_height, self.trans)
		
		print_debug("%s num tiles read: %d" % (self.uni_filename, len(self.images)),4)
			
			

	def debug(self):
		for state in self.animations:
			a = self.animations[state]
			print "%s %d %d %d %s" % (a.state, a.fire_tile, a.fire_x, a.fire_y, a.finish_state)
			for f in a.frames:
				print "%s %d %s" % (f.tile, f.time, f.sound)

    	def draw(self, screen, view, unit_state):
		if not self.invisible:
			#only attempt to plot this unit if it is not removed
			if not unit_state.removed:
				#check if unit within currentview...
				if unit_state.rect.colliderect(view):
					#on screen...
					#print_debug("Drawing %s %s %d tile %d at map pos %f %f" % (self.uni_filename, self.current_animation(unit_state).state, self.current_animation_state(unit_state).current_frame_index, self.current_frame(unit_state).tile, unit_state.rect.x, unit_state.rect.y), 5)
					#Convert the map relative position of the unit
					#to screen relative by subtracting the current view offset
					screen_relative = unit_state.rect.move(-view.x, -view.y)
					#print_debug("screen pos %f %f %d %d" % (screen_relative.x, screen_relative.y, screen_relative.w, screen_relative.h), 5)
					#print_debug("screen %d %d %d %d" % (view.x, view.y, view.w, view.h), 5)
					screen.blit(self.current_image(unit_state), (screen_relative.x,screen_relative.y))
					#clear the firing flag
					unit_state.firing = False
				#else:
					#print_debug("not on screen",5)

    	def update(self, time, display, unit_state, unit):
		view = display.view
		#only attempt to update this unit if it is not removed
		if not unit_state.removed:
			#todo check if within view...
			if self.should_update(display, unit):
        			self.current_animation_state(unit_state).update(time)
				self.behaviour.update(time, display, unit)
				print_debug("Unit Updating %s %s" % (self.uni_filename, unit_state.current_state), 5)
				return True
			else:
				print_debug("Unit Not updating %s" % self.uni_filename, 5)
				return False
				
	def current_animation(self, unit_state):
		return self.animations[unit_state.current_state]

	def current_animation_state(self, unit_state):
		return unit_state.current_animation_state()

	def current_frame(self, unit_state):
		return self.current_animation_state(unit_state).current_frame()

	def current_image(self, unit_state):
		#Normally take the image from the current frame of animation - unless we are firing
		tile = None
		if unit_state.firing:
			tile = self.current_animation(unit_state).fire_tile
			print_debug("Returning firing tile %d for animation %s" % (tile, self.current_animation(unit_state).state), 5)
			
		else:
			tile = self.current_frame(unit_state).tile
			
		return self.images[tile]

	def has_state(self, statename):
		return statename in animations

	def set_pos(self, x,y, unit):
		unit_state = unit.unit_state
		unit_state.rect = mygame.Rect(x,y, self.tile_width, self.tile_height)
		unit_state.collision_rects = self.calc_collision_rects(unit)
		
		
	def get_pos(self, unit_state):
		return unit_state.rect.x, unit_state.rect.y
	
	def stop(self, unit_state):
		self.current_animation_state(unit_state).stop()

	def collide_with(self, rect, unit_state):
		if self.collideable == 1 and not unit_state.removed:
			if unit_state.rect.colliderect(rect):
				return True
			
		return False
	
	def collide_unit(self, unit_us, unit_them, intersection_rect, time):
		if Cheats.getNoUnitCollides():
			print_debug("Not registering character collision due to cheat", 2)
			return
		if not unit_them.unit_state.removed and not unit_us.unit_state.removed:
			self.behaviour.collide_unit(unit_us, unit_them, intersection_rect, time)
			
	def is_blocking_collision(self, us, them):
		return self.behaviour.is_blocking_collision(us, them)
	
	def should_update(self, display, unit):
		return self.behaviour.should_update(display, unit)

	def do_action(self, action, unit, time):
		self.behaviour.do_action(action, unit, time)
	
	def is_current_position_blocked(self, unit):
		return self.behaviour.is_current_position_blocked(unit)
	
	def calc_collision_rects(self, unit):
		return self.behaviour.get_collision_rects(unit)
	
	@staticmethod
	def create_unit_definition(uni_filename, trans, mixer, level):
		unit_def = UnitDefinition(uni_filename, trans, mixer)
		
		if unit_def.object_type == 'door':
			unit_def.behaviour = DoorBehaviour(unit_def, mixer)
		elif unit_def.object_type == 'pickup':
			unit_def.behaviour =  PickupBehaviour(unit_def, mixer)
		elif unit_def.object_type == 'spawn':
			unit_def.behaviour = SpawnerBehaviour(unit_def, mixer, level)
		elif unit_def.ai_type == 'alien':
			unit_def.behaviour = AlienBehaviour(unit_def, mixer, level)
		elif unit_def.object_type == 'friendly':
			unit_def.behaviour = PlayerBehaviour(unit_def, mixer, level)
		elif unit_def.object_type == 'projectile':
			unit_def.behaviour = ProjectileBehaviour(unit_def, mixer, level)
		elif unit_def.object_type == 'enemyprojectile':
			unit_def.behaviour = EnemyProjectileBehaviour(unit_def, mixer, level)
		elif unit_def.ai_type == 'dome':
			unit_def.behaviour = DomeBehaviour(unit_def, mixer, level)
		elif unit_def.ai_type == 'egg':
			unit_def.behaviour = EggBehaviour(unit_def, mixer, level)
		elif unit_def.ai_type == 'hostage':
			unit_def.behaviour = HostageBehaviour(unit_def, mixer, level)
		elif unit_def.object_type == 'trigger':
			unit_def.behaviour = TriggerBehaviour(unit_def, mixer, level)
		elif unit_def.ai_type == 'boss4' or unit_def.ai_type == 'boss1' or unit_def.ai_type == 'boss2' or unit_def.ai_type == 'boss3':
			unit_def.behaviour = BossBehaviour(unit_def, mixer, level)
		elif unit_def.object_type == 'forcefieldhorizontal':
			unit_def.behaviour = ForceFieldHorizontalBehaviour(unit_def, mixer)
		elif unit_def.ai_type == 'barrel':
			unit_def.behaviour = BarrelBehaviour(unit_def, mixer, level)
		elif unit_def.ai_type == 'biospike':
			unit_def.behaviour = BioSpikeBehaviour(unit_def, mixer)
		elif unit_def.ai_type == 'shipfire':
			unit_def.behaviour = ShipFireBehaviour(unit_def, mixer)
		else:	
			unit_def.behaviour = DefaultBehaviour(unit_def, mixer)
		return unit_def
