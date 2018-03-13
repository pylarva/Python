import re
a = '192.168.0.0'
new_ip = re.match('\d+\.\d+\.\d+\.', a).group()
print(new_ip)
for i in range(5):
    new_ips = '%s%s' % (new_ip, i)
    print(new_ips)


