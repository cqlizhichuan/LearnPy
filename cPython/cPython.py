from ctypes import *
import types

#https://blog.csdn.net/linda1000/article/details/12623527

class Test(Structure):
    pass

    
Test._fields_ = [
        ('x', c_int),
        ('y', c_char),
        ('next', POINTER(Test))
]

class Person(Structure):
    _fields_ = [
        ("name", c_char_p), 
        ("age", c_int)
    ]

LIB_NAME = 'liblearn_so.so'
lib = cdll.LoadLibrary(LIB_NAME)

def init():
    ret = lib.init_person_list()
    if ret < 0:
        print('Init person list failed.')

def free():
    lib.free_person_list()

def add_new_person(name, age):
    p = Person()
    p.name = name
    p.age = age
    if (0 > lib.add_new_person(pointer(p))):
        print('Add person <%s, %d> failed.' % (name, age))

def test_add_person():
    pl = [
        ("lizhichuan", 26),
        ("wuaihong", 25),
        ("TOE", 2)
    ]

    for p in pl:
        add_new_person(p[0], p[1])

if __name__ == '__main__':
    init()
    test_add_person()
    free()