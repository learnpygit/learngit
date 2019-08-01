#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'lee'

import logging; logging.basicConfig(level=logging.INFO)

from coroweb import get

import orm
from models import User, Blog, Comment
import asyncio

@get('/')
async def index(request):
    users = await User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }