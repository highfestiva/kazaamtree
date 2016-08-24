#!/usr/bin/env python3

class coord:
	def __init__(self, x, y):
		self.x,self.y = x,y
	def __add__(self, v):
		return coord(self.x+v.x, self.y+v.y)
	def __sub__(self, v):
		return coord(self.x-v.x, self.y-v.y)
	def __mul__(self, f):
		return coord(self.x*f, self.y*f)
	def __truediv__(self, d):
		return coord(self.x/d, self.y/d)
	def __str__(self):
		return '(%3.3f,%3.3f)' % (self.x,self.y)
	def __repr__(self):
		return str(self)

class geocoord(coord):
	def lat(self):
		return self.y
	def lng(self):
		return self.x
	def __str__(self):
		return 'lat:%g, lng:%g' % (self.lat(),self.lng())

def latlng(lat, lng):
	return geocoord(lng,lat)
