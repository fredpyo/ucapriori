# -*- coding: utf-8 -*-
'''
Created on Dec 11, 2009

@author: fede
'''
import sqlalchemy
import re


class Arff2Sqlite(object):
    '''
    Clase para convertir de un archivo de texto plano en formato arff a una base de datos
    SQLite utilizando sqlalchemy para la creación de la tabla y la inserción de datos
    '''
    def __init__(self, filename="test.arff"):
        '''
        Init
        '''
        self.name = ""
        self.attributes = {}
        self.ordered_attributes = []
        self.data = []
        self.error = False
        self.error_message = ""
        
        self.filename = filename
        
    def parse(self):
        '''
        Parsear el archivo arff y extraer sus definiciones y datos para almacenarlos en la clase
        '''
        # abrimos el archivo
        file = open(self.filename)
        
        # actualmente estamos parados en ningún lugar
        currently_at = "nowhere"
        
        # EXPRESIONES REGULARES
        # utilizaremos expresiones regulares para comprender las definiciones de los atributos
        # - primero detectamos el literal @ATTRIBUTE --> \\@ATTRIBUTE
        # - luego una serie de espacios con barra o tab --> [ |\t]*
        # - luego el nombre del atributo --> '?([ |a-z|A-Z|0-9]*)'? --> puede o no tener comilla simple :D
        # - luego otra serie de espacios --> [ |\t]*
        # - finalmente el tipo de atributo --> ((\\NUMERIC)|({.*})|(\\STRING))
        relre = re.compile("\\@ATTRIBUTE[ |\t]*(\\'[ |a-z|A-Z|0-9]*\\'|[a-z|A-Z|0-9]*)[ |\t]*(([\\NUMERIC|\\REAL])|({.*})|(\\STRING))",re.IGNORECASE)
        # variables que indican las posiciones de las cosas parseadas en la expresión regular
        ATTRIBUTE_NAME = 1
        TYPE_NUMERIC = 3
        TYPE_NOMINAL = 4
        TYPE_STRING = 5
        #TYPE_DATE = 6
        
        # recorrer todas las lines
        for line in file:
            # saltar filas vacias o de comentario
            if line.strip() == "" or line[0] == "#":
                continue
            
            # buscar la cabecera
            if currently_at == "nowhere":
                # encontramos la cabecera
                if line.lower().startswith("@relation "):
                    currently_at = "header"
                    self.name = line[10:]
            # cargar datos de la cabecera
            elif currently_at == "header":
                # encontramos la definición de un atributo, parsearlo con la expresión regular
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
                    # almacenamos el nombre del atributo y su tipo
                    self.attributes[matches.group(ATTRIBUTE_NAME).strip("'")] = type
                    # HACK y además guardamos en una lista ordenada
                    self.ordered_attributes.append(matches.group(ATTRIBUTE_NAME))
                # encontramos el salto al cuerpo del archivo
                elif line.lower().startswith("@data"):
                    currently_at = "body"
            # cargar datos
            elif currently_at == "body":
                self.data.append(line.strip().split(","))
    
    def to_sqlite(self, database=":memory:", verbose=False):
        '''
        Converir la representación interna del archivo arff parseado a sqlite
        '''
        # connect
        engine = sqlalchemy.create_engine("sqlite:///%s" % database, echo=verbose)
        metadata = sqlalchemy.MetaData(bind=engine)
        
        # creamos una tabla con el nombre extraido de la relación en el arff
        table = sqlalchemy.Table(self.name, metadata)
        # iteramos sobre los atributos (nombre y tipo)
        for name, type in self.attributes.iteritems():
            # y agregamos la columna a la tabla indicando nombre y tipo de la columna
            table.append_column(sqlalchemy.Column(name, self._get_column_type(type)))
        # hacemos un commit de esto, creando la tabla en la base de datos
        metadata.create_all(engine)
        
        # agregamos los datos
        # creamos una conexión a la bd
        conn = engine.connect()
        # recorremos todos los datos extraidos
        for row in self.data:
            # diccionario con los valores que insertaremos
            insert_this = {}
            # recorremos cada valor en el row por su subindice
            for i in range(len(row)):
                # HACK utilizamos self.ordered_attributes para saber cual es el nombre de este
                #      atributo y así definimos bien en insert_this que dato agregar a que
                #      columna
                insert_this[self.ordered_attributes[i]] = row[i]
            # ejecutamos, insertamos
            conn.execute(table.insert(insert_this))
        # terminado, cerramos la conexión
        conn.close()
            
        
    
    def _get_column_type(self, type):
        if type == "numeric":
            return sqlalchemy.Numeric
        elif type == "string":
            return sqlalchemy.String
        else:
            return sqlalchemy.String


if __name__ == "__main__":
    # utilizar el options parser para pasarle argumentos a la aplicación :D
    from optparse import OptionParser
    # configurar opciones y argumentos
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-i", "--input", dest="input",
                      help="read arff data from FILENAME")
    parser.add_option("-o", "--output", dest="output",
                      help="store into DATABASE file",
                      default=":memory:")
    parser.add_option("-v", "--verbose", dest="verbose",
                      help="print verbose messages",
                      action="store_true", default=False)
    
    # leer las opciones y argumentos parseados
    (options, args) = parser.parse_args()
    
    # actuar
    if options.input:
        converter = Arff2Sqlite(options.input)
        converter.parse()
        print converter.ordered_attributes
        converter.to_sqlite(options.output)
    else:
        print "Debe al menos especificar un archivo de entrada"
