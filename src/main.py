# -*- coding:utf-8 -*-


import sys
from PyQt5 import QtWidgets
from src.ui.mainWindow import mainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = mainWindow()
    myshow.setCloseButton(True)
    myshow.setMinMaxButtons(True)
    myshow.show()
    sys.exit(app.exec_())

