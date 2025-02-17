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


POSITION_SCALE_W = 16
POSITION_SCALE_H = 8
DEFAULT_CAMERA_ALTITUDE = 12 
FRAME_STEP = 2
NUM_POINTS_CURVE = 5
NUM_FRAMES_ANIMATION = 2

import os

MODELS_PATH = '/var/www/pyl2/VideoGenerator'
RENDER_LOW_QUALITY = "True"
RENDER_VIDEO = os.getenv('RENDER_VIDEO') == "True"
SCRIPT_XML_FILENAME = os.getenv('SCRIPT_XML_FILENAME')
SCORE_XML_FILENAME = os.getenv('SCORE_XML_FILENAME')

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
for actor in actors.keys():
    if actors[actor]['asset'] == 'SBCamera':
        continue
    if actor.startswith("Chinchilla"):
	#quedo con el nombre invertido Chinchilla<->Squirrel
        bpy.ops.wm.link_append(directory="/home/jm.moreno743/production/scenes/pyl/ChinchillaEat.blend/Object/", filename="chinchillaPrueba", link=False)
        bpy.ops.wm.link_append(directory="/home/jm.moreno743/production/scenes/pyl/ChinchillaEat.blend/Object/", filename="chinchillaPrueba.001", link=False)
        bpy.ops.wm.link_append(directory="/home/jm.moreno743/production/scenes/pyl/ChinchillaEat.blend/Object/", filename="chinchillarigPrueba", link=False)
        bpy.data.objects["chinchillarigPrueba"].delta_location = actors[actor]['position']
        bpy.context.scene.objects.active = bpy.data.objects['chinchillaPrueba']
        bpy.context.object.scale = (1.0,1.0,1.0)
    elif actor.startswith("Squirrel"):
        bpy.ops.wm.link_append(directory="/home/jm.moreno743/production/scenes/pyl/SquirrelClap.blend/Object/", filename="SquirrelPrueba", link=False)
        bpy.ops.wm.link_append(directory="/home/jm.moreno743/production/scenes/pyl/SquirrelClap.blend/Object/", filename="SquirrelPrueba.001", link=False)
        bpy.ops.wm.link_append(directory="/home/jm.moreno743/production/scenes/pyl/SquirrelClap.blend/Object/", filename="Squirrel_proxyPrueba", link=False)
        bpy.data.objects["SquirrelPrueba"].location = actors[actor]['position']
        bpy.data.objects["SquirrelPrueba"].location[0] -= 1
        bpy.data.objects["SquirrelPrueba"].location[2] = 0
        bpy.data.objects["SquirrelPrueba.001"].location = actors[actor]['position']
        bpy.data.objects["SquirrelPrueba.001"].location[0] -=  1
        bpy.data.objects["SquirrelPrueba.001"].location[2] = 0
        bpy.data.objects["Squirrel_proxyPrueba"].location = actors[actor]['position']
        bpy.data.objects["Squirrel_proxyPrueba"].location[0] -= 1
        bpy.data.objects["Squirrel_proxyPrueba"].location[2] = 0
        bpy.context.scene.objects.active = bpy.data.objects['SquirrelPrueba']
        bpy.context.object.scale = (1.0,1.0,1.0)
    elif actor.startswith("FlyingSquirrel"):
        bpy.ops.wm.link_append(directory="/home/jm.moreno743/production/scenes/pyl/FSquirrelFlap.blend/Object/", filename="PruebaFlyingSquirrel", link=False)
        bpy.ops.wm.link_append(directory="/home/jm.moreno743/production/scenes/pyl/FSquirrelFlap.blend/Object/", filename="PruebaFlyingSquirrel.001", link=False)
        bpy.ops.wm.link_append(directory="/home/jm.moreno743/production/scenes/pyl/FSquirrelFlap.blend/Object/", filename="PruebaFlyingSquirrel_proxy", link=False)
        bpy.data.objects["PruebaFlyingSquirrel"].location = actors[actor]['position']
        bpy.data.objects["PruebaFlyingSquirrel"].location[2] = 3
        bpy.data.objects["PruebaFlyingSquirrel.001"].location = actors[actor]['position']
        bpy.data.objects["PruebaFlyingSquirrel.001"].location[2] = 3
        bpy.data.objects["PruebaFlyingSquirrel_proxy"].location = actors[actor]['position']
        bpy.data.objects["PruebaFlyingSquirrel_proxy"].location[2] = 3
        bpy.context.scene.objects.active = bpy.data.objects['PruebaFlyingSquirrel']
        bpy.context.object.scale = (1.0,1.0,1.0)
    elif actor.startswith("Butterfly"):
        bpy.ops.wm.link_append(directory="/home/jm.moreno743/production/scenes/pyl/ButterflyFly.blend/Object/", filename="ButterflyPrueba", link=False)
        bpy.ops.wm.link_append(directory="/home/jm.moreno743/production/scenes/pyl/ButterflyFly.blend/Object/", filename="ButterflyPrueba.001", link=False)
        bpy.ops.wm.link_append(directory="/home/jm.moreno743/production/scenes/pyl/ButterflyFly.blend/Object/", filename="Butterfly_proxyPrueba", link=False)
        bpy.data.objects["ButterflyPrueba"].location[0] = 3
        bpy.data.objects["ButterflyPrueba"].location[1] = 3
        bpy.data.objects["ButterflyPrueba"].location[2] = 3
        #bpy.data.objects["ButterflyPrueba.001"].location[0] = 3
        #bpy.data.objects["ButterflyPrueba.001"].location[1] = 3
        #bpy.data.objects["ButterflyPrueba.001"].location[2] = 3
        #bpy.data.objects["Butterfly_proxyPrueba"].location[0] = 3
        #bpy.data.objects["Butterfly_proxyPrueba"].location[1] = 3
        #bpy.data.objects["Butterfly_proxyPrueba"].location[2] = 3
        #bpy.context.scene.objects.active = bpy.data.objects['ButterflyPrueba']
        #bpy.context.object.scale = (10.0,10.0,10.0)
        
        #bpy.ops.wm.link_append(directory="/home/jm.moreno743/production/scenes/pyl/ButterflyFly.blend/Object/", filename="ButterflyPrueba", link=False)
        #bpy.ops.wm.link_append(directory="/home/jm.moreno743/production/scenes/pyl/ButterflyFly.blend/Object/", filename="ButterflyPrueba.001", link=False)
        #bpy.ops.wm.link_append(directory="/home/jm.moreno743/production/scenes/pyl/ButterflyFly.blend/Object/", filename="Butterfly_proxyPrueba", link=False)
        #bpy.data.objects["ButterflyPrueba"].location = actors[actor]['position']
        #bpy.data.objects["ButterflyPrueba"].location[2] = 3
        #bpy.data.objects["ButterflyPrueba.001"].location = actors[actor]['position']
        #bpy.data.objects["ButterflyPrueba.001"].location[2] = 3
        #bpy.data.objects["Butterfly_proxyPrueba"].location = actors[actor]['position']
        #bpy.data.objects["Butterfly_proxyPrueba"].location[2] = 3
        #bpy.context.scene.objects.active = bpy.data.objects['ButterflyPrueba']
        #bpy.context.object.scale = (10.0,10.0,10.0)
    elif actor.startswith("Rabbit"):
        bpy.ops.wm.link_append(directory="/home/jm.moreno743/production/scenes/02_rabbit/01_practice.blend/Object/", filename="Conejo", link=False)
        bpy.ops.wm.link_append(directory="/home/jm.moreno743/production/scenes/02_rabbit/01_practice.blend/Object/", filename="Conejo_Mov", link=False)
        bpy.data.objects["Conejo"].location = actors[actor]['position']
        bpy.data.objects["Conejo"].location[0] -= 2
        bpy.data.objects["Conejo"].location[2] = 0
        bpy.data.objects["Conejo_Mov"].location = actors[actor]['position']
        bpy.data.objects["Conejo_Mov"].location[0] -= 2
        bpy.data.objects["Conejo_Mov"].location[2] = 0
        bpy.context.scene.objects.active = bpy.data.objects['Conejo']
        bpy.context.object.scale = (1.0,1.0,1.0)
    elif actor.startswith("Bird"):
        bpy.ops.wm.link_append(directory="/home/jm.moreno743/production/scenes/pyl/bird001.blend/Object/", filename="Pajarito", link=False, instance_groups=False)
        bpy.ops.wm.link_append(directory="/home/jm.moreno743/production/scenes/pyl/bird001.blend/Object/", filename="Pajarito_proxy", link=False, instance_groups=False)
        bpy.data.objects["Pajarito"].location = actors[actor]['position']
        bpy.data.objects["Pajarito.001"].location = actors[actor]['position']
        bpy.data.objects["Pajarito_proxy"].location = actors[actor]['position']
        bpy.context.scene.objects.active = bpy.data.objects['Pajarito']
    elif actor.startswith("Apple"):
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/models/apple.blend/Object/", filename="apple1", link=False)
        bpy.data.objects["apple1"].location = actors[actor]['position']
        bpy.context.scene.objects.active = bpy.data.objects['apple1']
        bpy.context.object.scale = (2, 2, 2)
    else:
        bpy.ops.wm.link_append(directory=MODELS_PATH + "/models/pear.blend/Object/", filename="pearXL", link=False)
        bpy.data.objects["pearXL"].location = actors[actor]['position']
        bpy.context.scene.objects.active = bpy.data.objects['pearXL']
        bpy.context.object.scale = (2.0,2.0,2.0)
	
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
    
