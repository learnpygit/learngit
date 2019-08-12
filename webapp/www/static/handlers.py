#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'lee'

import logging; logging.basicConfig(level=logging.INFO)

from coroweb import get

import orm
from models import User
import asyncio

@get('/')
async def index(request):
    users = await User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }
    
@get('/blog/{id}')
async def get_blog(id):
    #users = await User.find('001563259626028f188f1b2c47a49c48a7d70619b85b20c000')
    blog_users = await User.find(id)
    return {
        '__template__': 'get_blog.html',
        'blog_users': blog_users
    }