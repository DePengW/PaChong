#!/usr/bin/env python
# encoding: utf-8
import xlwt

# 创建一个对象
workbook = xlwt.Workbook(encoding="utf-8")
worksheet = workbook.add_sheet('sheet1')
for i in range(9):
    for j in range(9):
        if(i >= j):
            worksheet.write(i, j, "{0} * {1} == {2}".format(i+1, j+1, (i+1)*(j+1)))
        else:
            break
workbook.save('test.xls')

# 创建一个表单
# 向表单里添加内容
# 保存xls