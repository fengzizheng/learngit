# from www.coroweb import get
# import asyncio
#
#
# @get('/')
# async def index(request):
#     return '<h1>Awesome</h1>'
#
#
# @get('/hello')
# async def hello(request):
#     return '<h1>hello!</h1>'
#
# def he():
#     a=[1]
#     while True:
#         yield a
#         a=[a[i]+a[i+1] for i in range(len(a)-1)]
#         a.insert(0,1)
#         a.append(1)
#
#
# n=0
# for t in he():
#     print(t)
#     n=n+1
#     if n==10:
#         break

# def triangles():
#     N=[1]
#     while True:
#         yield N
#         N.append(0)
#         N=[N[i-1] + N[i] for i in range(len(N))]
# n=0
# for t in triangles():
#     print(t)
#     n=n+1
#     if n == 10:
#         break

# -*- coding: utf-8 -*-

#
# import time
# def chi():
#     print('%s 吃火锅开始:'%time.ctime())
#     time.sleep(1)
#     print('%s jieshu'%time.ctime())
# def heng():
#     print('%s kaishi'%time.ctime())
#     time.sleep(2)
#     print('%s jieshu'%time.ctime())
#
# if __name__=='__main__':
#     chi()
#     heng()

# import threading
# import time
#
# def chi():
#     print('%s kaishi:'%time.ctime())
#     time.sleep(2)
#     print('%s jieshu'%time.ctime())
#
# def heng():
#     print('%s kaishi'%time.ctime())
#     time.sleep(3)
#     print('%s jieshu'%time.ctime())
#
# threads=[]
# t1=threading.Thread(target=chi)
# threads.append(t1)
# t2=threading.Thread(target=heng)
# threads.append(t2)
#
# if __name__=='__main__':
#     for t in threads:
#         t.start()
