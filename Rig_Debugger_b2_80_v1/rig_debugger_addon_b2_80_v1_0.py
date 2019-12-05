# ##### BEGIN GPL LICENSE BLOCK #####
#
# Iterate Objects is a workflow addon for easily creating duplicates of objects you're working on and sending them to a unique collection. 
# A kind of version-control system where duplicates function as "snapshots" of the object to be able to have a backup when doing destructive modeling on a mesh object.
#
# Copyright (C) 2019 Juan Cardenas
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Rig Debugger",
    "description": "Workflow Addon for easy debugging/ development of a rig in Blender.",
    "author": "Juan Cardenas (JohnGDDR5)",
    "version": (1, 0), 
    "blender": (2, 80, 0),
    "location": "3D View > Side Bar > Rig Debugger",
    "warning": "In Development",
    "support": "COMMUNITY",
    "category": "Scene"
}

import bpy
        
from bpy.props import *
#from math import pi, radians
#from mathutils import Matrix, Vector, Euler
#import decimal
#import copy
    
#Takes in an object as parameter, and returns a string of variable "icon"
def objectIcon(object):
    scene = bpy.context.scene
    data = bpy.data
    props = scene.RD_Props
    
    #icons = ["OUTLINER_OB_EMPTY", "OUTLINER_OB_MESH", "OUTLINER_OB_CURVE", "OUTLINER_OB_LATTICE", "OUTLINER_OB_META", "OUTLINER_OB_LIGHT", "OUTLINER_OB_IMAGE", "OUTLINER_OB_CAMERA", "OUTLINER_OB_ARMATURE", "OUTLINER_OB_FONT", "OUTLINER_OB_SURFACE", "OUTLINER_OB_SPEAKER", "OUTLINER_OB_FORCE_FIELD", "OUTLINER_OB_GREASEPENCIL", "OUTLINER_OB_LIGHTPROBE"]
    #Object Type
    
    icon = "QUESTION"
    
    dictionary = {
        "MESH": "OUTLINER_OB_MESH",
        "EMPTY": "EMPTY",
        "CAMERA": "OUTLINER_OB_CAMERA",
        "CURVE": "OUTLINER_OB_CURVE",
        "SURFACE": "OUTLINER_OB_SURFACE",
        "META": "OUTLINER_OB_META",
        "FONT": "OUTLINER_OB_FONT",
        "GPENCIL": "OUTLINER_OB_GREASEPENCIL",
        "ARMATURE": "OUTLINER_OB_ARMATURE",
        "LATTICE": "OUTLINER_OB_LATTICE",
        "LIGHT": "OUTLINER_OB_LIGHT",
        "LIGHT_PROBE": "OUTLINER_OB_LIGHTPROBE",
        "SPEAKER": "OUTLINER_OB_SPEAKER",
    }
    
    #If there is an object to see if it has a type
    if object is not None:
        type = object.type
    
        icon = dictionary.get(str(type), "QUESTION")
        
        if icon == "EMPTY":
            if object.empty_display_type != "IMAGE":
                icon = "OUTLINER_OB_EMPTY"
            elif object.empty_display_type == "IMAGE":
                icon = "OUTLINER_OB_IMAGE"
            elif object.field.type != "NONE":
                icon = "OUTLINER_OB_FORCE_FIELD"
                
    return icon

#Checks if a string has ".L, .R, .left, .right" to see if its flippable
def getDirection(string):
    
    case_low = string.lower()
    
    sides = (".l", ".r", ".left", ".right")
    # -1 to check if it changed, since .rfind() returns -1 if not found, 
    side = -1
    #side_new is the new flipped side index to use for sides[]
    side_new = 0
    
    #index is the index .rfind() found the last occurance in the String
    #index = 0
    
    #Only needs to use ".l" and ".r"
    for j in enumerate(sides[0:2]):
        rfound = case_low.rfind( sides[j[0]] )
        
        #if "L" / "R" is between two "." ex. ".L.001"
        between_dots = case_low.find(".", rfound+1)
        
        if rfound > -1:
            #print("rfound: %d" % (rfound))
            if j[1] == ".l":
                if case_low.rfind( ".left", rfound ) > -1:
                    #if last character is "left" or "right", or "left" / "right" is between two "." ex. ".left.001"
                    if rfound + 4 == len(case_low)-1 or between_dots == rfound + 5:
                        side = 2
                        #index = rfound
                        break
                #if last character is "L" or "R", or "L" / "R" is between two "." ex. ".L.001"
                elif rfound + 1 == len(case_low)-1 or between_dots == rfound + 2:
                    side = 0
                    #index = rfound
                    #print("rfound + 1: %d" % (rfound + 1) )
                    #print("len(case_low)-1: %d" % (len(case_low)-1) )
                    break
                else:
                    break
            elif j[1] == ".r":
                #if (rfound+1) == len(string)-1:   
                if case_low.rfind( ".right", rfound ) > -1:
                    #if last character is "left" or "right", or "left" / "right" is between two "." ex. ".right.001"
                    if rfound + 5 == len(case_low)-1 or between_dots == rfound + 6:
                        side = 3
                        #index = rfound
                        break
                #elif rfound + 1 == len(case_low)-1:
                #if last character is "L" or "R", or "L" / "R" is between two "." ex. ".R.001"
                elif (rfound + 1 == len(case_low)-1 ) or between_dots == rfound + 2:
                    side = 1
                    #index = rfound
                    break
                else:
                    break
        else:
            pass
    
    #returns the side to flip
    if side > -1:
        return sides[side]
    else:
        return ""

