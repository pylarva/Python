# import docker
# ip = '192.168.38.56'
# new = '192.168.38.57'
# c = docker.Client(base_url='tcp://%s:2375' % ip, version='auto', timeout=10)
# b = c.images()
#
# print(b)
import subprocess
from conf import jenkins_config

cmd = "ssh root@192.168.38.60 'python2.6 /opt/autopublishing.py http://build.xxd.com/prod/front/424/front.war 1e545a527904c6de68d15537ec1f96fa 424 tomcat front None'"

ret = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
ret_err = ret.stderr.read()
ret_out = ret.stdout.read()
if ret_err:
    print('----', ret_err)
    print('====', ret_out)