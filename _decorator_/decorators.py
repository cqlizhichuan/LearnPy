#-*- coding: utf-8 -*-
import inspect

from functools import wraps
from time import time, sleep
from threading import Thread

'''
修饰器是 Python 语言的标准特性，可以使用不同的方式修改函数的行为。惯
常用法是使用修饰器把函数注册为事件的处理程序.

在 Python 代码中嵌入响应字符串会导致代码难以维护，此处这么做只是为了
介绍响应的概念.
'''

def square_sum(func):

	def square(*args):
	
		print("*args = ", args)

		n = args[0]

		print("n + 1 = %d" % (n + 1))
		print func.__name__

		# 这个地方再执行func, 即sum_a的时候
		# 就不会再首先调用spuare_sum这个函数了
		func(n)
		print("*"*15)

		return func(n)

	return square

def square_sum_outter():

    def square_sum_inner(func) : 
        @wraps(func)
        def square(*args):
        
        	print("*args = ", args)
        
        	n = args[0]
        
        	print("n + 1 = %d" % (n + 1))
        	print func.__name__
        
        	# 这个地方再执行func, 即sum_a的时候
        	# 就不会再首先调用spuare_sum这个函数了
        	func(n)
        	print("*"*15)
        
        	return func(n)
        
        return square

    return square_sum_inner

@square_sum
def sum_a(a):
    print("in sum_a %d" % (a))

'''
*args =  (5,)
n + 1 =  6
sum_a
in sum_a 5
***************
in sum_a 5
'''
def test_sum_a(x = 5):
    sum_a(x)

@square_sum_outter()
def sum_a1(a):
    print("in sum_a %d" % (a))

#TypeError: square_sum_outter() takes no arguments (1 given)
def test_sum_a_1(x = 5):
    sum_a1(x)

############################################################################################################
def a_new_decorator(f):
    # @wraps(f)让f的名字保持不变
    # 例如，f_need_decorator的名字还是f_need_decorator，而不是wrap_the_func
    @wraps(f)
    def wrap_the_func():
        print('I am doing some boring work before executing a_func()')

        f()

        print('I am doing some boring work after executing a_func()')

    return wrap_the_func

# the @a_new_decorator is just a short way of saying:
# f_need_decorator = a_new_decorator(f_need_decorator)
@a_new_decorator
def f_need_decorator():
    print('I am the function which needs some decoration to remove my foul smell')

def test_simple_decorator():
    f_need_decorator()

############################################################################################################
can_run = False

