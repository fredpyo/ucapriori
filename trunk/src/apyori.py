import wx
import wx.lib.delayedresult as delayedresult
import wx.lib.filebrowsebutton as filebrowse
import wx.lib.newevent

from ui.wxjikken.aerowizard import *

from ui import wizzardpages

import string

app = wx.PySimpleApp()
wizard = AeroWizard(u"aPyori")
# load pages
page1 = wizzardpages.Page_DataOrigin(wizard)
page_dbsel = wizzardpages.Page_DatabaseSelector(wizard)
# chain pages
page1.Chain({"database":page_dbsel})
# init and run wizard
wizard.start_page = page1
wizard.RunWizzard()

