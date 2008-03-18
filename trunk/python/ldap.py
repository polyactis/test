#!/usr/bin/env python
"""
#2008-03-17
	test ldap connection to localhost/dl324b-1 and papaya
"""
import ldap
ds = ldap.initialize('%s://%s/' %  ('ldap', '127.0.0.1'))
ds = ldap.initialize('%s://%s:%d/' %  ('ldap', '127.0.0.1', 389))
ds.search_s('ou=users,dc=dl324b-1,dc=cmb,dc=usc,dc=edu', ldap.SCOPE_ONELEVEL, 'uid=yh' , ['userPassword'])
ds.search_s('ou=users,dc=dl324b-1,dc=cmb,dc=usc,dc=edu', ldap.SCOPE_ONELEVEL, 'uid=yh' , ['loginShell', 'uidNumber', 'objectClass'])


bind_user='cn=admin,dc=dl324b-1,dc=cmb,dc=usc,dc=edu'
ds.simple_bind_s(bind_user, 'secret')
ds.search_s('ou=users,dc=dl324b-1,dc=cmb,dc=usc,dc=edu', ldap.SCOPE_ONELEVEL, 'uid=yh' , ['userPassword'])

password = 'secret'
import md5, base64
base64.encodestring(md5.new(password).digest()).rstrip()

ds.search_s('ou=users,dc=dl324b-1,dc=cmb,dc=usc,dc=edu', ldap.SCOPE_ONELEVEL, '(objectclass=simpleSecurityObject)' , ['dn'])

import ldap.sasl
ds = ldap.initialize('%s://%s:%d/' %  ('ldap', 'papaya.usc.edu', 389))
auth_tokens = ldap.sasl.cram_md5('diradmin', 'secret' )
ds.sasl_interactive_bind_s("uid=diradmin,cn=users,dc=papaya,dc=usc,dc=edu", auth_tokens )
ds.search_s('cn=users,dc=papaya,dc=usc,dc=edu', ldap.SCOPE_ONELEVEL, '(objectclass=*)' , ['userPassword'])
#return things like {'userPassword': ['********']}). can't be used to test password matching or not.

ds.search_s('cn=users,dc=papaya,dc=usc,dc=edu', ldap.SCOPE_ONELEVEL, '(objectclass=*)' , ['dn'])
ds.search_s('dc=papaya,dc=usc,dc=edu', ldap.SCOPE_SUBTREE, '(objectclass=*)' , ['dn'])