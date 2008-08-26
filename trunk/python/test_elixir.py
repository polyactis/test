#!/usr/bin/env python
"""

Examples:
	test_elixir.py  -u crocea
	
Description:
	2008-08-26
	Test to see how 2 elixir-databases co-exist in one program.
	
"""
import sys, os, math
#bit_number = math.log(sys.maxint)/math.log(2)
#if bit_number>40:       #64bit
sys.path.insert(0, os.path.expanduser('~/lib/python'))
sys.path.insert(0, os.path.join(os.path.expanduser('~/script')))


import getopt, csv, math
import Numeric, cPickle
from pymodule import PassingData, importNumericArray, write_data_matrix, SNPData
from variation.src import Stock_250kDB
import TestDB

class TestElixir(object):
	__doc__ = __doc__
	option_default_dict = {('drivername', 1,):['mysql', 'v', 1, 'which type of database? mysql or postgres', ],\
							('hostname', 1, ):['localhost', 'z', 1, 'hostname of the db server', ],\
							('database', 1, ):['stock_250k', 'd', 1, '',],\
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
		import pdb
		from pymodule import ProcessOptions
		ad = ProcessOptions.process_function_arguments(keywords, self.option_default_dict, error_doc=self.__doc__, class_to_have_attr=self)
		if self.debug:
			pdb.set_trace()
		print ad
		db1 = Stock_250kDB.Stock_250kDB(**ad)
		ad.update({'database': 'testdb'})
		db2 = TestDB.TestDB(**ad)
		db1.setup()
		db2.setup()	#2008-08-26 this line could be commented out. One call of setup_all() from elixir is enough to setup both databases.
		row = Stock_250kDB.README.query.filter_by(id=1).first()
		print row.title
		test_type = TestDB.TestType(type='any thing')
		db2.session.save(test_type)
		db2.session.flush()
		
if __name__ == '__main__':
	from pymodule import ProcessOptions
	main_class = TestElixir
	po = ProcessOptions(sys.argv, main_class.option_default_dict, error_doc=main_class.__doc__)
	print po.long_option2value
	instance = main_class(**po.long_option2value)
