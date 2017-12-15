import docker
from conf import jenkins_config
ip = '192.168.38.56'
create_ip = '192.168.38.64'
create_env = 'dev'
create_business = 'ops'
host_name = jenkins_config.container_host_name.replace('A', create_env).replace('B', create_business).replace('C', create_ip.split('.')[-2]).replace('D', create_ip.split('.')[-1])
print(host_name)
# li = ['192.168.38.56']
# for i in li:
#     c = docker.Client(base_url='tcp://%s:2375' % ip, version='auto', timeout=10)
#     print(c.info()['Containers'])
#     print(c.info()['ContainersRunning'])
