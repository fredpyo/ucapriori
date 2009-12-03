# -*- coding: utf-8 -*-
'''
Tablas que se utilizarán para el wx.grid.Grid en la página del wizard que permite seleccionar
que columnas se procesarán y las transformaciones que se realizarán sobre esta.

@author: Federico Cáceres <fede.caceres@gmail.com>
'''

import wx
import wx.grid

from transformations import Transformer 

class TransformationTable(wx.grid.PyGridTableBase):
    '''
    Tabla donde se almacenan las reglas de transformación a ser aplicadas a una columna
    Las columnas 1 y 2 almacenan la condición en que se disparará la condición
    La tercera el valor que tomará la columna
    '''
    def __init__(self):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = [
                     [u'==', u'1', u"categoría"],
        ]
        
        self.column_labels = [u"Condición", u"Valor", u"Mapea a valor"]
        self.column_datatypes = [wx.grid.GRID_VALUE_CHOICE + ':==,!=,<,<=,>,>=', wx.grid.GRID_VALUE_STRING, wx.grid.GRID_VALUE_STRING]
        
    def GetRules(self):
        '''Retornar las reglas contenidas en esta tabla'''
        return self.data
    
    # --------------------------------
    # the following are required by PyGridTableBase
    
    def GetNumberRows(self):
        return len(self.data)
    
    def GetNumberCols(self):
        return 3
    
    def IsEmptyCell(self, row, col):
        if row > len(self.data) - 1:
            return True
        else:
            return False
        
    def GetValue(self, row, col):
        value = self.data[row][col]
        return value
    
    def SetValue(self, row, col, value):
        self.data[row][col] = value
    
    # --------------------------------
    # optional (extra sexy) stuff
    
    def GetColLabelValue(self, col):
        return self.column_labels[col]
    
    def GetRowLabelValue(self, row):
        return "Regla %d" % (row + 1)
    
    def GetTypeName(self, row, col):
        return self.column_datatypes[col]
        
    # --------------------------------
    # behavioural stuff
    
    def AppendRows(self, numRows = 1):
        self.data.append(["","",""])
        msg = wx.grid.GridTableMessage(self, 
                                       wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, 
                                       1 
                                       )
        self.GetView().ProcessTableMessage(msg) 
        return True
        
    def DeleteRows(self, pos, numRows=1):
        self.data = self.data[0:pos] + self.data[pos+1:]
        msg = wx.grid.GridTableMessage(self, 
                                       wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,
                                       pos,
                                       numRows
                                       )
        self.GetView().ProcessTableMessage(msg) 
        return True


class PreviewTable(wx.grid.PyGridTableBase):
    '''
    Tabla para previsualizar los cambios que se realizarán sobre una columna.
    La primera columna representa los datos sin modificar y la segunda los datos transformados.
    '''
    def __init__(self, rules, values):
        wx.grid.PyGridTableBase.__init__(self)
        
        # crear transformador
        transformer = Transformer(rules)
        
        # cargar datos y transformarlos
        self.data = [[value, transformer.transform_value(value)] for value in values]
        
        self.column_labels = [u"Valor Original", u"Valor Transformado"]
        
    # --------------------------------
    # the following are required by PyGridTableBase
    
    def GetNumberRows(self):
        return len(self.data)
    
    def GetNumberCols(self):
        return 2
    
    def IsEmptyCell(self, row, col):
        if row > len(self.data) - 1:
            return True
        else:
            return False
        
    def GetValue(self, row, col):
        value = self.data[row][col]
        return value
    
    def SetValue(self, row, col, value):
        pass
    
    # --------------------------------
    # optional (extra sexy) stuff
    
    def GetColLabelValue(self, col):
        return self.column_labels[col]
    
    def GetRowLabelValue(self, row):
        return "%d" % (row + 1)
