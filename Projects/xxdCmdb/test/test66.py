from netaddr import IPNetwork
import socket
import queue
from conf import kvm_config
from threading import Thread


def get_ip(host_machine):
    """
    自动获取IP地址
    :param host_machine:
    :return:
    """

    def aaa(ip, q):
        ip = str(ip)
        s = socket.socket()
        s.settimeout(1)
        if s.connect_ex((ip, 22)) != 0:
            q.put(ip)
        s.close()

    ipaddr = IPNetwork('%s/24' % host_machine)[kvm_config.kvm_range_ip[0]:kvm_config.kvm_range_ip[1]]
    q = queue.Queue()
    for ip in ipaddr:
        Thread(target=aaa, args=(ip, q)).start()
    try:
        new_ip = q.get(block=True, timeout=5)
        return new_ip
    except Exception as e:
        return False

ret = get_ip('192.168.31.10')
print(ret)


