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
        
        
    def minimumReq(self,variables=[],data=[],min=1):
        '''variables son la lista de variables = ['x1','x2','x3'....]
           data es toda la lista de la BD 
           min el el minimo de requerimiento 0...1 '''
        res=[]
        for i in range(1,len(varibles)+1):
            #generar las todas las combinaciones de varibldes de 1 a n logitud
            res.append(xuniqueCombinations(varibales,i))
            
            
            for i in res:
                for j in i:
                    #si pasa la prueba de minReq
                    #canditatos.append(j)
                    pass


    def generarReglas(self):
        res=[]
        
            #generar las todas las premutacios de caditatos de 2 logitud
        res = xcombinations(self.candidatos,2)
        for i in res:
            for item in i[0]:
                if item in i[1]:
                    break
                nueva_regla=Regla               #aqui sta mal preguntar a fede una solucion mas pythonica
                nueva_regla.izq=i[0]
                nueva_regla.der=i[1]
                self.reglas.append(nueva_regla)


class Regla:
    '''
        es una clase para definir una regla del tipo ['x1','x2'] -----> ['x3','x4']
       
    '''
    
    izq=[]
    der=[]
    
    
    
    