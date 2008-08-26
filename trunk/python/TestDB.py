#!/usr/bin/env python
"""
Examples:
	#setup database in postgresql
	TestDB.py -u crocea -k genome
	
	#setup database in mysql
	TestDB.py -v mysql -u yh -z papaya -d genome -k ""
	
Description:
	2008-08-26
	a test database to be used by test_elixir.py to test how 2-elixir databases co-exist in one program.
"""
import sys, os, math
bit_number = math.log(sys.maxint)/math.log(2)
sys.path.insert(0, os.path.expanduser('~/lib/python'))
sys.path.insert(0, os.path.join(os.path.expanduser('~/script')))

from sqlalchemy.engine.url import URL
from elixir import Unicode, DateTime, String, Integer, UnicodeText, Text
from elixir import Entity, Field, using_options, using_table_options
from elixir import OneToMany, ManyToOne, ManyToMany, OneToOne
from elixir import setup_all, session, metadata, entities
from elixir.options import using_table_options_handler	#using_table_options() can only work inside Entity-inherited class.
from datetime import datetime

from sqlalchemy.schema import ThreadLocalMetaData
from sqlalchemy.orm import scoped_session, sessionmaker

from pymodule.db import ElixirDB

__session__ = scoped_session(sessionmaker(autoflush=False, transactional=False))
__metadata__ = ThreadLocalMetaData()

class TestType(Entity):
	type = Field(String(256), unique=True)
	created_by = Field(String(256))
	updated_by = Field(String(256))
	date_created = Field(DateTime, default=datetime.now)
	date_updated = Field(DateTime)
	using_options(tablename='test_type')
	using_table_options(mysql_engine='InnoDB')

class TestDB(ElixirDB):
	__doc__ = __doc__
	option_default_dict = {('drivername', 1,):['postgres', 'v', 1, 'which type of database? mysql or postgres', ],\
							('hostname', 1, ):['localhost', 'z', 1, 'hostname of the db server', ],\
							('database', 1, ):['graphdb', 'd', 1, '',],\
							('schema', 0, ): [None, 'k', 1, 'database schema name', ],\
							('username', 1, ):[None, 'u', 1, 'database username',],\
							('password', 1, ):[None, 'p', 1, 'database password', ],\
							('port', 0, ):[None, 'o', 1, 'database port number'],\
							('commit',0, int): [0, 'c', 0, 'commit db transaction'],\
							('debug', 0, int):[0, 'b', 0, 'toggle debug mode'],\
							('report', 0, int):[0, 'r', 0, 'toggle report, more verbose stdout/stderr.']}
	def __init__(self, **keywords):
		"""
		2008-08-26
		"""
		from pymodule import ProcessOptions
		ProcessOptions.process_function_arguments(keywords, self.option_default_dict, error_doc=self.__doc__, class_to_have_attr=self)
		if self.debug:
			import pdb
			pdb.set_trace()
		
		if getattr(self, 'schema', None):	#for postgres
			for entity in entities:
				if entity.__module__==self.__module__:	#entity in the same module
					using_table_options_handler(entity, schema=self.schema)
		
		__metadata__.bind = self._url
		self.metadata = __metadata__
		self.session = __session__
	
	def setup(self):
		setup_all(create_tables=True)	#create_tables=True causes setup_all to call elixir.create_all(), which in turn calls metadata.create_all()

if __name__ == '__main__':
	from pymodule import ProcessOptions
	main_class = TestDB
	po = ProcessOptions(sys.argv, main_class.option_default_dict, error_doc=main_class.__doc__)
	
	instance = main_class(**po.long_option2value)
	instance.setup()