# Crear el piso
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
'''bpy.ops.wm.link_append(directory=MODELS_PATH + "/production/sets/intro.blend/Object/", filename="ground", link=False)
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
print(bpy.context.object.location)'''

# Agregar la camara

bpy.ops.object.camera_add()	
camera = bpy.data.objects["Camera"]
bpy.ops.object.lamp_add()
lamp = bpy.context.object
if 'SBCamera' in actors:
    camera.location = actors['SBCamera']['position']
    camera.location[1] += 0.5
    camera.location[1] -= 4
else:
    camera.location[0] = ( bb_max[0] + bb_min[0] ) / 2
    camera.location[1] = ( bb_max[1] + bb_min[1] ) / 2 - 12
    #camera.location[0] = 4
    #camera.location[1] = -11
camera.location[2] = 3
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

# Realizar animaciones

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = NUM_FRAMES_ANIMATION



################################################################################
#
# IMPLEMENTACION SONIDO
#
################################################################################

# Defino esquema de propagacion
bpy.context.scene.audio_distance_model = 'EXPONENT_CLAMPED'
bpy.context.scene.audio_doppler_speed = 343.3
bpy.context.scene.audio_doppler_factor = 1



# score = xml.dom.minidom.parse(SCORE_XML_FILENAME)

# Crear el sonido de ambiente
# for xmlScore in score.getElementsByTagName('score'):
#	for xmlAmbient in xmlScore.getElementsByTagName('scene'):
#		bpy.ops.sequencer.sound_strip_add(filepath=xmlAmbient.getAttribute('value'), frame_start=1, channel=1)

