#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import re
# from collections import defaultdict,OrderedDict
#
# dic = {}
# show_dic = defaultdict(list)
# with open('text_a', 'r') as file:
#     for line in file:
#         if line.split():
#             line = line.split()
#             print(line)

with open('text_a', 'a+') as file:
    name = input('shuru: ')
    file.write('\n'*2 + '%s' % name)
print('ok')