def decorator_name(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not can_run:
            return ('Function will not run')
        else:
            return f(*args, **kwargs)
    return decorated

@decorator_name
def func_decorator_name():
    return ('Function is running')

def test_func():
    global can_run

    print('\nWhen can_run is True ...')
    can_run = True
    print(func_decorator_name())

    print('\nWhen can_run is False ...')
    can_run = False
    print(func_decorator_name())

############################################################################################################
def logit(outfile = 'out.log'):
    def logging_decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            log_str = ('%s was called.' % (f.__name__))
            print(log_str)
            with open(outfile, 'a') as fd:
                fd.write(log_str + '\n')

            f(*args, **kwargs)

        return wrapped_function

    return logging_decorator

def logit1(f):
    outfile = 'out1.log'
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        log_str = ('%s was called.' % (f.__name__))
        print(log_str)
        with open(outfile, 'a') as fd:
            fd.write(log_str + '\n')
        
        f(*args, **kwargs)

    return wrapped_function

@logit()
def test_logit1():
    print('Enter test_logit1.')

@logit()
def test_logit2():
    print('Enter test_logit2.')

@logit1
def test_logit3():
    print('Enter test_logit3.')

@logit1
def test_logit4():
    print('Enter test_logit4.')

def test_logit():
    test_logit1()
    test_logit2()
    test_logit3()
    test_logit4()
############################################################################################################

# 这种语法也可以
def echo_it1(prefix, *args, **kwargs):
    def wrapped_function(f):
        @wraps(f)
        def inner_func(*args, **kwargs):
            print('%s before call %s' % (prefix, f.__name__))
            f(*args, **kwargs)

        return inner_func

    return wrapped_function
        

@echo_it1('lzc')
def test_echo_it1():
    print('real inner func.')

def test_echo():
    test_echo_it1()

############################################################################################################
class Logit(object):
    def __init__(self, logfile = 'out.log'):
        self.logfile = logfile

    def __call__(self, func):
        @wraps(func)
        def wrapped_func(*args, **kargs):
            logstr = ('%s was called.' % (func.__name__))
            print(logstr)
            with open(self.logfile, 'a') as fd:
                fd.write(logstr + '\n')

            self.notify()
            #return func(*args, **kargs)
            func(*args, **kargs)

        return wrapped_func

    def notify(self):
        print('Foo notify')

@Logit()
def test_Logit1():
    print('Enter test_Logit1')

@Logit()
def test_Logit2():
    print('Enter test_Logit2')

def test_Logit():
    test_Logit1()
    test_Logit2()

############################################################################################################
def memo(fn):
    cache = {}
    miss = object()
    @wraps(fn)
    def wrapper(*args):
        result = cache.get(args, miss)
        if result is miss:
            result = fn(*args)
            cache[args] = result
        return result

    return wrapper

@memo
def fib(n):
    if n >= 2:
        return fib(n-1) + fib(n-2)
    return n

def fib1(n):
    if n >= 2:
        return fib1(n-1) + fib1(n-2)
    return n

def test_fib_with_cache():
    '''
    我们用decorator，在调用函数前查询一下缓存，如果没有缓存，才调用，
    有了就从缓存中返回值。一下子，这个递归从二叉树式的递归成了线性的递归。
    '''

    #start = time()
    print fib(10)
    #middle = time()
    #print('fib with cache cost %f' % (middle - start))
    #print fib1(10)
    #print('fib without cache cost %f' % (time() - middle))

############################################################################################################
class MyApp(object):
    def __init__(self):
        self.func_map = {}

    def register(self, map_name):
        def wrapper(fn):
            if map_name not in self.func_map:
                self.func_map.setdefault(map_name, fn)
            return fn
        return wrapper

    def call_method(self, name):
        if name not in self.func_map:
            raise ValueError('Wrong url %s' % (name))

        return self.func_map[name]()

myapp = MyApp()

@myapp.register('/')
def myapp_root_func():
    return 'This is root func'

@myapp.register('/svm')
def myapp_svm_func():
    return 'This is svm func'

def test_myapp():
    print(myapp_root_func())
    print(myapp_svm_func())

############################################################################################################
def advance_logger(loglevel):
 
    def get_line_number():
        return inspect.currentframe().f_back.f_back.f_lineno
 
    def _basic_log(fn, result, *args, **kwargs):
        print "function   = " + fn.__name__,
        print "    arguments = {0} {1}".format(args, kwargs)
        print "    return    = {0}".format(result)
 
    def info_log_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            result = fn(*args, **kwargs)
            _basic_log(fn, result, args, kwargs)
        return wrapper
 
    def debug_log_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            ts = time.time()
            result = fn(*args, **kwargs)
            te = time.time()
            _basic_log(fn, result, args, kwargs)
            print "    time      = %.6f sec" % (te-ts)
            print "    called_from_line : " + str(get_line_number())
        return wrapper
 
    if loglevel is "debug":
        return debug_log_decorator
    else:
        return info_log_decorator

############################################################################################################
def async(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        t = Thread(target = fn, 
            args = args, kwargs = kwargs)
        t.start()
        return t

    return wrapper

def test_async():

    @async
    def do_something(x, N):
        for i in range(N):
            print('%d is doing...\n' % (x))
            sleep(2)

    N = 10
    for i in range(N):
        do_something(i, 10)
        
############################################################################################################
if __name__ == '__main__':
    #test_sum_a()
    #test_sum_a_1()
    #test_simple_decorator()
    #test_func()
    #test_logit()
    #test_Logit()
    #test_echo_it1()
    #test_fib_with_cache()
    #test_myapp()
    test_async()