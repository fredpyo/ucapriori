# -*- coding: utf-8 -*-
'''
Created on Nov 7, 2009

@author: Federico Cáceres <fede.caceres@gmail.com>
'''

from sqlalchemy.sql import select
import os
import sys
import wx
import  wx.lib.filebrowsebutton as filebrowse
import wx.lib.delayedresult as delayedresult
import wx.lib.scrolledpanel as scrolledpanel

from data import SQLDataSource
from data.gridtables import PreviewTable, TransformationTable
from data.transformations import Transformer
from graphing import Graphing
from wxjikken.aerowizard import *


from kernel.xpermutations import *
from kernel.clases import *

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
        self.panels[0].fields['host'] = wx.TextCtrl(self.panels[0], -1, "127.0.01", size=(150, -1))
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
        self.content.Add(self.database_choice_book, 0, wx.EXPAND | wx.BOTTOM, 10)
    
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
        self.table_list.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListDoubleClick)

    def OnListSelection(self, event):
        data['selected']['table'] = event.GetClientData()
        
    def OnListDoubleClick(self, event):
        data['selected']['table'] = event.GetClientData()
        self.GoToNext()

    def OnShow(self, event):
        if event.GetShow():
            #tables = [t.table_name for t in data['source'].get_tables()]
            #self.table_list.Set(tables)
            self.table_list.Set([])
            tables = [t for t in data['source'].get_tables()]
            tables.sort(key=lambda x: x.name)
            for t in tables:
                self.table_list.Append(t.name, t)
            
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
        
        self.text_info = AeroStaticText(self, -1, u"...")
        self.content.Add(self.text_info, 0, wx.BOTTOM, 10)
        
        self.text_instructions = AeroStaticText(self, -1, u"Seleccione las columnas que desea procesar y las tranformaciones necesarias.")
        self.content.Add(self.text_instructions, 0, wx.BOTTOM, 10)
        
        h = wx.BoxSizer(wx.HORIZONTAL)
        self.content.Add(h, 0, wx.EXPAND | wx.BOTTOM, 10)
        
        self.column_list = wx.CheckListBox(self, -1, (-1, -1), (120,200), [])
        h.Add(self.column_list, 0, wx.EXPAND | wx.RIGHT, 10)

        hv = wx.BoxSizer(wx.VERTICAL)
        h.Add(hv, 1, wx.EXPAND, 0)

#        self.text_indique = AeroStaticText(self, -1, u"Indique las reglas de transformación que desea aplicar sobre esta columna.")
        self.text_indique = AeroStaticText(self, -1, u"Reglas de transformación para la columna `´")        
        hv.Add(self.text_indique, 0, wx.BOTTOM, 5)
#        self.text_info_adicional = AeroStaticText(self, -1, u"Información adicional: < ALGO VA A DECIR ACA... ALGUN DIA >")
#        hv.Add(self.text_info_adicional, 0, wx.BOTTOM, 5)
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
            self.text_info.SetLabel(u"Se encontraron %d registros en la tabla `%s´." % (column_count, data['selected']['table'].name))
            
            columns = [c.name for c in data['selected']['table'].columns]
            columns.sort()
            #self.column_list.SetSelection(0, False)
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
            
            self.text_indique.SetLabel(u"Reglas de transformación para la columna `%s´." % event.GetString())
            
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
            
            query = select([data['selected']['table']])
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
            

