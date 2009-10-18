'''
Created on Oct 18, 2009

@author: sergio
'''

class Nucleo:
    '''
    classdocs
    '''


    def __init__(selfparams):
        '''
        Constructor
        '''
        
        
    def minimumReq(self,variables="",data=[],min=1):
        '''variables son la lista de variables = "ABCD"
           data es toda la lista de la BD 
           min el el minimo de requerimiento 0...1 '''
        res=[]
        for var in variables:
            for d in data:
                ''' recorrer los datos y contar '''
                count=0
                pass
            if  count/len(data) >= min:
                res.push(var)
        return res   