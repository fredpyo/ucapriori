import wx
import wx.lib.delayedresult as delayedresult
import wx.lib.filebrowsebutton as filebrowse
import wx.lib.newevent

from ui.wxjikken.aerowizard import *

from ui import wizzardpages

import string

app = wx.PySimpleApp(redirect = False)
wizard = AeroWizard(u"aPyori")

# load pages (database and default)
page1 = wizzardpages.Page_DataOrigin(wizard)
page_dbsel = wizzardpages.Page_DatabaseSelector(wizard)
page_connecting = wizzardpages.Page_Connecting(wizard)
page_tablesel = wizzardpages.Page_TableSelector(wizard)
page_colsel = wizzardpages.Page_ColumnSelector(wizard)
page_config = wizzardpages.Page_ConfigureApriori(wizard)
page_process = wizzardpages.Page_ProcessData(wizard)

# load pages (Arff)
page_arffsel = wizzardpages.Page_ArffSelector(wizard)
page_arffparsing = wizzardpages.Page_ArffParsing(wizard)

# chain pages
page1.Chain({"database":page_dbsel, "arff":page_arffsel})
page_dbsel.Chain({"database":page_connecting})
page_arffsel.Chain({"arff":page_arffparsing})
page_connecting.Chain({"database":page_tablesel})
page_arffparsing.Chain({"arff":page_colsel})
page_tablesel.Chain({"database":page_colsel})
page_colsel.Chain({"database":page_config, "arff":page_config})
page_config.Chain({"database":page_process, "arff":page_process})

# init and run wizard
wizard.start_page = page1
ib = wx.IconBundle()
ib.AddIconFromFile("ui/img/applications-engineering.ico", wx.BITMAP_TYPE_ANY)
wizard.SetIcons(ib)
wizard.RunWizzard()

