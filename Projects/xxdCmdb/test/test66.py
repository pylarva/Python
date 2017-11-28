import docker
ip = '192.168.38.56'
new = '192.168.38.57'
c = docker.Client(base_url='tcp://%s:2375' % ip, version='auto', timeout=10)
name = 'test01'
get_old_ip = c.inspect_container(name).get('Config').get('Hostname').split('-')[-1]
new_ip = new.split('.')[-1]

a = c.inspect_container(name).get('Config').get('Hostname')
b = a.replace(get_old_ip, new_ip)

print(b)