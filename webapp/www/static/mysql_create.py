#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'lee'

import mysql.connector
# 注意把password设为你的root口令:
conn = mysql.connector.connect(user='root', password='password', database='test')
cursor = conn.cursor()
# 创建user表:
cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
# 插入一行记录，注意MySQL的占位符是%s:
cursor.execute('insert into user (id, name) values (%s, %s)', ['1', 'lee'])
cursor.rowcount

# 提交事务:
conn.commit()
cursor.close()
conn.close()