# -*- coding: utf-8 -*-

class Entity(object):
    def __init__(self, **kw):
        '''automatic attribute mapping'''
        for k, v in kw.iteritems():
            setattr(self, k, v)
    
    def __repr__(self):
        '''Indicar para que tabla es entidad y que campos lo identifican'''
        return "<Entity %s %s>" % (self.table_name, " ".join(["=".join((x, str(getattr(self, x)))) for x in self.relevant_columns]))

def EntityFactory(table=None):
    '''Crear una nueva clase automágicamente'''
    e = type.__new__(type, str("Entity "+table.name), (Entity,), {})
    # almacenar la tabla a la que hace referencia
    e.table_name = table.name
    e._source_table = table
    # almacenar la lista de campos que son relevantes para esta entidad, como lo son los PK y campos UNIQUE
    e.relevant_columns = []
    for c in table.columns:
        if c.primary_key or c.unique:
            e.relevant_columns.append(c.name)
    return e