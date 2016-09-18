class coord:
	def __init__(self, x=0, y=0):
		self.x,self.y = x,y
	def __add__(self, v):
		return coord(self.x+v.x, self.y+v.y)
	def __sub__(self, v):
		return coord(self.x-v.x, self.y-v.y)
	def __mul__(self, f):
		return coord(self.x*f, self.y*f)
	def __truediv__(self, d):
		r = 1/d
		return coord(self.x*r, self.y*r)
	def __str__(self):
		return '(%3.3f,%3.3f)' % (self.x,self.y)
	def __repr__(self):
		return str(self)

class geocoord(coord):
	def lat(self):
		return self.y
	def lng(self):
		return self.x
	def __add__(self, v):
		return geocoord(self.x+v.x, self.y+v.y)
	def __sub__(self, v):
		return geocoord(self.x-v.x, self.y-v.y)
	def __mul__(self, f):
		return geocoord(self.x*f, self.y*f)
	def __truediv__(self, d):
		r = 1/d
		return geocoord(self.x*r, self.y*r)
	def __str__(self):
		return 'lat:%g, lng:%g' % (self.lat(),self.lng())

def latlng(lat=0, lng=0):
	return geocoord(lng,lat)

def crd2geo(crd):
	return geocoord(crd.x, crd.y)
