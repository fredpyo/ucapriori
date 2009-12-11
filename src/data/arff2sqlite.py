'''
Created on Dec 11, 2009

@author: fede
'''
import sqlalchemy
import re


class Arff2Sqlite(object):
    def __init__(self, filename="test.arff"):
        self.name = ""
        self.attributes = {}
        self.ordered_attributes = []
        self.data = []
        
        self.filename = filename
        
    def parse(self):
        file = open(self.filename)
        currently_at = "nowhere"
        # primero detectamos el literal @ATTRIBUTE --> \\@ATTRIBUTE
        # luego una serie de espacios con barra o tab --> [ |\t]*
        # luego el nombre del atributo --> ([a-z|A-Z|0-9]*)
        # luego otra serie de espacios --> [ |\t]*
        # finalmente el tipo de atributo --> ((\\NUMERIC)|({.*})|(\\STRING))
        relre = re.compile("\\@ATTRIBUTE[ |\t]*([a-z|A-Z|0-9]*)[ |\t]*((\\NUMERIC)|({.*})|(\\STRING))")
        ATTRIBUTE_NAME = 1
        TYPE_NUMERIC = 3
        TYPE_NOMINAL = 4
        TYPE_STRING = 5
        #TYPE_DATE = 6
        
        # recorrer todas las lines
        for line in file:
            # buscar la cabecera
            if currently_at == "nowhere":
                # encontramos la cabecera
                if line.lower().startswith("@relation "):
                    currently_at = "header"
                    self.name = line[10:]
            # cargar datos de la cabecera
            elif currently_at == "header":
                if line.lower().startswith("@attribute "):
                    matches = relre.match(line)
                    if matches.group(TYPE_NUMERIC):
                        type = "numeric"
                    elif matches.group(TYPE_NOMINAL):
                        type = "string"
                    elif matches.group(TYPE_STRING):
                        type = "string"
                    else:
                        type = "string"
                    self.attributes[matches.group(ATTRIBUTE_NAME)] = type
                    self.ordered_attributes.append(matches.group(ATTRIBUTE_NAME))
                elif line.lower().startswith("@data"):
                    currently_at = "body"
            # cargar datos
            elif currently_at == "body":
                self.data.append(line.strip().split(","))
    
    def to_sqlite(self, database=":memory:"):
        # connect
        engine = sqlalchemy.create_engine("sqlite:///%s" % database, echo=True)
        metadata = sqlalchemy.MetaData(bind=engine)
        
        # create table
        table = sqlalchemy.Table(self.name, metadata)
        for name, type in self.attributes.iteritems():
            table.append_column(sqlalchemy.Column(name, self._get_column_type(type)))
        metadata.create_all(engine)
        
        # add data
        conn = engine.connect()
        for row in self.data:
            insert_this = {}
            for i in range(len(row)):
                insert_this[self.ordered_attributes[i]] = row[i]
            conn.execute(table.insert(insert_this))
        conn.close()
            
        
    
    def _get_column_type(self, type):
        if type == "numeric":
            return sqlalchemy.Numeric
        elif type == "string":
            return sqlalchemy.String
        else:
            return sqlalchemy.String


if __name__ == "__main__":
    print "hello!"
    converter = Arff2Sqlite()
    converter.parse()
    print converter.name
    print converter.attributes
    print converter.data
    converter.to_sqlite("test.db")