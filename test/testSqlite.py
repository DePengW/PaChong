#!/usr/bin/env python
# encoding: utf-8
import sqlite3


# 连接数据库
conn = sqlite3.connect("test.db")

print("Opened database successfully")

# # 创建数据库
#
# #1.获取游标
# c = conn.cursor()
#
# #2.写sql语句
# sql = """
#     create table company
#     (
#         id int primary key not null,
#         name next not null,
#         age int not null,
#         address char(50),
#         salary resl
#     )
#
# """
#
# #3.执行sql
# c.execute(sql)
#
# #4.提交数据库操作
# conn.commit()
#
# #5.关闭数据库
# conn.close()
#
# print("成功建表")


# # 插入数据
# c = conn.cursor()
#
# sql1 = """
#    insert into company (id ,name, age, address, salary)
#    values (1, "张三", 32, "北京", 500)
# """
#
# sql2 = """
#    insert into company (id ,name, age, address, salary)
#    values (2, "李四", 30, "上海", 5000)
# """
#
# c.execute(sql1)
# c.execute(sql2)
#
# conn.commit()
# conn.close()
#
# print("成功插入数据")


# 查询数据
c = conn.cursor()

sql = """
   select id ,name, age, address, salary from company
"""

cursor = c.execute(sql)

for row in cursor:
    print("id = {0}".format(row[0]))
    print("name = {0}".format(row[1]))
    print("age = {0}".format(row[2]))
    print("address = {0}".format(row[3]))
    print("salary = {0}".format(row[4]), "\n")

conn.commit()
conn.close()

print("查询完毕")