class Page_ConfigureApriori(AeroPage):
    '''Configura los parámetros para el algoritmo apriori'''
    def __init__(self, parent):
        AeroPage.__init__(self, parent, u"Parámetros del Apriori")

        text = AeroStaticText(self, -1, u"Configure el algoritmo con los siguientes parámetros (estos representan los requerimientos mínimos)")
        self.content.Add(text, 0, wx.BOTTOM, 10)
        
        grid = wx.FlexGridSizer(rows=3, cols=6, hgap=10, vgap=10)
        # soporte, confianza, sensibilidad
        blank = wx.StaticText(self, -1, u"")
        support = wx.StaticText(self, -1, u"Soporte Minimo:")
        self.support_min_spinner = wx.SpinCtrl(self, -1, "", min=0, max=100, initial=30)
        self.support_check = wx.CheckBox(self, -1, "")
        self.support_max_text = wx.StaticText(self, -1, u"Máximo:")
        self.support_max_spinner = wx.SpinCtrl(self, -1, "", min=0, max=100, initial=100)
        
        blank2 = wx.StaticText(self, -1, u"")
        trust = wx.StaticText(self, -1, u"Confianza Mínima:")
        self.trust_spinner = wx.SpinCtrl(self, -1, "", min=0, max=100, initial=40)
        blank3 = wx.StaticText(self, -1, u"")
        blank4 = wx.StaticText(self, -1, u"")
        blank5 = wx.StaticText(self, -1, u"")
        
        self.sensibility_check = wx.CheckBox(self, -1, "")
        self.sensibility_text = wx.StaticText(self, -1, u"Sensibilidad Mínima:")
        self.sensibility_spinner = wx.SpinCtrl(self, -1, "", min=0, max=100, initial=25)
        blank6 = wx.StaticText(self, -1, u"")
        blank7 = wx.StaticText(self, -1, u"")
        blank8 = wx.StaticText(self, -1, u"")

        for i in [blank, support, self.support_min_spinner, self.support_check, self.support_max_text, self.support_max_spinner, blank2, trust, self.trust_spinner, blank3, blank4, blank5, self.sensibility_check, self.sensibility_text, self.sensibility_spinner, blank6, blank7, blank8]:
            grid.Add(i)

        self.content.Add(grid, 0, wx.EXPAND | wx.BOTTOM, 10)
        
        self.Bind(wx.EVT_CHECKBOX, self.OnSensibilityCheckbox, self.sensibility_check)
        self.Bind(wx.EVT_CHECKBOX, self.OnSupportCheckbox, self.support_check)
        
    def OnShow(self, event):
        self.sensibility_text.Disable()
        self.sensibility_spinner.Disable()
        self.support_max_text.Disable()
        self.support_max_spinner.Disable()

    def OnSupportCheckbox(self, event):
        if event.IsChecked():
            self.support_max_text.Enable()
            self.support_max_spinner.Enable()
        else:
            self.support_max_text.Disable()
            self.support_max_spinner.Disable()
        
    def OnSensibilityCheckbox(self, event):
        if event.IsChecked():
            self.sensibility_text.Enable()
            self.sensibility_spinner.Enable()
        else:
            self.sensibility_text.Disable()
            self.sensibility_spinner.Disable()
            
    def OnNext(self):
        # copiar las configuraciones
        parameters = {}
        parameters['support_min'] = self.support_min_spinner.GetValue()/100.0
        parameters['support_max'] = self.support_max_spinner.GetValue()/100.0
        parameters['trust'] = self.trust_spinner.GetValue()/100.0
        parameters['sensibility'] = self.sensibility_spinner.GetValue()/100.0 if self.sensibility_check.IsChecked() else 0
        data['parameters'] = parameters
        print parameters
        return True


class RedirectText(object):
    '''
    Redireccionador de print :D
    Sacado de: http://www.blog.pythonlibrary.org/2009/01/01/wxpython-redirecting-stdout-stderr/
    '''
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl
 
    def write(self,string):
        # normal
        # self.out.WriteText(string)
        # thread-safe
        wx.CallAfter(self.out.WriteText, string)


