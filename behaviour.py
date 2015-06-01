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
from movement import *
from charactermovement import *
from levelstate import *
from delayedcommands import *
from alienpath import *
from action import *

"""

All dynamic, non-tile objects in the game are Units.

All Units are modeled the same. Any behaviour which is specific to the Unit's
type (Player, Alien, Projectile etc) is encapsulated in the Unit's Behaviour
class. Every unit has a Behaviour class.

The Behavior class is responsible for performing behaviour on updating, 
collisions, trigger actions etc.

The DefaultBehaviour superclass is suitable for non-moving simle animation 
objects (like vents/fans). Anything that moves, hurt, shoots or can be 
destroyed is modeled as a subclass.

A number of units in the game exhibit similar behaviour (Dome, Eggs, Hostages). 
They can be shot and destroyed, when all are destroyed the game typically enters 
countdown or the exit becomes available. The first occurance of these are Dome 
objects so these are all modeled as Dome objects.

Behaviour objects belong to the UnitDefinition - a single instance per type of Unit.
Therefore they do not contain data specific to a particular unit instance. For example
the AlienBehaviour object is shared by all Alien instances.

Most methods take an argument of the actual Unit instance. If the behaviour needs to store
state data between method calls (for example tracking movement status or firing state) then
the Unit instance has a map for this purpose: unit.get_behaviour_data()

Most behaviour an be accompalished by modifying the unit's state by calling unit.enter_state(state)
e.g. enter_state('dying'), checking or setting the unit's player_state for 
example unit.get_player_state().add_ammo() or by changing level state e.g. level.start_countdown()

Some Units have complex Actions (for example Triggers) written using a simple action language. Those
behaviours delegate to an ActionHandler class to process those actions.

"""


GIVE_LIFE_SOUND=get_sound_pathname('life.ogg')
GIVE_KEY_SOUND=get_sound_pathname('key.ogg')
GIVE_AMMO_SOUND=get_sound_pathname('ammo.ogg')
GIVE_CREDITS_SOUND=get_sound_pathname('money.ogg')
PLAYER1_REQUIRES_KEYS_SOUND=get_sound_pathname('voc_key.ogg')
GIVE_PASS_SOUND=get_sound_pathname('pass.ogg')
SHOT_DOOR_SOUND=get_sound_pathname('shotdoor.ogg')


"""
Behaviour suitable for non-moving units which cannot be interacted with.

Also contains some useful methods common to subclasses (for example handling
hurt and dying states.
"""
class DefaultBehaviour:
	
	def __init__(self, unit_definition, mixer):
		self.unit_definition = unit_definition
		self.mixer = mixer
		
	def collide_unit(self, us, them, intersection_rect, time):
		return
	
	def collide_map(self, unit, horizontalOrVertical, pos_x, pos_y, time):
		return
	
	def is_blocking_collision(self, us, them):
		return False
	
	"""Majority of units update if on sceen"""
	def should_update(self,display, unit):
		return unit.get_rect().colliderect(display.view)
	
	def enter_state(self, statename, unit):
		return
	
	def update(self, time, display, unit):
		return
	
	def do_action(self, action, unit, time):
		return
	
	def on_remove(self, unit, time):
		""" By default allow the removal of the unit when requested """
		return True
	
	
	def hurt_unit(self, action, unit):
		dead = False
		collision = False
		
		if action == 'Hurt5':
			dead = unit.decrease_health(5)
		if action == 'Hurt10':
			dead = unit.decrease_health(10)
		if action == 'Hurt20':
			dead = unit.decrease_health(20)
		if action == 'Hurt30':
			dead = unit.decrease_health(30)
		if action == 'Hurt40':
			dead = unit.decrease_health(40)
		
		if action == 'HurtByPlayer':
			dead = unit.decrease_health(40)
			collision = True
				
		return dead,collision


	def state_not_dying(self, current_state):
		not_dying= current_state != 'dying' and current_state[0:3] != 'die'
		return not_dying

	def enter_dying_state(self, unit, time):
		if unit.get_current_state() == 'idle':
			unit.enter_state('dying', time)
		else:
			state = unit.current_state()[4:]
			die_state = 'die' + state
			unit.enter_state(die_state, time)

	def is_current_position_blocked(self):
		return False
	
	def get_collision_rects(self, unit):
		# By default all units will return a single rectangle
		# for collision detection. Some units (Bosses) will 
		# be different
		rects = []
		rects.append(calc_collision_rect(unit.get_rect()))
		return rects
	
	
class DoorBehaviour(DefaultBehaviour):
		
	def __init__(self, unit_definition, mixer):
		DefaultBehaviour.__init__(self, unit_definition, mixer)
		self.player1_requires_keys_sound = mixer.Sound(PLAYER1_REQUIRES_KEYS_SOUND)
	
		
	def collide_unit(self, unit, character_unit, intersection_rect, time):
		print_debug("Door collision with %s" % character_unit.get_object_type(),2)
		
		if character_unit.get_object_type() == 'friendly':
			if unit.current_state() == 'closed' and self.unit_definition.opens_with_key:
				#check if player has keys...
				if character_unit.get_player_stats().keys() > 0:
					unit.enter_state('opening', time)
					character_unit.get_player_stats().use_key()
		
				else:
					#only play this once
					if not character_unit.get_player_stats().key_warning:
						if not Cheats.getNoAudio():
							self.player1_requires_keys_sound.play()
						character_unit.get_player_stats().key_warning = True
						
	def is_blocking_collision(self, us, them):
		return us.current_state() != 'open'
	
	def do_action(self, action, unit, time):
		
		if unit.current_state() == 'closed':
			dead, collision = self.hurt_unit(action, unit)
			
			if dead:
				unit.enter_state('opening', time)
		return

	

