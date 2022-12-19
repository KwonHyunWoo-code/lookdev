# -*- coding: utf-8 -*-

###----Document대뜑 댁뿉maya -> version -> script 대뜑ㅽ겕由쏀듃 뚯씪ㅼ쓣 蹂듭궗script 섏젙댁빞



import maya.cmds as cm
import pymel.core as pm
import os, sys
import maya.OpenMayaUI as omui
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

#from Ui_MainWindow import QtBuildUI

from lookdev import HDR_Browser
from lookdev import ColorChecker as Colc

def maya_main_window():
    """
    Retrun the Maya main window widget as a Python object
    :return:
    """
    main_window_ptr = omui.MQtUtil.mainWindow()

    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class BuildUI(QtWidgets.QDialog):

    def __init__(self, maya=False):
#        super(BuildUI, self).__init__()
        self.setupUi()
        self.maya = maya
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)
        self.populate()


        self.hb = HDR_Browser.Browser()

    def populate(self):
        path = r"E:\HDRI"
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(path))
        self.treeView.setSortingEnabled(True)


    def context_menu(self):
        menu = QtWidgets.QMenu()
        open = menu.addAction("Open in new maya")
        open.triggered.connect(self.open_file)

        if self.maya:
            open_file = menu.addAction("Open file")
            open_file.triggered.connect(lambda: self.maya_file_operations(open_file=True))

            import_to_maya = menu.addAction("Import to Maya")
            import_to_maya.triggered.connect(self.maya_file_operations)

            reference_to_maya = menu.addAction("Add reference to Maya")
            reference_to_maya.triggered.connect(lambda: self.maya_file_operations(reference=True))

        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def open_file(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        os.startfile(file_path)


    def maya_file_operations(self, reference=False, open_file=False):
        """
        open ,  reference,  Import
        :return:
        """
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)

        if reference:
            cm.file(file_path, reference=True, type='mayaAscii', groupReference=True)
        elif open_file:
            file_location = cm.file(query=True, location=True)
            if file_location == 'unknown':
                cm.file(file_path, open=True, force=True)
            else:
                modify_file = cm.file(query=True, modified=True)
                if modify_file:
                    result = cm.confirmDialog(title='Opening new maya file',
                                                message='This file is modified. do you want to save this file.?',
                                                button=['yes', 'no'],
                                                defaultButton='yes',
                                                cancelButton='no',
                                                dismissString='no')
                    if result == 'yes':
                        cm.file(save=True, type='mayaAscii')
                        cm.file(file_path, open=True, force=True)
                    else:
                        cm.file(file_path, open=True, force=True)
                else:
                    cm.file(file_path, open=True, force=True)
        else:
            cm.file(file_path, i=True, groupReference=True)



        ## 곸닔媛ㅼ젙 - 踰꾩쟾, 뚯씪쒕ぉ
        Version = "v001"
        Title = "HDR_Browser"

#         WinName = Title + Version
#         WinWidth = 1200
#
#         if cm.window(WinName, q=True, exists=True):
#             cm.deleteUI(WinName)
#
#         WinFrom = cm.window(WinName, t=Title, w=WinWidth, mxb=True, mnb=True, s=True, resizeToFitChildren=True)
#         getWinWidth = cm.window(WinFrom, q=True, width=True)
#         getWinHeight = cm.window(WinFrom, q=True, height=True)
#         WinSize = [getWinWidth, getWinHeight]
#
#         # --------------------------------------------------------------------------------------------------------------
#
#         # Layout
#
#         MainForm = cm.formLayout(vis=True, numberOfDivisions=100, width=WinSize[0])
#         MainRow = cm.rowColumnLayout(adjustableColumn=True, width=WinSize[0])
#
#         # RowWidthRate = [0.1, 0.2, 0.3, 0.2, 0.2]
#         cm.rowLayout(numberOfColumns=5)
#         cm.radioButtonGrp(label="ColorChecker", labelArray3=['Type1_Col', 'Type2_Ball', 'Type3_Col+Ball'],
#                             numberOfRadioButtons=3)
#         cm.button(label="Apply", command=self.colorCheckerApply)
#
#         pm.button(label="Create_Env_LT", command="")
#
#         cm.text(label="Current_HDRLight")
#         cm.textField(enable=False, backgroundColor=[0.05, 0.05, 0.05])
#         cm.setParent("..")
#         cm.separator(width=WinSize[0], height=15, style="double")
#
#         cm.paneLayout('MainPanaLO', w=WinSize[0], paneSize=[1, 20, 100], configuration='vertical2')
#
#         # pane1---------------------------------------------------------------------------------------
#
#         FolderListTab = cm.tabLayout('FolderListTabLO', innerMarginWidth=5, innerMarginHeight=5, childResizable=True)
#         FolderListColumn = cm.columnLayout(adjustableColumn=True)
#
# ###        """TODO: select item command"""
#         FolderList = cm.textScrollList(numberOfRows=8, allowMultiSelection=False, deselectAll=True,
#                                          append=self.hb.foundFolder_NameList, font="plainLabelFont", height=WinSize[1], parent=FolderListColumn, selectCommand="")
#
#         cm.setParent('..')
#         cm.setParent('..')
#
#         cm.tabLayout(FolderListTab, edit=True, tabLabel=(FolderListColumn, 'FolderList'))
#
#         # pane2---------------------------------------------------------------------------------------
#
#         ImageListTab = cm.tabLayout('ImageListTabLO', innerMarginWidth=5, innerMarginHeight=5, childResizable=True)
#         ImageListColumn = cm.columnLayout(adjustableColumn=True)
#         ImageList = cm.scrollLayout(verticalScrollBarThickness=16, height=WinSize[1])
#
#         cm.tabLayout(ImageListTab, edit=True, tabLabel=(ImageListColumn, 'ImageList'))
#         cm.rowColumnLayout(adjustableColumn=2, numberOfColumns=WinSize[1]/100)
#
#         self.setIconBttn()
#
#
#         cm.setParent('..')
#         cm.setParent(MainRow)
#
#         cm.text(" HDR_Browser ( ver. 1.0.0 )  by Hyunwoo_Kwon ", align="right")
#         cm.text(" Email - dhfpswl704@gmail.com ", align="right")
#
#         cm.showWindow(WinName)


    def colorCheckerApply(self, *args):

        print("a")


        # Colch = Colc.ColorCheckerRig()
        #
        # Colch.deleteAll()
        # Colch.ColorCheckerRig()

    def setIconBttn(self):
        """
        ImageListHDRI 대吏 щ━湲
        :return:
        """
        width = 200
        height = 100

        self.hb = HDR_Browser.Browser()

        fileNameList = self.hb.getFileNameList(self.hb.MiniFilePathList)
        conformFileNameList = []

        ### 諛섎났 잛닔
        cnt = 0

        for filename in fileNameList:
            if self.hb.compareFileExt(filename)==1:
                conformFileNameList.append(filename.split(".")[0])
            else:
                pass

        getFileData = dict(zip(conformFileNameList, self.hb.MiniFilePathList))
        #print(getFileData)

        for key, value in getFileData.items():
            cm.iconTextButton(style="iconAndTextVertical", label=key, scaleIcon=True,
                                image1=value, w=width, h=height, command="")

            cnt += 1

        return cnt

maya_main_window()


# if __name__ == '__main__':

#     if not QtWidgets.QApplication.instance():
#         app = QtWidgets.QApplication(sys.argv)
#     else:
#         app = QtWidgets.QApplication.instance()
#     ui = BuildUI()
#     ui.show()
#     app.exec_()
