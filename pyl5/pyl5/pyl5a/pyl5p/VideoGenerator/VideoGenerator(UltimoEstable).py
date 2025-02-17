#
#Papel y Lapiz - Software para la creacion de pequeños cortos.
#Copyright (C) 2015  Universidad de Los Andes - Proyecto DAVID.   
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along
#with this program; if not, write to the Free Software Foundation,
#Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#

#!/usr/bin/python

import xml.dom.minidom
import pprint
import time

RESOLUTION_WIDTH = 1920 #1920
RESOLUTION_HEIGHT = 1080 #1080
RESOLUTION_PERCENTAGE = 50
POSITION_SCALE_W = 16
POSITION_SCALE_H = 8
DEFAULT_CAMERA_ALTITUDE = 4
OFFSET_CAMERA_DISTANCE = -6
FRAME_STEP = 1
NUM_POINTS_CURVE = 5
NUM_FRAMES_ANIMATION = 120 #120

import configparser, os

MODELS_PATH = '/var/www/pyl5/VideoGenerator'
RENDER_LOW_QUALITY = "True"
RENDER_VIDEO = os.getenv('RENDER_VIDEO') == "True"
SCRIPT_XML_FILENAME = os.getenv('SCRIPT_XML_FILENAME')
SCORE_XML_FILENAME = os.getenv('SCORE_XML_FILENAME')
OUTPUT_DIR = os.path.dirname(SCRIPT_XML_FILENAME)

from time import gmtime,strftime

# Cargar el archivo XML a memoria, en una estructura mas facilmente entendible
print ('Parsing: ' + SCRIPT_XML_FILENAME)

doc = xml.dom.minidom.parse(SCRIPT_XML_FILENAME)

actors = {}

for xmlActor in doc.getElementsByTagName('actor'):
    a = {}

    # Asigno los valores de los atributos de este elemento
    for attr_key in xmlActor.attributes.keys():
        a[attr_key] = xmlActor.getAttribute(attr_key)

    #Asigno el valor de la posicion del elemento
    for xmlPosition in xmlActor.getElementsByTagName('position'):
        a['position'] = ( float(xmlPosition.getAttribute('x')) * POSITION_SCALE_W , -float(xmlPosition.getAttribute('z')) * POSITION_SCALE_H, 0 )

    # Asigno la trayectoria que tiene este elemento
    a['trajectory'] = []
    for xmlPoint in xmlActor.getElementsByTagName('point'):
        a['trajectory'].append( ( float(xmlPoint.getAttribute('x')) * POSITION_SCALE_W , -float(xmlPoint.getAttribute('z')) * POSITION_SCALE_H , 0 ) )

    # Por ultimo agrego este elemento a la lista de actores de la composicion, pero me cuido de no sobreescribir otro actor que tenga el mismo nombre
    currIndex = 0
    assetName = a['asset']
    while assetName in actors: # Seria mas bonito con un do..while , pero Python no lo tiene
        assetName = "%s_%d" % ( a['asset'] , currIndex )
        currIndex += 1
    a['asset'] = assetName
    actors[assetName] = a

    # NUEVO
    #a["unlink"] = True 

# Invocar al API de Blender para crear los actores y acomodar todos los elementos en la escena

import bpy
import mathutils

# Borrar todo lo que haya en la escena:
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

for tmp_curve in bpy.data.curves:
    bpy.data.curves.remove(tmp_curve)

for tmp_mesh in bpy.data.meshes:
    bpy.data.meshes.remove(tmp_mesh)

# Para el calculo del BoundingBox de la escena mas abajo
bb_min = None
bb_max = None

