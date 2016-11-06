# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing



# xml是实现不同语言和程序之间进行数据交换的协议

from xml.etree import ElementTree as ET

# xml有两个常见格式
# 1）直接读取字符串格式的xml
str_xml = open('xo.xml', 'r').read()
root = ET.XML(str_xml)  # 这里没有建立 xml tree 所以不能直接将内存中的xml写回文件

# 2）读取xml格式文件
# tree = ET.parse('xo.xml')  # 首先建立了一个 xml tree 对象
# root = tree.getroot()
# print(root)  # 获取根节点
# print(root.tag)  # 取根节点名
# print(root.attrib)  # 获取节点属性

# 3) 遍历多层xml
for child in root:
    print(child.tag, child.attrib)
    for child_second in child:
        print(child_second.tag, child_second.text)  # child_second.text 节点内容

# 4) 遍历指定的节点
for node in root.iter('year'):
    print(node.tag, node.text)

# 5) 修改节点内容
for node in root.iter('year'):
    new_year = int(node.text) + 1
    node.text = str(new_year)

    node.set('name', 'london')
    node.set('age', '18')

    del node.attrib['age']

tree = ET.ElementTree(root)
tree.write('new_xo.xml', encoding='utf-8')


# 6、删除节点
str_xml = open('xo.xml', 'r').read()
root = ET.XML(str_xml)
for country in root.findall('country'):
    rank = int(country.find('rank').text)
    if rank > 50:
        root.remove(country)

tree = ET.ElementTree(root)
tree.write('new_xoo.xml', encoding='utf-8')


# 7、创建 xml 文档

from xml.dom import minidom


def prettify(elem):
    """将节点转换成字符串，并添加缩进。
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

# 创建根节点
root = ET.Element("famliy")

# 创建大儿子
# son1 = ET.Element('son', {'name': '儿1'})
son1 = root.makeelement('son', {'name': '儿1'})
# 创建小儿子
# son2 = ET.Element('son', {"name": '儿2'})
son2 = root.makeelement('son', {"name": '儿2'})

# 在大儿子中创建两个孙子
# grandson1 = ET.Element('grandson', {'name': '儿11'})
grandson1 = son1.makeelement('grandson', {'name': '儿11'})
# grandson2 = ET.Element('grandson', {'name': '儿12'})
grandson2 = son1.makeelement('grandson', {'name': '儿12'})

son1.append(grandson1)
son1.append(grandson2)


# 把儿子添加到根节点中
root.append(son1)
root.append(son1)

raw_str = prettify(root)  # 自动添加缩进

f = open("xxxoo.xml", 'w', encoding='utf-8')
f.write(raw_str)
f.close()





