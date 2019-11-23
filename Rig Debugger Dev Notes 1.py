

#Developer Script Version Notes

#Version 1.0000, 8/4/2019

#To do
1. use .startswith() and .split()
if d.data_path.startswith('pose.bones'):
        id = d.data_path.split('"')[1]
        prop = d.data_path.rsplit('.', 1)[1]
        if id == pb.name and prop == 'location':
            break

#New Notes
##############

for i in enumerate(bpy.data.objects['Armature.1'].animation_data.drivers):
    print("%d: Index %d" % (i[0], i[1].array_index))

bpy.context.object.pose.bones["Hoof.Front.Roll.Back.L"].rotation_euler[2]
#Adds a driver
bpy.context.object.pose.bones["Hoof.Front.Roll.Back.L"].driver_add('rotation_euler', 2)

bpy.context.object.animation_data.drivers[0].driver_add('rotation_euler', 2)

bruh = bpy.context.object.pose.bones["Hoof.Front.Roll.Back.L"].driver_add('rotation_euler', 2).driver
bruh.type = 'SCRIPTED'

bpy.context.object.animation_data.drivers[17].keyframe_points[0].interpolation
#Returns 'BEZIER'

.insert()
FCurveKeyframePoints.insert(frame, value, options=set(), keyframe_type='KEYFRAME')

bpy.context.object.animation_data.drivers[17].keyframe_points.insert(0, 0.0)
bpy.context.object.animation_data.drivers[17].keyframe_points.insert(1, 1.0)

bpy.context.object.animation_data.drivers[18].convert_to_keyframes()


bpy.data.objects['Armature.1'].animation_data.drivers[0].data_path
#Returns driver's bone 'pose.bones["Hoof.Front.Roll.Back.L"].rotation_euler'

bpy.data.objects['Armature.1'].animation_data.drivers[1].array_index
#Returns index of array of data_path, either 0,1,2 for X,Y,Z

bpy.data.objects['Armature.1'].animation_data.drivers[0].driver.expression
#Returns a string '-(var*RollM) if (var < 0) else False'

bpy.context.object.animation_data.drivers[0].driver.type
#Returns 'SCRIPTED', 'AVERAGE', 'SUM', 'SCRIPTED', 'MIN', 'MAX' 

bpy.context.object.animation_data.drivers[0].driver.use_self
#Returns boolean, False or True

len(bpy.data.objects['Armature.1'].animation_data.drivers)
#Returns number of drivers in the object

bpy.data.objects['Armature.1'].animation_data.drivers[0].driver.variables[0].name
#Returns the DriverVariable name of the Driver 'var'

bpy.data.objects['Armature.1'].animation_data.drivers[0].driver.variables[0].type
#Returns 'TRANSFORMS', 'SINGLE_PROP', 'ROTATION_DIFF', 'LOC_DIFF'

bpy.data.objects['Armature.1'].animation_data.drivers[0].driver.variables[0].targets[0].id
#Returns Object pointer bpy.data.objects['Armature.1']

bpy.context.object.animation_data.drivers[0].driver.variables[1].targets[0].id_type
#Returns the Object type, such as 'ARMATURE'

bpy.data.objects['Armature.1'].animation_data.drivers[0].driver.variables[0].targets[0].bone_target
#Returns bone name 'Hoof.Front.Roll.L'

bpy.data.objects['Armature.1'].animation_data.drivers[0].driver.variables[1].targets[0].data_path
#Returns String '["RollMultiplication"]'
#Note: Only returns value other than '' if Variable type is 'SINGLE_PROP'


bpy.context.object.animation_data.drivers[0].driver.variables[0].targets[0].transform_type
#Returns 'ROT_X'

bpy.context.object.animation_data.drivers[0].driver.variables[0].targets[0].transform_space
#Returns 'LOCAL_SPACE'

bpy.context.object.animation_data.drivers[0].driver.variables[0].targets[0].rotation_mode
#Returns 'AUTO'


bpy.data.objects['Armature.1'].animation_data.drivers[0].extrapolation
#Returns extrapolation 'LINEAR'

bpy.data.objects['Armature.1'].animation_data.drivers[0].select
#Returns boolean True if selected

bpy.data.objects['Armature.1'].animation_data.drivers[0].lock
bpy.data.objects['Armature.1'].animation_data.drivers[0].mute
bpy.data.objects['Armature.1'].animation_data.drivers[0].hide

bpy.data.objects['Armature.1'].animation_data.drivers[0].modifiers[0]
#Returns the modifier of driver if one is added.

bpy.data.objects['Armature.1'].animation_data.drivers[0].color_mode
#Returns 'AUTO_RAINBOW'
#Note: I couldn't find documentation of this in the API

bpy.data.objects['Armature.1'].animation_data.drivers[0].color
#Returns a color Color((1.0, 0.3999999761581421, 0.3999999761581421))



##############
#Old Notes
bpy.context.scene.collection.children['Collection 3']
Returns bpy.data.collections['Collection 3']

bpy.data.objects['Cube'].data.copy()
scene.collection.objects.link(ob)

#Copied from ResSwitch TOP
object = bpy.data.objects[obData.pose.bones[i.name].custom_shape.name]
#Checks if object was an Empty, since Empty types don't have a data.copy()
if object.type != "EMPTY":
    object_copy = object.data.copy()
else:
    object_copy = object.data
    emptyDrawType = object.empty_draw_type

ob = bpy.data.objects.new(str(object.name), object_copy)
#Links the duplicated object in the scene
scene.objects.link(ob)
#Copied from ResSwitch BOTTOM

bpy.context.object.users_collection
#Returns: (bpy.data.collections['Bruh'], bpy.data.collections['Cube.002'], bpy.data.collections['Cube.003'])

bpy.context.selected_objects[0].users_collection
#Returns: (bpy.data.collections['Bruh'], bpy.data.collections['Cube.002'], bpy.data.collections['Cube.003'])

bpy.context.selected_objects[0].users_collection[0].objects.unlink()

#bpy.context.object.local_view_get()
#bpy.context.screen.areas[5].type
#bpy.context.screen.areas[5].spaces.active.lens
#bpy.context.screen.areas[5].spaces[0].lens

#bpy.context.screen.areas[5].spaces[0].local_view is not None

#bpy.ops.object.mode_set(mode="OBJECT")

#IM_Props.
    #collection_parent:
    #collection_active: 
    #collections:
        #collection:
        #object:
        #duplicates:
        #recent:
        
"""
ob = bpy.context.object
if not ob.select_get():
    ob.select_set(True) """
    
bpy.context.preferences.addons[0]
#returns the activated Addons the User has