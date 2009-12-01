# -*- coding: utf-8 -*-
'''
Created on Nov 7, 2009

@author: fede
'''

import  wx.lib.filebrowsebutton as filebrowse

from wxjikken.aerowizard import *
from data import SQLDataSource

data = {'selected':{'table':None, 'columns':None}}

class Page_DataOrigin(AeroPage):
    '''
    Página para seleccionar origen de datos
    '''
    def __init__(self, parent):
        AeroPage.__init__(self, parent, u"Seleccione el origen de datos")
        
        text = AeroStaticText(self, -1, u"Indique de donde desea obtener los datos para aplicar el algoritmo.")
        self.content.Add(text)

        s = wx.BoxSizer(wx.HORIZONTAL)

        #bmp = writeCaption("WEKA FILE jgh jfg jg", wx.EmptyBitmap(100,48), wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False, "Segoe UI"), (10,10), "#ffffff")
        b = wx.BitmapButton(self, -1, wx.Bitmap("ui/img/weka.png", wx.BITMAP_TYPE_PNG))
        self.Bind(wx.EVT_BUTTON, self.OnButtonWeka, b)
        s.Add(b)
        
        s.AddSpacer(20)

        b = wx.BitmapButton(self, -1, wx.Bitmap("ui/img/database.png", wx.BITMAP_TYPE_PNG))
        self.Bind(wx.EVT_BUTTON, self.OnButtonDatabase, b)
        s.Add(b)
        
        self.content.Add(s, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
    def OnButtonDatabase(self, event):
        self.wizard.route = 'database'
        self.GoToNext()
    
    def OnButtonWeka(self, event):
        self.wizard.route = 'weka'
        self.GoToNext()
        
    def GetNext(self):
        return None
    
class DatabaseChoiceBook(wx.Choicebook):
    def __init__(self, parent, id):
        wx.Choicebook.__init__(self, parent, id, size=(-1, 500))

        self.panels = []
        # postgresql
        self.panels.append(wx.Panel(self))
        self.panels[0].SetBackgroundColour("#ffffff")
        self.panels[0].fields = {}
        # host, port, db, user, password
        self.panels[0].fields['host'] = wx.TextCtrl(self.panels[0], -1, "localhost", size=(150, -1))
        self.panels[0].fields['port'] = wx.TextCtrl(self.panels[0], -1, "5432", size=(75, -1))
        self.panels[0].fields['db'] = wx.TextCtrl(self.panels[0], -1, "", size=(220, -1))
        self.panels[0].fields['user'] = wx.TextCtrl(self.panels[0], -1, "", size=(220, -1))
        self.panels[0].fields['pass'] = wx.TextCtrl(self.panels[0], -1, "", size=(220, -1), style=wx.TE_PASSWORD)
        #layout
        vs = wx.BoxSizer(wx.VERTICAL)
        self.panels[0].SetSizer(vs)
        hs = wx.BoxSizer(wx.HORIZONTAL)
        hs.Add(wx.StaticText(self.panels[0], -1, "Host:"))
        hs.Add(self.panels[0].fields['host'], 0, wx.RIGHT, 5)
        hs.Add(wx.StaticText(self.panels[0], -1, "Puerto:"))
        hs.Add(self.panels[0].fields['port'], 0, wx.RIGHT, 5)
        vs.Add(hs, 0, wx.BOTTOM, 5)
        hs = wx.BoxSizer(wx.HORIZONTAL)
        hs.Add(wx.StaticText(self.panels[0], -1, "Base de Datos:"))
        hs.Add(self.panels[0].fields['db'])
        vs.Add(hs, 0, wx.BOTTOM, 5)
        hs = wx.BoxSizer(wx.HORIZONTAL)
        hs.Add(wx.StaticText(self.panels[0], -1, "Usuario:"))
        hs.Add(self.panels[0].fields['user'])
        vs.Add(hs, 0, wx.BOTTOM, 5)
        hs = wx.BoxSizer(wx.HORIZONTAL)
        hs.Add(wx.StaticText(self.panels[0], -1, u"Contraseña:"))
        hs.Add(self.panels[0].fields['pass'])
        vs.Add(hs, 0, wx.BOTTOM, 5)
        self.AddPage(self.panels[0], "PostgreSQL")
           
        # sqlite
        self.panels.append(wx.Panel(self))
        self.panels[1].SetBackgroundColour("#ffffff")
        self.panels[1].fields = {}
        # file
        self.panels[1].fields['db'] = filebrowse.FileBrowseButton(self.panels[1], -1, labelText= "Archivo:", buttonText="Seleccionar...", dialogTitle="Seleccione en archivo base de datos SQLite", fileMode = wx.OPEN, toolTip = u"Archivo de base de datos SQLite3 del cual se extraerán los datos.", startDirectory=wx.StandardPaths.Get().GetDocumentsDir(), fileMask="SQLite (*.db)|*.db|Todos|*.*")
        #layout
        vs = wx.BoxSizer(wx.VERTICAL)
        self.panels[1].SetSizer(vs)
        
        vs.Add(self.panels[1].fields['db'], 1, wx.EXPAND)
        self.AddPage(self.panels[1], "SQLite3")         

        self.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGING, self.OnPageChanging)

    def OnPageChanged(self, event):
        sel = self.GetSelection()
        event.Skip()

    def OnPageChanging(self, event):
        sel = self.GetSelection()
        event.Skip()
        
    def GetValues(self):
        '''
        Retorna los valores relevantes del choice book dependiendo de la selección actual.
        BONUS: Ya retorna un string formateado para sqlalchemy.
        '''
        sel = self.GetSelection()
        val = {}
        if sel == 0:
            val['name'] = 'postgres'
        else:
            val['name'] = 'sqlite'
        val['parameters'] = {}
        for k,v in self.panels[sel].fields.iteritems():
            val['parameters'].setdefault(k,v.GetValue())
        
        if val['name'] == 'sqlite':
            val['sqlalchemy_string'] = "sqlite:///%s" % val['parameters']['db']
        else:
            val['sqlalchemy_string'] = "%s://%s:%s@%s:%s/%s" % (val['name'], val['parameters']['user'], val['parameters']['pass'], val['parameters']['host'], val['parameters']['port'], val['parameters']['db'])
        return val
        
        
