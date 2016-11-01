#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Q1mi"
# Email: master@liwenzhou.com
# Date: 2016/9/18


"""
多层（以三层为例）嵌套循环的退出

主要思路：
利用break来跳出当前循环
先让外层循环的条件不成立（即修改预设的flag值），然后再利用break跳出当前循环，如此组合操作就能实现跳出多层循环了。
因为遇到break直接就跳出循环，跟break同级的后面的代码就没法执行了，所以要在break之前修改flag的值。
见下方的例子↓↓↓

"""


def test():
    exit_flag = False  # 设置一个跳出整个循环的标志

    while not exit_flag:
        print("这是第1层循环...")
        the_input = input("q/Q:退出整个循环,回车进入下一层循环:").strip()
        # 在第一层输入Q，使用break直接就能退出整个循环
        if the_input.upper() == "Q":
            print("再见！")
            break

        while not exit_flag:
            print("这是第2层循环...")
            the_input = input("b/B:返回上层循环;q/Q:退出整个循环,回车进入下一层循环:").strip()
            # 在第二层输入Q跳出整个循环，就需要先让第一层的循环条件不成立，然后再break跳出本层循环
            if the_input.upper() == "Q":
                exit_flag = True  # 让第一层的循环条件不成立
                print("再见！")
                break  # 跳出本层（第二层）循环
            # 在第二层输入B，返回第一层循环，只需要break跳出本层（第二层）循环即可
            elif the_input.upper() == "B":
                print("准备返回上一层循环...")
                break  # 跳出本层（第二层）循环，返回第一层循环

            while not exit_flag:
                print("这是第3层循环...")
                the_input = input("b/B:返回上层循环;q/Q:退出整个循环,回车进入下一层循环:").strip()
                # 在第三层输入Q跳出整个循环，就需要先让第一层和第二层的循环条件不成立，然后再break跳出本层循环
                if the_input.upper() == "Q":
                    exit_flag = True  # 让第一层和第二层的循环条件不成立
                    print("再见！")
                    break  # 跳出本层（第三层）循环
                # 在第三层输入B，返回第二层循环，只需要break跳出本层（第三层）循环即可
                elif the_input.upper() == "B":
                    print("准备返回上一层循环...")
                    break  # 跳出本层（第三层）循环，返回第二层循环


if __name__ == "__main__":
    test()
