#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

file_abc = "E:\\a.txt"

#with open(file_abc,"r") as f:
#    print(f.read())


with open(file_abc,"a") as f:
    f.write("\n")
    f.write("lichengbing")
with open(file_abc,"r") as f:
    refuse_user = f.find('lichengbing')
    if refuse_user != -1:
        print("Refuse Login...")
    else:
        print(f.read())

a = '1235678'
b = '456'
print(len(a and b))


'''
info = 'abca...bac'
print(info.find('bac'))
#print(info.index('33'))
'''

