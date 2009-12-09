from distutils.core import setup
import glob
import py2exe

import pkg_resources
pkg_resources.require("setuptools")

version = "1.0"

data_files = [("ui/img", ["ui/img/applications-engineering.ico", "ui/img/database.png", "ui/img/weka.png",])]

options = {
           "py2exe": {
                      "compressed": 1,
                      "optimize": 2,
                      "bundle_files": 2,
                      "dll_excludes": [
                                       "MSVCP90.dll", 
                                       ],
                      "includes" : [
                                    "data.entity",
                                    "data.gridtables",
                                    "data.transformations",
                                    "kernel.clases",
                                    "kernel.xpermutations",
                                    "ui.wizzardpages",
                                    "ui.wxjikken.aerowizard",
									
									"setuptools",
									"sqlalchemy",
                                    ],
                      "packages": ["sqlalchemy", "sqlalchemy.databases.sqlite"],
                      "dist_dir" : "../dist"
                      }
           }

manifest = """
<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<assembly xmlns='urn:schemas-microsoft-com:asm.v1' manifestVersion='1.0'>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level='asInvoker' uiAccess='false' />
      </requestedPrivileges>
    </security>
  </trustInfo>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity 
     type='win32' 
     name='Microsoft.VC90.CRT' 
     version='9.0.21022.8' 
     processorArchitecture='*' 
     publicKeyToken='1fc8b3b9a1e18e3b' />
    </dependentAssembly>
  </dependency>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity
         type="win32"
         name="Microsoft.Windows.Common-Controls"
         version="6.0.0.0"
         processorArchitecture="*"
         publicKeyToken="6595b64144ccf1df"
         language="*" />
    </dependentAssembly>
  </dependency>
</assembly>
"""

py_26_msdll = glob.glob(r"../dll/*.*")
data_files += [
               #("Microsoft.VC90.CRT", py_26_msdll),
               #("lib/Microsoft.VC90.CRT", py_26_msdll),
               ("", py_26_msdll),
               ]

setup(windows=[{
               'script':"apyori.py",
               'other_resources' : [(u"VERSIONTAG", 1, "APYORI " + version)],
               'icon_resources' : [(1, 'ui/img/applications-engineering.ico')],
               'other_resources' : [(24, 1, manifest)]
               }], 
        options=options,
        data_files = data_files,
        name = "aPyori",
        version=version
    )
		   
