from xpermutations import *
from clases import *


"""
var=['x1','x2','x3','x4']
p=[]
res=[]

for i in range(1,len(var)+1):
    p.append(xuniqueCombinations(var,i))
   # print i  

for i in p:
    for j in i:
        print j
        res.append(j)

       
p = xcombinations(res,2)
res=[]
print '---------------------------------------------------------------------------'        
for i in p:
    izq=set(i[0])
    der=set(i[1])
    
    if len(der&izq) == 0:
        res.append(i)
        

for i in res:
    print i
"""

datos = {"monto":('BAJO','ALTO','ALTO','ALTO','BAJO','BAJO','ALTO','ALTO',),"sexo":('F','M','F','M','F','M','F','F'),"genero":('gd','g','gd','g','g','g','g','g')}

prueba = Nucleo()

prueba.minimumReq(datos,min=0.20)
print "los que pasaron el min req"
for i in prueba.candidatos:
    print i.valor ,i.porcentaje
prueba.generarReglas()

print "las reglas"
for i in prueba.reglas:
    i.imprimir()