class PickupBehaviour(DefaultBehaviour):
		
	def __init__(self, unit_definition, mixer):
		DefaultBehaviour.__init__(self, unit_definition, mixer)
		self.give_life_sound = mixer.Sound(GIVE_LIFE_SOUND)
		self.give_key_sound = mixer.Sound(GIVE_KEY_SOUND)
		self.give_ammo_sound = mixer.Sound(GIVE_AMMO_SOUND)
		self.give_credits_sound = mixer.Sound(GIVE_CREDITS_SOUND)
		self.give_aid_sound = self.give_credits_sound
		self.give_pass_sound = mixer.Sound(GIVE_PASS_SOUND)
		
	
	def collide_unit(self, unit, character_unit, intersection_rect, time):
		print_debug("Pickup collision with %s" % character_unit.get_object_type(),2)
		if character_unit.get_object_type() == 'friendly':
			if unit.current_state() == 'idle':
				unit.enter_state('dying', time)
				action = unit.get_collision_action()
				self.perform_action(action, character_unit)

	def perform_action(self, action, character_unit):
		print_debug("Action %s" % action, 2)
		if action == 'Give1Life':
			if not Cheats.getNoAudio():
				self.give_life_sound.play()
			character_unit.get_player_stats().add_life()
			
		if action == 'Give1Key':
			if not Cheats.getNoAudio():
				self.give_key_sound.play()
			character_unit.get_player_stats().add_key()
			
		if action == 'Give1AmmoClip':
			if not Cheats.getNoAudio():
				self.give_ammo_sound.play()
			character_unit.get_player_stats().add_ammo_pack()
			
		if action == 'Give1FirstAid':
			if not Cheats.getNoAudio():
				self.give_aid_sound.play()
			character_unit.get_player_stats().add_energy_pack()
			
		if action == 'Give100Credits':
			if not Cheats.getNoAudio():
				self.give_credits_sound.play()
			character_unit.get_player_stats().money += 100
		
		if action == 'Give1000Credits':
			if not Cheats.getNoAudio():
				self.give_credits_sound.play()
			character_unit.get_player_stats().money += 1000
			
		if action == 'Give10000Credits':
			if not Cheats.getNoAudio():
				self.give_credits_sound.play()
			character_unit.get_player_stats().money += 10000

		if action == 'GiveBluePass':
			if not Cheats.getNoAudio():
				self.give_pass_sound.play()
			character_unit.get_player_stats().blue_pass = True
			
class SpawnerBehaviour(DefaultBehaviour):
	
	def __init__(self, unit_definition, mixer, level):
		DefaultBehaviour.__init__(self, unit_definition, mixer)
		#Need a call back when creating new aliens...
		self.level = level
	
	def handle_spawn(self, unit):
		
		if Cheats.getNoAliens():
			print_debug("spawner not spawning due to cheat", 3)
			return
		
		print_debug("spawner handle_spawn %s " % (self.unit_definition.spawn_object), 3)
		if not self.level.at_max_aliens_on_screen(): 
			if not self.spawner_blocked(unit):
				self.level.add_new_alien_unit(self.unit_definition.spawn_object, unit.get_rect().x, unit.get_rect().y)
		#else:
		#	print "Not spawning as too many aliens on screen"
		
	def spawner_blocked(self,spawner):
		#Check target space clear of units:
		spawner_blocked = False
		c_units = self.level.get_units_for_collision_detection(spawner.get_rect())
		for u in c_units:
			if u != spawner and  u.get_rect().colliderect(spawner.get_rect()):
				return True
		return False
		
	"""spawners update when just off the screen"""
	def should_update(self, display, unit):
		return display.rect_just_off_screen(unit.get_rect())
	
	def enter_state(self, statename,unit):
		if statename == 'spawning':
			self.handle_spawn(unit)

PLAYER_INVULNERABILITY_TIME=2000

