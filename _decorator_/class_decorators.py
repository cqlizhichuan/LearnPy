# -*- coding:utf-8 -*-
import time
def time_it(fn):
    "Example of a method decorator"
    def decorator(*args, **kwargs):
    	t1 = time.time()
    	ret = fn(*args, **kwargs)
    	print '\t\t%d seconds taken for %s' % (time.time() - t1, fn.__name__)
    	return ret
    
    return decorator
    
def class_decorator(*method_names):
    def class_rebuilder(cls):
        "The class decorator example"
        class NewClass(cls):
            "This is the overwritten class"
            def __getattribute__(self, attr_name):
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
        print "\tthis is a the MySecondClass.first_method"
    time.sleep(2)

    def second_method(self, *args, **kwargs):
        print "\tthis is the MySecondClass.second_method"
    time.sleep(1)

if __name__ == "__main__":
    print "::: With a decorated class :::"
    z = MySecondClass()
    z.first_method()
    z.second_method()