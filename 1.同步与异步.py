'''
Tornado是一个可扩展的非阻塞式Web服务器及其相关工具的开源本版。可以用简单命令 pip install tornado进行安装
Tornado每秒可以处理数以千计的连接，所以对于实时Web服务来说，Tornado是一个理想的Web框架。
特点：
1.完备的Web框架：与Django、Flask等一样，Tornado也提供了URL路由映射、Request上下文、基于模板的页面渲染技术等开发web应用的必备工具
2.是一个高效的网络库，性能与Twisted、Gevent等底层Python框架相媲美：提供了异步I/O支持、超时事件处理。这使得Tornado除了可以作为Web应用服务器框架，还可以用来做爬虫应用、物联网关、游戏服务器等后台应用、
3.提供高效 HTTPClient：除了服务器端框架，Tornado还提供了基于异步框架的HTTP客户端。
4.提供搞笑的内部HTTP服务器：虽然其他Python网络框架（Django、Flask）也提供了内部的HTTP服务器，但它们的HTTP服务器由于性能原因只能用于测试环境。而Tornado的HTTP服务器与Tornado异步调用紧密结合，可以直接用于生产环境
5.完备的WebSocket支持：WebSocket是HTML5的一种新标准，实现了浏览器与服务器之间的双向实时通信
概念：
同步I/O： 导致请求进程阻塞，直到I/O操作完成；在python中可以理解为：一个被调用的I/O函数会阻塞调用函数的执行
异步I/O：不导致进程阻塞。                                      一个呗调用的I/O函数不会阻塞调用函数的执行
'''
from tornado.httpclient import HTTPClient   # Tornado的HTTP客户端类

# todo：同步I/O访问www.baidu.com

def synchronous_visit():
    http_client = HTTPClient()
    response = http_client.fetch('www.baidu.com')  # 阻塞 ，直到对www.baidu.com访问完成  函数才能往下进行
    print(response.body)

'''
HTTPClient是Tornado的同步访问HTTP客户端。
上述代码中的synchronous_visit()函数使用了典型的同步I/P函数操作访问www.baidu.com网站，该函数的执行时间取决于网络速度、对方服务器响应速度等。
只有当对www.baidu.com的访问完成并获取到结果后，才能完成对synchronous_visit()函数的执行。

'''

# todo：异步I/O访问www.baidu.com
from tornado.httpclient import AsyncHTTPClient     # Tornado的异步访问HTTP客户端

def handle_response(response):
    print(response.body)

def asynchronous_visit():
    http_client = AsyncHTTPClient()
    http_client.fetch('www.baidu.com',callback=handle_response)


'''
AsyncHTTPClient是Tornado的异步访问HTTP客户端。
在上述代码的asynchronous_visit()函数中使用AsyncHTTPClient对第三方网站进行异步访问。
http_client.fetch()函数会在调用后立刻返回而无须等待实际访问的完成，从而导致asynchronous_visit()也会立刻执行完成。
当对www.baidu.com的访问实际完成后，AsyncHTTPClient会调用callback参数指定的函数，开发者可以在其中写入处理访问结果的逻辑代码
'''
