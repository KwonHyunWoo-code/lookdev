# -*- coding: utf-8 -*-

import maya.cmds as cmds
import os, sys


class HDR_Browser:

    def __init__(self):

        ## 파일 경로 설정 및 sourceimages 폴더 경로 설정

        ### SourceDrive 는 해당 드라이브
        ### HDR_SOURCE_BASEPATH 는 HDR 이미지가 있는 상위 폴더
        ###

        self.SourceDrive = "F:\\\\"
        self.HDR_SOURCE_BASEPATH = self.SourceDrive + "_3D_Resource\\HDRI\\"
        #self.HDR_FOLDER = os.path.dirname(os.path.abspath(__file__))
        #self.HDR_MINI_FORDER = os.path.join(self.COLORCHECK_FOLDER, "_Mini").replace("\\", "/")


        ## 상수값 설정 - 버전, 파일제목
        self.Version = "v001"
        self.Title = "HDR_Browser"


        self.foundFolder_NameList = os.path.basename(str(self.FindFolder(self.HDR_SOURCE_BASEPATH)[0]))

        ### HDRI 폴더 내에 하위폴더 경로 리스트
        self.foundFolder_Path = self.FindFolder(self.HDR_SOURCE_BASEPATH)
        print(self.foundFolder_Path)

        ### HDRI MINI 폴더 경로
        self.MiniDir = self.ConformMiniFolder(str(self.foundFolder_Path[0]))[1]
        print(self.MiniDir)

        ### HDRI MINI 폴더 내에 있는 파일 리스트
        self.MiniFullPathList = self.getFilePath(str(self.MiniDir))
        print(self.MiniFullPathList)

        ###
        self.HDRFileName = self.getFileNameList(self.MiniFullPathList)
        print(self.HDRFileName)


        # print(self.foundFolder_Path[0])
        # print(self.ConformMiniFolder(str(self.foundFolder_Path[0]))[1])
        # print(self.FindFilesList(str(self.MiniDir)))
        # print(self.getFilePath(str(self.MiniDir)))


        self.UI()

    def FindFolder(self, path):
        """
        해당 경로의 하위 목록을 검색하여 리스트로 반환
        :param path:
        :return searchedPathList:
        """

        pathItemList = os.listdir(path)

        searchedPathList = []

        for Item in pathItemList:

            if os.path.isdir(os.path.join(path, Item)):
                searchedPath = os.path.join(path, Item).replace("\\", "/")
                searchedPathList.append(searchedPath)

        return searchedPathList

    def ConformMiniFolder(self, path):
        """
        해당 경로의 하위 목록을 검색하여 리스트로 반환
        :param : path
        :return : Bool, MiniFolderPath
        """
        MiniFolderName = "_Mini"
        Bool = 0

        # MiniFolderPath = os.path.join(path, MiniFolderName).replace("\\", "/")

        if os.path.exists(path):
            Bool=1
        else:
            Bool=0

        return Bool, path

    def FindFilesList(self, path):

        FilesList = os.listdir(path)

        if len(FilesList) == 0:
            return 0

        else:
            return FilesList

    def getFilePath(self, path):
        FilesList = os.listdir(path)

        FilePathList = []

        for item in FilesList:
            FileDir = os.path.join(path, item).replace("\\", "/")
            FilePathList.append(FileDir)

        return FilePathList

    def getFileNameList(self, pathlist):

        FileNameList = []

        for path in pathlist:
            FileName = os.path.basename(path)
            FileNameList.append(FileName)

        return FileNameList



    def setIconBttn(self):

        width = 200
        height = 100

        getFileData = dict(zip(self.getFileNameList(self.MiniFullPathList), self.MiniFullPathList))
        print(getFileData)
        for key, value in getFileData.items():
            cmds.iconTextButton(style="iconAndTextVertical", label=key, scaleIcon=True,
                                image1=value, w=width, h=height, command="")

    def folderListSelectCmd(self):
        pass

    def CreateVrayDomeLight(self):

        cmds.shadingNode('VRayLightDomeShape', name='Env_LT', asLight=True)



    def setHDRTex(self):

        pass

    def UI(self):

        WinName = "HDR_Browser"
        WinWidth = 540

        if cmds.window("HDR_Browser", q=True, exists=True):
            cmds.deleteUI("HDR_Browser")

        WinFrom = cmds.window(WinName, t=self.Title, w=WinWidth, mxb=True, mnb=True, s=True, resizeToFitChildren=True)
        getWinWidth = cmds.window(WinFrom, q=True, width=True)
        getWinHeight = cmds.window(WinFrom, q=True, height=True)
        WinSize = [getWinWidth, getWinHeight]

        #--------------------------------------------------------------------------------------------------------------

        #Layout

        MainForm = cmds.formLayout(vis=True, numberOfDivisions=100, width=WinSize[0])
        cmds.rowColumnLayout(adjustableColumn=True, width=WinSize[0])

        RowWidthRate = [0.3, 0.1, 0.3, 0.3]
        cmds.rowLayout(numberOfColumns=4)
        cmds.radioButtonGrp(label="ColorChecker", labelArray3=['Type1_Col', 'Type2_Ball', 'Type3_Col+Ball'], numberOfRadioButtons=3)
        cmds.button(label="Apply")
        cmds.text(label="Current_HDRLight")
        cmds.textField(enable=False, backgroundColor=[0.05, 0.05, 0.05])
        cmds.setParent("..")
        cmds.separator(width=WinSize[0], height=15, style="double")

        cmds.paneLayout('MainPanaLO', w=WinSize[0], paneSize=[1, 20, 100], configuration='vertical2')

        #pane1---------------------------------------------------------------------------------------

        FolderListTab = cmds.tabLayout('FolderListTabLO', innerMarginWidth=5, innerMarginHeight=5, childResizable=True)
        FolderListColumn = cmds.columnLayout(adjustableColumn=True)
        FolderList = cmds.textScrollList(deselectAll=True, height=WinSize[1], parent=FolderListColumn)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.tabLayout(FolderListTab, edit=True, tabLabel=(FolderListColumn, 'FolderList'))
        #pane2---------------------------------------------------------------------------------------

        ImageListTab = cmds.tabLayout('ImageListTabLO', innerMarginWidth=5, innerMarginHeight=5, childResizable=True)
        ImageListColumn = cmds.columnLayout(adjustableColumn=True)
        ImageList = cmds.scrollLayout(verticalScrollBarThickness=16, height=WinSize[1])
        cmds.tabLayout(ImageListTab, edit=True, tabLabel=(ImageListColumn, 'ImageList'))

        cmds.rowColumnLayout(adjustableColumn=2, numberOfColumns=3)
        self.setIconBttn()


        cmds.setParent('..')





        cmds.showWindow("HDR_Browser")


HDR_Browser()