class PlayerBehaviour(DefaultBehaviour):
			
	def __init__(self, unit_definition, mixer, level):
		DefaultBehaviour.__init__(self, unit_definition, mixer)
		#Need a call back when moving player...
		self.level = level	
	
	def update(self, time, display, unit):
		self.level.player_mover.handle_key_press(unit, time)
		kh = self.level.player_mover.get_key_handler()
		
		if kh.is_firing() and unit.current_state() != 'dying':
			self.handle_fire(time, display, unit)
		
		if kh.change_weapons():
			self.handle_weapon_toggle(time, unit)
		
	def collide_unit(self, us, them, intersection_rect, time):
		if "pickup" == them.get_object_type() or "door" == them.get_object_type() or "character" == them.get_object_type() or "trigger" == them.get_object_type():
			#let the thing we have hit handle the collision...
			them.collide_unit(us, intersection_rect, time)
		
		return
		
	def handle_weapon_toggle(self, time, unit):
		weapon = unit.toggle_current_weapon_up()
		print_debug("current weapon %s" % unit.get_current_weapon().name, 5)
		
		
	def handle_fire(self, time, display,unit):
		print_debug("player fire", 3)
		if unit.get_player_stats().ammo > 0:
			weapon = unit.get_current_weapon()
			lt = unit.unit_state.last_fire_time
			rt = weapon.repeat_time
			if (time - lt) > rt:
				unit.unit_state.last_fire_time = time
			
				#Tell the unit to change to firing frame...
				unit.fire() 
				weapon.play_fire_sound()
				unit.get_player_stats().ammo -=1
				
				#determine firing frame and bullet coordinates...
				current_animation = unit.current_animation()
				
				#the bullet and gun flare are plotted adjacent to the player in the direction of movement
				#use the player state to determine correct bullet state
				player_state = unit.current_animation().state
				fire_x=current_animation.fire_x
				fire_y=current_animation.fire_y
				
				self.create_bullet(unit, player_state, fire_x, fire_y, weapon, time)
				self.plot_gunflare(unit, player_state, fire_x, fire_y, weapon, time)
		
		else:
			self.level.weapons.play_no_ammo_sound()
			
			
	def create_bullet(self, unit, player_state, fire_x, fire_y, weapon, time):
			
			fire_rect = self.level.get_bullet_dimensions(weapon.projectile)
			unit_rect = unit.get_rect()
			add_bullet = True
			
			if player_state == 'moveup':
				#bullet bottom edge on top left edge
				bullet_x = unit_rect.x + fire_x - fire_rect.w / 2
				bullet_y = unit_rect.y - fire_rect.h + fire_y
				
			elif player_state == 'movedown':
				#bullet top edge on bottom left edge
				bullet_x = unit_rect.x + fire_x - fire_rect.w / 2
				bullet_y = unit_rect.y + unit_rect.h + fire_y
			
			elif player_state == 'moveright':
				bullet_x = unit_rect.x  + unit_rect.w + fire_x
				bullet_y = unit_rect.y + fire_y - fire_rect.h / 2
			
			elif player_state == 'moveleft':
				bullet_x = unit_rect.x - fire_rect.w + fire_x
				bullet_y = unit_rect.y + fire_y - fire_rect.h / 2
			
			elif player_state == 'moveupright':
				bullet_x = unit_rect.x  + unit_rect.w + fire_x
				bullet_y = unit_rect.y + fire_y - fire_rect.h
			
			elif player_state == 'moveupleft':
				bullet_x = unit_rect.x + fire_x - fire_rect.w
				bullet_y = unit_rect.y + fire_y - fire_rect.h
			
			elif player_state == 'movedownleft':
				bullet_x = unit_rect.x + fire_x - fire_rect.w
				bullet_y = unit_rect.y + fire_y + unit_rect.h
			
			elif player_state == 'movedownright':
				bullet_x = unit_rect.x  + unit_rect.w + fire_x
				bullet_y = unit_rect.y + fire_y + unit_rect.h
			else:
				add_bullet = False
				
			if add_bullet:
				added = self.level.add_bullet_unit(weapon, bullet_x, bullet_y, player_state)
				#If thte bullet wasn't added due to
				#obstruction show explosion instead
				if not added:
					self.level.add_small_explosion(bullet_x, bullet_y)

		
	def plot_gunflare(self, unit, state, fire_x, fire_y, weapon, time):
		
		if weapon.nozzel_flash:
		
			rect = unit.get_rect()
			x = rect.x + fire_x
			y = rect.y + fire_y
			w = rect.w
			h = rect.h
			
			flare_rect = self.level.get_gunfire_dimensions()
			
			
			if state == 'moveup':
				x -= flare_rect.w / 2
				y -= flare_rect.h
			if state == 'movedown':
				x -= flare_rect.w / 2
				y += rect.h
			if state == 'moveright':
				x += rect.w
				y -= flare_rect.h /2
			if state == 'moveleft':
				x -= flare_rect.w
				y -= flare_rect.h /2
			elif state == 'moveupright':
				x += rect.w
				y -= flare_rect.h
			elif state == 'moveupleft':
				x -= flare_rect.w
				y -= flare_rect.h
			elif state == 'movedownleft':
				x -= flare_rect.w
				y += rect.h	
			elif state == 'movedownright':
				x += rect.w
				y += rect.h
				
			self.level.get_gun_flare_unit().set_pos(x, y)
			self.level.get_gun_flare_unit().enter_state(state, time)

	@staticmethod
	def invulnerable(unit, time):
		data = unit.get_behaviour_data()
		if 'spawn_time' in data:
			spawn_time = data['spawn_time']
			return time - spawn_time < PLAYER_INVULNERABILITY_TIME
		else:
			return False
		

	def do_action(self, action, unit, time):
		
		#Allow a small period of invulnerability after dying...
		if PlayerBehaviour.invulnerable(unit, time):
			return
			
		bias = self.level.hardnessbias	
			
		dead = False
		if action == 'Hurt5':
			dead = unit.decrease_health(5 * bias)
		if action == 'Hurt10':
			dead = unit.decrease_health(10 * bias)
		if action == 'Hurt20':
			dead = unit.decrease_health(20 * bias)
		if action == 'Hurt30':
			dead = unit.decrease_health(30 * bias)
		if action == 'Hurt40':
			dead = unit.decrease_health(40 * bias)
		if action == 'Kill':
			dead = unit.decrease_health(unit.get_health())
			
		if dead:
			print_debug("Dying...",3)
			unit.enter_state('dying', time)

	def on_remove(self, unit, time):
		""" Only allow the removal of the unit when requested if we have no more lives """
		if not unit.start_new_life():
			print_debug("No more lives. Player dead",3)
			level_state = self.level.get_level_state()
			all_dead = level_state.set_player_dead(unit)
			if all_dead:
				self.level.game_over()
			return True
		else:
			print_debug("Next life...",3)
			data = unit.get_behaviour_data()
			data['spawn_time'] = time
			unit.enter_state(unit.previous_state(), time)
	

