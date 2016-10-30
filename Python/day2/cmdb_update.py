#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

old_dict = {
    "#1": 8,
    "#2": 4,
    "#4": 2,
}

new_dict = {
    "#1": 4,
    "#2": 4,
    "#3": 2,
}

set_old = set(old_dict)
set_new = set(new_dict)

set_del = set_old.difference(set_new)
set_add = set_new.difference(set_old)
set_update = set_old.intersection(set_new)


