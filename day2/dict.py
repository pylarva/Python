#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

#生成字典
id_db = {
    100: {
        'name':"linux",
        'age':24,
        'addr':"shanghai"
    },
    101: {
        'name':"nuix",
        'age':23,
        'addr':"anhui",
    },
}
#del id_db[101]
#id_db.[185]['name']='li'
#id_db[185]['qq']=123
#print(id_db[340826199303031235])
#print(id_db[185185])
#id_db[185185].pop("addr")
#print(id_db[185185])
#v = id_db.get(185185)
#print(v)
#print(id_db.items())
dict2 = {
    'name': "Redhat",
     103: {
     'name':"Ubuntu",
    },
}
#id_db.update(dict2)
#print(id_db)
#print(id_db.items())
#print(id_db.values())
#print(id_db.keys())
#id_db.has_key(185185) #only in 2.x
'''
if 185185 in id_db:
    print("yes")
else:
    print("no")
'''
#print(id_db.setdefault(185,"9999")) #取一个值，如果值不存在则新添加一个默认值
#print(id_db.fromkeys([1,2,3,56],'dddd')) #设置一个新字典，前面是key后面填充value
print(id_db.popitem()) #随机删除一个key，不要用这个随机删除
print(id_db)
'''
for k,v in id_db.items():   #循环效率低，因为有一个dict转list的过程
    print(k,v)
'''

#for key in id_db:         #效率高
#    print(key,id_db[key])