USE_A_STAR = False

class AlienBehaviour(DefaultBehaviour):
	
	TOWARDS_PLAYER=1
	FIXED_DIRECTION=2
	MAX_ALIEN_COLLISIONS_BEFORE_MOVE = 20
	
	def __init__(self, unit_definition, mixer, level):
		DefaultBehaviour.__init__(self, unit_definition, mixer)
		#Need a call back when creating new aliens...
		self.level = level
		#Setup the Alien path finder utils...
		if USE_A_STAR:
			path_data = TileMapPathMap(level)
			self.alien_path_finder = PathFinder(path_data, ManhattanHeuristic(1))
		
	def update(self, time, display, unit):
		if self.state_not_dying(unit.current_state()):
			data = unit.get_behaviour_data()
			
			if 'alien_movement_type' not in data:
				data['alien_movement_type'] = AlienBehaviour.TOWARDS_PLAYER
			
			#print "Alien movement %s" % data['alien_movement_type']
			
			if data['alien_movement_type'] == AlienBehaviour.TOWARDS_PLAYER:
				#simple ai - if player is to left of alien try to move left etc...
				player_rect = self.level.get_player().get_rect()
				alien_rect = unit.get_rect()
				
				#TEST ALIEN PATH FINDING AI
				if USE_A_STAR:
					px,py = display.view_to_tile((player_rect.x, player_rect.y))
					ax,ay = display.view_to_tile((alien_rect.x, alien_rect.y))
					alien_path = self.alien_path_finder.find(ax,ay,px,py)
					if alien_path:
						#print "Path found %d steps" % alien_path.length()
						display.add_debug_alien_path(alien_path)
				
				
				alien_movement = self.update_movement_towards_player(player_rect, alien_rect, data, display)
				#print "movement %s " % alien_movement.to_state_name()
				
					
			elif data['alien_movement_type'] == AlienBehaviour.FIXED_DIRECTION:
				alien_movement = data['last_movement']
			
			else:
				alien_movement = Movement.none()
					
			#Remember the alien movement
			data['last_movement'] = alien_movement
				
			#change state of alien too match movement...
			new_state = alien_movement.to_state_name()
			if new_state:
				unit.enter_state(new_state, time)
	
			#TODO select appropriate mover...
			x,y = self.level.alien_mover.handle_movement(unit, alien_movement, time)
			self.check_and_handle_if_alien_blocked(unit, x,y, alien_movement)
		
	def check_and_handle_if_alien_blocked(self, unit, x,y, alien_movement):
		
		data = unit.get_behaviour_data()
		
		#If the alien is stuck for a while switch to either following player or moving randomly...
		if x==0 and y==0:
			if 'alien_blocked_count' in data:
				data['alien_blocked_count'] += 1
			else:
				data['alien_blocked_count'] = 0
		else:
			data['alien_blocked_count'] = 0
		
		if 'alien_blocked_count' in data:
			if data['alien_blocked_count'] > AlienBehaviour.MAX_ALIEN_COLLISIONS_BEFORE_MOVE:
				if data['alien_movement_type']== AlienBehaviour.TOWARDS_PLAYER:
					alien_movement.random()
					data['alien_movement_type'] = AlienBehaviour.FIXED_DIRECTION
					data['last_movement'] = alien_movement
				else:
					data['alien_movement_type'] = AlienBehaviour.TOWARDS_PLAYER	
				data['alien_blocked_count'] = 0
				

	def update_movement_towards_player(self, player_rect, alien_rect, data, display):
		if 'last_movement' in data:
			alien_movement = data['last_movement']
		else:
			alien_movement = Movement.new_none()
		
		player_mid_y = player_rect.y + player_rect.h / 2
		player_mid_x = player_rect.x + player_rect.w / 2
		alien_mid_x = alien_rect.x - alien_rect.w/2
		alien_mid_y = alien_rect.y - alien_rect.h/2
		
		px,py = display.view_to_tile((player_rect.x, player_rect.y))
		ax,ay = display.view_to_tile((alien_rect.x, alien_rect.y))
		
		move_right = px > ax
		move_left = px < ax
		move_down = py > ay
		move_up = py < ay		
		
		if move_left:
			if move_up:
				alien_movement.from_state('moveupleft')
			elif move_down:
				alien_movement.from_state('movedownleft')
			else:	
				alien_movement.from_state('moveleft')
				
		elif move_right:
			if move_up:
				alien_movement.from_state('moveupright')
			elif move_down:
				alien_movement.from_state('movedownright')
			else:
				alien_movement.from_state('moveright')
				
		else:
			if move_up:
				alien_movement.from_state('moveup')
			elif move_down:
				alien_movement.from_state('movedown')
		
			else:
				#We need to move at least something to trigger a collision...
				# keep going in same direction as before
				pass
			
		return alien_movement

	"""aliens should update when just off the screen"""
	def should_update(self, display, unit):
		return display.rect_just_off_and_on_screen(unit.get_rect())


	def do_action(self, action, unit, time):
		dead, collision = self.hurt_unit(action, unit)
			
		if dead:
			self.handle_dead(collision, unit,time)
		return

	def handle_dead(self, collision, unit, time):
		if collision:
			if self.state_not_dying(unit.current_state()):
				self.enter_dying_state(unit, time)
		
		else:
			#If being shot rather than colliding with player
			# show big explosions
			if self.state_not_dying(unit.current_state()):
				self.level.add_big_explosion(unit.get_rect().x, unit.get_rect().y)
				self.enter_dying_state(unit, time)
			
		 
	def collide_unit(self, unit, character_unit, intersection_rect, time):
		print_debug("Alien collision %s %s" % (character_unit.get_uni_filename(), unit.get_uni_filename()),3)
		
		if character_unit.get_object_type() == 'friendly' and self.state_not_dying(unit.current_state()):
			#Whether we get hurt by player depends
			#what kind of alien we are (boss does not)...	
			if self.player_should_hurt_us(character_unit, time):	 
				unit.do_action('HurtByPlayer', time)
				action = unit.get_collision_action()
				if not Cheats.getNoHurt():
					character_unit.do_action(action, time)
		
		elif character_unit.unit_definition.ai_type == 'shipfire':
			#let the shipfire we have hit handle the collision...
			character_unit.collide_unit(unit, intersection_rect, time)
		
		self.handle_collide_with_alien(unit, character_unit, time)
	
	def player_should_hurt_us(self, character_unit, time):
		#normal aliens are always hurt by player who is not dying...
		return self.state_not_dying(character_unit.current_state())
	
	
	def handle_collide_with_alien(self, unit, character_unit, time):
		if character_unit.get_object_type() == 'character' and character_unit.unit_definition.ai_type == 'alien':			
			# alien collided with alien. reverse direction of movement...
			data = unit.get_behaviour_data()
			data['alien_movement_type'] = AlienBehaviour.FIXED_DIRECTION
			alien_movement = data['last_movement']
			data['last_movement'] = self.level.alien_mover.calc_reverse_direction(alien_movement)
			
			#the alien we collided with may be blocking
			#increment its hit count and see if we should
			#move it
			if self.increment_alien_collision_count(character_unit):
				their_data = character_unit.get_behaviour_data()
				their_data['alien_movement_type'] = AlienBehaviour.FIXED_DIRECTION
				#randomise their movement
				old_movement = their_data['last_movement']
				if old_movement:
					old_movement.random()
				else:
					old_movement = Movement.new_random()
				their_data['last_movement'] = old_movement
				self.reset_collision_count(character_unit)
				
	def increment_alien_collision_count(self, character_unit):
		data = character_unit.get_behaviour_data()
		if 'collision_count' in data:
			c = data['collision_count']
			c+=1
		else:
			c=0
		data['collision_count'] = c
		return c == AlienBehaviour.MAX_ALIEN_COLLISIONS_BEFORE_MOVE
		
	def reset_collision_count(self, character_unit):
		data = character_unit.get_behaviour_data()
		data['collision_count'] = 0
			
	
	def is_blocking_collision(self, us, them):
		return True
	
