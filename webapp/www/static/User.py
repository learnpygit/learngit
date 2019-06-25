#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'lee'

from orm import Model, StringField, IntegerField, create_pool, destroy_pool
import asyncio
import sys
class User(Model):
    __table__ = 'user'

    id = IntegerField('id',primary_key=True)
    name = StringField('name')
    # password = StringField('password')
    
async def test():   
    kw = {'host': 'localhost', 'port': 3306,'user': 'root','password': 'password','db': 'test','charset': 'utf8','autocommit': 'True','maxsize': 10,'minsize': 1} 
    await create_pool(loop, **kw)
    user = User(id=3, name='主')
    await user.save()
    #user = await User.find('123')
    await destroy_pool() #关闭连接池
    # print(user)
    print(user)kkkkjkjkjhhh
#u = Model()    
#print(u.__delete__)  

    
# 获取EventLoop:
loop = asyncio.get_event_loop()

# 执行coroutine
loop.run_until_complete(test())
# sys.exit(0)
loop.close()

# class A(object):
    # bar = 1
    # def func1(self):  
        # print ('foo') 
    # @classmethod
    # def func2(cls):
        # print ('func2')
        # print (cls.bar)
        # cls().func1()   # 调用 foo 方法
        # print(cls())
 
# A.func2()     