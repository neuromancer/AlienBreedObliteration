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
from collisiontilemap import *
from collisionutils import *

class CollisionStats:
	
	def __init__(self):
		self.reset()
		
	def reset(self):
		self.invocations = 0
		self.total_units_checked = 0
		self.total_skipped = 0
		self.total_projectiles = 0
		self.__returned_units = 0
		
	@staticmethod
	def get_instance():
		return CollisionStats.INSTANCE

	def inc_invocations(self):
		self.invocations+=1
		
	def inc_units(self, checked, skipped):
		self.total_units_checked += checked
		self.total_skipped += skipped
	
	def inc_projectiles(self):
		self.total_projectiles +=1

	def inc_returned_units(self,r):
		self.__returned_units += r

	def get_returned_units(self):
		return self.__returned_units


	def debug_print(self):
		if self.invocations >0:
			r = self.get_returned_units() / self.invocations
		else:
			r=0
		print "Invocations %d units %d skipped %d projectiles %d avg returned %d" %(self.invocations, self.total_units_checked, self.total_skipped, self.total_projectiles, r)
		
CollisionStats.INSTANCE = CollisionStats()


class MyUnit:
	def __init__(self, unit, index):
		self.unit_id = str(unit)
		self.unit_index = index
		self.rect = unit.get_rect()
		self.collision_rects = unit.get_collision_rects()
		self.__collideable = unit.collideable()
		self.__removed = unit.removed()

	def get_rect(self):
		return self.rect
	
	def get_collision_rects(self):
		return self.collision_rects
	
	def collideable(self):
		return self.__collideable
	
	def removed(self):
		return self.__removed
	