#Flip names of string with, (".l", ".r", ".left", ".right") upper or lower case.
# the print() functions are commented, uncomment them for debugging.
def flipNames(string):
    
    case_low = string.lower()
    
    #sides = (".l", ".r")
    #sides = (".l", ".L", ".r", ".R", ".left", ".right", ".Left", ".Right")
    sides = (".l", ".r", ".left", ".right")
    # -1 to check if it changed, since .rfind() returns -1 if not found, 
    side = -1
    #side_new is the new flipped side index to use for sides[]
    side_new = 0
    
    #index is the index .rfind() found the last occurance in the String
    index = 0
    
    #Only needs to use ".l" and ".r"
    for j in enumerate(sides[0:2]):
        rfound = case_low.rfind( sides[j[0]] )
        
        #if "L" / "R" is between two "." ex. ".L.001"
        between_dots = case_low.find(".", rfound+1)
        
        if rfound > -1:
            #print("rfound: %d" % (rfound))
            if j[1] == ".l":
                if case_low.rfind( ".left", rfound ) > -1:
                    #if last character is "left" or "right", or "left" / "right" is between two "." ex. ".left.001"
                    if rfound + 4 == len(case_low)-1 or between_dots == rfound + 5:
                        side = 2
                        index = rfound
                        break
                #if last character is "L" or "R", or "L" / "R" is between two "." ex. ".L.001"
                elif rfound + 1 == len(case_low)-1 or between_dots == rfound + 2:
                    side = 0
                    index = rfound
                    #print("rfound + 1: %d" % (rfound + 1) )
                    #print("len(case_low)-1: %d" % (len(case_low)-1) )
                    break
                else:
                    break
            elif j[1] == ".r":
                #if (rfound+1) == len(string)-1:   
                if case_low.rfind( ".right", rfound ) > -1:
                    #if last character is "left" or "right", or "left" / "right" is between two "." ex. ".right.001"
                    if rfound + 5 == len(case_low)-1 or between_dots == rfound + 6:
                        side = 3
                        index = rfound
                        break
                #elif rfound + 1 == len(case_low)-1:
                #if last character is "L" or "R", or "L" / "R" is between two "." ex. ".R.001"
                elif (rfound + 1 == len(case_low)-1 ) or between_dots == rfound + 2:
                    side = 1
                    index = rfound
                    break
                else:
                    break
        else:
            pass
    
    #Switches the side index to the flipped one
    if side > -1:
        if side == 0:
            #case_flip = ".r"
            side_new = 1
        elif side == 1:
            #case_flip = ".l"
            side_new = 0
        elif side == 2:
            side_new = 3
        elif side == 3:
            side_new = 2
            
        #replace = sides[side_new]
            
        #if the "l" or "r" for original string is uppercase, uppercase the letter in "replace" variable
        if string[index+1].isupper():
            
            #
            replace = "." + sides[side_new][1:].capitalize()
            #replace = sides[side_new].capitalize()
            #replace[1].capitalize()
            #replace[1] = replace[1].capitalize()
           
            
        else:
            #The new flipped side
            replace = sides[side_new]
        #Uncomment for debug stuff    
        #print("replace: %s; string: %s" % (str(replace), string) )
            
        # adds text before, then the replace, and then any text that was after the .l or .r
        string = string[:index] + replace + string[index+len(sides[side]):]
        
        return string
    else:
        return ""
        
