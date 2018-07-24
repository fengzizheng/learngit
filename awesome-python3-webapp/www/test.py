# import sys
# def test():
#     args=sys.argv
#     print(len(args))
#     if len(args)==1:
#         print('hello,world')
#     elif len(args)==2:
#         print('hello,%s'%args[1])
#     else:
#         print('too many arguments')
#
# if __name__ =='__main__':
#     test()

# from selenium import webdriver
# import datetime,json
# page=webdriver.Chrome()
# page.get('http://www.baidu.com')

# import asyncio,os,json,time
# import logging;logging.basicConfig(level=logging.INFO)
# from datetime import datetime
# from aiohttp import web
#
# #制作响应函数
# def index(request):
#     return  web.Response(body='<h1 style="color:red">welcome china</h1>',content_type="text/html")
#
# @asyncio.coroutine    #web app 服务器初始化
# def init(loop):
#     app=web.Application(loop=loop) #制作响应函数集合
#     app.router.add_route('GET','/',index) #把响应函数添加到响应函数集合
#     srv=yield from loop.create_server(app.make_handler(),'127.0.0.1',9000) #创建服务器(连接网址,端口，绑定handler)
#     logging.info('server start at http://127.0.0.1:9000...')
#     return srv
#
# loop=asyncio.get_event_loop() #创建事件
# loop.run_until_complete(init(loop))#运行
# loop.run_forever() #服务器不关闭

# import asyncio
# from aiohttp import web
# import logging
# logging.basicConfig(level=logging.INFO)
#
#
# # 通过localhost:8080访问
# async def index(request):
#     resp = web.Response(body=b'<h1>Index</h1>')
#     # 如果不添加content_type，某些严谨的浏览器会把网页当成文件下载，而不是直接显示
#     resp.content_type = 'text/html;charset=utf-8'
#     return resp
#
#
# # 通过localhost:8080/hello/输入一个字符串 访问
# async def hello(request):
#     text = '<h1>hello,%s</h1>' % request.match_info['name']
#     resp = web.Response(body=text.encode('utf-8'))
#     # 如果不添加content_type，某些严谨的浏览器会把网页当成文件下载，而不是直接显示
#     resp.content_type = 'text/html;charset=utf-8'
#     return resp
#
# async def logger1_factory(app, handler):
#     async def logger1_handler(request):
#         print('i am logger1')
#         return await handler(request)
#
#     return logger1_handler
#
#
# async def logger2_factory(app, handler):
#     async def logger2_handler(request):
#         print('i am logger2')
#         return await handler(request)
#
#     return logger2_handler
#
#
#
# async def init(loop):
#     app = web.Application(loop=loop,middlewares={
#         logger1_factory, logger2_factory
#     })
#     app.router.add_route('GET', '/', index)
#     app.router.add_route('GET', '/hello/{name}', hello)
#     server = await loop.create_server(app.make_handler(), 'localhost', 8090)
#     logging.info('server started at http://127.0.0.1:8090...')
#     print('accepting request.....')
#     return server
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(init(loop))
# loop.run_forever()

# import sys
#
# if len(sys.argv) >2:
#     print('wrong')
# else:
#     print('yes')

# import sys
# import time
# import logging
# from watchdog.observers import  Observer
# from watchdog.events import  LoggingEventHandler
# import watchdog
#
# if __name__ =='__main__':
#     logging.basicConfig(level=logging.INFO,format='%(asctime)s-%(message)s',datefmt='%Y-%m-%d %H:%M:%S')
#     path=sys.argv[1] if len(sys.argv)>1 else '.'
#     event_handle=LoggingEventHandler()
#     observer=Observer()
#     observer.schedule(event_handle,path,recursive=True)
#     observer.start()
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()
#
#
# watchdog.events.FileSystemEvent(event_type,src_path,is_directory=false)
# #event.is_directory


#
# import requests
# from sys import argv
#
# USAGE = '''
# USAGE:
# python get.py https://api.github.com
# '''
#
# if len(argv) != 2:
#   print(USAGE)
#   exit()
#
# script_name, url = argv
#
# if url[:4] != 'http':
#   url = 'http://' + url
#
# r = requests.get(url)
#
# print(f"接口地址: {url}\n")
# print(f"状态码: {r.status_code}\n")
# print(f"Headers:")
# for key, value in r.headers.items():
#   print(f"{key} : {value}")
#
# print(r.text)

# import sys
#
# if len(sys.argv) ==1:
#     print('a')
# elif len(sys.argv) ==2:
#     print('b')
# else:
#     print('c')


