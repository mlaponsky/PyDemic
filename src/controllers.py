import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QJSValue

class iceController(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.callback = []
