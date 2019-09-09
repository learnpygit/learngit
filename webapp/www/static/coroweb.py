#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'lee'

import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time, functools, inspect #inspect模块有四大功能。这里的是第三个功能：获取类和方法的参数信息

from urllib import parse

from aiohttp import web

from apis import APIError


def get(path):
    # '''
    # Define decorator @get('/path')
    # '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator
    
def post(path):
    # '''
    # Define decorator @post('/path')
    # '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'post'
        wrapper.__route__ = path
        return wrapper
    return decorator   

def get_required_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters 
    #inspect.signature(fn)返回一个inspect.Signature类型对象，值为fn这个函数的所有参数。
    #inspect.Signature对象的parameters属性：一个mappingproxy（映射）类型的对象，值为一个有序字典（Orderdict）。字典的key为参数名，
    #  value是一个inspect.Parameter类型的对象
   
    for name, param in params.items(): #例如函数f(a, b=0))。name是函数的参数名a，param为a;以及name是函数的参数名b，param为b=0
    #inspect.Parameter对象的kind属性：一个_ParameterKind枚举类型的对象，值为这个参数的类型（可变参数，关键词参数，etc）
    #inspect.Parameter对象的default属性：如果这个参数有默认值，即返回这个默认值，如果没有，返回一个inspect._empty类
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            args.append(name)
    return tuple(args)

def get_named_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)

def has_named_kw_args(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            return True

def has_var_kw_arg(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True

def has_request_arg(fn):
    sig = inspect.signature(fn)
    params = sig.parameters
    found = False
    for name, param in params.items():
        if name == 'request':
            found = True
            continue
        if found and (param.kind != inspect.Parameter.VAR_POSITIONAL and param.kind != inspect.Parameter.KEYWORD_ONLY and param.kind != inspect.Parameter.VAR_KEYWORD):
            raise ValueError('request parameter must be the last named parameter in function: %s%s' % (fn.__name__, str(sig)))
    return found
    
#RequestHandler目的就是从URL函数中分析其需要接收的参数，从request中获取必要的参数，
#调用URL函数，然后把结果转换为web.Response对象
class RequestHandler(object):

    def __init__(self, app, fn):
        self._app = app
        self._func = fn
        self._has_request_arg = has_request_arg(fn)
        self._has_var_kw_arg = has_var_kw_arg(fn)
        self._has_named_kw_args = has_named_kw_args(fn)
        self._named_kw_args = get_named_kw_args(fn)
        self._required_kw_args = get_required_kw_args(fn)
        

    async def __call__(self, request):
        print('我是。。。')
        kw = None #获取参数
        if self._has_var_kw_arg or self._has_named_kw_args or self._required_kw_args:
            if request.method == 'POST':
                if not request.content_type:
                    return web.HTTPBadRequest('Missing Content-Type.')
                ct = request.content_type.lower()
                if ct.startswith('application/json'):
                    params = await request.json()
                    if not isinstance(params, dict):
                        return web.HTTPBadRequest('JSON body must be object.')
                    kw = params
                elif ct.startswith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
                    params = await request.post()
                    kw = dict(**params)
                else:
                    return web.HTTPBadRequest('Unsupported Content-Type: %s' % request.content_type)
            if request.method == 'GET':
                qs = request.query_string
                if qs:
                    kw = dict()
                    for k, v in parse.parse_qs(qs, True).items():
                        kw[k] = v[0]
        if kw is None:
            kw = dict(**request.match_info)
        else:
            if not self._has_var_kw_arg and self._named_kw_args:
                # remove all unamed kw:
                copy = dict()
                for name in self._named_kw_args:
                    if name in kw:
                        copy[name] = kw[name]
                kw = copy
            # check named arg:
            for k, v in request.match_info.items():
                if k in kw:
                    logging.warning('Duplicate arg name in named arg and kw args: %s' % k)
                kw[k] = v
        if self._has_request_arg:
            kw['request'] = request
        # check required kw:
        if self._required_kw_args:
            for name in self._required_kw_args:
                if not name in kw:
                    return web.HTTPBadRequest('Missing argument: %s' % name)
        logging.info('call with args: %s' % str(kw))
        try:
            r = await self._func(**kw)
            return r
        except APIError as e:
        #except Exception as e:
            return dict(error=e.error, data=e.data, message=e.message)


def add_static(app):
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')
    #add_static(self,prefix,path,*,name=None,expect_handler=None，...)aiohttp添加静态资源路径。
    #必要2个参数：prefix:静态文件的url前辍，以/开始，就比如这里的/static/。path：静态文件目录路径，可以是相对路径，也可以绝对路径。
    app.router.add_static('/static/', path)
    logging.info('add static %s => %s' % ('/static/', path))

#  用来注册一个URL处理函数          
def add_route(app, fn):
    method = getattr(fn, '__method__', None)
    path = getattr(fn, '__route__', None)
    if path is None or method is None:
        raise ValueError('@get or @post not defined in %s.' % str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
    logging.info('add route %s %s => %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys()))) #inspect.signature(fn).parameters.keys()fn函数的参数名
    logging.info('key %s:' % inspect.signature(fn).parameters.keys())#join返回新的字符串
    logging.info('join key: %s' % ', '.join(inspect.signature(fn).parameters.keys()))
    app.router.add_route(method, path, RequestHandler(app, fn))   #RequestHandler(app, fn)为实例，但这里 RequestHandler是一个类，由于定义了__call__()方法，因此可以将其实例视为函数
    
def add_routes(app, module_name):
    n = module_name.rfind('.') #rfind（）最后出现的位置
    logging.info('n: %s' % n)
    if n == (-1):
        #__import__()函数用于动态加载模块（类和函数），返回元组列表
        mod = __import__(module_name, globals(), locals()) #导入模块handlers
        logging.info('mod: %s' % mod)
        print(mod)
        logging.info('dir mod: %s' % dir(mod))
    else:
        name = module_name[n+1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    for attr in dir(mod): #这里的dir(mod)返回模块handlers的属性、方法列表。
        #dir(object)返回模块的属性、方法列表。dir()函数不带参数时，返回当前范围内的变量、方法和定义的类型列表;带参数时，返回参数的属性、方法列表。
        if attr.startswith('_'): #startswith(str, beg,end)用于检查字符串是否以指定子字符串开始，如果是则返回True，否则返回False
            continue
        logging.info('attr: %s' % attr)
        fn = getattr(mod, attr) #getattr(object, name, default)返回一个对象属性值。object:对象。 name：字符串，对象属性。
        logging.info('add_routes fn: %s' % fn)
        logging.info('callable: %s' % callable(fn))
        if callable(fn): #callable(object)用于检查一个对象是否可调用。可调用返回True，否则返回False.对于函数、方法、lambda函式、类以及实现了__call__方法的类实例，它都返回True
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__', None)
            if method and path:
                add_route(app, fn)
                #logging.info('diaoyong')
