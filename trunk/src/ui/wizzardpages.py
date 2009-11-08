# -*- coding: utf-8 -*-
'''
Created on Nov 7, 2009

@author: fede
'''

import  wx.lib.filebrowsebutton as filebrowse

from wxjikken.aerowizard import *

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

        
        # postgresql
        panel = wx.Panel(self)
        panel.SetBackgroundColour("#ffffff")
        panel.fields = {}
        # host, port, db, user, password
        panel.fields['host'] = wx.TextCtrl(panel, -1, "localhost", size=(150, -1))
        panel.fields['port'] = wx.TextCtrl(panel, -1, "5432", size=(75, -1))
        panel.fields['db'] = wx.TextCtrl(panel, -1, "", size=(220, -1))
        panel.fields['user'] = wx.TextCtrl(panel, -1, "", size=(220, -1))
        panel.fields['pass'] = wx.TextCtrl(panel, -1, "", size=(220, -1), style=wx.TE_PASSWORD)
        #layout
        vs = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vs)
        hs = wx.BoxSizer(wx.HORIZONTAL)
        hs.Add(wx.StaticText(panel, -1, "Host:"))
        hs.Add(panel.fields['host'], 0, wx.RIGHT, 5)
        hs.Add(wx.StaticText(panel, -1, "Puerto:"))
        hs.Add(panel.fields['port'], 0, wx.RIGHT, 5)
        vs.Add(hs, 0, wx.BOTTOM, 5)
        hs = wx.BoxSizer(wx.HORIZONTAL)
        hs.Add(wx.StaticText(panel, -1, "Base de Datos:"))
        hs.Add(panel.fields['db'])
        vs.Add(hs, 0, wx.BOTTOM, 5)
        hs = wx.BoxSizer(wx.HORIZONTAL)
        hs.Add(wx.StaticText(panel, -1, "Usuario:"))
        hs.Add(panel.fields['user'])
        vs.Add(hs, 0, wx.BOTTOM, 5)
        hs = wx.BoxSizer(wx.HORIZONTAL)
        hs.Add(wx.StaticText(panel, -1, u"Contraseña:"))
        hs.Add(panel.fields['pass'])
        vs.Add(hs, 0, wx.BOTTOM, 5)
        self.AddPage(panel, "PostgreSQL")
           
        # sqlite
        panel2 = wx.Panel(self)
        panel2.SetBackgroundColour("#ffffff")
        panel2.fields = {}
        # file
        panel2.fields['file'] = filebrowse.FileBrowseButton(panel2, -1, labelText= "Archivo:", buttonText="Seleccionar...", dialogTitle="Seleccione en archivo base de datos SQLite", fileMode = wx.OPEN, toolTip = u"Archivo de base de datos SQLite3 del cual se extraerán los datos.", startDirectory=wx.StandardPaths.Get().GetDocumentsDir(), fileMask="SQLite (*.db)|*.db|Todos|*.*")
        #layout
        vs = wx.BoxSizer(wx.VERTICAL)
        panel2.SetSizer(vs)
        
        vs.Add(panel2.fields['file'], 1, wx.EXPAND)
        self.AddPage(panel2, "SQLite3")         
        
        
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
        test = wx.Panel(self)
        database_choice_book = DatabaseChoiceBook(self, -1)
        self.content.Add(database_choice_book, 0, wx.EXPAND)
        
        #test.Layout() # distribute the window's new content
        #test.Fit() # fit the size of the wizard window
        #self.wizard.Center() # center :P
