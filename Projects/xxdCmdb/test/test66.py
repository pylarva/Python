import docker
ip = '192.168.38.56'
new = '192.168.38.57'
c = docker.Client(base_url='tcp://%s:2375' % ip, version='auto', timeout=10)
b = c.images()

print(b)