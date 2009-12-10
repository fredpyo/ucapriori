# -*- coding: utf-8 -*-
'''
Created on Oct 18, 2009

@author: sergio
'''
import datetime

from xpermutations import *


class Nucleo:
    '''
    motor responsable de analizar un conjunto de datos y aplicar el algoritmo apriori
    para generar los items sets y consecuentemente las reglas que complan con los parametros
    support, trust y sensibility
    '''
    candidatos=[] 
    reglas=[]
    popular=[]
    
    def __init__(selfparams):
        '''
        Constructor
        '''
        
    def minimumReq(self,datos={},min=1, max=1, verbose=True):
        '''variables son la lista de variables = ['x1','x2','x3'....]
           data es toda la lista de la BD 
           min el el minimo de requerimiento 0...1 '''
        # minimum Support
        res=[]
        variables=[]
        popular=[]

        if verbose:
            print u"Generando item sets que complen con el soporte mínimo=%.3f" % min
            print
            print "Generando todos los item sets posibles..."
            start = datetime.datetime.now()

        # convierte el diccionario en lista
        for i in datos: # iterar sobre las etiquetas del diccionario 
          for j in set(datos[i]):  # itera sobre los elementos unicos de cada lista
                variables.append(j) # almacena las variables unicas en variables, las variables que entrarán en juego
          
        # generar las todas las combinaciones de variables de 1 a n logitud        
        for i in range(1,len(datos)):
            res.append(xuniqueCombinations(variables,i))
            
        if verbose:
            end = datetime.datetime.now()
            print "Items sets posibles generados en: ", end - start
            print ""

            print "Convirtiendo los datos a la representación interna optimizada..."
            start = datetime.datetime.now()

        # matriz "transversa" de los datos
        for i in datos: # iterar sobre las etiquetas del diccionario 
            for j in datos[i]: # itera sobre los elementos unicos de cada lista
                popular.append([])
            break
       
        # convertir de la notación de entrada que es por columnas a una notación por filas 
        for i in datos:
            for x,y in zip(datos[i],popular):
                y.append(x)
        
        if verbose:
            end = datetime.datetime.now()
            print "Datos convertidos a representación interna en: ", end - start
            print ""

            print "Recortando item sets que no cumplen el minimum requirement..."
            start = datetime.datetime.now()

        # esto ya genera los sets que pasaron el minimum requirement 
        for i in res: # iterar sobre cada una de las combinaciones posibles
           for j in i: # iterar sobre cada elemento de la combinación, siempre son listas de longitud 1 a n 
              #si pasa la prueba de minReq
              contador = 0
             
              for ind in popular:
                  if set(j) <= set(ind): # Set1 <= Set2 es equivalente a Set1 "está incluido en" Set2 
                     contador += 1
             
              # minimo soporte
              if ((len(popular)*float(min)) < contador <= (len(popular)*float(max))): # len(popular) * float(min) == n * requerimiento_minimo, o sea, decir cuanto es 70% de n (por ejemplo) 
                  nuevo_candidato=Candidato(j,(float(contador)/float(len(popular))),contador)
                  self.candidatos.append(nuevo_candidato)

        if verbose:
            end = datetime.datetime.now()
            print "%s cumplen con el minimun support, obtenidos en: " % len(self.candidatos), end - start
            print ""

        # esto lo usamos luego
        self.popular=popular

    def generarReglas(self, trust=0, sensibility=0, verbose=True):
        # minimun trust
        #generar las todas las premutacios de caditatos de 2 logitud
        res=[]
        if verbose:
            print "Obteniendo reglas que complan con la confianza=%.3f y sensibilidad=%.3f" % (trust, sensibility)
            print ""
            print "Generando todas las combinaciones de reglas posibles..."
            start = datetime.datetime.now()
        
        # se convierte los candidatos a listas
        candidatos=self.candidatos  
        print len(candidatos)
        #for i in self.candidatos:
        #    candidatos.append(i.valor)
       # res = xcombinations(candidatos,2) # generar todas las combinaciones de 2 candidatos

        if verbose:
            end = datetime.datetime.now()
            print "Todas las combinaciones posibles generadas en: ", end - start
            print ""

            print "Calculando confianza y soporte de reglas"
            start = datetime.datetime.now()
        """
                for i in res:
                    if len(set(i[0])&set(i[1])) == 0: # interseccion de izq y der, tienen que ser disjuntos
        """           
        for i in range(len(candidatos)):
            for j in candidatos[i+1:]:
                if len(set(candidatos[i].valor)&set(j.valor))==0:
                    #print candidatos[i],j.valor
                # creamos la regla con el lado izquierdo y derecho
                    nueva_regla1 = Regla()
                    nueva_regla2 = Regla()
                    
                    nueva_regla1.izq=candidatos[i].valor
                    nueva_regla1.contador_izq=candidatos[i].contador
                    nueva_regla2.izq=j.valor
                    nueva_regla2.contador_izq=j.contador
                    
                    nueva_regla1.der=j.valor
                    nueva_regla1.contador_der=j.contador
                    nueva_regla2.der=candidatos[i].valor
                    nueva_regla2.contador_der=candidatos[i].contador
                    
                    
                    mis_reglas=[]
                    mis_reglas.append(nueva_regla1)
                    mis_reglas.append(nueva_regla2)
                    
                    for nueva_regla in mis_reglas:
                        # se recorre la matriz transpuesta y se calcula la validez de la reglas
                        for ind in self.popular:
                            if set(nueva_regla.izq)<=set(ind) and  set(nueva_regla.der)<=set(ind) : # esto vuelve a calcular las apariciones del set, (se podría optimizar)
                                #nueva_regla.contador_izq += 1
                                nueva_regla.contador_amb += 1
                                #nueva_regla.contador_der += 1
                            #else:
                            #    if set(nueva_regla.der)<=set(ind):
                            #        nueva_regla.contador_der += 1
                            #    if set(nueva_regla.izq)<=set(ind):
                            #        nueva_regla.contador_izq += 1
                        nueva_regla.confianza = nueva_regla.contador_amb / float(nueva_regla.contador_izq)
                        nueva_regla.sensibilidad = nueva_regla.contador_amb / float(nueva_regla.contador_der)
                        
                        if nueva_regla.confianza > trust and nueva_regla.sensibilidad > sensibility: # minima confiaza and minima sensibilidad
                            self.reglas.append(nueva_regla)

        if verbose:
            end = datetime.datetime.now()
            print "%d reglas generadas en: " % len(self.reglas), end - start
            print ""

                
class Regla:
    '''
        es una clase para definir una regla del tipo ['x1','x2'] -----> ['x3','x4']
    '''
    izq=[]
    der=[]
    contador_izq=0
    contador_der=0
    contador_amb=0
    confianza=0
    sensibilidad=0
    
    def imprimir(self):
        print self.izq, "-->", self.der
        print "contador", self.contador_amb, "////", self.contador_izq 
        print "Confianza -> ", self.confianza
        print "Sensibilidad -> ", self.sensibilidad
    
    def imprimir2(self):
        #print "%s --> %s :: Confianza=%.3f, Sensibilidad=%.3f" % (str(self.izq), str(self.der), self.confianza, self.sensibilidad)
        print "{%s} --> {%s} :: Confianza=%.3f, Sensibilidad=%.3f" % (", ".join(self.izq), ", ".join(self.der), self.confianza, self.sensibilidad)
    
    def como_cadena(self, lado, separador = ", "):
        if lado == "izq":
            return separador.join(self.izq)
        else:
            return separador.join(self.der)


class Candidato:
    valor=[]
    porcentaje=0
    contador=0
   
    def __init__(self,valor,porcentaje,contador):
        self.valor=valor
        self.porcentaje=porcentaje
        self.contador = contador    