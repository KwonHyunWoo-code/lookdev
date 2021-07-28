# -*- coding: utf-8 -*-

import maya.cmds as cmds
import pymel.core as pm
import os, sys


class Browser:


    ## 파일 경로 설정 및 sourceimages 폴더 경로 설정

    ### SourceDrive 는 해당 드라이브
    ### HDR_SOURCE_BASEPATH 는 HDR 이미지가 있는 상위 폴더

    SourceDrive = "D:\\\\"
    HDR_SOURCE_BASEPATH = SourceDrive + "HDRI\\"


    def __init__(self):

        ### 현재 파일 경로
        self.HDR_FOLDER = os.path.dirname(os.path.abspath(__file__))
        self.HDR_FOLDER_FullPath = os.path.abspath(__file__)

        ### HDRI 폴더 내에 하위폴더 이름 리스트
        self.foundFolder_NameList = self.getFolderBaseNameFromFolderList(self.FindFolder(self.HDR_SOURCE_BASEPATH))
        #print(self.foundFolder_NameList)

        ### HDRI 폴더 내에 하위폴더 경로 리스트
        self.foundFolder_PathList = self.FindFolder(self.HDR_SOURCE_BASEPATH)
        #print(self.foundFolder_Path)

        ### 해당 폴더의 MINI 폴더 경로
        self.MiniDir = self.FindFolder(self.foundFolder_PathList[1])
        print(self.MiniDir)

        ### HDRI MINI 폴더 내에 있는 파일 리스트
        self.MiniFilePathList = self.FindFilesList(self.MiniDir[0])
        print(self.MiniFilePathList)

        ### 해당 HDRI 폴더 내에 있는 파일 리스트
        #self.HDRFileName = self.getFileNameList(self.MiniFullPathList)
        #print(self.HDRFileName)


    def getFolderBaseNameFromFolderList(self, folderlist):
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

    def FindFilesList(self, path):

        FilesList = os.listdir(path)
        FilePathList = []

        if len(FilesList) == 0:
            return 0

        else:
            for item in FilesList:
                pathName = str(self.MiniDir[0]) + "/" + str(item)
                FilePathList.append(pathName)

            return FilePathList

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

    def CreateVrayDomeLight(self):
        pass
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
