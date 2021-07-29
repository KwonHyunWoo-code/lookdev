import sys
from PySide2.QtWidgets import *

app = QApplication(sys.argv)
mainDialog = QDialog()
mainDialog.show()
app.exec_()