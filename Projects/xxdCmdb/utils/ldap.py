# !/usr/bin/env python
# -*- coding:utf-8 -*-

import ldap3
from conf import ldap_acount


def authorize(host=ldap_acount.ldap_ip, port=ldap_acount.ldap_port, user=None, password=None):
    server = ldap3.Server(host, port, get_info=ldap3.ALL)
    conn = None
    auto_bind = True
    try:
        if user:
            users = 'baina\\%s'%user
        conn = ldap3.Connection(server, user=users, password=password, auto_bind=auto_bind, authentication=ldap3.NTLM)
        conn.search(ldap_acount.ldap_dn, '(&(sAMAccountName='+user+')(objectclass=person))',
                    attributes=['mail'])
        email = conn.entries[0]['mail']
        if not auto_bind:
            succ = conn.bind()
        else:
            succ = True
        msg = conn.result
        conn.unbind()
        return succ, msg, email
    except Exception as e:
        if conn:
            conn.unbind()
        return False, e