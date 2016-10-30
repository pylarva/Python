#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

age = 22

guess_number = int(input("input you guess number:"))
if guess_number == age :
    print("Congratulations!")
elif guess_number < age :
    print("Think smaller...")
else :
    print("Think larger...")