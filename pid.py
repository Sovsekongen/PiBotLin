class Pid:
	def __init__(self, p1, i, d, ts):
		self.p1 = p1
		self.i = i
		self.d = d
		self.ts = ts
		
	def p(self, diff):
		num = diff * self.p1
		return num
		
	def pi(self, diff):
		num = (diff * self.p1) + ((diff * self.i) * (self.ts/2))
		return num
		
	def pid(self, diff):
		num = (diff * self.p1) + ((diff * self.i) * (self.ts/2)) + ((2*(diff * self.d )) / self.ts)
		return num
