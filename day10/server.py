# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import socketserver


class MyClass(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.sendall(bytes('hello...', encoding='utf-8'))

        while True:
            data = self.request.recv(1024)
            self.request.sendall(data)

if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 8001), MyClass)
    server.serve_forever()