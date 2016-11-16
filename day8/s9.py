# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# 异常处理

while True:

    num1 = input('num1: ')
    num2 = input('num2: ')

    try:
        num1 = int(num1)
        num2 = int(num2)
        ret = num1 + num2

    except Exception as ex:
        print(ex)
    except ValueError as ex:
        print(ex)
    except IndexError as ex:
        print(ex)


# 异常处理完整代码块

try:
    raise Exception('主动错误一下...')
    pass
except ValueError as ex:
    print(ex)
except Exception as ex:
    print(ex)
else:
    pass
finally:
    pass


# 断言

assert 1 == 2