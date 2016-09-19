##作业要求
写一个三级菜单   
输入对应序号进入对应菜单，并展示列表   
支持随时退出
可以才下一级菜单回退到上一级菜单

###所需知识
* 字典
* 列表
* enumerate函数用法
<pre>
for i,j in enumerate(('a','b','c')):  #对字典的元素和下标进行遍历
    print(i,j)
0 a
1 b
2 c
</pre>
* dict、set、list区别
<pre>
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
print(type(a[2][21]))
print(type(a[3][31]))

输出：
class 'dict'
class 'set'
class 'list'
class 'list'
</pre>