MAX_BOUNCES = 1
SHOT_DOOR_DELAY = 100

class ProjectileBehaviour(DefaultBehaviour):
			
	def __init__(self, unit_definition, mixer, level):
		DefaultBehaviour.__init__(self, unit_definition, mixer)
		#Need a call back when moving bullets...
		self.level = level
		self.shot_door_sound = mixer.Sound(SHOT_DOOR_SOUND)
		self.last_shot_door_play_time = 0
			
	def update(self, time, display, unit):
		data = unit.get_behaviour_data()
		if 'movement' in data:
			movement = data['movement']
		else:
			state = unit.current_animation().state
			movement = Movement.new_from_state(state)

			#Not all projectiles are associated to weapons
			#enemy projectiles are not
			if 'weapon' in data:
				weapon = data['weapon']
				if weapon.arc:
					movement.arc_y = float(get_random_int(0,10)) / 10 -0.5
					movement.arc_x = float(get_random_int(0,10)) / 10 -0.5
						
			data['movement'] = movement
			
		self.level.bullet_mover.handle_movement(unit, movement, time)
	
	def collide_unit(self, unit, character_unit, intersection_rect, time):
		print_debug("Bullet collision %s %s" % (character_unit.get_uni_filename(), unit.get_uni_filename()),3)
		
		
		if character_unit.get_object_type() == 'door':
			if character_unit.is_blocking_collision(unit):
				self.handle_bullet_hit(unit, character_unit, intersection_rect, time)
				unit.remove(time)
				if time - self.last_shot_door_play_time > SHOT_DOOR_DELAY:
					self.shot_door_sound.play()
					self.last_shot_door_play_time = time
		
		elif character_unit.get_object_type() != 'projectile' and character_unit.get_object_type() != 'friendly' and character_unit.get_object_type() != 'pickup' and character_unit.get_object_type() != 'trigger':
			unit.remove(time)
		
		if character_unit.get_object_type() == 'character':
			self.handle_bullet_hit(unit, character_unit, intersection_rect, time)
	
	def handle_bullet_hit(self, unit, character_unit, intersection_rect, time):
		x,y = self.calc_explosion_pos(unit, character_unit, intersection_rect)
		self.level.add_small_explosion(x,y)
		action = unit.get_collision_action()
		character_unit.do_action(action, time)
	
	def calc_explosion_pos(self, bullet, them, intersection_rect):
		return intersection_rect.x, intersection_rect.y	
	
	def collide_map(self, unit, horizontalOrVertical, pos_x, pos_y, time):
		if not self.check_and_bounce(unit, horizontalOrVertical, time):
			unit.remove(time)
			self.level.add_small_explosion(pos_x, pos_y)
		
	def check_and_bounce(self, unit, horizontalOrVertical, time):
		data = unit.get_behaviour_data()
		#Not all projectiles are associated to weapons
		#enemy projectiles are not
		if 'weapon' in data:
			weapon = data['weapon']
			if 'movement' in data and weapon.bounce:
				movement = data['movement']
				
				if 'bounce_count' in data:
					bounce = data['bounce_count']
				else:
					bounce = 0
				bounce +=1
				data['bounce_count'] = bounce
				
				if bounce > MAX_BOUNCES:
					return False
				else:
					movement.bounce(horizontalOrVertical)
					unit.enter_state(movement.to_state_name(), time)
					data['movement'] = movement
					return True
		return False
		
	#We should move the bullets even if they have gone off screen
	def should_update(self,display, unit):
		return True
	
	def is_current_position_blocked(self, unit):
		return self.level.bullet_mover.is_current_position_blocked(unit)
	
