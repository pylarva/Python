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
#print(type(a))
#print(type(a[2][21]))
#print(type(a[3][31]))

haha_dict = {}
for i,j in enumerate(a[2][21]):
    haha_dict[i] = j
#    print('%d.%s' % (i, j))
#print(haha_dict)
b = a[2][21]
#print(b)
#print('%d.%s'% (i,j))

c = {
    100:[('1',11),('2',22),('3',33)],
    101:[('A',11),('B',22),('C',33)]
}
#print(type(c[100]))
#print(c[100][0])
#print(c.keys())

d = []
d.append(('a',2,1888))

#print(d)
#print(d[0][2])

f = open('C:/Users/lilongzi/Desktop/test.txt')
a_line = f.read()
b_line = f.readline()
c_line = f.readlines()

print('1:',b_line)
