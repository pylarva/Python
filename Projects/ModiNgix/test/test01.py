# !/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import fileinput

file = '/opt/live.conf'
new_file = '/opt/newfile.conf'

if not os.path.exists(new_file):
    os.system('touch %s' % new_file)

# if os.path.exists(file):
#     with open(file, 'r') as f:
#         for line in f:
#             if re.match('\s+still_range', line):
#                 s += 1
#     print('111', s)
#     with open(file, 'r+') as f:
#         for line in f:
#             if re.match('\s+still_range', line):
#                 s -= 1
#                 if s == 0:
#                     f.write('777\n')
#
#     print('222', s)
with open(file, 'r') as readfile, open(new_file, 'w') as writefile:
    for line in readfile:
        if re.match('\s+timeshift_segments_per_playlist', line):
            writefile.write(line)
            writefile.write('    666\n')
        else:
            writefile.write(line)
