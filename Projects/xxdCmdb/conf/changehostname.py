#!/bin/env python

import sys
import os
import subprocess
from threading import Timer


def execSystemCommand(cmd, timeout=30):
    """ run cmd return output and status, timeout will return"""
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, shell=True, preexec_fn=os.setsid)
    killProc = lambda pid: os.killpg(pid, signal.SIGKILL)
    timer = Timer(timeout, killProc, [popen.pid])
    timer.start()
    popen.wait()
    output = popen.stdout.read()
    timer.cancel()

    return popen.returncode, output

def execSystemCommandRunAs(cmd, user, timeout=30):
    """ run cmd return output and status, timeout will return"""
    cmd = "su - %s -c '%s'" %(user, cmd)
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, shell=True, preexec_fn=os.setsid)
    killProc = lambda pid: os.killpg(pid, signal.SIGKILL)
    timer = Timer(timeout, killProc, [popen.pid])
    timer.start()
    popen.wait()
    output = popen.stdout.read()
    timer.cancel()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Miss arguments."
        sys.exit(1)
    strHost = sys.argv[1]
    strHostname = sys.argv[2]
    strHosts = strHost + '    ' + strHostname
    strHostsEscape = strHosts.replace(' ','\ ')
    cmd = 'ssh %s "hostname %s && echo %s > /etc/hostname && \
            sed -i s/%s.*/%s/g /etc/hosts && \
            sed -i s/HOSTNAME=.*/HOSTNAME=%s/g /etc/sysconfig/network" ' %(strHost,strHostname,strHostname,strHost,strHostsEscape,strHostname)
    #print cmd
    retCode, output = execSystemCommand(cmd)
    print retCode
