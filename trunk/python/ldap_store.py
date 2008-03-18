from trac.core import *
from trac.config import Option
import crypt, md5, sha, base64

from api import IPasswordStore

from ldapplugin.api import *

class LdapAuthStore(Component):
    implements(IPasswordStore)

    def __init__(self, ldap=None):
        # looks for groups only if LDAP support is enabled
        self.enabled = self.config.getbool('ldap', 'enable')
        if not self.enabled:
            return
        self.util = LdapUtil(self.config)
        # LDAP connection
        self._ldap = ldap
        # LDAP connection config
        self._ldapcfg = {}
        for name,value in self.config.options('ldap'):
            if name in LDAP_DIRECTORY_PARAMS:
                self._ldapcfg[name] = value
        # user entry local cache
        self._cache = {}
        # max time to live for a cache entry
        self._cache_ttl = int(self.config.get('ldap', 'cache_ttl', str(15*60)))
        # max cache entries
        self._cache_size = min(25, int(self.config.get('ldap', 'cache_size', '100')))

    def has_user(self, user):
        return user in self.get_users()

    def get_users(self):
        self._openldap()
        ldap_users = self._ldap.get_dn(self._ldap.basedn, '(objectclass=simpleSecurityObject)')
        users = []
        for user in ldap_users:
            m = re.match('uid=([^,]+)', user)
            if m:
                users.append(m.group(1))
        return users

    def set_password(self, user, password):
        user = user.encode('utf-8')
        password = password.encode('utf-8')
        md5_password = "{MD5}" + base64.encodestring(md5.new(password).digest()).rstrip()

        userdn = self._get_userdn(user)
        p = self._ldap.get_attribute(userdn, 'userPassword')

        self._ldap.add_attribute(userdn, 'userPassword', md5_password)
        self._ldap.delete_attribute(userdn, 'userPassword', p[0])

    def check_password(self, user, password):
        userdn = self._get_userdn(user)
        if userdn is False:
            return False

        password = password.encode('utf-8')
        p = self._ldap.get_attribute(userdn, 'userPassword')

        stored = p[0]
        m = re.match('^({[^}]+})', stored)
        if m:
            mech = m.group(0)
            if mech == '{MD5}':
                password = "{MD5}" + base64.encodestring(md5.new(password).digest()).rstrip()
            elif mech == '{CRYPT}':
                password = '{CRYPT}' + crypt.crypt(password, stored[7:9])

        return (stored == password)

    def _openldap(self):
        """Open a new connection to the LDAP directory"""
        if self._ldap is None: 
            bind = self.config.getbool('ldap', 'store_bind')
            self._ldap = LdapConnection(self.env.log, bind, **self._ldapcfg)

    def _get_userdn(self, user):
        self._openldap()

        ldap_users = self._ldap.get_dn(self._ldap.basedn, '(objectclass=simpleSecurityObject)')
        for u in ldap_users:
            m = re.match('uid=([^,]+)', u)
            if m:
                if user == m.group(1):
                    return u
        return False