class DomeBehaviour(DefaultBehaviour):
	def __init__(self, unit_definition, mixer, level):
		DefaultBehaviour.__init__(self, unit_definition, mixer)
		self.level = level
		
	def do_action(self, action, unit, time):
		
		dead, collision = self.hurt_unit(action, unit)
		
		if not dead:
			#When hit by a projectile this unit shows its firing frame (flashes white)
			unit.fire()
		
			
		if dead:
			if self.state_not_dying(unit.get_current_state()):
				self.enter_dying_state(unit, time)
				self.level.get_level_state().remove_dome()
				trigger_action = unit.get_trigger_action()
				if trigger_action:
					ActionHandler.perform_action(self.level, trigger_action, unit, None, time)
					
						
		
		return

	
class TriggerBehaviour(DefaultBehaviour):
	def __init__(self, unit_definition, mixer, level):
		DefaultBehaviour.__init__(self, unit_definition, mixer)
		self.level = level

	def do_action(self, action, unit, time):
		#When hit by a projectile this unit shows its firing frame (flashes white)
		unit.fire()
		self.do_action(action, unit, time)
	

	def collide_unit(self, us, them, intersection_rect, time):
		if them.get_object_type() == 'friendly':
			action = us.get_trigger_action()
			if action:
				ActionHandler.perform_action(self.level, action, us, them, time)
						

BOSS_FIRE_DELAY=5000
BOSS_PAUSE_DELAY=2000
BOSS_REPEAT_FIRE_DELAY = 200

