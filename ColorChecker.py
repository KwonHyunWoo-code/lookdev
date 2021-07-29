# -*- coding: utf-8 -*-

import maya.cmds as cmds
import os, sys


class ColorCheckerRig:

    def __init__(self):
        self.cmds = cmds


        ## 파일 경로 설정 및 sourceimages 폴더 경로 설정
        self.COLORCHECK_FOLDER = os.path.dirname(os.path.abspath(__file__))
        self.COLORCHECKIMGPATH = os.path.join(self.COLORCHECK_FOLDER, "sourceimages").replace("\\", "/")


        ## 상수값 설정
        ballRadius = 0.25
        width=1.28
        height=0.86


        ## 각각의 오브젝트를 만들고 위치값 설정
        Ref_ColorPlane = cmds.polyPlane(name="Ref_ColorPlane", width=width, height=height, subdivisionsWidth=6, subdivisionsHeight=3)
        self.setAttrObj(Ref_ColorPlane, 0, (height*1.5) + (ballRadius*2) + (width*0.2*1.5), 90)
        cmds.setAttr(Ref_ColorPlane[0] + "Shape" + ".visibleInReflections", 0)
        cmds.makeIdentity(Ref_ColorPlane, apply=True)

        ColorPlane = cmds.polyPlane(name="ColorPlane", width=width, height=height, subdivisionsWidth=6, subdivisionsHeight=3)
        self.setAttrObj(ColorPlane, 0, (height/2) + (ballRadius*2) + (width*0.2), 90)
        cmds.setAttr(ColorPlane[0] + "Shape" + ".visibleInReflections", 0)
        cmds.makeIdentity(ColorPlane, apply=True)

        ChromeBall = cmds.polySphere(name="ChromeBall", radius=ballRadius, subdivisionsAxis=35, subdivisionsHeight=35)
        self.setAttrObj(ChromeBall, 0.33, ballRadius + (width*0.2/2), 0)
        cmds.makeIdentity(ChromeBall, apply=True)

        GreyBall = cmds.polySphere(name="GreyBall", radius=ballRadius, subdivisionsAxis=35, subdivisionsHeight=35)
        self.setAttrObj(GreyBall, -0.33, ballRadius + (width*0.2/2), 0)
        cmds.makeIdentity(GreyBall, apply=True)


        ## 그룹설정
        self.ColorChecker_GRP = cmds.group(empty=True, name="ColorCheckerGRP")
        ColorChecker_CTRL = cmds.group(empty=True, name="ColorCheckerCTRL")
        ColorChecker_Geo_GRP = cmds.group(empty=True, name="ColorChecker_Geo_GRP")




        ## 그룹 parent 설정
        self.setParents(ColorChecker_Geo_GRP, Ref_ColorPlane[0])
        self.setParents(ColorChecker_Geo_GRP, ColorPlane[0])
        self.setParents(ColorChecker_Geo_GRP, ChromeBall[0])
        self.setParents(ColorChecker_Geo_GRP, GreyBall[0])

        self.setParents(self.ColorChecker_GRP, ColorChecker_Geo_GRP)
        self.setParents(self.ColorChecker_GRP, ColorChecker_CTRL)


        ## 전체 boundbox 크기 및 min, max 값 구하기
        getbbox = self.getBoundBox(ColorChecker_Geo_GRP)


        ## 전체 boundbox의 위치값을 바탕으로하여 offset값 추가하여 square curve 만들기
        RigCurve_Ctrl = self.setSquareRig(getbbox[0], getbbox[3], getbbox[1], getbbox[4])

        ## 그룹 parent 설정
        self.setParents(ColorChecker_CTRL, RigCurve_Ctrl)




        YminValue = self.getBoundBox(RigCurve_Ctrl)[1]
        cmds.xform(RigCurve_Ctrl, piv=[0, YminValue, 0])
        cmds.makeIdentity(RigCurve_Ctrl, apply=True)


        ## translate Ctrl curve와 해당 오브젝트의 그룹과 constraint 연결하기
        cmds.parentConstraint(RigCurve_Ctrl, ColorChecker_Geo_GRP)
        cmds.scaleConstraint(RigCurve_Ctrl, ColorChecker_Geo_GRP)


        ## 해당 오브젝트에 쉐이더 적용하기
        self.makeVrayChromeShdr()
        cmds.sets(ChromeBall[0], edit=True, forceElement="VRayC_SG")

        self.makeVrayGreyShdr()
        cmds.sets(GreyBall[0], edit=True, forceElement="VRayG_SG")

        self.makeSurfaceColorCheckShdr()
        cmds.sets(ColorPlane[0], edit=True, forceElement="SurfaceCol_SG")

        self.makeVrayColorCheckShdr()
        cmds.sets(Ref_ColorPlane[0], edit=True, forceElement="VRayCol_SG")



        ## 전체 그룹의 attribute hide / new attribute add

        cmds.setAttr(self.ColorChecker_GRP + ".tx", keyable=False, channelBox=False)
        cmds.setAttr(self.ColorChecker_GRP + ".ty", keyable=False, channelBox=False)
        cmds.setAttr(self.ColorChecker_GRP + ".tz", keyable=False, channelBox=False)
        cmds.setAttr(self.ColorChecker_GRP + ".rx", keyable=False, channelBox=False)
        cmds.setAttr(self.ColorChecker_GRP + ".ry", keyable=False, channelBox=False)
        cmds.setAttr(self.ColorChecker_GRP + ".rz", keyable=False, channelBox=False)
        cmds.setAttr(self.ColorChecker_GRP + ".sx", keyable=False, channelBox=False)
        cmds.setAttr(self.ColorChecker_GRP + ".sy", keyable=False, channelBox=False)
        cmds.setAttr(self.ColorChecker_GRP + ".sz", keyable=False, channelBox=False)

        cmds.addAttr(self.ColorChecker_GRP, longName="Checker_Type", attributeType='long')
        cmds.setAttr(self.ColorChecker_GRP + ".Checker_Type", edit=True, keyable=True)


        self.deleteAll()

    def setParents(self, src, tgt):
        cmds.parent(tgt, src, r=True)

    def setAttrObj(self, objName, transX, transY, rotX):
        cmds.setAttr(objName[0] + ".translateX", transX)
        cmds.setAttr(objName[0] + ".translateY", transY)
        cmds.setAttr(objName[0] + ".rotateX", rotX)

    def getBoundBox(self, src):

        bbox = cmds.exactWorldBoundingBox(src)
        Xmin = bbox[0]
        Ymin = bbox[1]
        Zmin = bbox[2]
        Xmax = bbox[3]
        Ymax = bbox[4]
        Zmax = bbox[5]

        return Xmin, Ymin, Zmin, Xmax, Ymax, Zmax

    def setSquareRig(self, xmin, xmax, ymin, ymax):

        paddingValue = xmax*0.2

        rigCurve1 = cmds.curve(name='curve1', d=1, p=[(xmin-paddingValue, ymin-paddingValue, 0), (xmax+paddingValue, ymin-paddingValue, 0)])
        rigCurve2 = cmds.curve(name='curve2', d=1, p=[(xmax+paddingValue, ymin-paddingValue, 0), (xmax+paddingValue, ymax+paddingValue, 0)])
        rigCurve3 = cmds.curve(name='curve3', d=1, p=[(xmin-paddingValue, ymax+paddingValue, 0), (xmax+paddingValue, ymax+paddingValue, 0)])
        rigCurve4 = cmds.curve(name='curve4', d=1, p=[(xmin-paddingValue, ymin-paddingValue, 0), (xmin-paddingValue, ymax+paddingValue, 0)])

        rigCtrlGrp = cmds.group(name='rigCtrl', empty=True)

        SelList = [rigCurve1, rigCurve2, rigCurve3, rigCurve4]

        for sel in SelList:

            cmds.select(sel, r=True)
            cmds.select(rigCtrlGrp, add=True)
            sel = cmds.ls(sl=True)
            shp = cmds.listRelatives(sel[0], s=True)[0]
            cmds.parent(shp, sel[1], r=True, s=True)

        for removeSel in SelList:
            cmds.select(removeSel, r=True)
            cmds.delete()

        return rigCtrlGrp

    def makeVrayChromeShdr(self):

        ChromeShader = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="VRayC_SG")
        PureChromeMtl = cmds.shadingNode('VRayMtl', name="Chrome_Mtl", asShader=True)

        Shading_Connection = cmds.connectAttr('Chrome_Mtl.outColor', 'VRayC_SG.surfaceShader')

        cmds.setAttr("Chrome_Mtl.color", 0.0, 0.0, 0.0, type="double3")
        cmds.setAttr("Chrome_Mtl.brdfType", 3)
        cmds.setAttr("Chrome_Mtl.reflectionColor", 0.863, 0.863, 0.863, type="double3")
        cmds.setAttr("Chrome_Mtl.reflectionColorAmount", 1)
        cmds.setAttr("Chrome_Mtl.reflectionGlossiness", 1)
        cmds.setAttr("Chrome_Mtl.reflectionSubdivs", 16)
        cmds.setAttr("Chrome_Mtl.glossyFresnel", 0)
        cmds.setAttr("Chrome_Mtl.lockFresnelIORToRefractionIOR", 0)
        cmds.setAttr("Chrome_Mtl.fresnelIOR", 20)

    def makeVrayGreyShdr(self):

        GreyShader = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="VRayG_SG")
        GreyMtl = cmds.shadingNode('VRayMtl', name="Grey_Mtl", asShader=True)

        Shading_Connection = cmds.connectAttr('Grey_Mtl.outColor', 'VRayG_SG.surfaceShader')

        cmds.setAttr("Grey_Mtl.color", 0.18, 0.18, 0.18, type="double3")
        cmds.setAttr("Grey_Mtl.brdfType", 3)

    def makeSurfaceColorCheckShdr(self):

        SurfaceShader = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="SurfaceCol_SG")
        ColorCheckMtl = cmds.shadingNode('surfaceShader', name="ColorCheckMtl", asShader=True)

        Shading_Connection = cmds.connectAttr('ColorCheckMtl.outColor', 'SurfaceCol_SG.surfaceShader')

        CreateFile = cmds.shadingNode('file', name="ColorCheckImgFile", asTexture=True, isColorManaged=True)
        cmds.setAttr( CreateFile + ".filterType", 0)
        cmds.setAttr( CreateFile + ".fileTextureName", self.COLORCHECKIMGPATH + "/" + "sRGB_ColorChecker_Chart.jpg", type="string")
        Create2dTex = cmds.shadingNode('place2dTexture', name="place2dTexture_ColCh", asUtility=True)

        cmds.connectAttr('place2dTexture_ColCh.coverage', 'ColorCheckImgFile.coverage')
        cmds.connectAttr('place2dTexture_ColCh.translateFrame', 'ColorCheckImgFile.translateFrame')
        cmds.connectAttr('place2dTexture_ColCh.rotateFrame', 'ColorCheckImgFile.rotateFrame')
        cmds.connectAttr('place2dTexture_ColCh.mirrorU', 'ColorCheckImgFile.mirrorU')
        cmds.connectAttr('place2dTexture_ColCh.mirrorV', 'ColorCheckImgFile.mirrorV')
        cmds.connectAttr('place2dTexture_ColCh.stagger', 'ColorCheckImgFile.stagger')
        cmds.connectAttr('place2dTexture_ColCh.wrapU', 'ColorCheckImgFile.wrapU')
        cmds.connectAttr('place2dTexture_ColCh.wrapV', 'ColorCheckImgFile.wrapV')
        cmds.connectAttr('place2dTexture_ColCh.repeatUV', 'ColorCheckImgFile.repeatUV')
        cmds.connectAttr('place2dTexture_ColCh.offset', 'ColorCheckImgFile.offset')
        cmds.connectAttr('place2dTexture_ColCh.rotateUV', 'ColorCheckImgFile.rotateUV')
        cmds.connectAttr('place2dTexture_ColCh.noiseUV', 'ColorCheckImgFile.noiseUV')
        cmds.connectAttr('place2dTexture_ColCh.vertexUvOne', 'ColorCheckImgFile.vertexUvOne')
        cmds.connectAttr('place2dTexture_ColCh.vertexUvTwo', 'ColorCheckImgFile.vertexUvTwo')
        cmds.connectAttr('place2dTexture_ColCh.vertexUvThree', 'ColorCheckImgFile.vertexUvThree')
        cmds.connectAttr('place2dTexture_ColCh.vertexCameraOne', 'ColorCheckImgFile.vertexCameraOne')
        cmds.connectAttr('place2dTexture_ColCh.outUV', 'ColorCheckImgFile.uv')
        cmds.connectAttr('place2dTexture_ColCh.outUvFilterSize', 'ColorCheckImgFile.uvFilterSize')

        cmds.connectAttr('ColorCheckImgFile.outColor', 'ColorCheckMtl.outColor')

    def makeVrayColorCheckShdr(self):

        SurfaceShader = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="VRayCol_SG")
        ColorCheckMtl = cmds.shadingNode('VRayMtl', name="ColorCheckVrayMtl", asShader=True)

        Shading_Connection = cmds.connectAttr('ColorCheckVrayMtl.outColor', 'VRayCol_SG.surfaceShader')

        CreateFile = cmds.shadingNode('file', name="VrayColorCheckImgFile", asTexture=True, isColorManaged=True)
        cmds.setAttr( CreateFile + ".filterType", 0)
        cmds.setAttr( CreateFile + ".fileTextureName", self.COLORCHECKIMGPATH + "/" + "sRGB_ColorChecker_Chart.jpg", type="string")
        Create2dTex = cmds.shadingNode('place2dTexture', name="place2dTexture_VrayColCh", asUtility=True)

        cmds.connectAttr('place2dTexture_VrayColCh.coverage', 'VrayColorCheckImgFile.coverage')
        cmds.connectAttr('place2dTexture_VrayColCh.translateFrame', 'VrayColorCheckImgFile.translateFrame')
        cmds.connectAttr('place2dTexture_VrayColCh.rotateFrame', 'VrayColorCheckImgFile.rotateFrame')
        cmds.connectAttr('place2dTexture_VrayColCh.mirrorU', 'VrayColorCheckImgFile.mirrorU')
        cmds.connectAttr('place2dTexture_VrayColCh.mirrorV', 'VrayColorCheckImgFile.mirrorV')
        cmds.connectAttr('place2dTexture_VrayColCh.stagger', 'VrayColorCheckImgFile.stagger')
        cmds.connectAttr('place2dTexture_VrayColCh.wrapU', 'VrayColorCheckImgFile.wrapU')
        cmds.connectAttr('place2dTexture_VrayColCh.wrapV', 'VrayColorCheckImgFile.wrapV')
        cmds.connectAttr('place2dTexture_VrayColCh.repeatUV', 'VrayColorCheckImgFile.repeatUV')
        cmds.connectAttr('place2dTexture_VrayColCh.offset', 'VrayColorCheckImgFile.offset')
        cmds.connectAttr('place2dTexture_VrayColCh.rotateUV', 'VrayColorCheckImgFile.rotateUV')
        cmds.connectAttr('place2dTexture_VrayColCh.noiseUV', 'VrayColorCheckImgFile.noiseUV')
        cmds.connectAttr('place2dTexture_VrayColCh.vertexUvOne', 'VrayColorCheckImgFile.vertexUvOne')
        cmds.connectAttr('place2dTexture_VrayColCh.vertexUvTwo', 'VrayColorCheckImgFile.vertexUvTwo')
        cmds.connectAttr('place2dTexture_VrayColCh.vertexUvThree', 'VrayColorCheckImgFile.vertexUvThree')
        cmds.connectAttr('place2dTexture_VrayColCh.vertexCameraOne', 'VrayColorCheckImgFile.vertexCameraOne')
        cmds.connectAttr('place2dTexture_VrayColCh.outUV', 'VrayColorCheckImgFile.uv')
        cmds.connectAttr('place2dTexture_VrayColCh.outUvFilterSize', 'VrayColorCheckImgFile.uvFilterSize')

        cmds.connectAttr(CreateFile + '.outColor', ColorCheckMtl + '.diffuseColor')



    def deleteAll(self):

        cmds.delete('ColorCheckerGRP')

        cmds.select('ColorCheckVrayMtl', allDagObjects=False, noExpand=True)
        cmds.select('VRayCol_SG', allDagObjects=False, noExpand=True, add=True)
        cmds.select('VrayColorCheckImgFile', allDagObjects=False, noExpand=True, add=True)
        cmds.select('place2dTexture_VrayColCh', allDagObjects=False, noExpand=True, add=True)

        cmds.select('ColorCheckMtl', allDagObjects=False, noExpand=True, add=True)
        cmds.select('SurfaceCol_SG', allDagObjects=False, noExpand=True, add=True)
        cmds.select('ColorCheckImgFile', allDagObjects=False, noExpand=True, add=True)
        cmds.select('place2dTexture_ColCh', allDagObjects=False, noExpand=True, add=True)

        cmds.select('Chrome_Mtl', allDagObjects=False, noExpand=True, add=True)
        cmds.select('VRayC_SG', allDagObjects=False, noExpand=True, add=True)

        cmds.select('Grey_Mtl', allDagObjects=False, noExpand=True, add=True)
        cmds.select('VRayG_SG', allDagObjects=False, noExpand=True, add=True)

        cmds.delete()

        # if cmds.objExists(self.ColorChecker_GRP):
        #     cmds.delete('ColorCheckerGRP')
        #
        #     cmds.select('ColorCheckVrayMtl', allDagObjects=False, noExpand=True)
        #     cmds.select('VRayCol_SG', allDagObjects=False, noExpand=True, add=True)
        #     cmds.select('VrayColorCheckImgFile', allDagObjects=False, noExpand=True, add=True)
        #     cmds.select('place2dTexture_VrayColCh', allDagObjects=False, noExpand=True, add=True)
        #
        #     cmds.select('ColorCheckMtl', allDagObjects=False, noExpand=True)
        #     cmds.select('SurfaceCol_SG', allDagObjects=False, noExpand=True, add=True)
        #     cmds.select('ColorCheckImgFile', allDagObjects=False, noExpand=True, add=True)
        #     cmds.select('place2dTexture_ColCh', allDagObjects=False, noExpand=True, add=True)
        #
        #     cmds.select('Chrome_Mtl', allDagObjects=False, noExpand=True)
        #     cmds.select('VRayC_SG', allDagObjects=False, noExpand=True, add=True)
        #
        #     cmds.select('Grey_Mtl', allDagObjects=False, noExpand=True)
        #     cmds.select('VRayG_SG', allDagObjects=False, noExpand=True, add=True)
        #
        #     cmds.delete()
        #
        #     print("reset")
        #
        # else:
        #     print("Warning: No ColorCheckerGRP exists.")



        pass