class UnitCollision2:
	
	def __init__(self, level):
		self.level = level
		
	def get_unit_collisions(self, player, target_pos_rect):
		CollisionStats.get_instance().inc_invocations()
				
		if Cheats.getNoCollisions():
			return []
		
		#get list of unit possible in target area
		#move from source to destination in steps of minimum
		#unit width / height
		
		current_pos_rect = player.get_rect()
		entire_rect = current_pos_rect.copy()
		
		if target_pos_rect.x > current_pos_rect.x:
			xdir = 1
			entire_rect.w += (target_pos_rect.x - current_pos_rect.x)
			
		elif target_pos_rect.x < current_pos_rect.x:
			xdir = -1
			entire_rect.w += (current_pos_rect.x - target_pos_rect.x)
			entire_rect.x = target_pos_rect.x
		else:
			xdir = 0
		
		if target_pos_rect.y > current_pos_rect.y:
			ydir = 1
			entire_rect.h += (target_pos_rect.y - current_pos_rect.y)
		elif target_pos_rect.y < current_pos_rect.y:
			ydir = -1
			entire_rect.h += (current_pos_rect.y - target_pos_rect.y)
			entire_rect.y = target_pos_rect.y
		else:
			ydir = 0
		
		#print_debug("Path %d,%d" % (xdir, ydir),2)
		#print_debug("player at %d,%d" % (current_pos_rect.x, current_pos_rect.y),2)
		#print_debug("target at %d,%d" % (target_pos_rect.x, target_pos_rect.y),2)
		
		#Optimisation - if we are an alien then there is no need
		#to check collisions with aliens...
		alien = player.unit_definition.ai_type == 'alien'
		bullet = player.unit_definition.object_type =='projectile'
		
		
		
		c_units = self.level.get_units_for_collision_detection(entire_rect)
		CollisionStats.get_instance().inc_returned_units(len(c_units))
		
		""" Log info for replay """
		if Cheats.getLogCollisionsInfo():
			print "-------------"
			print "%d,%d,%d,%d-%d,%d,%d,%d,%s,%s,%s" % (current_pos_rect.x, current_pos_rect.y, current_pos_rect.w, current_pos_rect.h,
			target_pos_rect.x, target_pos_rect.y, target_pos_rect.w,
			target_pos_rect.h,player.unit_definition.ai_type, player.unit_definition.object_type, str(player))
			for c in c_units:
				print "%d,%d,%d,%d,%s,%d,%d,%s" % (c.get_rect().x, c.get_rect().y,
				c.get_rect().w, c.get_rect().h,c.unit_definition.object_type,c.collideable(), c.removed(), str(c))
		
		
		
		my_units = []
		index = 0
		for u in c_units:
			skip = False
			
			if u.unit_definition.object_type =='projectile':
				CollisionStats.get_instance().inc_projectiles()	
			
			if not u.unit_definition.collideable:
				skip = True
				
			#if alien and (u.unit_definition.ai_type == 'alien' or u.unit_definition.object_type == 'pickup'):
			if alien and u.unit_definition.object_type == 'pickup':
				skip = True
		
			if bullet and (u.unit_definition.object_type == 'pickup' or u.unit_definition.object_type == 'projectile'):
				skip=True
				
			#a hack to skip those too far away
			if not UnitCollision2.full_rect_collide_with(u, entire_rect):
				skip = True
			"""
			if u.get_rect().x > entire_rect.x + entire_rect.w:
				skip = True
			if (u.get_rect().x + u.get_rect().x) < entire_rect.x:
				skip = True
			if u.get_rect().y > entire_rect.y + entire_rect.w:
				skip = True
			if u.get_rect().y < entire_rect.y:
				skip = True
			"""
				
			if not skip:
				my_unit = MyUnit(u, index)
				my_units.append(my_unit)
				
			index += 1
		
		checking = len(my_units)
		skipped = index - checking
		CollisionStats.get_instance().inc_units(checking, skipped)
		
		player_id = str(player)
		
		hits = self._calculate_unit_hits(my_units, current_pos_rect, player_id, target_pos_rect, xdir, ydir)
		
		unit_hits = []
		#convert the hits back to unit defs...
		for h in hits:
			my_unit = h[1]
			u = c_units[my_unit.unit_index]
			unit_hits.append((0, u, h[2], h[3]))
			
		if Cheats.getLogCollisionsInfo():
			print "-- %d" % len(unit_hits)
			
		return unit_hits
		
		
	@staticmethod
	def _calculate_unit_hits(my_units, current_pos_rect, player_id, target_pos_rect, xdir, ydir):
		hits = []
		player_rect = current_pos_rect.copy()
		#We will calculate the min width/height on the first pass
		min_w = 9999
		min_h = 9999
		
		#print_debug( "Total Num unit %d" % (len(self.level.get_all_units())),3)
		#print_debug( "Num units for collision %d" % (len(c_units)),3)
		
		finished = False
		while not finished:	
			#TODO This isn't quite right - some units have multiple
			#collision rectangles rather than the hardcoded single
			#one here
			player_collision_rect = calc_collision_rect(player_rect)
			
			for u in my_units:
				
				if u.get_rect().w < min_w:
					min_w = u.get_rect().w
				if u.get_rect().h < min_h:
					min_h = u.get_rect().h

				
				#print_debug("Testing unit pos %f %f %s" %(u.get_pos()[0], u.get_pos()[1],u), 5)
				
				#don't register ourselves
				if u.unit_id != player_id:
					
					intersection = UnitCollision2.rect_collide_with(u, player_collision_rect)
					
					if intersection:	
						#print_debug("Collision unit %s at %d,%d" % (u.get_uni_filename(), player_rect.x, player_rect.y), 3)	
						hits.append((0, u, player_rect, intersection))
					
			# Not all movements will be perfectly diagonal
			# TODO this is probably not the path the player took but hopefully
			# any differences will be negligible 
			if player_rect.y == target_pos_rect.y:
				ydir = 0
			if player_rect.x == target_pos_rect.x:
				xdir = 0
					
			finished = (player_rect.x == target_pos_rect.x and player_rect.y == target_pos_rect.y)
				
			player_rect = player_rect.move(xdir * min_w, ydir * min_h)
			#print_debug("player at %d,%d" % (player_rect.x, player_rect.y),3)
			
			if ydir < 0:
				#going up
				if player_rect.y < target_pos_rect.y:
					player_rect.y = target_pos_rect.y
			if ydir > 0:
				#going down
				if player_rect.y > target_pos_rect.y:
					player_rect.y = target_pos_rect.y
			
			if xdir < 0:
				#going left
				if player_rect.x < target_pos_rect.x:
					player_rect.x = target_pos_rect.x
			
			if xdir > 0:
				#going right
				if player_rect.x > target_pos_rect.x:
					player_rect.x = target_pos_rect.x
				
		return hits

	@staticmethod
	def full_rect_collide_with(u, player_rect):
		if u.collideable() and not u.removed():
			return u.get_rect().colliderect(player_rect)
		return False


	@staticmethod
	def rect_collide_with(u, player_collision_rect):
		if u.collideable() and not u.removed():
			for r in u.get_collision_rects():
				if r.colliderect(player_collision_rect):
					#return r
					return UnitCollision2.calc_intersection(r, player_collision_rect)
		
		return None

	@staticmethod
	def calc_intersection(r, r2):
		return r.clip(r2)