class BossBehaviour(AlienBehaviour):
					
	STATE_MOVING = 1
	FIRE_PAUSE = 2
	REPEAT_FIRE = 3
	ALL_FIRE_STATES = ['moveupright', 'moveright', 'movedownright', 'movedown', 'movedownleft', 'moveleft', 'moveupleft', 'moveup']	
					
	def __init__(self, unit_definition, mixer, level):
		AlienBehaviour.__init__(self, unit_definition, mixer, level)
				
	def do_action(self, action, unit, time):
		#When hit by a projectile this unit shows its firing frame (flashes white)
		unit.fire()
		AlienBehaviour.do_action(self, action, unit, time)
		
	def update(self, time, display, unit):
		data = unit.get_behaviour_data()
		if 'current_state' not in data:
			data['current_state'] = BossBehaviour.STATE_MOVING
		
		if 'last_fire_time' not in data:
			data['last_fire_time'] = time
			
		state = data['current_state']
		
		if state == BossBehaviour.STATE_MOVING:
			lt = data['last_fire_time']
			if time > (lt + BOSS_FIRE_DELAY):
				self.handle_fire(unit, data, time)
			else:
				#Always move towards player
				data['alien_movement_type'] = AlienBehaviour.TOWARDS_PLAYER
				if not Cheats.getNoMoveBoss():
					AlienBehaviour.update(self, time, display, unit)
		
		if state == BossBehaviour.REPEAT_FIRE:
			lt = data['last_fire_time']
			if time > (lt + BOSS_REPEAT_FIRE_DELAY):
				self.handle_fire(unit, data, time)
	
				
		if state == BossBehaviour.FIRE_PAUSE:
			lt = data['last_fire_time']
			if time > (lt + BOSS_PAUSE_DELAY):
				data['current_state'] = BossBehaviour.STATE_MOVING
	
	def handle_fire(self, unit, data, time):
		
		if unit.unit_definition.ai_type == 'boss4':
			self.handle_fire_boss4(unit, data)
		if unit.unit_definition.ai_type == 'boss1':
			self.handle_fire_boss1(unit, data,  time)
		if unit.unit_definition.ai_type == 'boss2':
			self.handle_fire_boss2(unit, data, time)
		if unit.unit_definition.ai_type == 'boss3':
			self.handle_fire_boss3(unit, data, time)
			
		data['last_fire_time'] = time
			
	
	def handle_fire_boss3(self, unit, data, time):
		state = data['current_state']
		us = unit.get_rect()
		#repeat fire every 45 degrees
		if state == BossBehaviour.STATE_MOVING:
			data['current_state'] = BossBehaviour.REPEAT_FIRE
			fire_type = 0
		elif state == BossBehaviour.REPEAT_FIRE:
			fire_type = data['fire_type']
			if fire_type == 7:
				data['current_state'] = BossBehaviour.FIRE_PAUSE
		
		self.add_worm(us, BossBehaviour.ALL_FIRE_STATES[fire_type], time)
		data['fire_type'] = fire_type + 1
	
	def handle_fire_boss2(self, unit, data, time):
		state = data['current_state']
		us = unit.get_rect()
		if state == BossBehaviour.STATE_MOVING:
			#fire at diagonal angles
			self.add_worms(us, ['moveupleft', 'moveupright','movedownright', 'movedownleft'], time)
			data['current_state'] = BossBehaviour.REPEAT_FIRE
		else:
			#add fire horizontally and vertically
			self.add_worms(us, ['moveup', 'moveleft','moveright', 'movedown'], time)
			data['current_state'] = BossBehaviour.FIRE_PAUSE
		
	def add_worms(self, us, states, time):
		for state in states:
			self.add_worm(us, state, time)
			
	def add_worm(self, us, state, time):		
		if state == 'moveupleft':
			x,y = us.x, us.y
		elif state == 'moveupright':
			x,y = us.x + us.w, us.y
		elif state == 'movedownright':
			x,y = us.x + us.w, us.y + us.h
		elif state == 'movedownleft':
			x,y = us.x, us.y + us.h
		elif state == 'moveup':
			x,y = us.x + us.w / 2, us.y
		elif state == 'moveright':
			x,y = us.x + us.w, us.y + us.h/ 2
		elif state == 'movedown':
			x,y = us.x + us.w / 2, us.y + us.h
		elif state == 'moveleft':
			x,y = us.x, us.y + us.h / 2
			
		new_alien = self.level.add_new_alien_unit('firebossworm.uni', x, y)
		new_alien.enter_state(state, time)
		if state.find('left') > -1:
			new_alien.move(-new_alien.get_rect().w, 0)
		if state.find('up') >-1:
			new_alien.move(0, -new_alien.get_rect().h)
			

	def handle_fire_boss4(self, unit, data):
		new_alien = self.level.add_new_alien_unit('enemy5.uni', unit.get_rect().x, unit.get_rect().y)
		new_alien.move(-new_alien.get_rect().w, 0)
		data['current_state'] = BossBehaviour.FIRE_PAUSE
	
	def handle_fire_boss1(self, unit, data, time):
		us = unit.get_rect()
		x1,y1 = us.x + us.w / 2, us.y
		x2,y2 = us.x + us.w / 2, us.y + us.h
		new_alien = self.level.add_new_alien_unit('enemy9.uni', x1,y1)
		new_alien.move(-new_alien.get_rect().w, 0)
		new_alien.enter_state('moveup', time)
		new_alien = self.level.add_new_alien_unit('enemy9.uni', x2,y2)
		new_alien.move(+new_alien.get_rect().w, 0)
		new_alien.enter_state('movedown', time)
		data['current_state'] = BossBehaviour.FIRE_PAUSE
	
	
	def handle_dead(self, collision, unit, time):		
		action = unit.get_trigger_action()
		unit.remove(time)
		ActionHandler.perform_action(self.level, action, unit, None, time)
	
	"""Always move alien if in BOSS mode"""
	def should_update(self,display, unit):
		return self.level.level_state.get_game_mode() == LevelState.BOSS
	
	def handle_collide_with_alien(self, unit, character_unit, time):
		# bosses do not perform normal movement logic when colliding with aliens
		return
	
	def player_should_hurt_us(self, character_unit, time):
		if Cheats.getNoHurtBoss():
			return False
		
		#Boss are only hurt if the player is not invulnerable (that would
		#make it far too easy to kill the boss)...
		return self.state_not_dying(character_unit.current_state()) and not PlayerBehaviour.invulnerable(character_unit, time)
	
	def is_blocking_collision(self, us, them):
		return False
	
	def get_collision_rects(self, unit):
		if unit.unit_definition.ai_type == 'boss2':
			return calc_boss2_collision_rect(unit.get_rect())
		elif unit.unit_definition.ai_type == 'boss3':
			return calc_boss3_collision_rect(unit.get_rect())
		elif unit.unit_definition.ai_type == 'boss4':
			return calc_boss3_collision_rect(unit.get_rect())
		elif unit.unit_definition.ai_type == 'boss1':
			return calc_boss1_collision_rect(unit.get_rect())
		else:
			rects = []
			rects.append(calc_collision_rect(unit.get_rect()))
			return rects
		

	
	"""
	def check_pixel_perfect_collision(self, unit, character_unit):
		#print "Boss checking pixel collision"
		ur = unit.get_rect()
		cr = character_unit.get_rect()
		clipped = ur.clip(cr)
		#print "Clipped rect %d,%d,%d,%d" % (clipped.x, clipped.y, clipped.w, clipped.h)
		
		ui = unit.current_image()
		ur = unit.get_rect()
		
		x1 = clipped.x - ur.x
		y1 = clipped.y - ur.y
		x2 = x1 + clipped.w
		y2 = y1 + clipped.h
		
		for x in range(x1,x2):
			for y in range(y1, y2):
				c = ui.get_at(x,y)
				if c.get_red() != 0xff or c.get_green() !=0 or c.get_blue() != 0xff:
				
					print c
			
		return True
	"""
	
