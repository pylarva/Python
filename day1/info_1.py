#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import getpass

#name = input("name:")
#passwd = getpass.getpass("passwd:")

#print(name,passwd)

#username = input("uesrname:")
#password = getpass.getpass('password: ')
#print(username,password)

#for i,j in enumerate(('a','b','c')):
#    print(i,j)
'''
def show(b='',c=''):
    print(b,c)

a=1
b=2
show(a,b)
'''
a = {
    1:[1,2,3],
    2:{
        21:{
            'a',
            'b',
        },
        22:[4,5,6]
    },
    3:{
        31:[7,8,9]
    }
}
print(type(a))
print(type(a[2]))
print(type(a[3][31]))

b = a[2]
print(b)