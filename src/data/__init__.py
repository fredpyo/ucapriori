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
        self.tables = {}
       
        
    def connect(self):
        # conectar
        self.engine = sqlalchemy.create_engine(self.connection_string)
        self.metadata = sqlalchemy.MetaData(bind=self.engine)
        self.metadata.reflect()

        # iniciar "sesión"
        Session = sqlalchemy.orm.sessionmaker(bind=self.engine) # ver como funciona esto para hacer un "entity maker"
        self.session = Session()
        
        # agarrar todas las tablas que nos interesan
        # podriamos usar el diccionario self.metadata.tables directamente, pero queremos excluir algunas tablas primero :D
        for table in self.metadata.tables.itervalues():
            if self.connection_string[0:6] == "sqlite" and table.name[0:6] == "sqlite":
                # saltar las tablas del sistema
                continue 
            # almacenar la referencia a la tabla
            self.tables[table.name] = table
        
    def get_tables(self):
        '''
        Retorna una lista de tablas
        '''
        return self.tables.itervalues()
        #return self.metadata.sorted_tables
