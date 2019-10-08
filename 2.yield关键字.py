'''
协程是Tornado中进行异步I/O代码开发的方法。协程使用了Python关键字yield将调用者挂起或回复执行。
'''
# todo：迭代器
'''
迭代器(Iterator)是访问集合内元素的一种方式。迭代器对象从集合的第1个元素开始访问，直到所有元素都被访问一遍后结束。迭代器不能回退，只能往前进行迭代。
'''

# python中最常使用迭代器的场景是循环语句for，它用迭代器封装集合。并且逐个访问集合元素以执行循环体。

for number in range(5):      # range返回一个列表
    print(number)

'''
其中的range()返回一个包含所指定元素的集合，而for语句将其封装成一个迭代器后访问。
使用iter()调用可以将列表、集合转换为迭代器，比如：
'''
numbers = [1,3,5,7,8]
t = iter(numbers)   # 将列表转为迭代器
print(t) # <list_iterator object at 0x000001D1BD9A1278>   一个迭代器对象


'''
迭代器与普通python对象的区别是迭代器有一个next()方法，每次调用该方法可以返回一个元素。
python2中是next()方法，python3中需要使用__next__()方法
调用者（比如for语句）可以通过不断调用next()方法来逐个访问集合元素。比如：
'''

iter_object = iter(range(5))  # 一个迭代器对象，也可以用__iter__()函数     等同于 range(5).__iter__()
range(5).__iter__()
print(iter_object.__next__())  # 0
print(iter_object.__next__())  # 1
print(iter_object.__next__())  # 2
print(iter_object.__next__())  # 3
print(iter_object.__next__())  # 4
'''
超出长度会报错如下：
StopIteration
'''
# todo：使用yield

'''
迭代器在python编程中的适用范围很广，定制迭代器可以使用yield关键字。
调用任何定义中包含yield关键字的函数都不会执行该函数，而会获得一个对应该函数的迭代器
'''
def demoIterator():   # 定义一个迭代器函数
    yield 1
    yield 2
    yield 3

for i in demoIterator():
    print(i)

'''
每次调用迭代器的next()函数，将执行迭代器的函数，并返回yield的结果作为返回元素，当迭代器函数return时，迭代器会抛出StopIteration异常使迭代终止。

在python中，使用yield关键字定义的迭代器也被成为“生成器”
'''