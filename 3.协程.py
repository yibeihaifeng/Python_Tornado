'''
使用Tornado协程可以开发出类似同步代码的异步行为。同时，因为协程本身不使用线程，所以减少了线程上下文切换的开销，是一种更高效的开发模式。
'''
# todo：1.编写协程函数

from tornado import gen                        # 引入协程库gen
from tornado.httpclient import AsyncHTTPClient    # 引入异步访问的HTTP客户端


@gen.coroutine   # 加此装饰器表示该函数是协程函数
def coroutine_visit():
    htto_client = AsyncHTTPClient()
    reponse = yield htto_client.fetch('www.baidu.com')
    print(reponse.body)  # 结果处理逻辑代码

'''
本例中仍然使用了异步客户端AsyncHTTPClient进行页面访问，装饰器@gen.coroutine 声明这是一个协程函数。
由于yield关键字的使用，使得代码中不用再编写回调函数用于处理访问结果，而可以直接在yield语句的后面编写结果处理语句。
'''

# todo 2.调用协程函数
# 由于Tornado协程基于python的yield关键字实现，所以不能像调用普通函数一样调用协程函数，比如用下面的代码不能调用之前编写的coroutine_visit（）协程函数：
def bad_call():
    coroutine_visit()    # 无法调用协程函数


'''
协程函数可以通过以下三种方式进行调用：
在本身是协程的函数内通过yield关键字调用；
在IOLoop尚未启动时，通过IOLoop的run_sync()函数调用；
在IOLoop已经启动时，通过IOLoop的spawn_callback()函数调用。



# 2.1 在本身是协程的函数内通过yield关键字调用；
'''
@gen.coroutine
def couter_coroutine():
    print('start call another coroutine')
    yield coroutine_visit()
    print('end of outer coroutine')

'''
本例中 couter_coroutine()和coroutine_visit()都是协程函数,所以它们之间可以通过yield关键字进行调用




# 2.2 在IOLoop尚未启动时，通过IOLoop的run_sync()函数调用；
IOLoop是Tornado的主事件循环对象，Tornado程序通过它监听外部客户端的访问请求，并执行相应的操作。当程序尚未进入IOLoop的running状态时，可以通过run_sync()函数调用协程函数，
比如：
'''

from tornado.ioloop import IOLoop

# 2.2 在IOLoop尚未启动时，通过IOLoop的run_sync()函数调用；
def func_normal():
    print('start to call a coroutine')
    IOLoop.current().run_sync(lambda :coroutine_visit())
    print('end of calling a coroutine')


'''
本例中引用tornado.ioloop包中的IOLoop对象，之后在普通函数中使用run_sync()函数调用
经过lambda封装的协程函数run_sync()函数将阻塞当前函数的执行，直到被调用的协程执行完成。
事实上，Tornado要求协程函数在IOLoop的running状态中才能被调用，只不过run_sync()函数自动完成了启动、停止IOLoop的步骤，它的实现逻辑为：启动IOLoop——>调用被lambda封装的协程函数——>停止IOLoop

当Tornado程序已经处于running状态时的协程函数调用示例如下：
2.3  在IOLoop已经启动时，通过IOLoop的spawn_callback()函数调用。

'''
# 2.3在IOLoop已经启动时，通过IOLoop的spawn_callback()函数调用。

def func_normal_running():
    print('start to call a coroutine')
    IOLoop.current().spawn_callback(coroutine_visit)
    print('end of calling a coroutine')

'''
本例中spawn_callback()函数将不会等待被调用协程执行完成，所以spawn_callback()之前和之后的print语句将会被连续执行，而coroutine_visit本身将会由IOLoop在合适的时机进行调用。
IOLoop的spawn_callback()函数没有为开发者提供获取协程函数调用返回值的方法，所以只能用spawn_callback()函数调用没有返回值的协程函数
'''

# todo：3.在协程中调用阻塞函数
# 在协程中直接调用阻塞函数会影响协程本身的性能，所以Tornado提供了在协程中利用线程池调度阻塞函数，从而不影响协程本身继续执行的方法。如下：
from concurrent.futures import ThreadPoolExecutor
thread_pool = ThreadPoolExecutor(2)  # 实例化一个包含2个线程的线程池

def mySleep(count):   # 阻塞函数
    import time
    for i in range(count):
        time.sleep(1)


@gen.coroutine
def call_blocking():
    print('start of call_blocking')
    yield thread_pool.submit(mySleep,10)
    print('end of call_blocking')

'''
代码中首先引用了concurrent.futures中的ThreadPoolExecutor类，并实例化了一个有两个线程的线程池thread_pool。
在需要调用阻塞函数的协程call_blocking()中，使用thread_pool.submit调用阻塞函数，并通过yield返回。这样便不会阻塞协程所在线程的继续执行，也保证了阻塞函数前后代码的执行顺序。
'''



# todo：4.在协程中等待多个异步调用
# Tornado允许在协程中用一个yield关键字等待多个异步调用，只需把这些调用用列表或字典的方式传递给yield关键字即可
# 列表方式
@gen.coroutine
def coroutine_visit_list():
    http_client = AsyncHTTPClient
    list_response = yield [ http_client.fetch('www.baidu.com'),
                           http_client.fetch('www.sina.com'),
                           http_client.fetch('www.163.com') ]
    # 以列表的形式返回访问结果
    for response in list_response:
        print(response.body)

# 字典方式
@gen.coroutine
def coroutine_visit_dict():
    http_client = AsyncHTTPClient
    dict_response = yield {'baidu':http_client.fetch('www.baidu.com'),
                           'sina':http_client.fetch('www.sina.com'),
                          '163': http_client.fetch('www.163.com')}
    
    # 以字典的形式返回访问结果
    print(dict_response['sina'].body)