class RIG_DEBUGGER_OT_Debugging(bpy.types.Operator):
    bl_idname = "rig_debugger.debug"
    bl_label = "Iterate Objects Debugging Operators"
    bl_description = "To assist with debugging and development"
    bl_options = {'UNDO',}
    type: bpy.props.StringProperty(default="DEFAULT")
    #index: bpy.props.IntProperty(default=0, min=0)
    
    def execute(self, context):
        scene = bpy.context.scene
        context = bpy.context
        data = context.object.data
        props = scene.RD_Props
        
        #Fake "Deletes" Iterate Objects without an Object or Collection pointer
        if self.type == "PRINT_ALL":
            
            anim_data = bpy.context.object.animation_data
            direction = ("X", "Y", "Z")
            
            #For the Hidden, Muted, and Locked driver counts
            toggled = [0,0,0]
            
            if anim_data != None:
                for i in enumerate(anim_data.drivers):
                    print("%d: %s [%d]; Path: %s" % (i[0], direction[i[1].array_index], i[1].array_index, i[1].data_path))
                    print("  Hide: %s; Mute: %s; Lock: %s" % (i[1].hide, i[1].mute, i[1].lock))
                    
                    if i[1].hide == True:
                        toggled[0] += 1
                    elif i[1].mute == True:
                        toggled[1] += 1
                    elif i[1].lock == True:
                        toggled[2] += 1
                
                #reportString = "Drivers: %d; Left: %d; Right: %d" % (len(anim_data.drivers), removedObjects, removedCol)
                reportString = "Drivers: %d; Hidden: %d; Muted: %d; Locked: %d" % (len(anim_data.drivers), toggled[0], toggled[1], toggled[2])
                
                print(reportString)
                self.report({'INFO'}, reportString)
            
            else:
                reportString = "Object[%s] has No Drivers" % (bpy.context.object.name)
                
                print(reportString)
                self.report({'INFO'}, reportString)
                
        elif self.type == "PRINT_ADD_DRIVER_TEST":
            
            anim_data = bpy.context.object.animation_data
            direction = ("X", "Y", "Z")
            
            #For the Hidden, Muted, and Locked driver counts
            toggled = [0,0,0]
            
            if anim_data.drivers != None:
                data_path = anim_data.drivers[0].data_path
                print("data_path: %s" % (data_path))
                
                print('"pose.bones": %s' % (str(data_path.startswith('pose.bones'))))
                
                if data_path.startswith('pose.bones') == True:
                    #2 allows for 2 splits in string, meaning 3 strings in the .split() list
                    split = data_path.split('"', 2)
                    #1 allows for 1 splits in string, meaning 2 strings in the .split() list
                    rsplit = data_path.rsplit('.', 1)
                    
                    print("split: %s" % (str(split)))
                    print(" split[1]: %s" % (str(split[1] )))
                    
                    print("rsplit: %s" % (str(rsplit)))
                    print(" rsplit[1]: %s" % (str(rsplit[1] )))
                    #for i in enumerate(anim_data.drivers):
                    
                    print("flipNames: %s" % (flipNames( bpy.context.active_pose_bone.name )) )
                    
                reportString = "Done!"
                
                print(reportString)
                self.report({'INFO'}, reportString)
            
            else:
                reportString = "Object[%s] has No Drivers" % (bpy.context.object.name)
                
                print(reportString)
                self.report({'INFO'}, reportString)
                
        elif self.type == "FLIP_NAMES_TEST":
            ob = bpy.context.object
            anim_data = ob.animation_data
            
            print("\nFlipped Names of:")
            
            if bpy.context.active_pose_bone != None:
                nameNormal = bpy.context.active_pose_bone.name
                nameFlipped = flipNames( nameNormal )
                
                if nameFlipped != "":
                    print("Active Pose Bone: %s" % (nameFlipped) )
                else:
                    print("\tName didn't flip: %s" % (nameNormal) )
                
            if anim_data.drivers != None:
                data_path = anim_data.drivers[0].data_path
                
                if data_path.startswith('pose.bones') == True:
                    
                    split = data_path.split('"', 2)
                    
                    nameFlipped = flipNames( split[1] )
                    
                    if nameFlipped != "":
                        print("The 1st Driver: %s to %s" % (split[1], flipNames(split[1])) )
                    else:
                        print("\tName didn't flip: %s" % (split[1]) )
                    
                else:
                    print("\n Data_path didn't start with \"pose.bones\" \n")
            else:
                print("\n There were 0 drivers on %s \n" % (ob.name) )
                
            reportString = "Done!"
            self.report({'INFO'}, reportString)
                
        elif self.type == "MIRROR_DRIVER_TEST":
            
            anim_data = bpy.context.object.animation_data
            direction = ("X", "Y", "Z")
            
            #For the Hidden, Muted, and Locked driver counts
            toggled = [0,0,0]
            
            if anim_data.drivers != None:
                side_list = []
                
                for i in enumerate(anim_data.drivers):
                    #data_path = anim_data.drivers[i[0]].data_path
                    data_path = i[1].data_path
                    #array_index = anim_data.drivers[i[0]].array_index
                    array_index = i[1].array_index
                    print("data_path: %s" % (data_path))
                    
                    #print('"pose.bones": %s' % (str(data_path.startswith('pose.bones'))))
                    
                    if data_path.startswith('pose.bones') == True:
                        #2 allows for 2 splits in string, meaning 3 strings in the .split() list
                        split = data_path.split('"', 2)
                        #1 allows for 1 splits in string, meaning 2 strings in the .split() list
                        rsplit = data_path.rsplit('.', 1)
                        
                        #name of the bone's property that is driver ex. ".rotation_euler"
                        prop = rsplit[1]
                        
                        nameNormal = split[1]
                        nameFlipped = flipNames( split[1] )
                        
                        if nameFlipped != "":
                            
                            #print("split: %s" % (str(split)))
                            #print(" split[1]: %s" % (str(split[1] )))
                            
                            #print("rsplit: %s" % (str(rsplit)))
                            print(" prop: %s" % (str(prop)) )
                            
                            print("flipNames: %s" % (nameFlipped) )
                            
                            split[1] = nameFlipped
                            
                            print(" split Flipped: %s; Array_Index: %d" % (str(split), array_index) )
                            
                            
                            #eval("bpy.context.object.pose.bones["+split[1]+"]."+prop])
                            #data_path_2 = str("bpy.context.object.pose.bones[\""+split[1]+"\"]")
                            #print("Data Path 2: %s; Array_Index: %d" % (data_path_2, array_index) )
                            #eval(data_path_2).driver_add(prop, array_index)
                            
                            #This one works
                            driver_new = bpy.context.object.pose.bones[nameFlipped].driver_add(prop, array_index)
                            
                            print("New Driver: Data_Path: %s; Array_Index: %d; Type: %s;" % (driver_new.data_path, driver_new.array_index, driver_new.driver.type) )
                            
                            reportString = "Done!"
                            #break here is placeholder to just do 1 iteration
                            break
                        else:
                            print("\tName didn't flip: %s" % (nameNormal) )
                    
                    else:
                        reportString = "Data_path didn't start with \"pose.bones\" "
                        break
                    
                print(reportString + "\n")
                self.report({'INFO'}, reportString)
                
            
            else:
                reportString = "Object[%s] has No Drivers" % (bpy.context.object.name)
                
                print(reportString)
                self.report({'INFO'}, reportString)
                
        elif self.type == "MIRROR_DRIVER_FROM_BONE_TEST_PRINT":
            
            anim_data = bpy.context.object.animation_data
            direction = ("X", "Y", "Z")
            
            #For the Hidden, Muted, and Locked driver counts
            toggled = [0,0,0]
            
            bone_active = bpy.context.active_pose_bone
            bones_selected = bpy.context.selected_pose_bones_from_active_object
            
            #If there is an active pose bone
            if bone_active != None:
                bone_active_direction = getDirection(bone_active.name)
                print("bone_active_direction: %s" % (bone_active_direction))
                
                #Checks if active bone's name can be flipped
                if bone_active_direction != "":
                    #If there is at least one driver in object
                    if anim_data.drivers != None:
                        list_nothing = []
                        list_side = []
                        
                        #bone name dictionary from drivers[].datapath
                        dict_1 = {}
                        
                        #instead of a copy of a dictionary, just have a list of strings of the names of the dictionary
                        dict_direction = []
                        
                        #gets all the drivers with .L or .R
                        for i in enumerate(anim_data.drivers):
                            data_path = i[1].data_path
                            
                            array_index = i[1].array_index
                            #print("data_path: %s" % (data_path))
                            #for i in enumerate(anim_data.drivers):
                            if data_path.startswith('pose.bones') == True:
                                
                                split = data_path.split('"', 2)
                                nameNormal = split[1]
                                
                                nameFlipped = flipNames(nameNormal)
                                
                                #splits data_path to get property string name to drive ex. ".rotation_euler"
                                rsplit = data_path.rsplit('.', 1)
                                
                                #name of the bone's property that is driver ex. ".rotation_euler"
                                prop = rsplit[1]
                                
                                #print("split: %s" % (split) )
                                #print("nameNormal: %s" % (nameNormal) )
                                
                                #if flippedNames() actually returns a flipped name, else it can't be flipped
                                if nameFlipped != "":
                                    #name of bone and index of the bone's driver
                                    #dict_1[nameNormal] = i[0]
                                    if nameNormal not in dict_1:
                                        dict_1[nameNormal] = {}
                                        
                                    if prop not in dict_1[nameNormal]:
                                        dict_1[nameNormal][prop] = {}
                                        
                                    #dict_1[nameNormal][prop].append([array_index, i[0]])
                                    dict_1[nameNormal][prop][array_index] = i[0]
                                    #dict_1[nameNormal] = i[0]
                                    #dict_1[nameNormal][prop].append(i[0])
                                    """
                                    print("split: %s" % (split) )
                                    print("nameNormal: %s" % (nameNormal) )
                                    print("flipNames(nameNormal): %s" % (flipNames(nameNormal)) )
                                    #"""
                                    
                                else:
                                    pass
                            else:
                                print("Passed: %s" % (str(i)) )
                                
                        print("\nitems(): %s" % (str(dict_1.items())) )
                        
                        print("\nkeys(): %s" % (str(dict_1.keys())) )
                        
                        #
                        print("\nlen() of dict_1: %d" % (len(dict_1)) )
                        
                        print("\nlen() of dict_1.keys(): %d" % (len(dict_1.keys())) )
                        
                        """
                        for i in dict_1.items():
                            #checks if the getDirection returned includes ".l", slice is since ".left" has ".l"
                            if getDirection(i[0]).find(bone_active_direction[0:2]) > -1:
                                #Adds this bone to the dictionary with its index
                                dict_direction[i[0]] = i[1]
                                    
                        #"""
                        
                        #for loop to only include selected pose bones in armature, not all of them
                        #for i in dict_1.items():
                        for i in dict_1:
                            #checks if the getDirection returned includes ".l", slice is since ".left" has ".l"
                            if getDirection(i).find(bone_active_direction[0:2]) > -1:
                                
                                #If bone is selected, add it
                                if data.bones[i].select == True:
                                    #Adds this bone to the dictionary with its index
                                    #dict_direction[i[0]] = i[1]
                                    dict_direction.append(i)
                                    
                            #print(i[0])
                            
                        #print("\ndict_direction.items(): %s" % (str(dict_direction.items())) )
                        print("\ndict_direction.items(): %s" % (str(dict_direction)) )
                        
                        #for i in dict_direction.items():
                        for i in dict_direction:
                            print("i: %s" % (i))
                            #nameFlipped = flipNames(i[0])
                            nameFlipped = flipNames(i)
                            #if the nameFlipped from dict_direction isn't in dict_1
                            if nameFlipped not in dict_1:
                                #goes through properties now ex. ".rotation_euler"
                                #for j in dict_1[i].items():
                                
                                #Checks if nameFlipped is a bone in the armature
                                if data.bones.get(nameFlipped) is not None:
                                    for j in dict_1[i]:
                                        print("j.items(%s): %s" % (j, dict_1[i].items()) )
                                        print("j: %s" % (j) )
                                        
                                        for k in dict_1[i][j]:
                                            print("k: %s" % (k) )
                                            
                                            index_driver = dict_1[i][j][k]
                                            
                                            driver_to_flip = anim_data.drivers[index_driver]
                                            #driver_to_flip = anim_data.drivers[dict_1[i] ]
                                            
                                            data_path = driver_to_flip.data_path
                                            
                                            #splits data_path to get property string name to drive ex. ".rotation_euler"
                                            rsplit = data_path.rsplit('.', 1)
                                            
                                            #name of the bone's property that is driver ex. ".rotation_euler"
                                            prop = rsplit[1]
                                            
                                            print("data_path: %s; index: %d" % (data_path, index_driver) )
                                            
                                            #This adds the new driver
                                            driver_new = bpy.context.object.pose.bones[nameFlipped].driver_add(j, k)
                                            
                                            print("Added Driver: %s; Prop: %s; Index: %d" % (nameFlipped, j, k))
                                            
                                            #This changes the driver_new's properties
                                            driver_new.driver.type = driver_to_flip.driver.type
                                            
                                            #This bottom section is for 
                                            driver_new_vars = driver_new.driver.variables
                                            #driver_vars is variables of driver_to_flip
                                            driver_vars = driver_to_flip.driver.variables
                                            print("variables: %d" % (len(driver_vars)))
                                            
                                            #print("" % ())
                                            
                                            if len(driver_vars) > 0:
                                                for m in enumerate(driver_vars):
                                                    print("Var[%d]: \"%s\"; Targets: %d" % (m[0], m[1].name, len(m[1].targets)))
                                                    
                                                    new_var = driver_new_vars.new()
                                                    
                                                    new_var.name = m[1].name
                                                    
                                                    for p in enumerate(m[1].targets):
                                                        print("%d: transform_type: %s" % (p[0], p[1].transform_type))
                                                        
                                            else:
                                                print("No Variables")
                                            
                                            
                                
                                else:
                                    print("\"%s\" isn\'t a bone" % (nameFlipped))
                        
                        #print("\ndict_direction.items(): %s" % (str(dict_direction.items())) )
                        print("\ndict_direction.items(): %s" % (str(dict_direction)) )
                        
                        reportString = "Done!"
                            
                        print(reportString + "\n")
                        self.report({'INFO'}, reportString)
                        
                    
                    else:
                        reportString = "Object[%s] has No Drivers" % (bpy.context.object.name)
                else:
                    reportString = "Active Bone Name [%s] can\'t be flipped" % (bone_active.name)
            else:
                reportString = "No Active Bone found"
                
            print(reportString)
            self.report({'INFO'}, reportString)
                
        elif self.type == "MIRROR_DRIVER_TEST_PRINT":
            
            anim_data = bpy.context.object.animation_data
            direction = ("X", "Y", "Z")
            
            #For the Hidden, Muted, and Locked driver counts
            toggled = [0,0,0]
            
            if anim_data.drivers != None:
                list_nothing = []
                list_side = []
                
                #bone name dictionary
                dict_1 = {}
                
                #gets all the drivers with .L or .R
                for i in enumerate(anim_data.drivers):
                    data_path = i[1].data_path
                    
                    array_index = i[1].array_index
                    #print("data_path: %s" % (data_path))
                    #for i in enumerate(anim_data.drivers):
                    if data_path.startswith('pose.bones') == True:
                        
                        split = data_path.split('"', 2)
                        nameNormal = split[1]
                        
                        nameFlipped = flipNames(nameNormal)
                        
                        #print("split: %s" % (split) )
                        #print("nameNormal: %s" % (nameNormal) )
                        
                        #if flippedNames() actually returns a flipped name, else it can't be flipped
                        if nameFlipped != "":
                            #name of bone and index of the bone's driver
                            dict_1[nameNormal] = i[0]
                            
                            print("split: %s" % (split) )
                            print("nameNormal: %s" % (nameNormal) )
                            print("flipNames(nameNormal): %s" % (nameFlipped) )
                            
                        else:
                            pass
                    else:
                        print("Passed: %s" % (str(i)) )
                        
                print("\nitems(): %s" % (str(dict_1.items())) )
                
                print("\nkeys(): %s" % (str(dict_1.keys())) )
                    
                reportString = "Done!"
                    
                print(reportString + "\n")
                self.report({'INFO'}, reportString)
                
            
            else:
                reportString = "Object[%s] has No Drivers" % (bpy.context.object.name)
                
                print(reportString)
                self.report({'INFO'}, reportString)
                
                
        #Resets default settings
        self.type == "DEFAULT"
        
        return {'FINISHED'}
        