class Page_DatabaseSelector(AeroPage):
    '''
    Página para seleccionar el tipo de base de datos y sus parámetros
    '''
    def __init__(self, parent):
        AeroPage.__init__(self, parent, u"Conectarse a base de datos")
        
        basesdedatos = ['sqlite', 'postgresql']
        
        text = AeroStaticText(self, -1, u"Seleccione el tipo de base de datos a la que se conectará\ny los parámetros necesarios para la conexión.")
        self.content.Add(text, 0, wx.BOTTOM, 10)
        
        """
        self.combo_db = wx.ComboBox(self, -1, "seleccione...", (15, 30), wx.DefaultSize, basesdedatos, wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.content.Add(self.combo_db, 0, wx.ALL, 10)
        """
        self.database_choice_book = DatabaseChoiceBook(self, -1)
        self.content.Add(self.database_choice_book, 0, wx.EXPAND)
        
        b = wx.BitmapButton(self, -1, wx.Bitmap("ui/img/database.png", wx.BITMAP_TYPE_PNG))
        self.Bind(wx.EVT_BUTTON, self.Test, b)
        self.content.Add(b)

        #test.Layout() # distribute the window's new content
        #test.Fit() # fit the size of the wizard window
        #self.wizard.Center() # center :P
    
    def OnNext(self):
        print data
        data.update(self.database_choice_book.GetValues())
        print data
        return True
    
    def Test(self, event):
        print self.database_choice_book.GetValues()
        
        
class Page_Connecting(AeroPage):
    '''
    Página intermedia para la conexión a la base de datos...
    '''
    def __init__(self, parent):
        AeroPage.__init__(self, parent, u"Conectando a base de datos")
        
        text = AeroStaticText(self, -1, u"Intendando abrir una conexión con la base de datos %s" % "xxxxxxxxxx")
        self.content.Add(text, 0, wx.BOTTOM, 10)
        
        self.gauge = wx.Gauge(self, -1, 50)
        self.content.Add(self.gauge, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.BOTTOM, 10)

    def OnShow(self, event):
        if event.GetShow():
            data['source'] = SQLDataSource(data['sqlalchemy_string'], data['parameters'])
            data['source'].connect()


class Page_TableSelector(AeroPage):
    '''
    Página donde el usuario selecciona de que tabla se seleccionaran los datos
    '''
    def __init__(self, parent):
        AeroPage.__init__(self, parent, u"Seleccione datos a procesar")
        
        text = AeroStaticText(self, -1, u"Seleccione una de las siguientes tablas")
        self.content.Add(text, 0, wx.BOTTOM, 10)
        
        self.table_list = wx.ListBox(self, -1, (-1, -1), (400,200), [])
        self.content.Add(self.table_list, 0, wx.EXPAND | wx.ALL, 10)
        
        self.table_list.Bind(wx.EVT_LISTBOX, self.OnListSelection)

    def OnListSelection(self, event):
        data['selected']['table'] = event.GetClientData()

    def OnShow(self, event):
        if event.GetShow():
            #tables = [t.table_name for t in data['source'].get_tables()]
            #self.table_list.Set(tables)
            self.table_list.Set([])
            for t in data['source'].get_tables():
                self.table_list.Append(t.table_name, t)
            
    def OnNext(self):
        return data['selected']['table'] != None

    def OnPrev(self):
        data['selected']['table'] = None
            
class Page_ColumnSelector(AeroPage):
    '''
    Página donde el usuario selecciona de que columnas de la tabla seleccionada se quitarna los datos
    '''
    def __init__(self, parent):
        AeroPage.__init__(self, parent, u"Seleccione datos a procesar")
        
        text = AeroStaticText(self, -1, u"Seleccione una de las siguientes tablas")
        self.content.Add(text, 0, wx.BOTTOM, 10)
        
        self.column_list = wx.CheckListBox(self, -1, (-1, -1), (400,200), [])
        self.content.Add(self.column_list, 0, wx.EXPAND | wx.ALL, 10)
        
    def OnShow(self, event):
        if event.GetShow():
            print data['selected']['table']
            print dir(data['selected']['table'])
            columns = [c.name for c in data['selected']['table']._source_table.columns]
            self.column_list.Set(columns)