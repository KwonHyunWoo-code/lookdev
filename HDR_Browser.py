# -*- coding: utf-8 -*-

import maya.cmds as cm
import pymel.core as pm
#import mtoa.utils as mutils;
import os, sys


class Browser:


    ## �일 경로 �정 �sourceimages �더 경로 �정

    ### SourceDrive �당 �라�브
    ### HDR_SOURCE_BASEPATH HDR ��지가 �는 �위 �더

    SourceDrive = "E:\\\\"
    HDR_SOURCE_BASEPATH = SourceDrive + "HDRI\\"


    def __init__(self):

        ### �재 �일 경로
        self.HDR_FOLDER = os.path.dirname(os.path.abspath(__file__))
        self.HDR_FOLDER_FullPath = os.path.abspath(__file__)

        ### HDRI �더 �에 �위�더 �름 리스
        self.foundFolder_NameList = self.getFolderBaseNameFromFolderList(self.FindFolder(self.HDR_SOURCE_BASEPATH))
        #print(self.foundFolder_NameList)

        ### HDRI �더 �에 �위�더 경로 리스
        self.foundFolder_PathList = self.FindFolder(self.HDR_SOURCE_BASEPATH)
        #print(self.foundFolder_PathList)

        ### �당 �더MINI �더 경로
        self.MiniDir = self.FindFolder(self.foundFolder_PathList[1])
        print(self.MiniDir)

        ### HDRI MINI �더 �에 �는 �일 리스
        self.MiniFilePathList = self.FindFilesList(self.MiniDir[0])
        print(self.MiniFilePathList)

        ### �당 HDRI �더 �에 �는 �일 리스
        #self.HDRFileName = self.getFileNameList(self.MiniFullPathList)
        #print(self.HDRFileName)


    def getFolderBaseNameFromFolderList(self, folderlist):
        """
        �더 리스�의 각각경로�서 basenamereturn
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
        �당 경로�위 목록검�하리스�로 반환
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


        createVrayDomeLight = cm.shadingNode('VRayLightDomeShape', name='Env_LTShape', asLight=True)

        cm.setAttr(createVrayDomeLight + '.useDomeTex', 1)

        createFile = cm.shadingNode('file', name='envfile', asTexture=True, isColorManaged=True)
        cm.setAttr(createFile + ".filterType", 0)
        # cmds.setAttr(CreateFile + ".fileTextureName", "???????????---path---??????????????", type="string")

        createVrayPlaceEnvTex = cm.shadingNode('VRayPlaceEnvTex', name="VrayPlaceEnvTex_envfile", asUtility=True)

        createPlace2dTexture = cm.shadingNode('place2dTexture', name="place2dTexture_envfile", asUtility=True)

        cm.connectAttr(createPlace2dTexture + ".uv", createVrayPlaceEnvTex + ".outUV")
        cm.connectAttr(createVrayPlaceEnvTex + '.outUV', createFile + '.uv')
        cm.connectAttr(createFile + '.outColor', createVrayDomeLight + ".domeTex")

    def CreateAnorldDomeLight(self):

        mutils.createLocator("aiSkyDomeLight", asLight=True)


    def setHDRTex(self):

        pass
