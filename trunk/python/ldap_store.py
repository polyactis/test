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
		for name, value in self.config.options('ldap'):
			if name in LDAP_DIRECTORY_PARAMS:
				self._ldapcfg[name] = value

		# user entry local cache
		self._cache = {}
		# max time to live for a cache entry
		self._cache_ttl = int(self.config.get('ldap', 'cache_ttl', str(15*60)))
		# max cache entries
		self._cache_size = min(25, int(self.config.get('ldap', 'cache_size', '100')))

	def has_user(self, user):
		self.env.log.info("checking user: %s"%user)
		return user in self.get_users()

	def get_users(self):
		self._openldap()
		#2008-03-17 change objectclass=simpleSecurityObject to object=*
		ldap_users = self._ldap.get_dn(self._ldap.basedn, '(objectclass=*)')
		
		self.env.log.info("ldap_users: %s"%(ldap_users))
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
		"""
		2008-04-30 wrap "self._ldap._ds.sasl_interactive_bind_s(userdn, auth_tokens)==0:" up in try ... except ... . Except occurs when it's communicating with LDAP server with no support for sasl binding.
		"""
		userdn = self._get_userdn(user)
		if userdn is False:
			return False
		import ldap.sasl
		#2008-03-17 yh: try sasl binding first.
		auth_tokens = ldap.sasl.cram_md5(user, password)
		#2008-04-30 wrap it up in try ... except ... . Except occurs when it's communicating with LDAP server with no support for sasl binding.
		try:
			if self._ldap._ds.sasl_interactive_bind_s(userdn, auth_tokens)==0:
				return True
		except:
			import traceback, sys
			self.env.log.error('%s'%traceback.print_exc())
			self.env.log.error("%s"%repr(sys.exc_info()))
			#2008-04-30 reopen it because the above sasl_interactive_bind_s() probably breaks down the LDAP connection
			#not exactly sure. this line fixes the problem of getting no 'userPassword' below after this exception handling.
			self._ldap._open()
		
		password = password.encode('utf-8')
		p = self._ldap.get_attribute(userdn, 'userPassword')
		#self.env.log.info("p: %s"%(p))
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
		self._ldap._open()

	def _get_userdn(self, user):
		self._openldap()
		#2008-03-17 yh: change objectclass=simpleSecurityObject to object=*
		ldap_users = self._ldap.get_dn(self._ldap.basedn, '(objectclass=*)')
		for u in ldap_users:
			m = re.match('uid=([^,]+)', u)
			if m:
				if user == m.group(1):
					return u
		return False
