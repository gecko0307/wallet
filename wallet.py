# -*- coding: utf-8 -*-

import os
import sys
print(sys.stdout.encoding)
sys.path.append(os.getcwd())

import io
import threading

import bottle
from bottle import request
from bottle_sqlite import SQLitePlugin

from app.config import *
from app.routes import *

bottle.install(SQLitePlugin(dbfile = Config.databasePath))

def serverMain():
    bottle.run(host = '0.0.0.0', port = 8080)

serverThread = threading.Thread(target=serverMain)
serverThread.daemon = True
serverThread.start()

from cefpython3 import cefpython as cef
import platform
import sys

def cefMain():
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    browser = cef.CreateBrowserSync(url="http://localhost:8080/", window_title="Wallet")
    browser.SetClientHandler(LifespanHandler())
    cef.MessageLoop()
    cef.Shutdown()

class LifespanHandler(object):
    def OnBeforeClose(self, browser):
        print("shutdown")

cefMain()
