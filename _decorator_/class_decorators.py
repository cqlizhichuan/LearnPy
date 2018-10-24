# -*- coding:utf-8 -*-
import time

############################## 1 修改类函数 START ##############################
# 场景 : 如果要给一个类的所有方法加上计时, 并打印出来

def time_it(fn):
    "Example of a method decorator"
    def decorator(*args, **kwargs):
    	t1 = time.time()
    	ret = fn(*args, **kwargs)
    	print('%d seconds taken for %s' % (time.time() - t1, fn.__name__))
    	return ret
    
    return decorator
    
def class_decorator(*method_names):
    def class_rebuilder(cls):
        "The class decorator example"
        class NewClass(cls):
            "This is the overwritten class"
            def __getattribute__(self, attr_name):
                print('\n%s is about to called' % (attr_name))
                attr_val = super(NewClass, self).__getattribute__(attr_name)
                if callable(attr_val) and attr_name in method_names:
                    return time_it(attr_val)
                return attr_val

        return NewClass
    return class_rebuilder

@class_decorator('first_method', 'second_method')
class MySecondClass(object):
    """
    This class is decorated
    """
    def first_method(self, *args, **kwargs):
        print("this is the MySecondClass.first_method")
        time.sleep(1)

    def second_method(self, *args, **kwargs):
        print("this is the MySecondClass.second_method")
        time.sleep(2)

def test_decorated_class():
    print("::: With a decorated class :::")
    z = MySecondClass()
    z.first_method()
    z.second_method()

############################## 1 修改类函数 END ################################

############################## 2 增加类成员 START ##############################
# -*- coding:utf-8 -*-
def addAttrs(*attrs):
    def re_build(cls):
        class NewClass(cls):
            def __init__(self, *args, **kws):
                print('__init__ in NewClass')
                for attr in attrs:
                    setattr(self, attr, 9527)
                self.__id = id
                super(NewClass, self).__init__(*args, **kws)

            def get__id(self):
                return self.__id

        return NewClass
    return re_build

@addAttrs('id', 'created_time')
class DBModelOne(object):
    def __init__(self, *args, **kwargs):
        print('__init__ in DBModelOne')

def test_add_class_members():
    m = DBModelOne(5)
    print(m.id, m.created_time)
    print(m.get__id())
    print(type(m))

############################## 2 增加类成员 END ################################

############################## 3 增加类成员 START ##############################
def cd(cls):
    def init(*args, **kwargs):
        cls_obj = cls(*args, **kwargs)
        setattr(cls_obj, 'id', time.time())
        return cls_obj
    return init

@cd
class A(object):
    def __init__(self, name, age, sex='f'):
        self.name=name
        self.age=age
        self.sex=sex
    def s(self):
        print(self.id)

############################## 3 增加类成员 END ################################

if __name__ == "__main__":
    #test_decorated_class()
    test_add_class_members()