class ForceFieldHorizontalBehaviour(DefaultBehaviour):
							
	def __init__(self, unit_definition, mixer):
		DefaultBehaviour.__init__(self, unit_definition, mixer)
		
	def is_blocking_collision(self, us, them):
		them_y = them.get_rect().y
		us_y = us.get_rect().y
		if them_y > (us_y - them.get_rect().h):
			return False
		return True
	
class EggBehaviour(DefaultBehaviour):
		
	def __init__(self, unit_definition, mixer, level):
		DefaultBehaviour.__init__(self, unit_definition, mixer)
		self.level = level
		
	def do_action(self, action, unit, time):		
		dead, collision = self.hurt_unit(action, unit)		
		if dead:
			if self.state_not_dying(unit.get_current_state()):
				self.enter_dying_state(unit, time)
				self.level.get_level_state().remove_dome()
		
		return
	

class HostageBehaviour(DefaultBehaviour):
		
	def __init__(self, unit_definition, mixer, level):
		DefaultBehaviour.__init__(self, unit_definition, mixer)
		self.level = level
		
	def do_action(self, action, unit, time):		
		dead, collision = self.hurt_unit(action, unit)
		if not dead:
			#When hit by a projectile this unit shows its firing frame (flashes white)
			unit.fire()
		if dead:
			if self.state_not_dying(unit.get_current_state()):
				self.enter_dying_state(unit, time)
				self.level.get_level_state().remove_dome()
		
		return
	

class BarrelBehaviour(EggBehaviour):
	def __init__(self, unit_definition, mixer, level):
		DefaultBehaviour.__init__(self, unit_definition, mixer)
		self.level = level
		
	def do_action(self, action, unit, time):		
		dead, collision = self.hurt_unit(action, unit)		
		if dead:
			if self.state_not_dying(unit.get_current_state()):	
				self.explode_me_and_adjacent_barrels(unit, time)
		return
	
	def explode_me_and_adjacent_barrels(self, unit, time):
		if self.state_not_dying(unit.get_current_state()):
			self.level.add_big_explosion(unit.get_rect().x, unit.get_rect().y)
			self.enter_dying_state(unit, time)
		
		#look for barrels, friendlies or characters in 3x3 square around barrel...
		barrel_rect = unit.get_rect().copy()
		barrel_rect.x -= barrel_rect.w
		barrel_rect.w *=3
		barrel_rect.y -= barrel_rect.h
		barrel_rect.h *=3
		
		c_units = self.level.get_units_for_collision_detection(barrel_rect)
		for u in c_units:
			#adjacent barrel - lets blow that up too
			if u != unit and u.unit_definition.ai_type =='barrel' and self.state_not_dying(u.get_current_state()):
				if u.get_rect().colliderect(barrel_rect):
					#Add a delayed kill to this barrel to simulate a ripple effect...
					command = DelayedKillUnitCommand(self, u)
					self.level.add_delay_command(command)
			if u.get_object_type() == 'friendly' or u.get_object_type() == 'character':
				if u.get_rect().colliderect(barrel_rect):
					#adjacent player or alien - apply blast damage...
					action = unit.get_collision_action()
					if action:
						u.do_action(action, time)			
	
	def is_blocking_collision(self, us, them):
		return self.state_not_dying(us.get_current_state())
	
class BioSpikeBehaviour(DefaultBehaviour):
	def __init__(self, unit_definition, mixer):
		DefaultBehaviour.__init__(self, unit_definition, mixer)

	def is_blocking_collision(self, us, them):
		return False
	
	def collide_unit(self, us, them, intersection_rect, time):
		if us.get_current_state() == 'moving':
			if them.get_object_type() == 'friendly' or u.get_object_type() == 'character':
				action = us.get_collision_action()
				if action:
					them.do_action(action, time)	
					
class ShipFireBehaviour(AlienBehaviour):
	def __init__(self, unit_definition, mixer):
		DefaultBehaviour.__init__(self, unit_definition, mixer)
		
	def update(self, time, display, unit):
		return
	
	def do_action(self, action, unit, time):
		return

	def is_blocking_collision(self, us, them):
		return False

	def collide_unit(self, us, them, intersection_rect, time):
		if them.get_object_type() == 'friendly' or them.get_object_type() == 'character':
			action = us.get_collision_action()
			if action:
				them.do_action(action, time)	

"""
Behaviour unique to the worm like projectiles fired by the Bosses
"""
class EnemyProjectileBehaviour(ProjectileBehaviour):
	def __init__(self, unit_definition, mixer, level):
		ProjectileBehaviour.__init__(self, unit_definition, mixer, level)
		
	def collide_unit(self, unit, character_unit, intersection_rect, time):	
		if character_unit.get_object_type() == 'friendly':
			x,y = self.calc_explosion_pos(unit, character_unit, intersection_rect)
			self.level.add_small_explosion(x,y)
			action = unit.get_collision_action()
			character_unit.do_action(action, time)
			unit.remove(time)
		else:
			unit.remove(time)
		
		
