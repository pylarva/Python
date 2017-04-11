# !/usr/bin/env python
# -*- coding:utf-8 -*-

from xml.etree import ElementTree as ET

tree = ET.parse('template.xml')  # 首先建立了一个 xml tree 对象
root = tree.getroot()
print(root)  # 获取根节点
print(root.tag)  # 取根节点名
print(root.attrib)  # 获取节点属性

# for child in root:
#     print(child.tag, child.attrib)
#     for child_second in child:
#         print(child_second.tag, child_second.text)

# for node in root[10][1][1]:
#     print(node.tag, node.attrib)
    # new = int(8388608)
    # node.text = str(new)
print(root[10][1][1].tag)
root[10][1][1].attrib['file'] = '1111'
print(root[10][1][1].attrib)

tree = ET.ElementTree(root)
tree.write('new_xo.xml', encoding='utf-8')