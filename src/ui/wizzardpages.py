# -*- coding: utf-8 -*-
'''
Created on Nov 7, 2009

@author: Federico Cáceres <fede.caceres@gmail.com>
'''

from sqlalchemy.sql import select
import wx
import  wx.lib.filebrowsebutton as filebrowse
import wx.lib.delayedresult as delayedresult


from data import SQLDataSource
from data.gridtables import PreviewTable, TransformationTable
from data.transformations import Transformer
from wxjikken.aerowizard import *


import pprint
pp = pprint.PrettyPrinter(indent=4)

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
        # gague timer
        self.Bind(wx.EVT_TIMER, self.TimerHandler)
        self.timer = wx.Timer(self)
        # threading
        self.abort_event = delayedresult.AbortEvent()

    def TimerHandler(self, event):
        self.gauge.Pulse()

    def OnNext(self):
        self.timer.Stop()
        return True
    
    def OnPrev(self):
        self.timer.Stop()
        return True

    def OnShow(self, event):
        if event.GetShow():
            self.abort_event.clear()
            self.worker = delayedresult.startWorker(self._Consumer, self._ConnectWorker, wargs=(10,self.abort_event), jobID=10)
            self.timer.Start(50)

    def _Consumer(self, delayedResult):
        jobID = delayedResult.getJobID()
        try:
            connect_success = delayedResult.get()
        except Exception, exc:
            wx.MessageBox(u"Error de conexión:\n%s" % exc, u"Error de Conexión", wx.OK | wx.ICON_ERROR, self)
            #print "Error thread: %d expection: %s" % (jobID, exc)
            connect_success = False 
        if connect_success:
            self.GoToNext()
        else:
            self.GoToPrev()

    def _ConnectWorker(self, jobID, abortEvent):
        data['source'] = SQLDataSource(data['sqlalchemy_string'], data['parameters'])
        data['source'].connect()
        print dir(data['source'])
        return True



class Page_TableSelector(AeroPage):
    '''
    Página donde el usuario selecciona de que tabla se seleccionaran los datos
    '''
    def __init__(self, parent):
        AeroPage.__init__(self, parent, u"Seleccione datos a procesar")
        
        text = AeroStaticText(self, -1, u"Seleccione una de las siguientes tablas")
        self.content.Add(text, 0, wx.BOTTOM, 10)
        
        self.table_list = wx.ListBox(self, -1, (0, 0), (400,200), [])
        self.content.Add(self.table_list, 0, wx.EXPAND | wx.BOTTOM, 10)
        
        self.table_list.Bind(wx.EVT_LISTBOX, self.OnListSelection)

    def OnListSelection(self, event):
        data['selected']['table'] = event.GetClientData()

    def OnShow(self, event):
        if event.GetShow():
            #tables = [t.table_name for t in data['source'].get_tables()]
            #self.table_list.Set(tables)
            self.table_list.Set([])
            for t in data['source'].get_tables():
                self.table_list.Append(t.__table__.name, t)
            
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
        
        self.text_instructions = AeroStaticText(self, -1, u"...")
        self.content.Add(self.text_instructions, 0, wx.BOTTOM, 10)
        
        h = wx.BoxSizer(wx.HORIZONTAL)
        self.content.Add(h, 0, wx.EXPAND | wx.BOTTOM, 10)
        
        self.column_list = wx.CheckListBox(self, -1, (-1, -1), (120,200), [])
        h.Add(self.column_list, 0, wx.EXPAND | wx.RIGHT, 10)

        hv = wx.BoxSizer(wx.VERTICAL)
        h.Add(hv, 1, wx.EXPAND, 0)

        self.text_indique = AeroStaticText(self, -1, u"Indique las reglas de transformación que desea aplicar sobre esta columna.")
        hv.Add(self.text_indique, 0, wx.BOTTOM, 5)
        self.text_info_adicional = AeroStaticText(self, -1, u"Información adicional: < ALGO VA A DECIR ACA... ALGUN DIA >")
        hv.Add(self.text_info_adicional, 0, wx.BOTTOM, 5)
        self.transformations_grid = wx.grid.Grid(self, -1, (-1, -1), (500, 300))
        hv.Add(self.transformations_grid, 0, wx.EXPAND)
        text = AeroStaticText(self, -1, u"NOTA: Si un valor no coincide con ninguna de las reglas, el mismo quedará igual.")
        hv.Add(text, 0, wx.TOP | wx.BOTTOM, 5)
        
        hvh = wx.BoxSizer(wx.HORIZONTAL)
        button_add = wx.Button(self, -1, "Agregar")
        button_remove = wx.Button(self, -1, "Quitar")
        self.button_preview = wx.ToggleButton(self, -1, "Previsualizar")
        hvh.Add(button_add, 0, 0)
        hvh.Add(button_remove, 0, 0)
        hvh.AddStretchSpacer(1)
        hvh.Add(self.button_preview, 0, wx.ALIGN_RIGHT, 0)
        hv.Add(hvh, 0, wx.EXPAND, 0)
        
        # clics en el lista
        self.Bind(wx.EVT_LISTBOX, self.OnSelect, self.column_list)
        # clics en los botones
        self.Bind(wx.EVT_BUTTON, self.OnAddRule, button_add)
        self.Bind(wx.EVT_BUTTON, self.OnRemoveRule, button_remove)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnTogglePreview, self.button_preview)

    def OnShow(self, event):
        if event.GetShow():
            
            column_count = data['source'].session.query(data['selected']['table']).count()
            self.text_instructions.SetLabel(u"Se encontraron %d registros en la tabla %s.\nSeleccione las columnas que desea procesar y las tranformaciones necesarias." % (column_count, data['selected']['table'].__table__.name))
            
            columns = [c.name for c in data['selected']['table'].__table__.columns]
            self.column_list.SetSelection(0, False)
            self.column_list.Set(columns)
            # inicializar tablas de transformación
            data['transformation_tables'] = {}
            for column in columns:
                data['transformation_tables'][column] = TransformationTable()
            
            dummy_data = TransformationTable()
            dummy_data.data = []
            self.transformations_grid.SetTable(dummy_data, True)
            self.transformations_grid.SetColSize(2, 200)
            self.wizard.LayoutFitCenter()
            self.dummy_panel = wx.Panel(self, -1, self.transformations_grid.GetPosition(), self.transformations_grid.GetSize())

            
    def OnSelect(self, event):
        if event.GetString():
            self.button_preview.SetValue(False)
            
            self.text_indique.SetLabel(u"Indique las reglas de transformación que desea aplicar sobre la columna <%s>." % event.GetString())
            
            self.transformations_grid.Show()
            self.dummy_panel.Hide()
            self.dummy_panel.Parent.Refresh()
            self.transformations_grid.SetTable(data['transformation_tables'][event.GetString()], False)
            self.transformations_grid.SetColSize(2, 200)
            self.transformations_grid.Refresh()
            
    def OnAddRule(self, event):
        self.transformations_grid.AppendRows(1)
        
    def OnRemoveRule(self, event):
        print "-------------"
        for row in self.transformations_grid.GetSelectedRows(): 
            self.transformations_grid.DeleteRows(row)
            
    def OnTogglePreview(self, event):
        if event.IsChecked():
            print "Change table"
            
            query = select([data['selected']['table'].__table__])
            conn = data['source'].engine.connect()
            
            
            rules = self.transformations_grid.GetTable().GetRules() 
            values = [row[self.column_list.GetStringSelection()] for row in conn.execute(query)]
            self.transformations_grid.SetTable(PreviewTable(rules, values), True)
            #self.transformations_grid.SetColSize(2, 200)
            self.transformations_grid.Refresh()
            
        else:
            
            self.transformations_grid.SetTable(data['transformation_tables'][self.column_list.GetStringSelection()], False)
            self.transformations_grid.SetColSize(2, 200)
            self.transformations_grid.Refresh()
    
    def OnNext(self):
        # prevenir saltar a la siguiente página si es que no hay nada seleccionado!
        if len(self.column_list.GetChecked()) < 2:
            return False
        # guardar las columnas seleccionadas
        data['selected']['columns'] = self.column_list.GetCheckedStrings()
        return True
            
            
