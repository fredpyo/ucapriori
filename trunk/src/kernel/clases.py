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
        res=[]
        variables=[]
        popular=[]
        
        for i in datos:
          for j in set(datos[i]):  
                variables.append(j)
          
                      
        for i in range(1,len(variables)):
            #generar las todas las combinaciones de varibldes de 1 a n logitud
            res.append(xuniqueCombinations(variables,i))
            
        for i in datos:
            for j in datos[i]:
                
                popular.append([])
            break
       
        for i in datos:
            for x,y in zip(datos[i],popular):
                y.append(x)
       
        for i in res:
           for j in i:
              #si pasa la prueba de minReq
              contador = 0
             
              for ind in popular:
                  if set(j) <= set(ind):
                     contador += 1
             
              if (contador > (len(popular)*float(min))):
                  nuevo_candidato=Candidato(j,(float(contador)/float(len(popular))),contador)
                  
                  self.candidatos.append(nuevo_candidato)
              
        self.popular=popular

    def generarReglas(self):
        
            #generar las todas las premutacios de caditatos de 2 logitud
        candidatos=[] 
        for i in self.candidatos:
            candidatos.append(i.valor)
        res = xcombinations(candidatos,2)
        for i in res:
            
    
            if len(set(i[0])&set(i[1])) == 0: #interseccion de izq y der
                print i
                nueva_regla = Regla()
                nueva_regla.izq=i[0]
                nueva_regla.der=i[1]
                 
                for ind in self.popular:
                    if set(nueva_regla.izq)<=set(ind):
                        nueva_regla.contador_izq += 1
                        if set(nueva_regla.der)<=set(ind):
                            nueva_regla.contador_amb += 1
                nueva_regla.porcentaje = nueva_regla.contador_amb / float(nueva_regla.contador_izq)
                
                self.reglas.append(nueva_regla)

                
class Regla:
    '''
        es una clase para definir una regla del tipo ['x1','x2'] -----> ['x3','x4']
       
    '''
    
    izq=[]
    der=[]
    contador_izq=0
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