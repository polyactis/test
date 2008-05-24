#!/usr/bin/env python
"""
2008-04-27 Test SQLAlchemy

This doctest part is copied from http://www.sqlalchemy.org/docs/04/index.html. Some of them (sessionmaker and etc) doesn't work as expected due to version 0.3.10-1 installed on ubuntu at this moment.

For this tutorial we will use an in-memory-only SQLite database. This is an easy way to test things without needing to have an actual database defined anywhere. To connect we use create_engine():

>>> from sqlalchemy import create_engine
>>> engine = create_engine('sqlite:///:memory:', echo=True)

The echo flag is a shortcut to setting up SQLAlchemy logging, which is accomplished via Python's standard logging module. With it enabled, we'll see all the generated SQL produced. If you are working through this tutorial and want less output generated, set it to False. This tutorial will format the SQL behind a popup window so it doesn't get in our way; just click the "SQL" links to see whats being generated. 

We define our tables all within a catalog called MetaData, using the Table construct, which resembles regular SQL CREATE TABLE statements. We'll make two tables, one of which represents "users" in an application, and another which represents zero or more "email addreses" for each row in the "users" table:

>>> from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
>>> metadata = MetaData()
>>> users = Table('users', metadata,
...     Column('id', Integer, primary_key=True),
...     Column('name', String(40)),
...     Column('fullname', String(100)),
... )

>>> addresses = Table('addresses', metadata, 
...   Column('id', Integer, primary_key=True),
...   Column('user_id', None, ForeignKey('users.id')),
...   Column('email_address', String(50), nullable=False)
...  )

All about how to define Table objects, as well as how to create them from an existing database automatically, is described in Database Meta Data.

Next, to tell the MetaData we'd actually like to create our selection of tables for real inside the SQLite database, we use create_all(), passing it the engine instance which points to our database. This will check for the presence of each table first before creating, so it's safe to call multiple times:

>>> metadata.create_all(engine)

The first SQL expression we'll create is the Insert construct, which represents an INSERT statement. This is typically created relative to its target table:

>>> ins = users.insert()

To see a sample of the SQL this construct produces, use the str() function:

>>> str(ins)
'INSERT INTO users (id, name, fullname) VALUES (:id, :name, :fullname)'

Notice above that the INSERT statement names every column in the users table. This can be limited by using the values keyword, which establishes the VALUES clause of the INSERT explicitly:

>>> ins = users.insert(values={'name':'jack', 'fullname':'Jack Jones'})
>>> str(ins)
'INSERT INTO users (name, fullname) VALUES (:name, :fullname)'

Above, while the values keyword limited the VALUES clause to just two columns, the actual data we placed in values didn't get rendered into the string; instead we got named bind parameters. As it turns out, our data is stored within our Insert construct, but it typically only comes out when the statement is actually executed; since the data consists of literal values, SQLAlchemy automatically generates bind parameters for them. We can peek at this data for now by looking at the compiled form of the statement:

>>> ins.compile().get_params()
>>> dir(ins.compile())
>>> ins.compile().parameters
{'fullname': 'Jack Jones', 'name': 'jack'}

The interesting part of an Insert is executing it. In this tutorial, we will generally focus on the most explicit method of executing a SQL construct, and later touch upon some "shortcut" ways to do it. The engine object we created is a repository for database connections capable of issuing SQL to the database. To acquire a connection, we use the connect() method:

>>> conn = engine.connect()
>>> conn 
<sqlalchemy.engine.base.Connection object at 0x...>

The Connection object represents an actively checked out DBAPI connection resource. Lets feed it our Insert object and see what happens:

>>> result = conn.execute(ins)

INSERT INTO users (name, fullname) VALUES (?, ?)
['jack', 'Jack Jones']
COMMIT

So the INSERT statement was now issued to the database. Although we got positional "qmark" bind parameters instead of "named" bind parameters in the output. How come ? Because when executed, the Connection used the SQLite dialect to help generate the statement; when we use the str() function, the statement isn't aware of this dialect, and falls back onto a default which uses named parameters. We can view this manually as follows:

>>> ins.bind = engine
>>> str(ins)
'INSERT INTO users (name, fullname) VALUES (?, ?)'

What about the result variable we got when we called execute() ? As the SQLAlchemy Connection object references a DBAPI connection, the result, known as a ResultProxy object, is analogous to the DBAPI cursor object. In the case of an INSERT, we can get important information from it, such as the primary key values which were generated from our statement:

>>> result.last_inserted_ids()
[1]

The value of 1 was automatically generated by SQLite, but only because we did not specify the id column in our Insert statement; otherwise, our explicit value would have been used. In either case, SQLAlchemy always knows how to get at a newly generated primary key value, even though the method of generating them is different across different databases; each databases' Dialect knows the specific steps needed to determine the correct value (or values; note that last_inserted_ids() returns a list so that it supports composite primary keys). 


Next we want to tell SQLAlchemy about our tables. We will start with just a single table called users, which will store records for the end-users using our application (lets assume it's a website). We define our tables all within a catalog called MetaData, using the Table construct, which resembles regular SQL CREATE TABLE syntax:

>>> from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey    
>>> metadata = MetaData()
>>> users_table = Table('users', metadata,
...     Column('id', Integer, primary_key=True),
...     Column('name', String(40)),
...     Column('fullname', String(100)),
...     Column('password', String(15))
... )

All about how to define Table objects, as well as how to create them from an existing database automatically, is described in Database Meta Data.

Next, to tell the MetaData we'd actually like to create our users_table for real inside the SQLite database, we use create_all(), passing it the engine instance which points to our database. This will check for the presence of a table first before creating, so it's safe to call multiple times:

>>> metadata.create_all(engine) 

PRAGMA table_info("users")
{}
CREATE TABLE users (
id INTEGER NOT NULL,
name VARCHAR(40),
fullname VARCHAR(100),
password VARCHAR(15),
PRIMARY KEY (id)
)
{}
COMMIT

>>> class User(object):
...     def __init__(self, name, fullname, password):
...         self.name = name
...         self.fullname = fullname
...         self.password = password
...
...     def __repr__(self):
...        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

With our users_table and User class, we now want to map the two together. That's where the SQLAlchemy ORM package comes in. We'll use the mapper function to create a mapping between users_table and User:

>>> from sqlalchemy.orm import mapper
>>> mapper(User, users_table) 
<sqlalchemy.orm.mapper.Mapper object at 0x...>

The mapper() function creates a new Mapper object and stores it away for future reference. It also instruments the attributes on our User class, corresponding to the users_table table. The id, name, fullname, and password columns in our users_table are now instrumented upon our User class, meaning it will keep track of all changes to these attributes, and can save and load their values to/from the database. Lets create our first user, 'Ed Jones', and ensure that the object has all three of these attributes:

>>> ed_user = User('ed', 'Ed Jones', 'edspassword')
>>> ed_user.name
'ed'
>>> ed_user.password
'edspassword'
>>> str(ed_user.id)
'None'

which is configured by the sessionmaker() function. This function is configurational and need only be called once.

>>> from sqlalchemy.orm import sessionmaker
>>> from sqlalchemy import create_session
>>> Session = sessionmaker(bind=engine, autoflush=True, transactional=True)

In the case where your application does not yet have an Engine when you define your module-level objects, just set it up like this:

>>> Session = sessionmaker(autoflush=True, transactional=True)

Later, when you create your engine with create_engine(), connect it to the Session using configure():

>>> Session.configure(bind=engine)  # once engine is available

This Session class will create new Session objects which are bound to our database and have the transactional characteristics we've configured. Whenever you need to have a conversation with the database, you instantiate a Session:


The above Session is associated with our SQLite engine, but it hasn't opened any connections yet. When it's first used, it retrieves a connection from a pool of connections maintained by the engine, and holds onto it until we commit all changes and/or close the session object. Because we configured transactional=True, there's also a transaction in progress (one notable exception to this is MySQL, when you use its default table style of MyISAM). There's options available to modify this behavior but we'll go with this straightforward version to start.
back to section top
Saving Objects

So saving our User is as easy as issuing save():

>>> Session.save(ed_user)


"""
import os,sys

