import sys
from PySide2 import QtWidgets
from BuildUI import UI

if __name__ == '__main__':

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()

    mainDialog = BuildUI()
    mainDialog.show()
    app.exec_()