# -*- coding:utf-8 -*-
import ldap3


def authorize(host=None, port=None, user=None, password=None):
    if not host:
        return False, 'no host'
    server = ldap3.Server(host, port, get_info=ldap3.ALL)
    conn = None
    auto_bind = False
    try:
        if user:
            user = 'baina\\%s'%user
            if password:
                auto_bind = True
        conn = ldap3.Connection(server, user=user, password=password, auto_bind=auto_bind, authentication=ldap3.NTLM)
        if not auto_bind:
            succ = conn.bind()
        else:
            succ = True
        msg = conn.result
        conn.unbind()
        return succ, msg
    except Exception as e:
        if conn:
            conn.unbind()
        return False, e

succ, msg = authorize(host='192.168.39.21', port=389, user='lichengbing')
print(succ, msg)
