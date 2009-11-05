#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlalchemy
import entity
import pprint
from sqlalchemy.orm import sessionmaker
#from sqlalchemy import BoundMetaData, Column, Table, mapper

pp = pprint.PrettyPrinter(indent=4)

#print dir(sqlalchemy)

# conectarse a la bd
engine = sqlalchemy.create_engine("postgres://django:django@127.0.0.1:5432/mastergoal")
#metadata = sqlalchemy.MetaData("sqlite:///sqlite3.db")
metadata = sqlalchemy.MetaData(bind=engine)
metadata.reflect()

print metadata
print dir(metadata.metadata)

# open connection
Session = sqlalchemy.orm.sessionmaker(bind=engine) # ver como funciona esto para hacer un "entity maker"
session = Session()

# probar consultas
entities = {}
for table in metadata.sorted_tables:
    entities[table.name] = entity.EntityFactory(metadata.tables[table.name])
    sqlalchemy.orm.mapper(entities[table.name], metadata.tables[table.name])

x = session.query(entities['auth_user']).all()
pp.pprint(x)

for table in metadata.sorted_tables:
  if table.name != "auth_user":
    continue
  print table
  print table.name
  #print dir(table)
  #print "index: %s, foreign_keys: %s" % ("", table.columns.foreign_keys())
  for column in table.columns:
    print "  %s (%s) PK:%s U:%s FK:%s I:%s" % (column, column.name, column.primary_key, column.unique, column.foreign_keys, column.index)
    #for u in session.query(Entity).all():
      #print "    %s" % u
    #print dir(column)
  #print dir(table)


#print help(metadata.reflect)
#engine = sqlalchemy.create_engine("sqlite:///sqlite3.db", echo=True)
#engine = sqlalchemy.create_engine("postgres://django:django@localhost:5432/mastergoal", echo=True)
#session = sessionmaker(bind=engine)

#print dir(engine)
#print engine.table_names()



