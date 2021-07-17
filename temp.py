import maya.cmds as cm

#--------------Create Vray Dome Light-----------------

def createVrayDomeLight():
    createVrayDomeLight = cm.shadingNode('VRayLightDomeShape', name='Env_LTShape', asLight=True)

    cm.setAttr(createVrayDomeLight + '.useDomeTex', 1)

    createFile = cm.shadingNode('file', name='envfile', asTexture=True, isColorManaged=True)
    cmds.setAttr(createFile + ".filterType", 0)
    #cmds.setAttr(CreateFile + ".fileTextureName", "???????????---path---??????????????", type="string")

    createVrayPlaceEnvTex = cm.shadingNode('VRayPlaceEnvTex', name="VrayPlaceEnvTex_envfile", asUtility=True)

    createPlace2dTexture = cm.shadingNode('place2dTexture', name="place2dTexture_envfile", asUtility=True)


    cm.connectAttr(createPlace2dTexture + ".uv", createVrayPlaceEnvTex + ".outUV")
    cm.connectAttr(createVrayPlaceEnvTex + '.outUV', createFile + '.uv')
    cm.connectAttr(createFile + '.outColor', createVrayDomeLight + ".domeTex")



def replaceEnvFile():
    envFilePath = ""


def currentEnvDisplay():
    envFilePath = ""


def


createVrayDomeLight()