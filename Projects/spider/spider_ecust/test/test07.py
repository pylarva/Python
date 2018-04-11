# !/usr/bin/env python
# -*- coding:utf-8 -*-

import re
s = "<script>alert('成功记录学习时间！本章节累计学习时间为：61分0秒');window.opener=null;window.close();</script>"
print(re.search(('\d+'), s).group())