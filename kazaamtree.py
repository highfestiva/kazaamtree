from .coord import coord

class kazaamtree(list):
	'''A 2D tree structure which quickly finds static objects approximately inside an AABB.
	   Whenever a bucket is filled, two subnodes are created. Odd buckets are split by
	   median X, even buckets are split on median Y.'''
	def __init__(self, bucket_size=100, depth=0):
		self.bucket_size = bucket_size
		self.depth = depth
		self.splitx = self.splity = None
		self.lo = self.hi = self.parent = None
		self._set_add(self._add)

	def _add(self, crd):
		self.append(crd)
		l = len(self)
		if l > self.bucket_size:
			if self.depth&1:	# split on x
				self.sort(key=lambda crd:crd.x)
				self.splitx = (self[l//2-1].x + self[l//2].x) / 2
				self._set_add(self._add_split_x)
			else: # split on y
				self.sort(key=lambda crd:crd.y)
				self.splity = (self[l//2-1].y + self[l//2].y) / 2
				self._set_add(self._add_split_y)
			self.lo = kazaamtree(self.bucket_size, self.depth+1)
			self.hi = kazaamtree(self.bucket_size, self.depth+1)
			self.lo.parent = self.hi.parent = self
			self.lo.extend(self[:l//2])
			self.hi.extend(self[l//2:])
			super(kazaamtree, self).clear()

	def _add_split_x(self, crd):
		(self.lo if crd.x < self.splitx else self.hi).add(crd)

	def _add_split_y(self, crd):
		(self.lo if crd.y < self.splity else self.hi).add(crd)

	def _set_add(self, addfun):
		self.add = addfun

	def _pr(self):
		f = self.splitx if self.splitx!=None else (self.splity if self.splity!=None else 0)
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
		if self.splitx != None:
			if self.splitx <= topleft.x:
				#print('hi x')
				return self.hi._aabb(topleft, bottomright)
			elif self.splitx >= bottomright.x:
				#print('lo x')
				return self.lo._aabb(topleft, bottomright)
			#print('both x')
			return self.lo._aabb(topleft, bottomright) + self.hi._aabb(topleft, bottomright)
		elif self.splity != None:
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

	def buckets(self):
		return [self] if self.lo==None else self.lo.buckets() + self.hi.buckets()

	def center(self, crdtype=coord, weightfunc=None):
		if not weightfunc:
			return sum(self, crdtype()) * (1 / len(self))
		# Weighted coordinates; calculate a weighted average.
		wsum,avg = 0,crdtype()
		for crd in self:
			w = weightfunc(crd)
			wsum += w
			avg += crd*w
		return avg * (1 / wsum)

	def join_children(self):
		if self.lo != None:
			self.lo.join_children()
			self.extend(self.lo)
		if self.hi != None:
			self.hi.join_children()
			self.extend(self.hi)
		self.splitx = self.splity = None
		self.lo = self.hi = None

	def clear(self):
		super(kazaamtree, self).clear()
		self.splitx = self.splity = None
		self.lo = self.hi = None
		self._set_add(self._add)

	def __hash__(self):
		h = self.depth*127 + len(self)*29
		if self.lo:
			h += len(self.lo)*31 + len(self.hi)*37
		if self.splitx:
			h += int(self.splitx)*41
		if self.splity:
			h += int(self.splity)*43
		return h


class kazaamindextree(kazaamtree):
	def __init__(self, bucket_size=100, depth=0):
		super(kazaamindextree,self).__init__(bucket_size, depth)
		self.index = []
	def add(self, crd):
		crd.index = len(self.index)
		self.index.append(crd)
		self._super_add(crd)
	def clear(self):
		super(kazaamindextree, self).clear()
		self.index.clear()
	def _set_add(self, addfun):
		self._super_add = addfun


if __name__ == '__main__':
	# Test that fetching via an AABB gets us the approximate number of coords.
	from random import random
	tree = kazaamindextree()
	crdcnt = 17530
	for i in range(crdcnt):
		tree.add(coord(random()*20-10, random()*20-10))
	assert len(tree.index) == crdcnt
	assert len(tree.get_approx_aabb_crds(coord(-100,-100),coord(100,100))) == crdcnt
	assert len(tree.get_approx_aabb_crds(coord(-20,-20),coord(1,+20))) + len(tree.get_approx_aabb_crds(coord(1,-20),coord(20,+20))) <= crdcnt*1.3
	assert len(tree.get_approx_aabb_crds(coord(1,-20),coord(20,+20))) >= crdcnt*9/20*0.8
