# -*- coding: utf-8 -*-

import os
import sys
print(sys.stdout.encoding)
sys.path.append(os.getcwd())

import io
import threading
import socket

import bottle
from bottle import request
from bottle_sqlite import SQLitePlugin

from app.config import *
from app.routes import *

bottle.install(SQLitePlugin(dbfile = Config.databasePath))

def randomPort():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port

def serverMain(port):
    bottle.run(host = "0.0.0.0", port = port)

port = randomPort()
serverThread = threading.Thread(target=serverMain, args=(port,))
serverThread.daemon = True
serverThread.start()

from cefpython3 import cefpython as cef
import platform
import sys

def cefMain(port):
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    url = "http://localhost:%s/" % port
    browser = cef.CreateBrowserSync(url = url, window_title = "Wallet")
    browser.SetClientHandler(LifespanHandler())
    cef.MessageLoop()
    cef.Shutdown()

class LifespanHandler(object):
    def OnBeforeClose(self, browser):
        print("shutdown")

cefMain(port)