# bpy.ops.sequencer.sound_strip_add(filepath='/Users/barcodepandora/Sites/VideoGenerator/sound/jazz.mp3', frame_start=1, channel=1)
print ('##### INICIO #####')
print (strftime('%Y-%m-%d %H:%M:%S', gmtime()))
# Crear los objetos en las posiciones que nos hayan dicho en el XML
id = 0
camaraExist = 0
camera = "";
for actor in actors.keys():
    offset = (0,0,0)
    textOffset = (0,0,1)
    textScale = (0.5,0.5,0.5)
    textCorrection = 1
    textRotate = (3.1416/2,0,0)
    mainParent = ""
    bpy.ops.object.select_all(action="DESELECT")
    if actor.startswith("SBCamera"):
        print('***loading SBCamera - DEFAULT***')
        camaraExist = 1
        mainParent = "Camera"
        bpy.ops.object.camera_add()
        camera = bpy.data.objects[mainParent]
        offset = (0,OFFSET_CAMERA_DISTANCE,DEFAULT_CAMERA_ALTITUDE)
        bpy.data.objects[mainParent].location[0] += actors[actor]['position'][0] + offset[0]
        bpy.data.objects[mainParent].location[1] += actors[actor]['position'][1] + offset[1]
        bpy.data.objects[mainParent].location[2] += actors[actor]['position'][2] + offset[2]
    elif actor.startswith("Chinchilla"):
        # Dependency cycle detected: Aunque no veo porque, al parecer es por el padre que estoy agregando....
        mainParent = str(id) + "Chinchilla"
        if actors[actor]['animation'].upper() == 'EAT': #OK
            print('***loading Chinchilla - EAT***')
            offset = (-0.5,0.26,0)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/ChinchillaEat.blend/Object/", filename="chinchillaPrueba", link=False)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/ChinchillaEat.blend/Object/", filename="chinchillarigPrueba", link=False)
            bpy.ops.object.add(type='EMPTY', view_align=False, location=actors[actor]['position'])
            bpy.data.objects["Empty"].name = mainParent
            bpy.data.objects['chinchillarigPrueba'].name = mainParent + "Proxy"
            bpy.data.objects['chinchillaPrueba'].parent=bpy.data.objects[mainParent]
            bpy.data.objects['chinchillaPrueba.001'].parent=bpy.data.objects[mainParent]
            bpy.data.objects[mainParent].location[0] += offset[0]
            bpy.data.objects[mainParent].location[1] += offset[1]
            bpy.data.objects[mainParent].location[2] += offset[2]
        elif actors[actor]['animation'].upper() == 'RUN': #OK
            print('***loading Chinchilla - RUN***')
            offset = (0.4,0,0)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/ChinchillaRun.blend/Object/", filename="PruebaEmpty", link=False)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/ChinchillaRun.blend/Object/", filename="Pruebagamerarig", link=False)
            bpy.ops.object.add(type='EMPTY', view_align=False, location=actors[actor]['position'])
            bpy.data.objects["Empty"].name = mainParent
            bpy.data.objects['Pruebagamerarig'].name = mainParent + "Proxy"
            bpy.data.objects['PruebaEmpty'].parent = bpy.data.objects[mainParent]
            bpy.data.objects['PruebaEmpty.001'].parent = bpy.data.objects[mainParent]
            bpy.data.objects[mainParent].rotation_euler = (0,0,3.1416)
            bpy.data.objects[mainParent].location[0] += offset[0]
            bpy.data.objects[mainParent].location[1] += offset[1]
            bpy.data.objects[mainParent].location[2] += offset[2]
            textRotate = (3.1416/2,0,-3.1416)
        else: #OK
            print('***loading Chinchilla - DEFAULT***')
            offset = (-0.5,0.26,0)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/ChinchillaEat.blend/Object/", filename="chinchillaPrueba", link=False)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/ChinchillaEat.blend/Object/", filename="chinchillarigPrueba", link=False)
            bpy.ops.object.add(type='EMPTY', view_align=False, location=actors[actor]['position'])
            bpy.data.objects["Empty"].name = mainParent
            bpy.data.objects['chinchillarigPrueba'].name = mainParent + "Proxy"
            bpy.data.objects['chinchillaPrueba'].parent=bpy.data.objects[mainParent]
            bpy.data.objects['chinchillaPrueba.001'].parent=bpy.data.objects[mainParent]
            bpy.data.objects[mainParent].location[0] += offset[0]
            bpy.data.objects[mainParent].location[1] += offset[1]
            bpy.data.objects[mainParent].location[2] += offset[2]
    elif actor.startswith("Squirrel"):
        mainParent = str(id) + "Squirrel"
        if actors[actor]['animation'].upper() == 'CLAP': #OK
            print('***loading Squirrel - CLAP***')
            offset = (0.35,0,0)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/SquirrelClap.blend/Object/", filename="SquirrelPrueba", link=False)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/SquirrelClap.blend/Object/", filename="Squirrel_proxyPrueba", link=False)
            bpy.ops.object.add(type='EMPTY', view_align=False, location=actors[actor]['position'])
            bpy.data.objects["Empty"].name = mainParent
            bpy.data.objects['Squirrel_proxyPrueba'].name = mainParent + "Proxy"
            bpy.data.objects['SquirrelPrueba'].parent=bpy.data.objects[mainParent]
            bpy.data.objects['SquirrelPrueba.001'].parent=bpy.data.objects[mainParent]
            bpy.data.objects[mainParent].location[0] += offset[0]
            bpy.data.objects[mainParent].location[1] += offset[1]
            bpy.data.objects[mainParent].location[2] += offset[2]
        elif actors[actor]['animation'].upper() == 'FLAP': #OK
            print('***loading Squirrel - FLAP***')
            offset = (-1.6,1.0,0)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/SquirrelFlap.blend/Object/", filename="SquirrelPrueba", link=False)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/SquirrelFlap.blend/Object/", filename="Squirrel_proxyPrueba", link=False)
            bpy.ops.object.add(type='EMPTY', view_align=False, location=actors[actor]['position'])
            bpy.data.objects["Empty"].name = mainParent
            bpy.data.objects['Squirrel_proxyPrueba'].name = mainParent + "Proxy"
            bpy.data.objects['SquirrelPrueba'].parent=bpy.data.objects[mainParent]
            bpy.data.objects['SquirrelPrueba.001'].parent=bpy.data.objects[mainParent]
            bpy.data.objects[mainParent].location[0] += offset[0]
            bpy.data.objects[mainParent].location[1] += offset[1]
            bpy.data.objects[mainParent].location[2] += offset[2]
        else: #OK
            print('***loading Squirrel - DEFAULT***')
            offset = (-1.6,1.0,0)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/SquirrelFlap.blend/Object/", filename="SquirrelPrueba", link=False)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/SquirrelFlap.blend/Object/", filename="Squirrel_proxyPrueba", link=False)
            bpy.ops.object.add(type='EMPTY', view_align=False, location=actors[actor]['position'])
            bpy.data.objects["Empty"].name = mainParent
            bpy.data.objects['Squirrel_proxyPrueba'].name = mainParent + "Proxy"
            bpy.data.objects['SquirrelPrueba'].parent=bpy.data.objects[mainParent]
            bpy.data.objects['SquirrelPrueba.001'].parent=bpy.data.objects[mainParent]
            bpy.data.objects[mainParent].location[0] += offset[0]
            bpy.data.objects[mainParent].location[1] += offset[1]
            bpy.data.objects[mainParent].location[2] += offset[2]
    elif actor.startswith("FlyingSquirrel"):
        mainParent = str(id) + "FlyingSquirrel"
        if actors[actor]['animation'].upper() == 'RUN':
            print('***loading FlyingSquirrel - RUN***')
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/FSquirrelRun.blend/Object/", filename="PruebaEmpty.001", link=False)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/FSquirrelRun.blend/Object/", filename="PruebaEmpty.001_proxy", link=False)
            bpy.ops.object.add(type='EMPTY', view_align=False, location=actors[actor]['position'])
            bpy.data.objects["Empty"].name = mainParent
            bpy.data.objects['PruebaEmpty.000'].parent = bpy.data.objects[mainParent]
            bpy.data.objects['PruebaEmpty.001'].parent = bpy.data.objects[mainParent]
            bpy.data.objects['PruebaEmpty.001_proxy'].hide_render = True
            bpy.data.objects['PruebaEmpty.001_proxy'].name = mainParent + "Proxy"
        elif actors[actor]['animation'].upper() == 'FLAP':
            print('***loading FlyingSquirrel - FLAP***')
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/FSquirrelFlap.blend/Object/", filename="PruebaFlyingSquirrel", link=False)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/FSquirrelFlap.blend/Object/", filename="PruebaFlyingSquirrel_proxy", link=False)
            bpy.ops.object.add(type='EMPTY', view_align=False, location=actors[actor]['position'])
            bpy.data.objects["Empty"].name = mainParent
            bpy.data.objects['PruebaFlyingSquirrel'].parent = bpy.data.objects[mainParent]
            bpy.data.objects['PruebaFlyingSquirrel.001'].parent = bpy.data.objects[mainParent]
            bpy.data.objects['PruebaFlyingSquirrel_proxy'].name = mainParent + "Proxy"
            bpy.data.objects[mainParent].rotation_euler = (0,0,-1.5708)
            textRotate = (3.1416/2,0,1.5708)
        else:
            print('***loading FlyingSquirrel - DEFAULT***')
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/FSquirrelFlap.blend/Object/", filename="PruebaFlyingSquirrel", link=False)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/FSquirrelFlap.blend/Object/", filename="PruebaFlyingSquirrel_proxy", link=False)
            bpy.ops.object.add(type='EMPTY', view_align=False, location=actors[actor]['position'])
            bpy.data.objects["Empty"].name = mainParent
            bpy.data.objects['PruebaFlyingSquirrel'].parent = bpy.data.objects[mainParent]
            bpy.data.objects['PruebaFlyingSquirrel.001'].parent = bpy.data.objects[mainParent]
            bpy.data.objects['PruebaFlyingSquirrel_proxy'].name = mainParent + "Proxy"
            bpy.data.objects[mainParent].rotation_euler = (0,0,-1.5708)
            textRotate = (3.1416/2,0,1.5708)
    elif actor.startswith("Butterfly"):
        mainParent = str(id) + "Butterfly"
        if actors[actor]['animation'].upper() == 'FLY': #OK
            print('***loading Butterfly - FLY***')
            offset = (0.44,1.22,0.5)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/ButterflyFly.blend/Object/", filename="ButterflyPrueba", link=False)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/ButterflyFly.blend/Object/", filename="Butterfly_proxyPrueba", link=False)
            bpy.ops.object.add(type='EMPTY', view_align=False, location=actors[actor]['position'])
            bpy.data.objects["Empty"].name = mainParent
            bpy.data.objects['ButterflyPrueba'].parent = bpy.data.objects[mainParent]
            bpy.data.objects['Butterfly_proxyPrueba'].name = mainParent + "Proxy"
            bpy.data.objects['Curve'].name = mainParent + "ProxyCurve"
            bpy.data.objects[mainParent].location[0] += offset[0]
            bpy.data.objects[mainParent].location[1] += offset[1]
            bpy.data.objects[mainParent].location[2] += offset[2]
            bpy.data.objects[mainParent].scale = (2, 2, 2)
            textCorrection = 2
        else: #OK
            print('***loading Butterfly - DEFAULT***')
            offset = (0.44,1.22,0.5)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/ButterflyFly.blend/Object/", filename="ButterflyPrueba", link=False)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/ButterflyFly.blend/Object/", filename="Butterfly_proxyPrueba", link=False)
            bpy.ops.object.add(type='EMPTY', view_align=False, location=actors[actor]['position'])
            bpy.data.objects["Empty"].name = mainParent
            bpy.data.objects['ButterflyPrueba'].parent = bpy.data.objects[mainParent]
            bpy.data.objects['Butterfly_proxyPrueba'].name = mainParent + "Proxy"
            bpy.data.objects['Curve'].name = mainParent + "ProxyCurve"
            bpy.data.objects[mainParent].location[0] += offset[0]
            bpy.data.objects[mainParent].location[1] += offset[1]
            bpy.data.objects[mainParent].location[2] += offset[2]
            bpy.data.objects[mainParent].scale = (2, 2, 2)
            textCorrection = 2
    elif actor.startswith("Rabbit"):
        mainParent = str(id) + "Rabbit"
        textOffset=(0,0,2.2)
        if actors[actor]['animation'].upper() == 'JUMP': #OK
            print('***loading Rabbit - JUMP***')
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/BunnyJump.blend/Object/", filename="EmptyBunny", link=False)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/BunnyJump.blend/Object/", filename="Empty_proxyBunny", link=False)
            bpy.ops.object.add(type='EMPTY', view_align=False, location=actors[actor]['position'])
            bpy.data.objects["Empty"].name = mainParent
            bpy.data.objects['Empty_proxyBunny'].name = mainParent + "Proxy"
            bpy.data.objects['EmptyBunny'].parent=bpy.data.objects[mainParent]
            bpy.data.objects['EmptyBunny.001'].parent=bpy.data.objects[mainParent]
        elif actors[actor]['animation'].upper() == 'WALK': #OK
            print('***loading Rabbit - WALK***')
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/BunnyWalk.blend/Object/", filename="RabbitPrueba", link=False)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/BunnyWalk.blend/Object/", filename="Empty_proxy_Prueba", link=False)
            bpy.ops.object.add(type='EMPTY', view_align=False, location=actors[actor]['position'])
            bpy.data.objects["Empty"].name = mainParent
            bpy.data.objects['Empty_proxy_Prueba'].name = mainParent + "Proxy"
            bpy.data.objects['RabbitPrueba'].parent = bpy.data.objects[mainParent]
            bpy.data.objects['RabbitPrueba.001'].parent = bpy.data.objects[mainParent]
        else: #OK
            print('***loading Rabbit - DEFAULT***')
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/BunnyWalk.blend/Object/", filename="RabbitPrueba", link=False)
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/BunnyWalk.blend/Object/", filename="Empty_proxy_Prueba", link=False)
            bpy.ops.object.add(type='EMPTY', view_align=False, location=actors[actor]['position'])
            bpy.data.objects['Empty'].name = mainParent
            bpy.data.objects['Empty_proxy_Prueba'].name = mainParent + "Proxy"
            bpy.data.objects['RabbitPrueba'].parent = bpy.data.objects[mainParent]
            bpy.data.objects['RabbitPrueba.001'].parent = bpy.data.objects[mainParent]
    elif actor.startswith("Bird"):
        mainParent = str(id) + "Bird"
        if actors[actor]['animation'].upper() == 'FLAP': #OK
            print('***loading Bird - FLAP***')
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/BirdSing.blend/Object/", filename="Pajarito_proxy", link=False, instance_groups=False)
            bpy.ops.object.add(type='EMPTY', view_align=False, location=actors[actor]['position'])
            bpy.data.objects["Empty"].name = mainParent
            #bpy.data.objects['Pajarito_proxy'].name = mainParent + "Proxy"
            bpy.data.objects['Pajarito'].parent = bpy.data.objects[mainParent]
            bpy.data.objects['Pajarito_proxy'].parent = bpy.data.objects[mainParent]
        else: #OK
            print('***loading Bird - DEFAULT***')
            bpy.ops.wm.link_append(directory="/var/www/production/scenes/pyl/BirdSing.blend/Object/", filename="Pajarito_proxy", link=False, instance_groups=False)
            bpy.ops.object.add(type='EMPTY', view_align=False, location=actors[actor]['position'])
            bpy.data.objects["Empty"].name = mainParent
            #bpy.data.objects['Pajarito_proxy'].name = mainParent + "Proxy"
            bpy.data.objects['Pajarito'].parent = bpy.data.objects[mainParent]
            bpy.data.objects['Pajarito_proxy'].parent = bpy.data.objects[mainParent]
    elif actor.startswith("Apple"): #OK
        print('***loading Apple - DEFAULT***')
        offset = (-0.5,0,0)
        mainParent = str(id) + "Apple"
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/models/apple.blend/Object/", filename="apple1", link=False)
        bpy.ops.object.add(type='EMPTY', view_align=False, location=actors[actor]['position'])
        bpy.data.objects["Empty"].name = mainParent
        bpy.data.objects['apple1'].scale = (2, 2, 2)
        bpy.data.objects['apple1'].parent = bpy.data.objects[mainParent]
        bpy.data.objects[mainParent].location[0] += offset[0]
        bpy.data.objects[mainParent].location[1] += offset[1]
        bpy.data.objects[mainParent].location[2] += offset[2]
        #bpy.data.objects[mainParent].scale = (2, 2, 2)
        #textCorrection = 2
    else: #OK
        print('***loading DEFAULT - DEFAULT***')
        mainParent = str(id) + "PearXL"
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/models/pear.blend/Object/", filename="pearXL", link=False)
        bpy.ops.object.add(type='EMPTY', view_align=False, location=actors[actor]['position'])
        bpy.data.objects["Empty"].name = mainParent
        bpy.data.objects["pearXL"].scale = (2, 2, 2)
        bpy.data.objects["pearXL"].parent = bpy.data.objects[mainParent]
        #bpy.context.scene.objects.active = bpy.data.objects['pearXL']
        #bpy.context.object.scale = (2,2,2)
        #textCorrection = 2

    #textName = mainParent + "Animation"
    #textOffsets = ( (textOffset[0]-offset[0])/textCorrection , (textOffset[1]-offset[1])/textCorrection , (textOffset[2]-offset[2])/textCorrection)
    #textScales = (textScale[0]/textCorrection , textScale[1]/textCorrection , textScale[2]/textCorrection)
    #bpy.ops.object.text_add( location=textOffsets , rotation=textRotate )
    #bpy.data.objects["Text"].name = textName
    #bpy.data.objects[textName].parent = bpy.data.objects[mainParent]
    #bpy.data.objects[textName].data.align = 'CENTER'
    #bpy.data.objects[textName].data.bevel_depth = 0.04
    #bpy.data.objects[textName].scale = textScales
    #if actors[actor]['animation'] == '':
    #    bpy.data.objects[textName].data.body = "Default"
    #    bpy.data.objects[textName].location[0] -= 0.5
    #else:
    #    bpy.data.objects[textName].data.body = actors[actor]['animation'].upper();

    bpy.data.objects[mainParent].select = True
    bpy.context.scene.objects.active = bpy.data.objects[mainParent]
    for n in range(len(actors[actor]['trajectory'])):
        bpy.data.scenes["Scene"].frame_current=n
        bpy.data.objects[mainParent].location[0] = offset[0] + actors[actor]['trajectory'][n][0]
        bpy.data.objects[mainParent].location[1] = offset[1] + actors[actor]['trajectory'][n][1]
        bpy.data.objects[mainParent].location[2] = offset[2] + actors[actor]['trajectory'][n][2]
        bpy.data.objects[mainParent].keyframe_insert(data_path="location", frame=n)
    bpy.data.scenes["Scene"].frame_current=1
    bpy.data.objects[mainParent].location = actors[actor]['position']
    bpy.data.objects[mainParent].location[0] += offset[0]
    bpy.data.objects[mainParent].location[1] += offset[1]
    bpy.data.objects[mainParent].location[2] += offset[2]
    id+=1
    # ob = bpy.context.object
    # ob.name = actors[actor]['asset']
    # ob.location = actors[actor]['position']
    ##ob.location[2] = ob.location[2]+5.0
    # print('Object '+ob.name+' '+str(actors[actor])+'.')
    # print(ob.location) 

    # Voy calculando donde debe quedar la camara (en caso de que no me digan donde de manera explicita) con base en la posicion de cada elemento de la escena:
    # La camara debe estar por sobre el centro del BoundingBox que contiene a todos los elementos, y mirando
    # hacia abajo
    if bb_min is None:
        bb_min = mathutils.Vector(actors[actor]['position'])
    else:
        bb_min[0] = min( bb_min[0] , actors[actor]['position'][0] )
        bb_min[1] = min( bb_min[1] , actors[actor]['position'][1] )
        bb_min[2] = min( bb_min[2] , actors[actor]['position'][2] )

    if bb_max is None:
        bb_max = mathutils.Vector(actors[actor]['position'])
    else:
        bb_max[0] = max( bb_max[0] , actors[actor]['position'][0] )
        bb_max[1] = max( bb_max[1] , actors[actor]['position'][1] )
        bb_max[2] = max( bb_max[2] , actors[actor]['position'][2] )