import sqlalchemy
eng = sqlalchemy.engine.create_engine('postgres://yh@localhost:5432/graphdb', strategy='threadlocal')

connection = eng.connect()
result = connection.execute("select * from go2ug")
i = 0
for row in result:
	i += 1
	if i == 10:
		break
	print row.go
	print row['go']
	print row[0]
	print row
	print dir(row)

"""
2008-04-28 below is copied from
http://www.rmunn.com/sqlalchemy-tutorial/tutorial.html
"""

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)

from sqlalchemy import create_session
session = create_session()

from sqlalchemy.orm.session import Session
session = Session(bind=eng)
"""
2008-05-24
	direct engine binding here.
	but it's not necessary. session seems to be able to figure out engine on its own. although it could be bad when the engine
	was changed, it still binds the old engine.

"""
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, clear_mappers
from sqlalchemy.orm import mapper, relation

metadata = MetaData()
articles = Table('articles', metadata,
	Column('article_id', Integer, primary_key = True),
	Column('headline', String(150)),
	Column('body', String),
)

keywords = Table('keywords', metadata,
	Column('keyword_id', Integer, primary_key = True),
	Column('keyword_name', String(50)),
)


association = Table('articles_keywords', metadata,
	Column('article_id', Integer, ForeignKey('articles.article_id')),
	Column('keyword_id', Integer, ForeignKey('keywords.keyword_id')),
)


