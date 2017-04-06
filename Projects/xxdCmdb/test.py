# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
import paramiko
from io import StringIO

key_str = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAx8BCwoZYq/fwQ9Q1qXi/u52eEzmLNiDA/OZdaJhvduRPd7Xh
drrkIm7IRpWawzoiVr5esTLA9n98on5vDE5QbP3VTWxAtnMXT3i6g2zenjRcH7pj
8LxiZcxy8OyeMdoQcnKCKTeSi3MzX7p9r4qE9krYRMU5CoPV4vNuodb21kLtDXok
5GiEQTxR1mCaxAYKlw7GM3bCNq9nKVOkwbnDx6tiHqWWOi2RbFGp6RQiNIRwv9px
YCV3hjRhhsBHmjX7TzzMud4UK+TelMFDWW9W0/HReBZYhdiMOcWOnUBRuuzq26xm
jm4ek2Z/YlYLpudtM0E7MbSXDc4Uay6Vjv+ClwIDAQABAoIBAQCVtE0UdxWrxMWI
QFn7amjgFq/rHpxr875Pi+MDygL36wJ36JNSpZznBXoKFIOJv18O/dwAF9awpzlk
mzdk1KjIFrEvNmuFkdotkIDQkN6DWSCWEt5mBPoF62VVlTC2kgTzkUhl1aV559vf
6efakQk3gT52xA0NCWNalTEcD/ys9OavCw3TFyioLXgs3IJji4LOgu20sCu/mfBM
wG4TnU+OElhXDQnQy/kvg2RSFGzBlGlaTfRljMGncf8LE0Sf1U2nQUmtbFWZcAR0
9s6F1eiN1sTHlGyMikdBAxe+Xmr9eYxScs7whorWjYGYoTolo9sVW2z6kmqF2fN+
+BddtFKBAoGBAOWpsDoe08uplzpWJRRetrhhH8VXlNMAZXzTZ5Ch+Qtp+1ef5VDK
9Ifn4IMLdBmHHFCSFvbidSWNbH6jjHODqid2K0aTx6imvIndUZk/rMDcPQYiY4Vd
k5/nPiouc7MB9DWD15P7Z807C4chMrdMCIWw4EzTtTNpUVhVYilqP/9XAoGBAN6o
cB0+ls1O+QJT7olccdazY48mVQDwfZvkCQL15ehAkt32Gtt1dR8pEmR65QrPH2Gs
v4zXBxGDbaBy/vWEgU1Hyx689JKnQw8QGM7znw74xI63hGKFHhQuvb1VDmDl2Cuu
vdMysXK4+sqF9BwLcxbkELn3HXD+kIXlXCSP+M7BAoGAfjqvHrLU7ErRUQIKLVEF
kv/nC3tg1DySi3JSqP8tuCVPPVEoJCj5ED3Ve5FvBZzqZip1rsq3YqWBrXVM/Cyw
+DGOBaOyCLNkS042zElgNTyX2ehK1QGi4y+hTmPrucboKAXIFpEG85lxc5s+mdqT
kI+wKOnv3UsUp71+T48Tj88CgYAMVulftYhF+Ip0RpKBqk3kyCxMUqODWdCcQxb8
wwPqyylYg7sZTnkfMPeD+guXfcMPdrNm6sPJhK8epUDb+mvwDHqFSZOETSC6RPoa
/gVinwbFogYEL7xrAewiAgS5+gLw6M48ViLfaMD9WE8e/sNyEVGb/MX07Sa1RPDG
VfREAQKBgQDZ91mTadB09U5HXYNq0r2roxqdLRMWc0tFiCOJnelMJ7Ix+mQUh3sE
T6DHO/D5779SW8xy8Fo0O3bHr41boCBgRn7/x4sxYiOPaR05Z9e4xW4GQvbSHs3F
M3ccnsavjnp8EhqL/P+OP9YwqVmk+TH4nx4bQZegTn2DmIH8SRXCcQ==
-----END RSA PRIVATE KEY-----"""


def change_ip():
    transport = paramiko.Transport(('192.168.31.115', 22))
    transport.connect(username='root', password='123456')

    ssh = paramiko.SSHClient()
    ssh._transport = transport

    print('更改ip...')
    stdin, stdout, stderr = ssh.exec_command("sed -i 's#192.168.31.115#192.168.31.119#g' /etc/sysconfig/network-scripts/ifcfg-eth0")
    result = stdout.read()
    print('IP完成...', result)
    stdin, stdout, stderr = ssh.exec_command("ifdown eth0 && ifup eth0", timeout=1)
    result = stdout.read()
    print('虚机部署完成...', result)

    transport.close()

private_key = paramiko.RSAKey(file_obj=StringIO(key_str))
transport = paramiko.Transport(('192.168.31.111', 22))
transport.connect(username='root', pkey=private_key)

ssh = paramiko.SSHClient()
ssh._transport = transport

virsh_cmd = 'virt-clone --connect=qemu:///system -o a0-kvm-vhost-38-115.yh -n a0-kvm-vhost-38-119.yh -f /opt/mv/a0-kvm-vhost-38-119.yh.qcow2'
stdin, stdout, stderr = ssh.exec_command(virsh_cmd)
result = stdout.read()
print('拷贝文件...', result)
time.sleep(5)

virsh_cmd = 'virsh start a0-kvm-vhost-38-119.yh'
stdin, stdout, stderr = ssh.exec_command(virsh_cmd)
result = stdout.read()
print('启动虚拟机...', result)
time.sleep(30)
transport.close()


data = os.system("ping -c 1 192.168.31.115 > /dev/null 2>&1")
if data == 0:
    print('启动成功...')
    change_ip()
else:
    print('lost...')


