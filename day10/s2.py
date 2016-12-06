# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import socketserver


class MyClass(socketserver.BaseRequestHandler):

    def handle(self):
        pass


obj = socketserver.ThreadingTCPServer(('127.0.0.1', 9999), MyClass)
obj.serve_forever()