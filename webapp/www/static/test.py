#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'lee'

import User


    
def test0():   
    # user = User(id=123, name='Michael')
    # user.save()
    #user = yield from User.find('1')
    user = User(id=123, name='Michael')
    yield from user.save()
    
test0()
    
