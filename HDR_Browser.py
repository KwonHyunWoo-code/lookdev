# -*- coding: utf-8 -*-

import maya.cmds as cmds
import pymel.core as pm
import os, sys


class Browser:


    ## 파일 경로 설정 및 sourceimages 폴더 경로 설정

    ### SourceDrive 는 해당 드라이브
    ### HDR_SOURCE_BASEPATH 는 HDR 이미지가 있는 상위 폴더

    SourceDrive = "E:\\\\"
    HDR_SOURCE_BASEPATH = SourceDrive + "HDRI\\"


    def __init__(self):

        # self.SourceDrive = "E:\\\\"
        # self.HDR_SOURCE_BASEPATH = self.SourceDrive + "HDRI\\"
        #self.HDR_FOLDER = os.path.dirname(os.path.abspath(__file__))
        #self.HDR_MINI_FORDER = os.path.join(self.HDR_SOURCE_BASEPATH, "Mini_").replace("\\", "/")
        #print(self.HDR_MINI_FORDER)





        #print(self.HDR_SOURCE_BASEPATH)

        self.foundFolder_NameList = self.getFolderBaseName(self.FindFolder(self.HDR_SOURCE_BASEPATH))
        #print(self.foundFolder_NameList)

        ### HDRI 폴더 내에 하위폴더 경로 리스트
        self.foundFolder_Path = self.FindFolder(self.HDR_SOURCE_BASEPATH)
        #print(self.foundFolder_Path)

        ### HDRI MINI 폴더 경로
        self.MiniDir = self.ConformMiniFolder(self.foundFolder_Path)[0]
        print(self.MiniDir)

        ### HDRI MINI 폴더 내에 있는 파일 리스트
        self.MiniFullPathList = self.getFilePath(str(self.MiniDir))
        #print(self.MiniFullPathList)

        ###
        self.HDRFileName = self.getFileNameList(self.MiniFullPathList)
        #print(self.HDRFileName)


        # print(self.foundFolder_Path[0])
        # print(self.ConformMiniFolder(str(self.foundFolder_Path[0]))[1])
        # print(self.FindFilesList(str(self.MiniDir)))
        # print(self.getFilePath(str(self.MiniDir)))

    def getMiniFullPathList(self):
        print("test")


    def getFolderBaseName(self, folderlist):
        """
        폴더 리스트의 각각의 경로에서 basename을 return
        :param folderlist:
        :return: folderbasenamelist
        """
        folderBaseNameList = []

        for folderPath in folderlist:
            folderBaseName = os.path.basename(folderPath)
            folderBaseNameList.append(folderBaseName)

        return folderBaseNameList


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


    def ConformMiniFolder(self, pathlist):
        """
        해당 경로의 하위 목록을 검색하여 리스트로 반환
        :param : path
        :return : Bool, MiniFolderPath
        """
        MiniFolderName = "Mini"
        #print(type(MiniFolderName))
        Bool = 0

        MiniFolderList = []

        for filepath in pathlist:

            file = os.path.basename(filepath).split('_')


            if MiniFolderName in file:
                MiniFolderList.append(filepath)

        return MiniFolderList

        # MiniFolderPath = os.path.join(path, MiniFolderName).replace("\\", "/")

        # if os.path.exists(path):
        #     Bool=1
        # else:
        #     Bool=0


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

    def compareFileExt(self, filename):

        filenameSplited = filename.split(".")
        #print(filenameSplited)


        if filenameSplited[1] == "jpg":
            return True
        else:
            return False


        # if filenameSplited[1] == "exr" or filenameSplited[1] == "hdr":
        #     return True
        # else:
        #     return False



    # def setIconBttn(self):
    #     """
    #     ImageList에 HDRI 이미지 올리기
    #     :return:
    #     """
    #     width = 200
    #     height = 100
    #
    #     fileNameList = self.getFileNameList(self.MiniFullPathList)
    #     conformFileNameList = []
    #     for filename in fileNameList:
    #         if self.compareFileExt(filename)==1:
    #             conformFileNameList.append(filename.split(".")[0])
    #         else:
    #             pass
    #
    #     getFileData = dict(zip(conformFileNameList, self.MiniFullPathList))
    #     #print(getFileData)
    #
    #     for key, value in getFileData.items():
    #         cmds.iconTextButton(style="iconAndTextVertical", label=key, scaleIcon=True,
    #                             image1=value, w=width, h=height, command="")

    def folderListSelectCmd(self):
        pass

    # def CreateVrayDomeLight(self):
    #
    #     createVrayDomeLight = cm.shadingNode('VRayLightDomeShape', name='Env_LTShape', asLight=True)
    #
    #     cm.setAttr(createVrayDomeLight + '.useDomeTex', 1)
    #
    #     createFile = cm.shadingNode('file', name='envfile', asTexture=True, isColorManaged=True)
    #     cmds.setAttr(createFile + ".filterType", 0)
    #     # cmds.setAttr(CreateFile + ".fileTextureName", "???????????---path---??????????????", type="string")
    #
    #     createVrayPlaceEnvTex = cm.shadingNode('VRayPlaceEnvTex', name="VrayPlaceEnvTex_envfile", asUtility=True)
    #
    #     createPlace2dTexture = cm.shadingNode('place2dTexture', name="place2dTexture_envfile", asUtility=True)
    #
    #     cm.connectAttr(createPlace2dTexture + ".uv", createVrayPlaceEnvTex + ".outUV")
    #     cm.connectAttr(createVrayPlaceEnvTex + '.outUV', createFile + '.uv')
    #     cm.connectAttr(createFile + '.outColor', createVrayDomeLight + ".domeTex")


    def setHDRTex(self):

        pass
