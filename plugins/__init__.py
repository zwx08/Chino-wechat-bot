import os
import pkgutil
pkgpath = os.path.dirname(__file__)
pkgname = os.path.basename(pkgpath)

for _, file, _ in pkgutil.iter_modules([pkgpath]):
	abfile = os.path.join(pkgpath, file)
	__import__(pkgname+'.'+file)
#from action_sql import *
#ALL_plugin=[]
#rows=plugins.read()
#for row in rows:
#    if row["Enabled"] == True:
#        ALL_plugin.append(row["NAME"])
        

#__all__=ALL_plugin
#__all__=["ip"]