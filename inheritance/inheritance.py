# -*- coding: utf-8 -*-

class A(object):
	def go(self):
		print('go A go')
		
	def stop(self):
		print('stop A stop')
		
	def pause(self):
		raise Exception('Not Implemented')

class B(A):
	def go(self):
		super(B, self).go()
		print('go B go')

class C(A):
	def go(self):
		super(C, self).go()
		print('go C go')

	def stop(self):
		super(C, self).stop()
		print('stop C stop')

class D(B, C):
	def go(self):
		super(D, self).go()
		print('go D go')

	def stop(self):
		super(D, self).stop()
		print('stop D stop')

	def pause(self):
		raise Exception('wait D wait')

class E(B, C):
	pass
	
a = A()
b = B()
c = C()
d = D()
e = E()

# 说明下列代码的输出结果

print('\na.go')
a.go()
print('\nb.go')
b.go()
print('\nc.go')
c.go()
print('\nd.go')
d.go()
print('\ne.go')
e.go()

print('\na.stop')
a.stop()
print('\nb.stop')
b.stop()
print('\nc.stop')
c.stop()
print('\nd.stop')
d.stop()
print('\ne.stop')
e.stop()

print('\na.pause')
a.pause()
print('\nb.pause')
b.pause()
print('\nc.pause')
c.pause()
print('\nd.pause')
d.pause()
print('\ne.pause')
e.pause()

'''
a.go
go A go

b.go
go A go
go B go

c.go
go A go
go C go

d.go
go A go
go C go
go B go
go D go

e.go
go A go
go C go
go B go

a.stop
stop A stop

b.stop
stop A stop

c.stop
stop A stop
stop C stop

d.stop
stop A stop
stop C stop
stop D stop

e.stop
stop A stop
stop C stop

a.pause
Traceback (most recent call last):
  File "inheritance.py", line 73, in <module>
    a.pause()
  File "inheritance.py", line 11, in pause
    raise Exception('Not Implemented')
Exception: Not Implemented
'''