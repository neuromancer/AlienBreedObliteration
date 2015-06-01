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
A* path finder classes for Alien movement.

Not currently enabled in game due to performance issues.

See 

USE_A_STAR = False

in behaviour.py
"""

class Heuristic:
	
	def _init__(self):
		return
	
	def get_cost(self, x, y, tx, ty):
		return



class PathMap:
	
	def __init__(self, tilemap):
		return
	
	def get_width(self):
		return
	
	def get_height(self):
		return
	
	def blocked(self, x, y):
		return
	
	def get_cost(self, start_x, start_y, targetl_x, target_y):
		return
		
	def is_valid_tile(self, x, y):
		return

class Step:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def equals(self, x, y):
		return self.x == x and self.y == y
	
class Path:
		
	def __init__(self):
		self.steps = []
		
	def append(self, step):
		self.steps.append(step)
		
	def prepend(self, step):
		self.steps.insert(0, step)
		
	def length(self):
		return len(self.steps)
	
	def contains(self, x, y):
		for s in self.steps:
			if s.equals(x,y):
				return True
		return False
		
	def get_step(self, index):
		return self.steps[index]
	

class PathNode:
	def __init__(self, x, y):
		self.cost = 0
		self.depth = 0
		self.parent = None
		self.heuristic = 0
		self.x = x
		self.y = y
		
	def set_parent(self, p):
		self.parent = p
		self.depth = p.depth + 1
	"""	
	def __cmp__(self, other):
		print "Node compare"
		f = self.cost + self.heuristic
		of = other.cost + other.heuristic
		if f < of:
			return -1
		elif f > of:
			return 1
		else:
			return 0
	
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
	"""
		
class PathNodeComparator:
	
	@staticmethod
	def compare(one, other):
		f = one.cost + one.heuristic
		of = other.cost + other.heuristic
		if f < of:
			return -1
		elif f > of:
			return 1
		else:
			return 0

		
		
class PathFinder:
		
	def __init__(self, path_map, heuristic):
		self.map = path_map
		self.heuristic = heuristic
		self.nodes = []
		for y in range(0, self.map.get_width()):
			row = []
			self.nodes.append(row)
			for x in range(0, self.map.get_height()):
				row.append(PathNode(x,y))
				
		self.open = []
		self.closed = []
		self.max_search_distance = 10
		
		return
	
	
	def find(self, start_x, start_y, target_x, target_y):
		
		if self.map.blocked(target_x, target_y):
			#No route to target as target is blocked
			return None
		
		#initialise starting position and target
		#print "start %d,%d" % (start_x, start_y)
		starting_node = self.nodes[start_y][start_x]
		starting_node.cost = 0
		starting_node.depth = 0
		starting_node.parent = None
		
		#print "target %d,%d" % (target_x, target_y)
		target_node = self.nodes[target_y][target_x]
		target_node.parent = None
		
		#Initialise our working lists
		del self.open[0:len(self.open)]
		del self.closed[0:len(self.closed)]
		self.open.append(starting_node)
		
		max_depth = 0
		
		#Repetitively loop through the candidate list ('open') for potential steps
		#up until a maximum number of steps and then give up if not found target
		while len(self.open) > 0 and max_depth < self.max_search_distance:
			
			#print "Open %d " % len(self.open)
			#print "About to find best option"
			
			#Open list is ordered by heuristic
			current = self.get_best_cadidate()
			
			#print "Found current %d,%d cost %d" % (current.x, current.y, current.cost)
			
			if current == target_node:
				#found our route - we can stop looping...
				#print "Found target"
				break;
			
			#Move node from candidate to searched list
			self.open.remove(current)
			self.closed.append(current)
			
			#now check immediate neighbours of tile
			for y in [-1,0,1]:
				for x in [-1,0,1]:
					
					if y ==0 and x==0:
						#skip current position
						continue
					#print "tring neighbour"
					
					neighbour_x = x + current.x
					neighbour_y = y + current.y
					
					if self.map.is_valid_tile(neighbour_x, neighbour_y):
						
						#print "Valid"
						
						neighbour = self.nodes[neighbour_y][neighbour_x]
						
						#calc the cost of moving to the target node
						cost = current.cost + self.map.get_cost(current.x, current.y, neighbour.x, neighbour.y)
						
						#if we have already seen this node but this is a better route (lower cost) dscard previous route
						if cost < neighbour.cost:
							#print "Found lower cost"
							if neighbour in self.open:
								self.open.remove(neighbour)
							if neighbour in self.closed:
								self.closed.remove(neighbour)
					
						#if we have not previously processed this node then record this route and add to candidates
						if neighbour not in self.open and neighbour not in self.closed:		
							neighbour.cost = cost
							neighbour.set_parent(current)
							max_depth = max(max_depth, neighbour.depth)
							neighbour.heuristic = self.heuristic.get_cost(neighbour_x, neighbour_y, target_x, target_y)
							self.open.append(neighbour)
							
							#print "Add neighbour %d,%d cost %d from %d,%d" % (neighbour.x, neighbour.y, cost,neighbour.parent.x, neighbour.parent.y)
											
							

						
						
		#now check if we have a path, build and return
		if not target_node.parent:
			#No path to target found
			return None
		
		#print "About to construct path"
		
		path = Path()
		current = target_node
		while current.parent:
			#print "Added %d,%d  %d,%d" % (current.x, current.y, current.parent.x, current.parent.y)
			path.prepend(current)
			current = current.parent
			
		return path
		
		
	def get_best_cadidate(self):
		#TODO this list should be maintained sorted
		self.open.sort(PathNodeComparator.compare)
		return self.open[0]
