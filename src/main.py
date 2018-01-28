# -*- coding:utf-8 -*-


import sys
from PyQt5 import QtWidgets
from src.ui.mainWindow import mainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = mainWindow()
    myshow.show()
    sys.exit(app.exec_())

