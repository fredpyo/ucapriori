# -*- coding: utf-8 -*-
'''
Created on Oct 18, 2009

@author: sergio
'''
from xpermutations import *


class Nucleo:
    '''
    classdocs
    '''
    candidatos=[] 
    reglas=[]
    popular=[]
    
    def __init__(selfparams):
        '''
        Constructor
        '''
        
        
    def minimumReq(self,datos={},min=1):
        '''variables son la lista de variables = ['x1','x2','x3'....]
           data es toda la lista de la BD 
           min el el minimo de requerimiento 0...1 '''
        # minimum Support
        res=[]
        variables=[]
        popular=[]

        # convierte el diccionario en lista
        for i in datos: # iterar sobre las etiquetas del diccionario 
          for j in set(datos[i]):  # itera sobre los elementos unicos de cada lista
                variables.append(j) # almacena las variables unicas en variables, las variables que entrarán en juego
          
        #generar las todas las combinaciones de variables de 1 a n logitud        
        for i in range(1,len(variables)):
            res.append(xuniqueCombinations(variables,i))
            
        # matriz "transversa" de los datos
        for i in datos: # iterar sobre las etiquetas del diccionario 
            for j in datos[i]: # itera sobre los elementos unicos de cada lista
                popular.append([])
            break
       
        # convertir de la notación de entrada que es por columnas a una notación por filas 
        for i in datos:
            for x,y in zip(datos[i],popular):
                y.append(x)

        # esto ya genera los sets que pasaron el minimum requirement 
        for i in res: # iterar sobre cada una de las combinaciones posibles
           for j in i: # iterar sobre cada elemento de la combinación, siempre son listas de longitud 1 a n 
              #si pasa la prueba de minReq
              contador = 0
             
              for ind in popular:
                  if set(j) <= set(ind): # Set1 <= Set2 es equivalente a Set1 "está incluido en" Set2 
                     contador += 1
             
              # minimo soporte
              if (contador > (len(popular)*float(min))): # len(popular) * float(min) == n * requerimiento_minimo, o sea, decir cuanto es 70% de n (por ejemplo) 
                  nuevo_candidato=Candidato(j,(float(contador)/float(len(popular))),contador)
                  self.candidatos.append(nuevo_candidato)

        # esto lo usamos luego
        self.popular=popular

    def generarReglas(self, trust=0, support=0):
        # minimun trust
        #generar las todas las premutacios de caditatos de 2 logitud
        
        # se convierte los candidatos a listas
        candidatos=[]  
        for i in self.candidatos:
            candidatos.append(i.valor)
        res = xcombinations(candidatos,2) # generar todas las combinaciones de 2 candidatos

        for i in res:
            if len(set(i[0])&set(i[1])) == 0: # interseccion de izq y der, tienen que ser disjuntos
                # print i
                # creamos la regla con el lado izquierdo y derecho
                nueva_regla = Regla()
                nueva_regla.izq=i[0]
                nueva_regla.der=i[1]
                
                # se recorre la matriz transpuesta y se calcula la validez de la reglas
                for ind in self.popular:
                    if set(nueva_regla.izq)<=set(ind): # esto vuelve a calcular las apariciones del set, (se podría optimizar)
                        nueva_regla.contador_izq += 1
                        if set(nueva_regla.der)<=set(ind):
                            nueva_regla.contador_amb += 1
                    if set(nueva_regla.der)<=set(ind):
                        nueva_regla.contador_der += 1
                nueva_regla.porcentaje = nueva_regla.contador_amb / float(nueva_regla.contador_izq)
                
                if nueva_regla.porcentaje > trust and nueva_regla.porcentaje > support: # minima confiaza and minimo soporte
                    self.reglas.append(nueva_regla)


                
class Regla:
    '''
        es una clase para definir una regla del tipo ['x1','x2'] -----> ['x3','x4']
       
    '''
    
    izq=[]
    der=[]
    contador_izq=0
    contador_der=0
    contador_amb=0
    porcentaje=0
    
    def imprimir(self):
        print self.izq, "-->", self.der
        print "contador", self.contador_amb, "////", self.contador_izq 
        print "% -> ", self.porcentaje


class Candidato:
    valor=[]
    porcentaje=0
    contador=0
   
    def __init__(self,valor,porcentaje,contador):
        self.valor=valor
        self.porcentaje=porcentaje
        self.contador = contador    