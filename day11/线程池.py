# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import queue
import threading
import contextlib
import time

# 空任务标识 终止进程
StopEvent = object()


class ThreadPool(object):

    def __init__(self, max_num, max_task_num=None):
        if max_task_num:
            # 装任务的队列q
            self.q = queue.Queue(max_task_num)
        else:
            self.q = queue.Queue()
        # 允许的最大大线程数
        self.max_num = max_num
        # 终止线程
        self.cancel = False
        self.terminal = False
        # 当前已创建的线程数量
        self.generate_list = []
        # 当前空闲的线程数量
        self.free_list = []

    def run(self, func, args, callback=None):
        """
        线程池执行一个任务
        :param func: 任务函数
        :param args: 任务函数所需参数
        :param callback: 任务执行失败或成功后执行的回调函数，回调函数有两个参数1、任务函数执行状态；2、任务函数返回值（默认为None，即：不执行回调函数）
        :return: 如果线程池已经终止，则返回True否则None
        """
        if self.cancel:
            return
        # 判断已经创建的线程数量是否小于最大线程数 表示所有的线程在忙 多余任务不再创建线程
        if len(self.free_list) == 0 and len(self.generate_list) < self.max_num:
            self.generate_thread()
        # 任务元组放到队列
        w = (func, args, callback,)
        self.q.put(w)

    def generate_thread(self):
        """
        创建一个线程
        """
        t = threading.Thread(target=self.call)
        t.start()

    def call(self):
        """
        循环去获取任务函数并执行任务函数
        """
        current_thread = threading.currentThread()
        # 将已经创建的线程加入线程列表
        self.generate_list.append(current_thread)

        # 取任务元组
        event = self.q.get()
        while event != StopEvent:

            # 得到任务元组的内容
            func, arguments, callback = event
            try:
                # 执行 action 函数
                result = func(*arguments)
                success = True
            except Exception as e:
                success = False
                result = None

            if callback is not None:
                try:
                    callback(success, result)
                except Exception as e:
                    pass

            # 将线程标记为空闲
            with self.worker_state(self.free_list, current_thread):
                if self.terminal:
                    event = StopEvent
                else:
                    # 如果取到的是空任务执行下面的else
                    event = self.q.get()
        else:

            self.generate_list.remove(current_thread)

    def close(self):
        """
        执行完所有的任务后，所有线程停止
        """
        self.cancel = True
        # 创建了多少线程就传几个空任务
        full_size = len(self.generate_list)
        while full_size:
            self.q.put(StopEvent)
            full_size -= 1

    def terminate(self):
        """
        无论是否还有任务，终止线程
        """
        self.terminal = True

        while self.generate_list:
            self.q.put(StopEvent)

        self.q.queue.clear()

    @contextlib.contextmanager
    def worker_state(self, state_list, worker_thread):
        """
        用于记录线程中正在等待的线程数
        """
        state_list.append(worker_thread)
        try:
            yield
        finally:
            state_list.remove(worker_thread)

# How to use


pool = ThreadPool(5)


def callback(status, result):
    # status, execute action status
    # result, execute action return value
    pass


def action(i):
    print(i)

# 30个任务
for i in range(30):
    ret = pool.run(action, (i,), callback)

time.sleep(5)
print(len(pool.generate_list), len(pool.free_list))
print(len(pool.generate_list), len(pool.free_list))
pool.close()
# pool.terminate()