class Entity:

	def __init__(self, rect, dir_x, dir_y):
		self.x = rect.x
		self.ox = rect.x
		self.y = rect.y
		self.oy = rect.y
		#total amount we wish to move in x
		self.dir_x = dir_x
		self.odir_x = dir_x
		#total amount we wish to move in y
		self.dir_y = dir_y
		self.odir_y = dir_y
		self.w = rect.w
		self.h = rect.h
		self.prevented_move_x = False
		self.prevented_move_y = False
		self.collision = False
		#starting position (tile coors) see _check_starting_position 
		self.sx = 0
		self.sy = 0
		self.sx2 = 0
		self.sy2 = 0

class LevelMapCollision2:

	def __init__(self, level):
		self.tile_data = CollisionTileData(level)
	

	def move(self, player, dir_x, dir_y, attempt_bump):
		# create an entity representing our moving player
		entity = Entity(player.get_rect(), dir_x, dir_y)
		tile_data = self.tile_data
		
		cheat = Cheats.getNoCollisions() or Cheats.getWalkThroughWalls()
		
		LevelMapCollision2._c_move(entity, tile_data, attempt_bump, cheat)
		
		return entity.x, entity.y, entity.collision
	
	def is_current_position_blocked(self, player):
		entity = Entity(player.get_rect(), 0, 0)
		tile_data = self.tile_data
		cheat = Cheats.getNoCollisions() or Cheats.getWalkThroughWalls()
		if not cheat:
			LevelMapCollision2._check_starting_position(entity, tile_data)
			
		return entity.collision
	
	@staticmethod
	def _c_move(entity, tile_data, attempt_bump, cheat):
		
		if not cheat:
			
			#Calculate starting position
			LevelMapCollision2._calc_starting_position(entity, tile_data)
		
			#this logic works assuming the dirx and diry are less than the tile dimensions
			#otherwise we could jump straight over a blocking tile
			
			is_diagonal = entity.dir_x != 0 and entity.dir_y != 0
			
			LevelMapCollision2._move_horizontal(entity, tile_data)
			# if entity wanted to move horizontally but couldn't due to obstruction
			# check if we bumped the entity to closest boundary if it would move
			if not is_diagonal and attempt_bump:
				LevelMapCollision2._attempt_vertical_bump(entity, tile_data)
			
			LevelMapCollision2._move_vertical(entity, tile_data)
			# if entity wanted to move vertically but couldn't due to obstruction
			# check if we bumped the entity to closest boundary if it would move
			if not is_diagonal and attempt_bump:
				LevelMapCollision2._attempt_horizontal_bump(entity, tile_data)
		
		# Now apply the movement

		entity.x += entity.dir_x
		entity.y += entity.dir_y
	
		if entity.x < 0:
			entity.x = 0
		elif entity.x + entity.w >= tile_data.max_map_x:
			entity.x = tile_data.max_map_x - entity.w - 1
	
		if entity.y < 0:
			entity.y = 0
		elif entity.y > tile_data.max_map_y:
			entity.y = tile_data.max_map_y - entity.h - 1
		
		return
	
	@staticmethod
	def _calc_starting_position(entity, tile_data):
		entity.sx = entity.x / tile_data.tile_w
		entity.sx2 = (entity.x + entity.w -1) / tile_data.tile_w
		entity.sy = entity.y / tile_data.tile_h
		entity.sy2 = (entity.y + entity.h -1) / tile_data.tile_h

	
	@staticmethod
	def _check_starting_position(entity, tile_data):
		LevelMapCollision2._calc_starting_position(entity, tile_data)
				
		#Check whether the starting position is blocked
		if LevelMapCollision2.is_blocked(entity.sx,entity.sy,entity,tile_data) or LevelMapCollision2.is_blocked(entity.sx,entity.sy2,entity,tile_data) or  LevelMapCollision2.is_blocked(entity.sx2,entity.sy,entity,tile_data) or LevelMapCollision2.is_blocked(entity.sx2,entity.sy2,entity,tile_data):
			entity.prevented_move_x = True
			entity.prevented_move_y = True
			entity.dir_x = 0
			entity.dir_y = 0
			entity.collision = True
	
	
	@staticmethod
	def _attempt_vertical_bump(entity, tile_data):
		#print "%d" % entity.prevented_move_x
		if entity.prevented_move_x:
			#print "bump?"
			above = (entity.y / tile_data.tile_h) * tile_data.tile_h
			below = above + tile_data.tile_h
			#print "y%d a%d b%d" %(entity.y, above, below)
			bump_up = (entity.y - above) <= (below - entity.y) and entity.dir_y <=0
			if bump_up:
				#print "bump up"
				#bump up
				entity.y = above
			else:
				#print "bump down"
				#bump down
				entity.y = below
			entity.prevented_move_x = False
			entity.dir_x = entity.odir_x
			LevelMapCollision2._move_horizontal(entity, tile_data)
			#print "aftr bump %d" % entity.prevented_move_x
			if entity.prevented_move_x:
				#print "still blocked"
				#still blocked, restore original position
				entity.y = entity.oy
			else:
				#bumped! clear the vertical movement requested 
				entity.dir_y = 0
		
		
	@staticmethod
	def _attempt_horizontal_bump(entity, tile_data):
		#print "%d" % entity.prevented_move_y
		if entity.prevented_move_y:
			#print "bump?"
			left = (entity.x / tile_data.tile_w) * tile_data.tile_w
			right = left + tile_data.tile_w
			#print "y%d a%d b%d" %(entity.x, left, right)
			#only attempt to bump in the direction of travel if moving diagonal
			bump_left = (entity.x - left) <= (right - entity.x) and entity.dir_x <= 0
			if bump_left:
				#print "bump left"
				#bump left
				entity.x = left
			else:
				#print "bump right"
				#bump right
				entity.x = right
			entity.prevented_move_y = False
			entity.dir_y = entity.odir_y
			LevelMapCollision2._move_vertical(entity, tile_data)
			#print "aftr bump %d" % entity.prevented_move_y
			if entity.prevented_move_y:
				#print "still blocked"
				#still blocked, restore original position
				entity.x = entity.ox
			else:
				#bumped! clear the horizontal movement requested 
				entity.dir_x = 0
		
		
	@staticmethod	
	def _move_horizontal(entity, tile_data):
		# if the entity is bigger than a tile we must split entity up and check each 
		# tile sized part
		if entity.h > tile_data.tile_h:
			y_inc = tile_data.tile_h
		else:
			y_inc = entity.h
		
		#Starting left and right edges...
		#sx = entity.x / tile_data.tile_w
		#sx2 = (entity.x + entity.w -1) / tile_data.tile_w

		# test horizontal. Loop over each tile_height sized row
		while True:
			# target left edge
        		x1 = (entity.x + entity.dir_x) / tile_data.tile_w
			#target right edge
        		x2 = (entity.x + entity.dir_x + entity.w -1) / tile_data.tile_w
			#target middle
			x3 = (entity.x + entity.dir_x + entity.w /2 -1) / tile_data.tile_w
			
        		y1 = (entity.y) / tile_data.tile_h
        		y2 = (entity.y + y_inc -1) / tile_data.tile_h

			#print "%d %d,%d   %d" %(x1, y1, y2, y_inc)

			#player on the map
        		if x1 >= 0 and x2 < tile_data.max_map_tile_x and y1 >= 0 and y2 < tile_data.max_map_tile_y:
				"""
				#Check whether the starting position is blocked
				if tile_data.tile_map[y1][sx] == 1 or tile_data.tile_map[y2][sx] == 1 or tile_data.tile_map[y1][sx2] == 1 or tile_data.tile_map[y2][sx2] == 1:
					#print "Starting pos blocked"
					entity.prevented_move_x = True
					entity.dir_x = 0
					entity.collision = True
				"""	
					
            			if entity.dir_x > 0:
					#print "trying right"
                			# Trying to move right 
					#test right edge and middle at top and bottom
					if LevelMapCollision2.is_blocked(x2,y1,entity,tile_data) or LevelMapCollision2.is_blocked(x2,y2,entity,tile_data)  or LevelMapCollision2.is_blocked(x3,y1,entity,tile_data) or LevelMapCollision2.is_blocked(x3,y2,entity,tile_data):
						#obstruction. Place the player as close to the solid tile as possible 
						#print "trying but blocked right"
						orig_x = entity.x
                    				entity.x = x2 * tile_data.tile_w
                    				entity.x -= entity.w
						#can't move x anymore
                    				entity.dir_x = 0
						#check if we have moved anywhere
						entity.prevented_move_x = orig_x == entity.x
						#print "%d" % entity.prevented_move_x
						entity.collision = True
            			elif entity.dir_x < 0:
					#print "trying left"
					# Trying to move left
					# test left edge and middle at top and bottom
					if LevelMapCollision2.is_blocked(x1,y1,entity,tile_data) or LevelMapCollision2.is_blocked(x1,y2,entity,tile_data) or LevelMapCollision2.is_blocked(x3,y1,entity,tile_data) or LevelMapCollision2.is_blocked(x3,y2,entity,tile_data):
						#obstruction. Place the player as close to the solid tile as possible 
						orig_x = entity.x
						entity.x = (x1 + 1) * tile_data.tile_w
						#can't move x anymore
                    				entity.dir_x = 0
        					#check if we have moved anywhere
						entity.prevented_move_x = orig_x == entity.x
						entity.collision = True
			if y_inc == entity.h:
				break
			
			if entity.prevented_move_x:
				break
			
			y_inc += tile_data.tile_h
			
			if y_inc > entity.h:
				y_inc = entity.h
								
			
	@staticmethod
	def _move_vertical(entity, tile_data):

		# if the entity is bigger than a tile we must split entity up and check each 
		# tile sized part
		if entity.w > tile_data.tile_w:
			x_inc = tile_data.tile_w
		else:
			x_inc = entity.w		


		#Starting left and right edges...
		#sy1 = entity.y / tile_data.tile_h
		#sy2 = (entity.y + entity.h -1) / tile_data.tile_h

    		# Now test the vertical movement. Loop over each tile_width sized column
		while True:
    
    			#left edge
        		x1 = (entity.x) / tile_data.tile_w
			#right edge
        		x2 = (entity.x + x_inc -1) / tile_data.tile_w
    
    			#target top
        		y1 = (entity.y + entity.dir_y) / tile_data.tile_h
			#target bottom
        		y2 = (entity.y + entity.dir_y + entity.h -1) / tile_data.tile_h
        		#target middle
			y3 = (entity.y + entity.dir_y + entity.h /2 -1) / tile_data.tile_h
	
			#player on the map
        		if x1 >= 0 and x2 < tile_data.max_map_tile_x and y1 >= 0 and y2 < tile_data.max_map_tile_y:
        
				"""
				#Check whether the starting position is blocked
				if tile_data.tile_map[sy1][x1] == 1 or tile_data.tile_map[sy2][x1] == 1 or tile_data.tile_map[sy1][x2] == 1 or tile_data.tile_map[sy2][x1] == 1:
					#print "Starting pos blocked"
					entity.prevented_move_y = True
					entity.dir_y = 0
					entity.collision = True
				"""	
	
            			if entity.dir_y > 0:
                			# Trying to move down. check bottom edge and middle
                			if LevelMapCollision2.is_blocked(x1,y2,entity,tile_data) or LevelMapCollision2.is_blocked(x2,y2,entity,tile_data)	or LevelMapCollision2.is_blocked(x1,y3,entity,tile_data) or LevelMapCollision2.is_blocked(x2,y3,entity,tile_data):
						
                    				# obstruction. Place the player as close to the solid tile as possible
						orig_y = entity.y
                    				entity.y = y2 * tile_data.tile_h
                    				entity.y -= entity.h
        					#can't move y anymore
                    				entity.dir_y = 0
						#check if we have moved anywhere
						entity.prevented_move_y = orig_y == entity.y
						#print "%d" % entity.prevented_move_y
						entity.collision = True

	            		elif entity.dir_y < 0:
                			# Trying to move up. check top edge and middle
                			if LevelMapCollision2.is_blocked(x1,y1,entity,tile_data) or LevelMapCollision2.is_blocked(x2,y1,entity,tile_data) or LevelMapCollision2.is_blocked(x1,y3,entity,tile_data) or LevelMapCollision2.is_blocked(x2,y3,entity,tile_data):
                    				# obstruction. Place the player as close to the solid tile as possible
						orig_y = entity.y
                    				entity.y = (y1 + 1) * tile_data.tile_h  #tile below
        					#can't move y anymore
                    				entity.dir_y = 0
						#check if we have moved anywhere
						entity.prevented_move_y = orig_y == entity.y
						#print "%d" % entity.prevented_move_y
						entity.collision = True

	
        		if x_inc == entity.w:
				break
			
        		x_inc += tile_data.tile_w
			
        		if x_inc > entity.w:
            			x_inc = entity.w
	
	@staticmethod
	def is_blocked(x,y, entity, tile_data):
		
		if tile_data.tile_map[y][x] == CollisionTileData.NOT_BLOCKED:
			return False
		elif tile_data.tile_map[y][x] == CollisionTileData.BLOCKED:
			return True
		

		elif tile_data.tile_map[y][x] == CollisionTileData.BLOCKED_ABOVE:
			#If entity is above this tile then bloked
			return entity.sy2 < y
		elif tile_data.tile_map[y][x] == CollisionTileData.BLOCKED_BELOW:
			#If entity is below this tile then blocked
			return entity.sy > y
		elif tile_data.tile_map[y][x] == CollisionTileData.BLOCKED_LEFT:
			#If entity is to left of tile then blocked
			#return entity.sx2 < y
			return entity.sx2 < x
		elif tile_data.tile_map[y][x] == CollisionTileData.BLOCKED_RIGHT:
			#If entity is to right of tile then blocked
			return entity.sx > x
		elif tile_data.tile_map[y][x] == CollisionTileData.BLOCKED_ABOVE_LEFT:
			#If entity is above and to left then blocked
			return entity.sx2 <= x and entity.sy2 <= y
		elif tile_data.tile_map[y][x] == CollisionTileData.BLOCKED_BELOW_LEFT:
			#If entity is below and to left then blocked
			return entity.sx2 <=x and entity.sy >=y
		elif tile_data.tile_map[y][x] == CollisionTileData.BLOCKED_BELOW_RIGHT:
			#If entity is below and to right then blocked
			return entity.sx >= x and entity.sy >= y
		elif tile_data.tile_map[y][x] == CollisionTileData.BLOCKED_ABOVE_RIGHT:
			#If entity is above and to right then blocked
			return entity.sx>=x and entity.sy2 <=y
