import maya.cmds as cm
import pymel.core as pm
import os, sys
#import HDR_Browser as hb

class UI:
    def __init__(self):

        ## 상수값 설정 - 버전, 파일제목
        Version = "v001"
        Title = "HDR_Browser"

        WinName = Title + Version
        WinWidth = 1200

        if cm.window(WinName, q=True, exists=True):
            cm.deleteUI(WinName)

        WinFrom = cm.window(WinName, t=Title, w=WinWidth, mxb=True, mnb=True, s=True, resizeToFitChildren=True)
        getWinWidth = cm.window(WinFrom, q=True, width=True)
        getWinHeight = cm.window(WinFrom, q=True, height=True)
        WinSize = [getWinWidth, getWinHeight]

        # --------------------------------------------------------------------------------------------------------------

        # Layout

        MainForm = cm.formLayout(vis=True, numberOfDivisions=100, width=WinSize[0])
        MainRow = cm.rowColumnLayout(adjustableColumn=True, width=WinSize[0])

        # RowWidthRate = [0.1, 0.2, 0.3, 0.2, 0.2]
        cm.rowLayout(numberOfColumns=5)
        cm.radioButtonGrp(label="ColorChecker", labelArray3=['Type1_Col', 'Type2_Ball', 'Type3_Col+Ball'],
                            numberOfRadioButtons=3)
        cm.button(label="Apply", command="")

        pm.button(label="Create_Env_LT", command="")

        cm.text(label="Current_HDRLight")
        cm.textField(enable=False, backgroundColor=[0.05, 0.05, 0.05])
        cm.setParent("..")
        cm.separator(width=WinSize[0], height=15, style="double")

        cm.paneLayout('MainPanaLO', w=WinSize[0], paneSize=[1, 20, 100], configuration='vertical2')

        # pane1---------------------------------------------------------------------------------------

        FolderListTab = cm.tabLayout('FolderListTabLO', innerMarginWidth=5, innerMarginHeight=5, childResizable=True)
        FolderListColumn = cm.columnLayout(adjustableColumn=True)
        FolderList = cm.textScrollList(allowMultiSelection=False, deselectAll=True,
                                         append=["", '--------------------', 'three', 'four',
                                                 'five', 'six', 'seven', 'eight', 'nine', 'ten',
                                                 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen'],
                                         height=WinSize[1], parent=FolderListColumn)

        cm.setParent('..')
        cm.setParent('..')

        cm.tabLayout(FolderListTab, edit=True, tabLabel=(FolderListColumn, 'FolderList'))

        # pane2---------------------------------------------------------------------------------------

        ImageListTab = cm.tabLayout('ImageListTabLO', innerMarginWidth=5, innerMarginHeight=5, childResizable=True)
        ImageListColumn = cm.columnLayout(adjustableColumn=True)
        ImageList = cm.scrollLayout(verticalScrollBarThickness=16, height=WinSize[1])
        cm.tabLayout(ImageListTab, edit=True, tabLabel=(ImageListColumn, 'ImageList'))

        cm.rowColumnLayout(adjustableColumn=2, numberOfColumns=3)
        self.setIconBttn()

        cm.setParent('..')
        cm.setParent(MainRow)

        cm.text(" HDR_Browser ( ver. 1.0.0 )  by Hyunwoo_Kwon ", align="right")
        cm.text(" Email - dhfpswl704@gmail.com ", align="right")

        cm.showWindow(WinName)

UI()