metadata.bind = eng
#start a transaction. it can't roll back tables created by metadata. only metadata can drop them.
transaction = session.create_transaction()

metadata.create_all()

sys.path.insert(0, os.path.join(os.path.expanduser('~/script')))
from pymodule.db import TableClass

class Article(TableClass):
	def __init__(self, headline=None, body=None):
		self.headline = headline
		self.body = body
	
	def __repr__(self):
		return 'Article %d: "%s"' % (self.article_id, self.headline)

class Keyword(object):
	keyword_name = None
	def __init__(self, name=None):
		self.keyword_name = name
	def __repr__(self):
		return self.keyword_name

clear_mappers()

mapper(Article, articles, properties = {
    'keywords': relation(Keyword, secondary=association, backref='articles'),
})
mapper(Keyword, keywords)

a1 = Article(headline="Python is cool!")
a1.body="(to be written)"
a2 = Article(headline="SQLAlchemy Tutorial", body="You're reading it")
session.save(a1)
session.save(a2)
a3 = Article(headline='whatever 1')
session.save(a3)
a3 = Article(headline='whatever 2')
session.save(a3)
#session.flush()

print "check stuff in db before flush:"
#entries above wouldn't be found because session.flush() was commented out. Old stuff in db would be shown if it exists.
i = 0
row = session.query(Article).offset(i).limit(1).list()
while row:
	row = row[0]
	print row.headline
	print row.keywords
	i += 1
	row = session.query(Article).offset(i).limit(1).list()	#all() = list() returns a list of objects. first() returns the 1st object. one() woud raise error because 'Multiple rows returned for one()'


k_tutorial = Keyword('tutorial')
k_cool = Keyword('cool')
k_unfinished = Keyword('unfinished')

#2008-04-28 these lines are not necessary
#session.save(k_tutorial)
#session.save(k_cool)
#session.save(k_unfinished)
#session.flush()

a1.keywords.append(k_unfinished)
k_cool.articles.append(a1)
k_cool.articles.append(a2)
# Or:
k_cool.articles = [a1, a2]  # This works as well!
a2.keywords.append(k_tutorial)
#one flush will save all relevant unsaved objects into database

session.flush()
print "check stuff in db after flush:"
i = 0
row = session.query(Article).offset(i).limit(1).list()
while row:
	row = row[0]
	print row.headline
	print row.keywords
	i += 1
	row = session.query(Article).offset(i).limit(1).list()	#all() = list() returns a list of objects. first() returns the 1st object. one() woud raise error because 'Multiple rows returned for one()'

#"""
#2008-05-07
s = sqlalchemy.sql.select([Article.c.body, Article.c.headline])
#connection = eng.connect()
result = connection.execute(s)
print "Fetched from Article table before commit"
for row in result:
	print row
#"""

print dir(Article)
#rollback all table savings
yes_or_no = raw_input("Commit Database Transaction?(y/n):")
yes_or_no = yes_or_no.lower()
#default is rollback. so no need to take care 'n' or 'no'.
if yes_or_no=='y' or yes_or_no=='yes':
	transaction.commit()	#it will also execute session.flush() if it's not executed.
else:
	transaction.rollback()

aa = articles.alias()
s = sqlalchemy.sql.select([aa.c.body, aa.c.headline, association.c.article_id], aa.c.article_id==association.c.article_id, order_by=[association.c.article_id])
#connection = eng.connect()
result = connection.execute(s).fetchmany(3)
print "Fetched from Article table"
for row in result:
	print row.headline
	print row['headline']
	print row

#drop all tables created by this program
yes_or_no = raw_input("Drop All Relevant Tables?(y/n):")
yes_or_no = yes_or_no.lower()
#default is rollback. so no need to take care 'n' or 'no'.
if yes_or_no=='y' or yes_or_no=='yes':
	metadata.drop_all()
"""
print a1, a1.keywords
print a2, a2.keywords
print k_tutorial, k_tutorial.articles
print k_cool, k_cool.articles
print k_unfinished, k_unfinished.articles
"""
		

def _test():
	import doctest
	doctest.testmod()

if __name__ == "__main__":
	#_test()
	pass
