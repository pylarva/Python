# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

# python内存队列 进程退出后 队列失效

import queue

# queue.Queue 先进先出
# q = queue.LifoQueue() 后进先出

# 权重队列
# q = queue.PriorityQueue()
# q.put((1, "alex"))
# print(q.get())

# 双向队列
# q = queue.deque()
# q.append(123)
# q.append(456)
# q.appendleft(789)
# q.pop()
# q.popleft()


# 先进先出队列
# 参数10表示最多只接收10个数据
# q = queue.Queue(10)
# q.put(11)
# q.put(22)
# 超时时间timeout block是否阻塞
# q.put(33, timeout=2)
# q.put(33, block=False)

# print(q.qsize())
# get默认阻塞 有数据才能取
# print(q.get())
# print(q.get(block=False))

# join task_done 阻塞进程 当队列中的任务执行完毕后 不再阻塞
q = queue.Queue()
q.put(123)
q.put(456)
q.get()
q.task_done()
q.get()
q.task_done()

q.join()