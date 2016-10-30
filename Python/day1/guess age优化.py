#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

age = 22
counter = 0
for i in range(10):
    if counter <3:
        guess_number = int(input("input you guess number:"))
        if guess_number == age :
            print("Congratulations!")
            break
        elif guess_number < age :
            print("Think smaller...")
        else :
            print("Think larger...")
    else:
        #print("Too namy attempts...bye!")
        #break
        continue_confirm = input("Do you want to continue guess? Y or N: ")
        if continue_confirm == 'Y':
            counter = 0
            continue
        else:
            print("bye...")
            break
    counter += 1