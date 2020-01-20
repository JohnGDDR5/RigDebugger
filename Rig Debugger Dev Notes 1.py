

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

#bl_options explained
bl_options = {"REGISTER", "UNDO",}
#"REGISTER" is to allow the Left-Bottom UI panel to display in the 3D-Viewport
#"UNDO" is to allow undos


##How to access Drivers of different types:
##Shape Keys
bpy.context.object.data.shape_keys.animation_data.drivers[0]
##Pose Bone Drivers
bpy.context.object.animation_data.drivers[18]


##Shape Key Notes:
bpy.context.object.active_shape_key
#Returns bpy.data.shape_keys['Key'].key_blocks["Key 1.L"]

bpy.context.object.active_shape_key_index
#Returns Integer, ex. 1




for i in enumerate(bpy.data.objects['Armature.1'].animation_data.drivers):
    print("%d: Index %d" % (i[0], i[1].array_index))

##Pose Bone Driver Notes:

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

bpy.context.screen.areas[7].spaces[0].cursor_position_x

#bpy.ops.object.mode_set(mode="OBJECT")

for i in enumerate(bpy.context.screen.areas):
    print("%d %s" % (i[0], i[1].type))

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


###Notes for adding an Operator that creates empty Vertex Groups to an Object's Data based on the names of the Armature's bones that are selected

bpy.context.object.vertex_groups.get("Spine") is not None
#Returns Boolean
#Checks if Vertex Group of Bone Name exists

bpy.context.active_pose_bone
#Returns bpy.data.objects['Armature.1'].pose.bones["IK.Hoof.Back.R"]

bpy.context.selected_objects
#Returns [bpy.data.objects['Body.1'], bpy.data.objects['Armature.1']]

bpy.context.selected_pose_bones
#Returns [bpy.data.objects['Armature.1'].pose.bones["IK.Hoof.Back.R"]]

bpy.context.selected_pose_bones_from_active_object
#Returns [bpy.data.objects['Armature.1'].pose.bones["IK.Hoof.Back.R"]]


##Notes for Vertex Mode Brushes, in order to create some kind of operator panel Pi-menu to select brushes faster

bpy.data.brushes['Subtract.Zero'].weight_tool
#Returns 'DRAW'

bpy.context.tool_settings
#Returns bpy.data.scenes['Scene'].tool_settings

bpy.context.tool_settings.weight_paint.brush
#Returns bpy.data.brushes['Subtract']
#Note: This one returns the selected Brush

###Notes for Groups Weight Assign operator

bpy.context.object.vertex_groups.active.name
#Returns name of active Vertex Group of Object: 'Hips'

bpy.context.object.vertex_groups.active_index
#Returns index of active Vertex Group of Object


bpy.context.object.vertex_groups['Thigh.L']

bpy.context.object.vertex_groups['Thigh.L'].index
#Returns the index of the vertex group

bpy.context.object.vertex_groups.new(name="")
#Creates new Vertex Group

bpy.context.object.vertex_groups[4].name
#Returns 'Ear.2.R'

bpy.context.object.data.vertices[0].select
#Returns Boolean, True or False

bpy.context.object.vertex_groups[4].index
#Returns 4, which is the index of the vertex group

len(bpy.context.object.data.vertices[0].groups)
#Returns how many vertex groups a vertice is influenced by


bpy.context.object.data.vertices[0].groups[4].group
#Returns the index of one of the vertex groups that influences this vertex

bpy.context.object.data.vertices[0].groups[0].weight
#Returns Float, ex. 0.5394619703292847 of Vertex in Group

bpy.context.object.vertex_groups[35].weight(0)
#Returns 0.00933530181646347
#Note: This returns the weight of the vertice of index 0, however it will result in a Runtime Error if the vertex isn't in the vertex_group
#Note 2: This value seems to not update after changing it from .data, so use the values from .data instead

bpy.context.object.vertex_groups[4].remove(0)
#Will remove a vertex in the vertex_group

#bpy.context.object.vertex_groups[4].add(index, weight, type)
bpy.context.object.vertex_groups[4].add(0, 1.0, 'REPLACE')
#Adds a vertex to the group with a weight value
#Notes: type option can be 'REPLACE', 'ADD', 'SUBTRACT'


###Python Notes from the Addon

bpy.types.RIG_DEBUGGER_OT_vertex_group_ops.resetSelf()
#resetSelf() is a custom function I made in the operator, this is how you access it.

self.resetSelf(self)
#In a class, the first argument in a function is always self, even if you rename it something else, like "cls", it is still self. This self.resetSelf(self) results in an error, as you don't need to state "self" inside a class function as it is inferred
#Use, self.resetSelf()