print('bb_min')
print(bb_min)
print('bb_max')
print(bb_max)

# Escenario actual (screenshot)

# Se carga la captura
img = bpy.data.images.load("/var/www/production/scenes/background.bmp")
# Se crea la textura y se le asigna la imagen
cTex = bpy.data.textures.new('ColorTex', type = 'IMAGE')
cTex.image = img
# Se crea el material
mat = bpy.data.materials.new('TexMat')
mat.use_shadeless = True
mat.preview_render_type = 'FLAT'
# Se asigna la textura al material
mtex = mat.texture_slots.add()
mtex.texture = cTex
mtex.texture_coords = 'WINDOW'
mtex.mapping = 'FLAT'
# Se crea el plano para asignarle el material
bpy.ops.mesh.primitive_plane_add(view_align=False, enter_editmode=False, location=(8, 2, 0), rotation=(3.1416/2, 3.1416, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
bpy.data.objects["Plane"].dimensions= (32,18,0)
bpy.data.objects["Plane"].data.materials.append(mat)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.001", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.002", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.003", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.004", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.005", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.006", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.007", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.008", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.009", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.010", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.011", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.012", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="lightbeam", link=False)

# Escenario actual (modelos)
'''
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="matte_hills", link=False)
bpy.context.scene.objects.active = bpy.data.objects['matte_hills']
bpy.context.object.scale = (0.055,0.055,0.07)
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(0.0,0.0,-0.4622))
print('Matte_hills')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="matte_haze", link=False)
bpy.context.scene.objects.active = bpy.data.objects['matte_haze']
bpy.context.object.scale = (0.051,0.051,0.051)
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(0.0,0.0,59.4459))
print('Matte_haze')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="matte_sky", link=False)
bpy.context.scene.objects.active = bpy.data.objects['matte_sky']
bpy.context.object.scale = (0.05,0.05,0.05)
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(0.0,0.0,-0.6622))
print('Matte_sky')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="matte_clouds", link=False)
bpy.context.scene.objects.active = bpy.data.objects['matte_clouds']
bpy.context.object.scale = (0.055,0.055,0.07)
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(0.0,0.0,57.8609))
bpy.ops.transform.rotate(value=(-0.5235,), constraint_axis=(False,False,True))
print('Matte_clouds')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="smellingfield_ground", link=False)
bpy.context.scene.objects.active = bpy.data.objects['smellingfield_ground']
bpy.context.object.scale = (1.0,1.0,1.0)
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(11.5,0.0,-0.5))
print('Smelling_Field_Ground')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="kite_trees_big1", link=False)
bpy.context.scene.objects.active = bpy.data.objects['kite_trees_big1']
bpy.context.object.scale = (0.1,0.1,0.15)
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(128.0,-15.0,2.24))
print('Kite_Trees_Big')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.001", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.002", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.003", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.004", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.005", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.006", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.007", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.008", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.009", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.010", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.011", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="Lamp.012", link=False)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/scenes/03_apple/02_04.blend/Object/", filename="lightbeam", link=False)
'''

# Escenario viejo
'''
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/sets/intro.blend/Object/", filename="ground", link=False)
bpy.context.scene.objects.active = bpy.data.objects['ground']
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(7.0,0.0,-2.005))
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/sets/intro.blend/Object/", filename="grass_ground", link=False)
bpy.context.scene.objects.active = bpy.data.objects['grass_ground']
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(7.0,0.0,-2.105))
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/sets/intro.blend/Object/", filename="matte_forest_treeA", link=False)
bpy.context.scene.objects.active = bpy.data.objects['matte_forest_treeA']
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(-20.0,-76.0,10.4883))
print('Matte_Forest_treeA')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/sets/intro.blend/Object/", filename="matte_forest_treeB", link=False)
bpy.context.scene.objects.active = bpy.data.objects['matte_forest_treeB']
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(-16.0,-51.0,5.3335))
print('Matte_Forest_treeB')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/sets/intro.blend/Object/", filename="matte_forest_treeC", link=False)
bpy.context.scene.objects.active = bpy.data.objects['matte_forest_treeC']
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(0.0,-54.0,7.9643))
print('Matte_Forest_treeC')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/sets/intro.blend/Object/", filename="matte_forest_treeD", link=False)
bpy.context.scene.objects.active = bpy.data.objects['matte_forest_treeD']
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(39.8691,-196.2142,22.3492))
print('Matte_Forest_treeD')
print(bpy.context.object.location)
bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/sets/intro.blend/Object/", filename="matte_forest_treeD", link=False)
bpy.context.scene.objects.active = bpy.data.objects['matte_forest_treeD']
bpy.context.object.lock_location = [False,False,False]
bpy.ops.transform.translate(value=(36.8691,-196.2142,22.3492))
print('Matte_Forest_treeD')
print(bpy.context.object.location)
'''

# Agregar la camara
textName = "MainMessage"
textOffsets = ( (bb_max[0] + bb_min[0] ) / 2 , bb_max[1] , 2.5)
#textScales = (textScale[0]/textCorrection , textScale[1]/textCorrection , textScale[2]/textCorrection)
bpy.ops.object.text_add( location=textOffsets , rotation=(3.1416/2,0,0) )
bpy.data.objects["Text"].name = textName
#bpy.data.objects[textName].parent = bpy.data.objects[mainParent]
bpy.data.objects[textName].data.align = 'CENTER'
bpy.data.objects[textName].data.bevel_depth = 0.04
bpy.data.objects[textName].scale = (0.3,0.3,0.3)
bpy.data.objects[textName].data.body = " ";
if RENDER_VIDEO:
    messageText = ""
    wordsPerLine = 5
    config = configparser.ConfigParser()
    config.read(OUTPUT_DIR + '/mail.properties')
    messageWords = config['section_name']['html'].replace('nwln','\n').split()
    for n in range(len(messageWords)):
        if (n % wordsPerLine == 0):
            messageText=messageText+'\n'
        messageText=messageText + messageWords[n] + " "
    bpy.data.objects[textName].data.body = messageText;

bpy.ops.object.lamp_add()
lamp = bpy.context.object

if (camaraExist == 0):
    bpy.ops.object.camera_add()
    camera = bpy.data.objects["Camera"]
    camera.location[0] = ( bb_max[0] + bb_min[0] ) / 2
    camera.location[1] = ( bb_max[1] + bb_min[1] ) / 2 + 2*OFFSET_CAMERA_DISTANCE
    camera.location[2] = DEFAULT_CAMERA_ALTITUDE

print('la camara quedo en ' + str(camera.location[0]) + ', ' + str(camera.location[1]) + ', ' + str(camera.location[2]))

bpy.context.scene.camera = camera

#Agregar lampara a la escena
lamp.location = mathutils.Vector(actors[actor]['position'])
lamp.location[0] = ( bb_max[0] + bb_min[0] ) / 2
lamp.location[1] = ( (bb_max[1] + bb_min[1]) - 5 ) / 2
lamp.location[2] = actors[actor]['position'][2] + 5

# Agregar Rotaciones de Camara
print ('Rotatin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

rx = 75.0
#rx = 90.0
ry = 0.0
rz = 0.0
pi = 3.14159265

camera.rotation_mode = 'XYZ'
camera.rotation_euler[0] = rx*(pi/180.0)
camera.rotation_euler[1] = ry*(pi/180.0)
camera.rotation_euler[2] = rz*(pi/180.0)

# Agregar Fondo de la Escena - Cielo
world = bpy.context.scene.world
# World settings
world.use_sky_blend = True
world.ambient_color = (0.030, 0.030, 0.030)
world.horizon_color = (0.0883, 0.272, 0.704)
world.zenith_color = (0.04, 0.0, 0.04)
'''
# Stars
sset = world.star_settings
sset.use_stars = True
sset.average_separation = 7.8
sset.color_random = 1.0
sset.distance_min = 0.7
sset.size = 10

# Environment lighting
wset = world.light_settings
wset.use_environment_light = True
wset.environment_color = 'PLAIN'
wset.environment_energy = 1.0
wset.use_ambient_occlusion = True
wset.ao_blend_type = 'MULTIPLY'
wset.ao_factor = 0.8
wset.gather_method = 'APPROXIMATE'
'''
# Realizar animaciones

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = NUM_FRAMES_ANIMATION



################################################################################
#
# IMPLEMENTACION SONIDO
#
################################################################################
'''
# Defino esquema de propagacion
bpy.context.scene.audio_distance_model = 'EXPONENT_CLAMPED'
bpy.context.scene.audio_doppler_speed = 343.3
bpy.context.scene.audio_doppler_factor = 1

# FOLEY
i = 0;
print ('Foleyin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

score = xml.dom.minidom.parse(SCORE_XML_FILENAME) # Creamos arbol XML score
for actor in actors.keys():
    for tagScore in score.getElementsByTagName('score'): # score
        for tagActor in tagScore.getElementsByTagName('actor'): # actor
            if actors[actor]['asset'] == tagActor.getAttribute('asset'): # hay un actor que en el score se llama igual
                #speakerName = str(id) + actors[actor]['asset']
                # creo speaker con su sonido
                fileName = os.path.basename( tagActor.getElementsByTagName('sound')[0].getAttribute('value') )
                bpy.context.scene.frame_current = 1 # posicion en timeline donde quiero que se escuche el speaker
                print ('Cargando el sonido ' + '../../' + tagActor.getElementsByTagName('sound')[0].getAttribute('value'))
                bpy.ops.object.speaker_add(location=actors[actor]['position']) # agregamos speaker en posicion en escena
                #bpy.data.objects["Speaker"].name = speakerName
                bpy.ops.sound.open_mono(filepath= '../../' + tagActor.getElementsByTagName('sound')[0].getAttribute('value')) # agregamos sonido
                #time.sleep(3.0) #Una pausa por la forma tan terrible que se maneja el stack del sonido....

                print ('Agregando el sonido ' + str(i) + ': '+ bpy.data.sounds[fileName].name)
                bpy.data.speakers[i].sound = bpy.data.sounds[fileName] # Se asigna el sonido cargado al parlante

                # uso propiedades para sonorizacion 3D
                bpy.data.speakers[i].volume_min = 0 # valor mínimo de volumen no importa qué tan lejos esté el speaker
                bpy.data.speakers[i].volume_max = 1
                bpy.data.speakers[i].attenuation = 3
                bpy.data.speakers[i].distance_reference = 5

                # creamos foley
                for tagFoley in tagActor.getElementsByTagName('foley'): # actor
                    for tagSoundFoley in tagFoley.getElementsByTagName('foley'): # actor
                        print ('Agregando el foley ' + tagSoundFoley.getAttribute('value'))
                        bpy.context.scene.frame_current = int( tagSoundFoley.getAttribute('frame') ) # posicion en timeline donde quiero que se escuche el speaker
                        bpy.ops.object.speaker_add(location=actors[actor]['position']) # agregamos speaker en posicion en escena
                        bpy.ops.sound.open_mono(filepath=tagSoundFoley.getAttribute('value')) # agregamos sonido
                        bpy.data.speakers[i].sound = bpy.data.sounds[fileName] # extraemos de los sonidos de escena

# uso propiedades para sonorizacion 3D
                        bpy.data.speakers[i].volume_min = 0 # valor mínimo de volumen no importa qué tan lejos esté el speaker
                        bpy.data.speakers[i].volume_max = 1
                        bpy.data.speakers[i].attenuation = 3
                        bpy.data.speakers[i].distance_reference = 5

                # agrego un parent para que cuando el parent cambie de posicion el speaker se escuche en esa posicion
                #bpy.data.speakers[i].parent = actors[actor]['model'] # El parent funciona

                # deselecciono todo en el editor nla
                # esto es porque necesito en los demas speakers hacer copias de uns trip de sonido en el mismo track
                #for soundTrack in bpy.context.active_object.animation_data.nla_tracks:
                    #soundTrack.select = False
                    #for stripOfTrack in soundTrack.strips:
                        #stripOfTrack.select = False
                i = i + 1
'''




# Fondo

print ('Ambientin at:')
print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print ('################################################################################')

x = 0 #TODO: ¿Que pasa si inicializo en una sola linea?
y = 0
z = 0
#i = len(bpy.data.speakers)

bpy.context.scene.frame_current = 1

# }


# Renderizar la imagen o el video
# {
bpy.context.scene.camera = camera
bpy.context.scene.render.parts_x = 1
bpy.context.scene.render.parts_y = 1
bpy.context.scene.render.use_sss = False
    
if RENDER_LOW_QUALITY:
    bpy.context.scene.render.use_raytrace = False
    bpy.context.scene.render.use_envmaps = False
    bpy.context.scene.render.use_textures = True
    bpy.context.scene.render.use_shadows = False
    bpy.context.scene.render.use_antialiasing = False
else:
    bpy.context.scene.render.use_raytrace = True
    bpy.context.scene.render.use_envmaps = False
    bpy.context.scene.render.use_textures = True
    bpy.context.scene.render.use_shadows = True
    bpy.context.scene.render.use_antialiasing = False


if RENDER_VIDEO:
    #Archivo muy grande: bpy.context.scene.render.image_settings.file_format='AVI_JPEG'
    #Archivo 1.3M .dvd: 
    bpy.context.scene.render.image_settings.file_format='FFMPEG'
    bpy.data.scenes["Scene"].render.resolution_x = RESOLUTION_WIDTH
    bpy.data.scenes["Scene"].render.resolution_y = RESOLUTION_HEIGHT
    bpy.data.scenes["Scene"].render.resolution_percentage = RESOLUTION_PERCENTAGE
    bpy.data.scenes["Scene"].frame_step = FRAME_STEP
    #NO funciona: bpy.context.scene.render.image_settings.file_format='AVICODEC'
    #no lo probe: bpy.context.scene.render.image_settings.file_format='XVID'
    #bpy.context.scene.render.image_settings.file_format='THEORA'
    #1.1M avi : bpy.context.scene.render.image_settings.file_format='H264'
    bpy.context.scene.render.filepath = "outputcard.mpg"
    bpy.context.scene.render.ffmpeg.audio_codec = 'MP3'
    bpy.ops.render.render(animation=True)
    #os.rename("output-0001-0300.ogg", "output.ogg")    
else:
    bpy.context.scene.render.image_settings.file_format='PNG'
    bpy.data.scenes["Scene"].render.resolution_x = RESOLUTION_WIDTH
    bpy.data.scenes["Scene"].render.resolution_y = RESOLUTION_HEIGHT
    bpy.data.scenes["Scene"].render.resolution_percentage = RESOLUTION_PERCENTAGE
    bpy.context.scene.render.filepath = "output.png"
    bpy.ops.render.render(write_still=True)

# }
print ('##### FIN #####')
print (strftime('%Y-%m-%d %H:%M:%S', gmtime()))
bpy.ops.wm.save_mainfile(filepath="output.blend", check_existing=False)
