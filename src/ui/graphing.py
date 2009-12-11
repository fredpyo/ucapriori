# -*- coding: utf-8 -*-
'''
Created on Dec 10, 2009

@author: fede
La idea de esto es manejar la graficación por separado... manejo de archivos temporales, etc.
'''
import os
import pydot
import tempfile
import wx

class Graphing(object):
    def __init__(self):
        self.graph = pydot.Dot('rt', graph_type='digraph')
        self.dir = tempfile.mkdtemp() 
    
    def graph_rules(self, rules):
        '''
        Grafica las reglas... usamos la misma clase que en kernel.clases
        '''
        for i in rules:
            node_izq = pydot.Node(i.como_cadena("izq", "\\n"), style="filled", fillcolor="#a7ff9f", color="#12df00", fontsize="10.0")
            node_der = pydot.Node(i.como_cadena("der", "\\n"), style="filled", fillcolor="#a7ff9f", color="#12df00", fontsize="10.0")
            self.graph.add_node(node_izq)
            self.graph.add_node(node_der)
            edge = pydot.Edge(node_izq, node_der, color="#669966", labelfontcolor="#669966", fontsize="8.0", label="Confianza=%d%%\\nSensibilidad=%d%%" % (i.confianza*100,i.sensibilidad*100))
            #edge = pydot.Edge(node_izq, node_der, color="#669966", labelfontcolor="#669966", fontsize="11.0", label="asdads")
            self.graph.add_edge(edge)
        self.graph.write_png(self.dir+'graph.png')
        
    def get_wx_image(self):
        '''
        Retorna una xw image
        '''
        return wx.Image(self.dir+'graph.png', wx.BITMAP_TYPE_ANY)
    
    def save(self, filename):
        '''Guardar en un archivo png'''
        return self.graph.write_png(filename)
    
    def __del__(self):
        '''Al destruir este objeto, eliminar el directorio temporal :D'''
        os.rmdir(self.dir)