# i = 0;
# print ('Foleyin at:')
# print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
# print ('################################################################################')

# score = xml.dom.minidom.parse(SCORE_XML_FILENAME) # Creamos arbol XML score
# for actor in actors.keys():
    # for tagScore in score.getElementsByTagName('score'): # score
        # for tagActor in tagScore.getElementsByTagName('actor'): # actor
            # if actors[actor]['asset'] == tagActor.getAttribute('asset'): # hay un actor que en el score se llama igual

                # # creo speaker con su sonido
                # bpy.context.scene.frame_current = 1 # posicion en timeline donde quiero que se escuche el speaker
                # print ('Agregando el sonido ' + tagActor.getElementsByTagName('sound')[0].getAttribute('value'))
                # bpy.ops.object.speaker_add(location=actors[actor]['position']) # agregamos speaker en posicion en escena
                # bpy.ops.sound.open_mono(filepath=tagActor.getElementsByTagName('sound')[0].getAttribute('value')) # agregamos sonido
                # bpy.data.speakers[i].sound = bpy.data.sounds[i] # extraemos de los sonidos de escena

                # # uso propiedades para sonorizacion 3D
                # bpy.data.speakers[i].volume_min = 0 # valor mínimo de volumen no importa qué tan lejos esté el speaker
                # bpy.data.speakers[i].volume_max = 1
                # bpy.data.speakers[i].attenuation = 3
                # bpy.data.speakers[i].distance_reference = 5

				# # creamos foley
                # for tagFoley in tagActor.getElementsByTagName('foley'): # actor
                    # for tagSoundFoley in tagFoley.getElementsByTagName('foley'): # actor
                        # print ('Agregando el foley ' + tagSoundFoley.getAttribute('value'))
                        # bpy.context.scene.frame_current = int( tagSoundFoley.getAttribute('frame') ) # posicion en timeline donde quiero que se escuche el speaker
                        # bpy.ops.object.speaker_add(location=actors[actor]['position']) # agregamos speaker en posicion en escena
                        # bpy.ops.sound.open_mono(filepath=tagSoundFoley.getAttribute('value')) # agregamos sonido
                        # bpy.data.speakers[i].sound = bpy.data.sounds[i] # extraemos de los sonidos de escena

# # uso propiedades para sonorizacion 3D
                        # bpy.data.speakers[i].volume_min = 0 # valor mínimo de volumen no importa qué tan lejos esté el speaker
                        # bpy.data.speakers[i].volume_max = 1
                        # bpy.data.speakers[i].attenuation = 3
                        # bpy.data.speakers[i].distance_reference = 5

                # # agrego un parent para que cuando el parent cambie de posicion el speaker se escuche en esa posicion
                # #bpy.data.speakers[i].parent = actors[actor]['model'] # El parent funciona

                # # deselecciono todo en el editor nla
                # # esto es porque necesito en los demas speakers hacer copias de uns trip de sonido en el mismo track
                # #for soundTrack in bpy.context.active_object.animation_data.nla_tracks:
                    # #soundTrack.select = False
                    # #for stripOfTrack in soundTrack.strips:
                        # #stripOfTrack.select = False
                # i = i + 1

# # Fondo

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
    #NO funciona: bpy.context.scene.render.image_settings.file_format='AVICODEC'
    #no lo probe: bpy.context.scene.render.image_settings.file_format='XVID'
    #bpy.context.scene.render.image_settings.file_format='THEORA'
    #1.1M avi : bpy.context.scene.render.image_settings.file_format='H264'
    bpy.context.scene.render.filepath = "output.mpg"
    bpy.context.scene.render.ffmpeg.audio_codec = 'MP3'
    bpy.ops.render.render(animation=True)
    #os.rename("output-0001-0300.ogg", "output.ogg")    
else:
    bpy.context.scene.render.image_settings.file_format='PNG'
    bpy.context.scene.render.filepath = "output.png"
    bpy.ops.render.render(write_still=True)

# }
print ('##### FIN #####')
print (strftime('%Y-%m-%d %H:%M:%S', gmtime()))
bpy.ops.wm.save_mainfile(filepath="output.blend", check_existing=False)
