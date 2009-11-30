# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy.orm import sessionmaker

import entity


class SQLDataSource(object):
    def __init__(self, connection_string, parameters = None):
        self.connection_string = connection_string
        self.parameters = parameters
        
        self.engine = None
        self.metadata = None
        self.session = None
        self.entities = {}
       
        
    def connect(self):
        # conectar
        self.engine = sqlalchemy.create_engine(self.connection_string)
        self.metadata = sqlalchemy.MetaData(bind=self.engine)
        self.metadata.reflect()

        # iniciar "sesión"
        Session = sqlalchemy.orm.sessionmaker(bind=self.engine) # ver como funciona esto para hacer un "entity maker"
        self.session = Session()
        
        # registrar entidades usando el mapeador automático de entidades :D
        entities = {}
        for table in self.metadata.sorted_tables:
            if self.connection_string[0:6] == "sqlite" and table.name[0:6] == "sqlite":
                # saltar las tablas del sistema
                continue 
            # crear entidad nueva
            self.entities[table.name] = entity.EntityFactory(self.metadata.tables[table.name])
            # registrar al ORM
            sqlalchemy.orm.mapper(self.entities[table.name], self.metadata.tables[table.name])
           
        
    def get_tables(self):
        '''
        Retorna una lista de tablas
        '''
        return self.metadata.sorted_tables
        
        
        
        