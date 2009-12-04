# -*- coding: utf-8 -*-
'''
Clases que realizarán la transformación según un conjunto de reglas dadas

@author: Federico Cáceres <fede.caceres@gmail.com>
'''

class Transformer(object):
    '''
    Clase que transforma datos de una forma a otra
    '''
    def __init__(self, rules):
        '''
        Las reglas deben estar en el siguiente formato:
        [[condición, valor, valor], ...]
        donde
        - condición = '==' | '!=' | '<' | '<=' | '>' | '>='
        - valor = numero | "cadena"
        '''
        # validar las reglas
        if type(rules) != list and type(rules) != tuple:
            raise Exception(u'La lista de reglas no está bien formada, debe ser una lista o tupla')
        else:
            for rule in rules:
                if type(rule) != list and type(rule) != tuple:
                    raise Exception(u'Las reglas dentro de la lista deben ser listas o tuplas')
                elif len(rule) != 3:
                    raise Exception(u'Cada regla debe contener 3 elementos, esta tiene %d' % len(rule))
                elif rule[0] not in ['==', '!=', '<', '<=', '>', '>=']:
                    raise Exception(u"El primer elemento de la lista debe ser uno de los siguientes valures: '==' | '!=' | '<' | '<=' | '>' | '>='. Se encontró %s" % rule[0])
                elif type(rule[1]) not in [long, float, int, str, unicode]:
                    raise Exception(u"El tipo de dato de la segundo y tercera parte de la regla debe ser uno de los siguientes: long, float, int, string, unicode. Se encontraron %s, %s" % (str(type(rule[1])), str(type(rule[2]))))
        # todo ok :)
        self.rules = rules
    
    def transform_value(self, value):
        '''
        Convertir un valor según las reglas
        Este método itera sobre las reglas con las que se inicializó la clase
        Por cada regla, arma una cadena con los valores rule[0] y rule[1] de cada elemento de rules
        Supongamos que rules es así:
        [["==", 1, "NORMAL"], ["<", 1, "BAJO"], [">", 1, "ALTO"]]
        entonces armá cadenas así:
        "value == 1"
        "value < 1"
        "value > 1"
        Si alguna de esas condiciones se cumple, entonces se almacena el valor rule[2], se salta el resto de las reglas y se retorna este valor
        '''
        
        # al comenzar no tenemos un nuevo valor, o un valor que concuerde con las reglas
        new_value = None
        # iteramos sobre las reglas
        for rule in self.rules:
            # convierte la regla en una condición ejecutable, algo como:
            # value == 231
            # que es interpretado por eval y retorna True o False
            if eval("value %s %s" % (rule[0], rule[1])):
                new_value = rule[2] # asignamos el valor que debe ser
                break # salimos del ciclo de reglas porque ya no nos importa el resto
        # si encontramos un acierto en las reglas, retornamos el nuevo valor, o si no, el viejo
        if new_value != None:
            return new_value
        else:
            return value
    
    def transform_values(self, values):
        '''
        Convertir de a muchos, retorna una lista de valores
        Recorre todos los valores y aplica a cada valor la función convert_value de esta misma clase
        '''
        converted = []
        # iteramos sobre la lista
        for value in values:
            # y convertimos
            converted.append(self.transform_value(value))
        return converted 