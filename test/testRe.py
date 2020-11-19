#!/usr/bin/env python
# encoding: utf-8


import re

pat = re.compile("AA")      # pat：需要匹配的字符串
# m = pat.search("ABC")       # "ABC"：要被校验的内容

m = re.findall("[A-Z]", "ABCdefGHI")


print(m)