class RIG_DEBUGGER_UL_items(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        scene = bpy.context.scene
        data = bpy.data
        props = scene.RD_Props
        
        #active = props.RIA_ULIndex
        IMCollect = props.collections
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            
            row = layout.row(align=True)
            
            if len(IMCollect) > 0:
                #obName
                #obName = item.object.name if item.object != None else "Row"+str(index)
                
                #obItems
                if item.collection != None:
                    obItems = len(item.collection.objects)
                else:
                    obItems = 0
                
                info = '%d. (%d)' % (index+1, obItems)#, obName, obItems)
                #bpy.context.scene.RD_Props.collections.add()
                
                #Displays icon of objects in list
                if props.display_icons == True:
                    
                    if item.object != "EMPTY" and item.icon != "NONE":
                        row.label(text="", icon=item.icon)
                        
                    else:
                        #obIcon = objectIcon(item.object)
                        row.label(text="", icon="QUESTION")
                        
                #Checks if the item has an object pointed
                if item.object != None:
                    row.prop(item.object, "name", text=info)
                    
                else:
                    row.label(text=info+": [No Object]")
                
                if props.display_collections == True:
                    if item.collection != None:
                        row.prop(item.collection, "name", text="", icon="GROUP")
                        
                    else:
                        row.label(text="[No Collection]")
                    
            else:
                row.label(text="No Iterations Here")
                
        #Theres nothing in this layout_type since it isn't intended to be used.
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'

    def invoke(self, context, event):
        pass

#Calculates ammounts of different attributes drivers have
def calculateUIALL(string):
    ob = bpy.context.object
    anim_data = ob.animation_data
    
    count = 0
    
    if len(anim_data.drivers) > 0:
        #If driver toggled as hidden/inactive in the UI
        if string == "hide":
            for i in anim_data.drivers:
                if i.hide == True:
                    count += 1
                    
        elif string == "mute":
            for i in anim_data.drivers:
                if i.mute == True:
                    count += 1
                    
        elif string == "lock":
            for i in anim_data.drivers:
                if i.lock == True:
                    count += 1
                    
        #Calculates how many Drivers have at least 1 modifier
        elif string == "modifiers":
            for i in anim_data.drivers:
                if len(i.modifiers) > 0:
                    count += 1
        
    else:
        pass
    
    return count
   
#Tried to do this for the active/selected "Driver" in the Driver Editor, but it isn't accessable via python, so I would have to learn C in order to expose the RNA   
"""
#Calculates ammounts of different attributes drivers have
def calculateUIActive(string):
    ob = bpy.context.object
    anim_data = ob.animation_data
    
    count = 0
    
    if ob.type == 'ARMATURE':
        
    
    if len(anim_data.drivers) > 0:
        #If driver toggled as hidden/inactive in the UI
        if string == "hide":
            for i in anim_data.drivers:
                if i.hide == True:
                    count += 1
                    
        elif string == "mute":
            for i in anim_data.drivers:
                if i.mute == True:
                    count += 1
                    
        elif string == "lock":
            for i in anim_data.drivers:
                if i.lock == True:
                    count += 1
                    
        #Calculates how many Drivers have at least 1 modifier
        elif string == "modifiers":
            for i in anim_data.drivers:
                if len(i.modifiers) > 0:
                    count += 1
        
    else:
        pass
    
    return count """
    
class RIG_DEBUGGER_PT_CustomPanel1(bpy.types.Panel):
    #A Custom Panel in Viewport
    bl_idname = "RIG_DEBUGGER_PT_CustomPanel1"
    bl_label = "Rig Debugger"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    #bl_context = "output"
    bl_category = "Rig Debugger"
    
    # draw function
    def draw(self, context):
                 
        layout = self.layout
        ob = bpy.context.object
        scene = context.scene
        props = scene.RD_Props
        
        #Layout Starts
        col = layout.column()
        
        #Debug Operators
        row = col.row(align=True)
        row.label(text="Debug Operators:")
        
        row = col.row(align=True)
        row.operator("rig_debugger.debug", text="Print All Drivers").type = "PRINT_ALL"
        
        row = col.row(align=True)
        row.operator("rig_debugger.debug", text="Print Add Driver Test").type = "PRINT_ADD_DRIVER_TEST"
        
        #Just to test my FlipNames function
        row = col.row(align=True)
        row.operator("rig_debugger.debug", text="Flip Names Test").type = "FLIP_NAMES_TEST"
        
        row = col.row(align=True)
        row.operator("rig_debugger.debug", text="Mirror Driver Test").type = "MIRROR_DRIVER_TEST"
        
        row = col.row(align=True)
        row.operator("rig_debugger.debug", icon="BONE_DATA", text="Active Bone Mirror Driver Test").type = "MIRROR_DRIVER_FROM_BONE_TEST_PRINT"
        
        row = col.row(align=True)
        row.operator("rig_debugger.debug", icon="INFO", text="Mirror Driver Test Print").type = "MIRROR_DRIVER_TEST_PRINT"
        
        """
        if ob.pose != None:
            row = col.row(align=True)
            row.label(text="Drivers: %d" % (len(ob.animation_data.drivers))) """
            
        drivers = len(ob.animation_data.drivers)
            
        row = col.row(align=True)
        row.prop(props, "dropdown_1", text="", icon="DOWNARROW_HLT")
        row.label(icon= "DRIVER", text="Armature Drivers: %d" % (len(ob.animation_data.drivers)) )
        
        if props.dropdown_1 == True:
            row = col.row(align=True)
            row.label(icon= "HIDE_OFF", text="Hidden: %d/%d" % (calculateUIALL("hide"), drivers) )
            
            row = col.row(align=True)
            row.label(icon= "CHECKBOX_HLT", text="Muted: %d/%d" % (calculateUIALL("mute"), drivers) )
            
            row = col.row(align=True)
            row.label(icon= "DECORATE_LOCKED", text="Locked: %d/%d" % (calculateUIALL("lock"), drivers) )
            
            row = col.row(align=True)
            row.label(icon= "MODIFIER_ON", text="With Modifiers: %d/%d" % (calculateUIALL("modifiers"), drivers) )
            
        
        
        #End of CustomPanel
        
def ListOrderUpdate(self, context):
    scene = bpy.context.scene
    data = bpy.data
    props = scene.RD_Props
    #list_order "DUPLICATES" "RECENT" "CUSTOM"
    #list_reverse: "DESCENDING" "ASCENDING"
    
    reverseBool = False
    if props.list_reverse == "ASCENDING":
        reverseBool = True
        
    #Updates the UI List selected index when ListOrderUpdate is called
    props.IM_ULIndex = len(props.collections)-props.IM_ULIndex-1
        
    # "a" parameter would be an object with methods
    def returnOrder(a):
        #Returns len() of objects in collection, else return 0
        if props.list_order == "DUPLICATES":
            
            return len(a.collection.objects) if a.collection != None else 0
            
        #Returns the integer value of the order the objects were created
        if props.list_order == "RECENT":
            return a.recent
            
        #Returns custom value order made by user in the UI List
        if props.list_order == "CUSTOM":
            return a.custom
        
    #This is where sorting is done
    #sort = sorted(props.collections, key=lambda a: a.duplicates, reverse=reverseBool)
    sort = sorted(props.collections, key=returnOrder, reverse=reverseBool)
    
    nameList = []
    
    #For loop appends the names of objects in props.collections.objects into nameList
    for i in enumerate(sort):
        if i[1].object is not None:
            nameList.append(i[1].object.name)
        else:
            print("Collection: %s missing object" % (i[1].name))
            #This section calculates the index of props.collection even when they are being removed in order to remove them
            newIndex = None
            for j in enumerate(props.collections):
                if i[1] == j[1]:
                    newIndex = j[0]
            props.collections.remove(newIndex)
    
    #For loop uses object names in nameList to move props.collections
    for i in enumerate(nameList):
        colLocation = 0
        #Loops through props.collections to see if their names matches the names of object names in nameList
        for j in enumerate(props.collections):
            #if j[1].name == i[1]:
            if j[1].object.name == i[1]:
                colLocation = j[0]
                break
        props.collections.move(colLocation, i[0])
    
    return
    
class RIG_DEBUGGER_PreferencesMenu(bpy.types.AddonPreferences):
    bl_idname = "rig_debugger_addon_b2_80_v1_0"
    # here you define the addons customizable props
    ui_tab: bpy.props.EnumProperty(name="Enum", items= [("GENERAL", "General", "General Options"), ("ABOUT", "About", "About Author & Where to Support")], description="Iterate Model UI Tabs", default="GENERAL")
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.RD_Props
        
        col = layout.column()
        
        row = col.row(align=True)
        row.prop(self, "ui_tab", expand=True)
        row = col.row(align=True)
        
        box = layout.box()
        col = box.column()
        #row = col.row(align=True)
        
        if self.ui_tab == "GENERAL":
            row = col.row(align=True)
            #row.label(text="Add Button to 3D Viewport Header?")
            row.prop(props, "debug_mode", expand=True, text="Debug Mode")
            
            row = col.row(align=True)
            
        elif self.ui_tab == "ABOUT":
            row = col.row(align=True)
            row.label(text="JohnGDDR5 on: ")
            row.operator("wm.url_open", text="Youtube").url = "https://www.youtube.com/channel/UCzPZvV24AXpOBEQWK4HWXIA"
            row.operator("wm.url_open", text="Twitter").url = "https://twitter.com/JohnGDDR5"
            row.operator("wm.url_open", text="Artstation").url = "https://www.artstation.com/johngddr5"
    
class RIG_DEBUGGER_Props(bpy.types.PropertyGroup):
    #Tries to set collection_parent's default to Master Collection
    
    #Dropdown for Iterate Display
    dropdown_1: bpy.props.BoolProperty(name="Dropdown", description="Show Props of all Drivers", default=True)
    
    dropdown_2: bpy.props.BoolProperty(name="Dropdown", description="Show Props of active Driver", default=True)
    
    collection_active: bpy.props.PointerProperty(name="Collection to add Collections for Object duplicates", type=bpy.types.Collection)
    
    #Booleans for locking default collection of parent
    
    lock_active: bpy.props.BoolProperty(name="Lock Collection of Active", description="When locked, you can now edit the name of the selected collection", default=False)
    
    #collections: bpy.props.CollectionProperty(type=RIG_DEBUGGER_CollectionObjects)
    
    IM_ULIndex: bpy.props.IntProperty(name="List Index", description="UI List Index", default= 0, min=0)
    
    clean_leave: bpy.props.IntProperty(name="List Index", description="Ammount of recent Objects to leave when cleaning.", default=2, min=0)
    
    
    
    group_name_use: bpy.props.BoolProperty(name="Use Object Name for New Collection", description="Use the Object\'s name for the New Collection when creating a new Iteration Object", default=True)
    
    group_name: bpy.props.StringProperty(name="New Collection Name", description="Name used when creating a new collection for Active", default="Group")
    
    listDesc =  ["Displays List in order of how many duplicates each object has", "Displays List in the order they were created", "Displays List in order user specified"]
    listDesc2 =  ["List displays in Descending Order", "List displays in Ascending Order"]
    
    list_order: bpy.props.EnumProperty(name="Display Mode", items= [("DUPLICATES", "Duplicates", listDesc[0], "DUPLICATE", 0), ("RECENT", "Recent", listDesc[1], "SORTTIME", 1), ("CUSTOM", "Custom", listDesc[2], "ARROW_LEFTRIGHT", 2)], description="Display Mode of List", default="DUPLICATES", update=ListOrderUpdate)
    
    list_reverse: bpy.props.EnumProperty(name="Display Mode", items= [("DESCENDING", "Descending", listDesc2[0], "SORT_DESC", 0), ("ASCENDING", "Ascending", listDesc2[1], "SORT_ASC", 1)], description="Display Mode of List", default="DESCENDING", update=ListOrderUpdate)
    
    display_collections: bpy.props.BoolProperty(name="Display Collections in List", description="Iterate Object Collections where duplicates are sent.", default=True)
    
    display_icons: bpy.props.BoolProperty(name="Display Icons", description="Display icons of objects in the list", default=True)
    
    index_to_new: bpy.props.BoolProperty(name="Updates Active List Index to New Iteration Object", description="Sets Active list index to New Iteration Object that was added.", default=True)
    
    debug_mode: bpy.props.BoolProperty(name="Display Debug Operators", description="To aid in Debugging Operators. Displayed in \"Display Settings\"", default=True)
    
    #For Iterate Collection Settings and Operators
    
    #hide_types_last
    #hide_last: bpy.props.BoolProperty(name="Exclude Recent Iteration", description="When using the operators for toggling \"all objects\"", default=False)
    
#Classes that are registered
classes = (
    
    RIG_DEBUGGER_OT_Debugging,
    #RIG_DEBUGGER_OT_UIOperators,
    
    RIG_DEBUGGER_UL_items,
    
    RIG_DEBUGGER_PT_CustomPanel1,
    
    RIG_DEBUGGER_PreferencesMenu,
    #RIG_DEBUGGER_CollectionObjects,
    RIG_DEBUGGER_Props,
)

def register():
    #ut = bpy.utils
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
    #bpy.types.Scene.IM_Collections = bpy.props.CollectionProperty(type=REF_IMAGEAID_Collections)
    bpy.types.Scene.RD_Props = bpy.props.PointerProperty(type=RIG_DEBUGGER_Props)
    
def unregister():
    #ut = bpy.utils
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    
    del bpy.types.Scene.RD_Props
    
if __name__ == "__main__":
    register()
