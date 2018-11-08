#-*- coding: utf-8 -*-

# 迭代器 & 生成器 ?

################### Simple yield Start ##################

def twice(i):
    return i * 2

def yield_iter0(n):
    for i in range(n):
        print('\nBefore yield i = %d' % (i))
        yield twice(i)
        print('After yield i = %d\n' % (i))

def test_yield0():
    for i in yield_iter0(5):
        print('Outer Loop i = %d' % (i))

################### Simple yield End ####################


################### Simple iter  Start ##################
class MyRange(object):
    def __init__(self, n):
        self.n = n
        self.idx = 0

    def __iter__(self):
        return self

    def next(self):
        if self.idx < self.n:
            val = self.idx
            self.idx += 1
            return val
        else:
            raise StopIteration()

def test_MyRange():
    for i in MyRange(5):
        print('MyRange i = %d' % (i))
################### Simple iter  End ####################

################### Simple generator Start ##############
class MyGenerator(object):
    def __init__(self, n):
        self.n = n
        self.idx = 0

    '''
    def __iter__(self):
        return self
    '''

    def __iter__(self):
        print('Enter __iter__')
        while self.idx < self.n:
            val = self.idx
            self.idx += 1
            yield val
        else:
            raise StopIteration() 

    def next(self):
        print('Enter next')
        if self.idx < self.n:
            val = self.idx
            self.idx += 1
            yield val
        else:
            raise StopIteration()

def test_MyGenerator():
    for i in MyGenerator(5):
        print('MyGenerator i = %d' % (i))

################### Simple generator End ############

################### Generator next & send Start #####
def h():
    print('lzc')
    m = yield 5
    print('yield to m = {}'.format(m))
    print('Toe')

def test_h():

    # 第一次调用 next 或 send(None)
    # send(None) 是因为h一开始没有 yield 来接收值
    # 就算是 m = yield 5 这行代码在 print('lzc') 前面
    # 也不能直接 c.send(val), 会出现异常
    # TypeError: can't send non-None value to a just-started generator

    c = h()
    print('Start to 1 next.')
    c.next()

    print('Start to 2 next.')
    c.next()

################### Generator next & send End #######

if __name__ == '__main__':
    #test_yield0()
    #test_MyRange()
    #test_MyGenerator()
    test_h()