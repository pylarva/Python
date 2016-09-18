## 作业要求


编写用户登陆接口  
输入用户名和密码，成功后显示欢迎信息  
输入三次错误后锁定 
   
###所需知识点
* 文件操作   
<pre>
打开文件
open_file = open('file.txt','r+') # r+以读写方式打开
读取文件
user_list = open_file.readline() # read读取所有行；readline读取每行；reandlins读取并返回一个列表
写文件
open_file.write("2" + "\n")
关闭文件
open_file.close()
</pre>   
* 字典
<pre>
循环字典
user_list = user_file.readlines()
for user_line in user_list
</pre>
* 函数split用法
<pre>
str = "123 \n456 \n789"
print(str.split())
print (str.split(' ',1)) # num=1 分片次数
输出
['123', '456', '789']
['123', '\n456 \n789']
</pre>
###user.txt   
Jordan 123   
kobe 456   
wade 789   
###user_lock.txt   
gasol

###程序设计图
![login](http://i.imgur.com/DunQRGR.png)









