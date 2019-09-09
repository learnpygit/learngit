#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'lee'

import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web
from jinja2 import Environment, FileSystemLoader

import orm
from coroweb import add_routes, add_static, get, add_route

from handlers import COOKIE_NAME, cookie2user

def init_jinja2(app, **kw):
    logging.info('init jinja2...')
    options = dict(
        autoescape = kw.get('autoescape', True),
        block_start_string = kw.get('block_start_string', '{%'),
        block_end_string = kw.get('block_end_string', '%}'),
        variable_start_string = kw.get('variable_start_string', '{{'),
        variable_end_string = kw.get('variable_end_string', '}}'),
        auto_reload = kw.get('auto_reload', True)
    )
    path = kw.get('path', None)
    logging.info('path: %s' % path)
    logging.info('文件名: %s' % __file__)
    logging.info('绝对路径: %s' % os.path.abspath(__file__))
    logging.info('目录路径: %s' % os.path.dirname(os.path.abspath(__file__)))
    logging.info('目录路径中的目录路径: %s' % os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if path is None:
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
        #path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
        #os.path.join合成一个路径。os.path.dirname返回目录路径。os.path.abspath返回绝对路径
    logging.info('set jinja2 template path: %s' % path)
    env = Environment(loader=FileSystemLoader(path), **options)
    logging.info('env: %s' % env)
    filters = kw.get('filters', None)
    logging.info('filters: %s' % filters)
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f
            logging.info('env.filters[name]: %s' % env.filters[name])
    app['__templating__'] = env    
    

async def logger_factory(app, handler):
    async def logger(request):
        # 记录日志:
        logging.info('我Request: %s %s' % (request.method, request.path))
        # await asyncio.sleep(0.3)
        # 继续处理请求:
        return (await handler(request))
    return logger

async def data_factory(app, handler):
    async def parse_data(request):
        if request.method == 'POST':
            if request.content_type.startswith('application/json'):
                request.__data__ = await request.json()
                logging.info('request json: %s' % str(request.__data__))
            elif request.content_type.startswith('application/x-www-form-urlencoded'):
                request.__data__ = await request.post()
                logging.info('request form: %s' % str(request.__data__))
        return (await handler(request))
    return parse_data

async def response_factory(app, handler):
    async def response(request):
        logging.info('Response handler...: %s' % handler)
        r = await handler(request)
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):
            if r.startswith('redirect:'):
                return web.HTTPFound(r[9:])
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        if isinstance(r, dict):
            template = r.get('__template__')
            if template is None:
                resp = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            else:
                r['__user__'] = request.__user__
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                resp.content_type = 'text/html;charset=utf-8'
                logging.info('resp: %s ' % resp)
                return resp
        if isinstance(r, int) and r >= 100 and r < 600:
            return web.Response(r)
        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and t >= 100 and t < 600:
                return web.Response(t, str(m))
        # default:
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp
    return response

async def auth_factory(app, handler):
    async def auth(request):
        logging.info('check user: %s %s' % (request.method, request.path))
        request.__user__ = None
        cookie_str = request.cookies.get(COOKIE_NAME)
        if cookie_str:
            user = await cookie2user(cookie_str)
            if user:
                logging.info('set current user: %s' % user.email)
                request.__user__ = user
        logging.info('Response auth handler...: %s' % handler)        
        return (await handler(request))
    return auth

def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return '1分钟前'
    if delta < 3600:
        return '%s分钟前' % (delta // 60)
    if delta < 86400:
        return '%s小时前' % (delta // 3600)
    if delta < 604800:
        return '%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return '%s年%s月%s日' % (dt.year, dt.month, dt.day)

# @get('/')
# def index(request):
    # users = yield from User.findAll()
    # return {
        # '__template__': 'test.html',
        # 'users': users
    # }

async def init(loop):
    await orm.create_pool(loop=loop,host='127.0.0.1', port=3306, user='www',password='www',db='webapp')
    app = web.Application(loop=loop, middlewares=[
        logger_factory, response_factory, auth_factory
    ])
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    add_routes(app, 'handlers') # 自动把handler模块的所有符合条件的函数注册了
    # add_routes(app, 'index')
    add_static(app)
    # add_route(app, index)
    
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()