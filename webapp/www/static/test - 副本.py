#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'lee'

# import User


    
# def test0():   
    # # user = User(id=123, name='Michael')
    # # user.save()
    # #user = yield from User.find('1')
    # user = User(id=123, name='Michael')
    # yield from user.save()
    
# test0()

import orm
from models import User, Blog, Comment
import asyncio

    
async def test():   
    kw = {'host': 'localhost', 'port': 3306,'user': 'root','password': 'password','db': 'webapp','charset': 'utf8','autocommit': 'True','maxsize': 10,'minsize': 1} 
    await orm.create_pool(loop, **kw)
    user = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')
    await user.save()
    #user = await User.find('123')
    await orm.destroy_pool() #关闭连接池
    print(user)
#u = Model()    
#print(u.__delete__)  

    
# 获取EventLoop:
loop = asyncio.get_event_loop()

# 执行coroutine
loop.run_until_complete(test())
# sys.exit(0)
loop.close()

    