class Page_TransformData(AeroPage):
    '''Transforma los datos de la página anterior y los envia al algoritmo'''
    def __init__(self, parent):
        AeroPage.__init__(self, parent, u"Transformado datos")

        text = AeroStaticText(self, -1, u"Transformando... ¡sea paciente!")
        self.content.Add(text, 0, wx.BOTTOM, 10)
        
        self.gauge = wx.Gauge(self, -1, 50)
        self.content.Add(self.gauge, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.BOTTOM, 10)
        # gague timer
        self.Bind(wx.EVT_TIMER, self.TimerHandler)
        self.timer = wx.Timer(self)
        # threading
        self.abort_event = delayedresult.AbortEvent()

    def TimerHandler(self, event):
        self.gauge.Pulse()

    def OnShow(self, event):
        if event.GetShow():
            self.abort_event.clear()
            self.worker = delayedresult.startWorker(self._Consumer, self._TransformWorker, wargs=(10,self.abort_event), jobID=10)
            self.timer.Start(50)

    def _Consumer(self, delayedResult):
        '''Espera que se complete la transformación'''
        jobID = delayedResult.getJobID()
        try:
            success = delayedResult.get()
        except Exception, exc:
            wx.MessageBox(u"Error de conexión:\n%s" % exc, u"Error de Conexión", wx.OK | wx.ICON_ERROR, self)
            #print "Error thread: %d expection: %s" % (jobID, exc)
            success = False 
        if success:
            self.GoToNext()
        else:
            self.GoToPrev()

    def _TransformWorker(self, jobID, abortEvent):
        data['transformed'] = {}
        conn = data['source'].engine.connect()
        for checked_column in data['selected']['columns']:
            rules = data['transformation_tables'][checked_column].GetRules()
            column = data['selected']['table'].__table__.columns[checked_column]
            values = [row[0] for row in conn.execute(select([column]))]
            transformer = Transformer(rules)
            data['transformed'][checked_column] = transformer.transform_values(values)
            
        pp.pprint(data['transformed'])
        return True
            