class Page_ProcessData(AeroPage):
    '''Transforma los datos de la página anterior y los envia al algoritmo'''
    def __init__(self, parent):
        AeroPage.__init__(self, parent, u"Procesando datos")

        text = AeroStaticText(self, -1, u"Procesando... ¡sea paciente!")
        self.content.Add(text, 0, wx.BOTTOM, 10)
        
        self.gauge = wx.Gauge(self, -1, 50, size=(200,-1))
        self.content.Add(self.gauge, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.BOTTOM, 10)
        
        tabs = wx.Notebook(self, -1, size=(550, 300), style=wx.BK_DEFAULT)
        
        
        self.log = wx.TextCtrl(tabs, -1, "", size=(550, 250), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        tabs.AddPage(self.log, "Registro")
        
        spanel = scrolledpanel.ScrolledPanel(tabs, -1, size=(550, 250))
        spanel.SetBackgroundColour("#ffffff")
        self.graph_bitmap = wx.StaticBitmap(spanel, -1)
        tabs.AddPage(spanel, "Grafo de Reglas")
        
        self.content.Add(tabs, 0, wx.BOTTOM, 10)
        
        hs = wx.BoxSizer(wx.HORIZONTAL)
        self.log_save_button = wx.Button(self, -1, u"Guardar Log")
        hs.Add(self.log_save_button, 0, wx.RIGHT, 10)
        self.graph_save_button = wx.Button(self, -1, u"Guardar Grafo")
        hs.Add(self.graph_save_button, 0)
        self.content.Add(hs, 0, wx.ALIGN_RIGHT | wx.BOTTOM, 10)
        
        # gague timer
        self.Bind(wx.EVT_TIMER, self.TimerHandler)
        self.timer = wx.Timer(self)
        # threading
        self.abort_event = delayedresult.AbortEvent()
        
        # redirection
        self.redir=RedirectText(self.log)
        
        self.Bind(wx.EVT_BUTTON, self.OnSaveLog, self.log_save_button)
        self.Bind(wx.EVT_BUTTON, self.OnSaveGraph, self.graph_save_button)

    def TimerHandler(self, event):
        self.gauge.Pulse()

    def OnShow(self, event):
        if event.GetShow():
            self.log.Clear()
            sys.stdout=self.redir
            print "Iniciando..."
            self.abort_event.clear()
            self.worker = delayedresult.startWorker(self._Consumer, self._TransformWorker, wargs=(10,self.abort_event), jobID=10)
            self.timer.Start(50)
    
    def OnSaveLog(self, event):
        dlg = wx.FileDialog(self, "Guardar log...", wx.StandardPaths.Get().GetDocumentsDir(), style=wx.SAVE | wx.OVERWRITE_PROMPT, wildcard="Archivo de texto (*.txt)|*.txt|Todos los archivos (*.*)|*.*")
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            if not os.path.splitext(filename)[1]:
                filename = filename + ".txt"
            f = open(filename, "w")
            f.write(self.log.GetValue())
            f.close()
            
    def OnSaveGraph(self, event):
        dlg = wx.FileDialog(self, "Guardar grafo...", wx.StandardPaths.Get().GetDocumentsDir(), style=wx.SAVE | wx.OVERWRITE_PROMPT, wildcard=u"Imágen PNG (*.png)|*.png|Todos los archivos (*.*)|*.*")
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            if not os.path.splitext(filename)[1]:
                filename = filename + ".png"
            self.graph.save(filename)

    def _Consumer(self, delayedResult):
        '''Espera que se complete la transformación'''
        jobID = delayedResult.getJobID()
        try:
            success = delayedResult.get()
            width, height = self.graph_bitmap.GetSize()
            
            try:
                self.graph.save("grafo.png")
                self.graph_bitmap.SetBitmap(wx.BitmapFromImage(self.graph.get_wx_image()))
            except:
                wx.MessageBox(u"Error al generar el grafo.\nNo graphs for you!", u"Error de grafación", wx.OK | wx.ICON_ERROR, self)
        except Exception, exc:
            wx.MessageBox(u"Error:\n%s" % exc, u"Error", wx.OK | wx.ICON_ERROR, self)
            #print "Error thread: %d expection: %s" % (jobID, exc)
            success = False 
        if success:
            self.GoToNext()
            self.timer.Stop()
            self.gauge.SetValue(50)
            self.is_end = True
            self.wizard.UpdateButtons()
        else:
            self.GoToPrev()

    def _TransformWorker(self, jobID, abortEvent):
        data['transformed'] = {}
        conn = data['source'].engine.connect()
        for checked_column in data['selected']['columns']:
            rules = data['transformation_tables'][checked_column].GetRules()
            column = data['selected']['table'].columns[checked_column]
            values = [row[0] for row in conn.execute(select([column]))]
            transformer = Transformer(rules)
            data['transformed'][checked_column] = transformer.transform_values(values)
            
        print u"Transformación terminada..."
        print "----------"
        print u"Iniciando algoritmo Apriori...\n"
        prueba = Nucleo()
        # generar item sets
        prueba.minimumReq(data['transformed'],min=data['parameters']['support_min'],max=data['parameters']['support_max'])
        print "Sets generados:"
        for i in prueba.candidatos:
            print "%s :: Soporte=%.3f" % (i.valor ,i.porcentaje)
        print "----------"
        # generar reglas
        prueba.generarReglas(data['parameters']['trust'], data['parameters']['sensibility'])
        print "Reglas generadas:"
        for i in prueba.reglas:
            i.imprimir2()

        # generar el grafo de las reglas
        self.graph = Graphing()
        self.graph.graph_rules(prueba.reglas)
            
        return True
            
