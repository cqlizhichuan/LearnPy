#-*- coding: utf-8 -*-
from random import random

############################## 函数当成变量来使用 START ########################
'''
例子inc()函数返回了另一个函数incx()，
于是我们可以用inc()函数来构造各种版本的inc函数，
比如：inc2()和inc5()。这个技术其实就是上面所说的Currying技术。
把函数当成变量来用，关注于描述问题而不是怎么实现，这样可以让代码更易读
'''
def inc(x):
    def incx(y):
        return x + y

    return incx

def test_inc():
    inc2 = inc(2)
    inc5 = inc(5)

    print(inc2(5))
    print(inc5(5))

############################## 函数当成变量来使用 END ##########################

############################## Map & Reduce START ##############################
'''
1）代码更简单了。
2）数据集，操作，返回值都放到了一起。
3）你在读代码的时候，没有了循环体，于是就可以少了些临时变量，以及变量倒来倒去逻辑。
4）你的代码变成了在描述你要干什么，而不是怎么去干
'''

def test_map_name_len():
    name_len = map(len, ['lizichuan', 'wuaihong', 'TOE'])
    print(name_len)

def to_upper(item):
    return item.upper()

def test_to_upper():
    upper_name = map(to_upper, ['lizichuan', 'wuaihong', 'TOE'])
    print(upper_name)

# lambda表达式相当于 def func(x): return x*x
def test_lambda():
    squares = map(lambda x : x * x, range(9))
    print(squares)

def test_reduce():
    print(reduce(lambda x, y: x + y, range(9)))

def compute_avg():
    nums = [2, -5, 9, 7, -2, 5, 3, 1, 0, -3, 8]
    positive_num = filter(lambda x : x > 0, nums)
    avg = reduce(lambda x, y : x + y, positive_num) / float(len(positive_num))
    print('avg = %f' % (avg))

def car_race():
    car_positions = [1, 1, 1]
    car_num = len(car_positions)
    times = 5

    def draw_car(val):
        print('-' * val)

    for j in range(1, times):
        for i in range(car_num):
            if random() > 0.3:
                car_positions[i] += 1

        print('\n%d cycle' % (j))
        map(draw_car, car_positions)

def car_race1():

    times = 5
    car_positions = [1, 1, 1]

    def draw_car(car_position):
        print('-' * car_position)

    def draw():
        print('')
        map(draw_car, car_positions)

    def move_cars():
        for i, _ in enumerate(car_positions):
            if random() > 0.3:
                car_positions[i] += 1

    def run_step_of_race():
        times -= 1
        move_cars()

    while times:
        run_step_of_race()
        draw()

'''
1）它们之间没有共享的变量。
2）函数间通过参数和返回值来传递数据。
3）在函数里没有临时变量。

递归的本质就是描述问题是什么
'''
def car_race2():
    def output_car(car_position):
        return ('-' * car_position)

    def draw(state):
        print('\nRemain steps %d' % (state['time']))
        print('\n'.join(map(output_car, state['car_positions'])))

    def move_cars(car_positions):
        return map(
            lambda x : x + 1 if random() > 0.3 else x,
            car_positions
        )

    def run_step_of_race(state):
        return {
            'time' : state['time'] - 1,
            'car_positions' : move_cars(state['car_positions'])
        }

    def race(state):
        draw(state)
        if state['time'] > 0:
            race(run_step_of_race(state))

    race({
        'time' : 5,
        'car_positions' : [1, 1, 1]
    })

def print_even_num():
    def even_filter(nums):
        return filter(lambda x : x % 2 == 0, nums)

    def multiply_by_three(nums):
        return map(lambda x : x * 3, nums)

    def convert_to_string(nums):
        return map(str, nums)

    def pipeline_func(data, fns):
        return reduce(
            lambda a, x : x(a), # lambda 数据, 函数 : 函数(数据)
            fns, # 函数
            data # 数据
        )

    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    fns = [even_filter, multiply_by_three, convert_to_string]
    print pipeline_func(nums, fns)

	

def test_map_reduce():
    #test_map_name_len()
    #test_to_upper()
    #test_lambda()
    #test_reduce()
    #compute_avg()
    #car_race()
    #car_race1()
    #car_race2()
    print_even_num()

############################## Map & Reduce END   ##############################

############################## pipe  line START ################################
class Pipe(object):
    def __init__(self, func):
        self.func = func
 
    def __ror__(self, other):
        def generator():
            for obj in other:
                if obj is not None:
                    yield self.func(obj)
        return generator()
 
@Pipe
def even_filter(num):
    return num if num % 2 == 0 else None
 
@Pipe
def multiply_by_three(num):
    return num*3
 
@Pipe
def convert_to_string(num):
    return str(num)

@Pipe
def echo(item):
    print item
    return item

def force(sqs):
    for item in sqs: pass

def test_pipline():
	nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	print force(nums | even_filter | multiply_by_three | convert_to_string)

############################## pipe  line END ##################################
if __name__ == '__main__':
    #test_inc()
    #test_map_reduce()
	test_pipline()