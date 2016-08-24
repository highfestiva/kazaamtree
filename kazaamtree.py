#!/usr/bin/env python3

from coord import coord

bucket_size = 100

class kazaamtree(list):
	'''A 2D tree structure which quickly finds static objects approximately inside an AABB.
	   Whenever a bucket is filled, two subnodes are created. On even depths the subnodes
	   are split in median X, on odd depths they are split on median Y.'''
	def __init__(self, depth=0):
		self.depth = depth
		self.splitx = self.splity = None
		self.lo = self.hi = None

	def add(self, crd):
		if self.splitx:
			(self.lo if crd.x < self.splitx else self.hi).add(crd)
		elif self.splity:
			(self.lo if crd.y < self.splity else self.hi).add(crd)
		else:
			self.append(crd)
			l = len(self)
			if l > bucket_size:
				if self.depth&1:	# split on x
					self.sort(key=lambda crd:crd.x)
					self.splitx = (self[l//2-1].x + self[l//2].x) / 2
				else: # split on y
					self.sort(key=lambda crd:crd.y)
					self.splity = (self[l//2-1].y + self[l//2].y) / 2
				self.lo = kazaamtree(self.depth+1)
				self.hi = kazaamtree(self.depth+1)
				self.lo.extend(self[:l//2])
				self.hi.extend(self[l//2:])
				super(kazaamtree, self).clear()

	def _pr(self):
		f = self.splitx if self.splitx else (self.splity if self.splity else 0)
		print('%3i%s%g%s %s' % (self.depth, 'x' if self.depth&1 else 'y', f, '  '*self.depth, self))
		if self.lo != None:
			print('  '*self.depth, '     - lo')
			self.lo._pr()
			print('  '*self.depth, '     - hi')
			self.hi._pr()

	def get_approx_aabb_crds(self, topleft, bottomright):
		if topleft.x > bottomright.x:
			topleft.x,bottomright.x = bottomright.x,topleft.x
		if topleft.y < bottomright.y:
			topleft.y,bottomright.y = bottomright.y,topleft.y
		return self._aabb(topleft, bottomright)

	def _aabb(self, topleft, bottomright):
		#print('AABB %s - %s on %i: %s/%s.' % (topleft,bottomright,self.depth,self.splitx,self.splity))
		if self.splitx:
			if self.splitx <= topleft.x:
				#print('hi x')
				return self.hi._aabb(topleft, bottomright)
			elif self.splitx >= bottomright.x:
				#print('lo x')
				return self.lo._aabb(topleft, bottomright)
			#print('both x')
			return self.lo._aabb(topleft, bottomright) + self.hi._aabb(topleft, bottomright)
		elif self.splity:
			if self.splity <= bottomright.y:
				#print('hi y')
				return self.hi._aabb(topleft, bottomright)
			elif self.splity >= topleft.y:
				#print('lo y')
				return self.lo._aabb(topleft, bottomright)
			#print('both y')
			return self.lo._aabb(topleft, bottomright) + self.hi._aabb(topleft, bottomright)
		else:
			# Don't go through all of them, just return every coordinate in this node.
			#print('leaf size:', len(self))
			return self

	def clear(self):
		super(kazaamtree, self).clear()
		self.splitx = self.splity = None
		self.lo = self.hi = None


class kazaamindextree(kazaamtree):
	def __init__(self, depth=0):
		super(kazaamindextree,self).__init__(depth)
		self.index = []
	def add(self, crd):
		crd.index = len(self.index)
		self.index.append(crd)
		super(kazaamindextree,self).add(crd)
	def clear(self):
		super(kazaamindextree, self).clear()
		self.index.clear()


if __name__ == '__main__':
	# Test that fetching via an AABB gets us the approximate number of coords.
	from random import random
	tree = kazaamtree()
	for i in range(1753):
		tree.add(coord(random()*20-10, random()*20-10))
	assert len(tree.get_approx_aabb_crds(coord(-100,-100),coord(100,100))) == 1753
	assert len(tree.get_approx_aabb_crds(coord(-20,-20),coord(1,+20))) + len(tree.get_approx_aabb_crds(coord(1,-20),coord(20,+20))) <= 1753*1.2
	assert len(tree.get_approx_aabb_crds(coord(1,-20),coord(20,+20))) >= 1753*9/20*0.8
