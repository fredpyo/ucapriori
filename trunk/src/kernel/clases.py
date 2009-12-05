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
              print j
              for ind in popular:
                  if j == ind:
                     contador += 1
              print contador ,(len(popular)*float(min))
              if (contador > (len(popular)*float(min))):
                  self.candidatos.append(j)
              


    def generarReglas(self):
        
            #generar las todas las premutacios de caditatos de 2 logitud
        res = xcombinations(self.candidatos,2)
        for i in res:
            
    
            if len(set(i[0])&set(i[1])) == 0: #interseccion de izq y der
                nueva_regla = Regla
                nueva_regla.izq=i[0]
                nueva_regla.der=i[1]
                self.reglas.append(nueva_regla)


class Regla:
    '''
        es una clase para definir una regla del tipo ['x1','x2'] -----> ['x3','x4']
       
    '''
    
    izq=[]
    der=[]
    
    
    
    