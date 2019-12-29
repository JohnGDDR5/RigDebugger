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

import bpy, re
        
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

#Will return match object or None if string wasn't found
def getDirectionRegEx(string):
    pattern = '(?<=[ \.\-_])[rRlL]((?=$|[ \.\-_])|(?i)(ight|eft))'
    
    #print("pattern: %s" % (pattern) )
    rawString = r'%s' % (pattern)
    
    #print("rawString: %s" % (rawString) )
    
    #compiled RegEx object
    regex = re.compile(rawString)
    
    match = regex.search(string)
    
    return match
    
def getDirection(string, flip=False):
    #print("getDirection(): %s" % (string) )
    
    match = getDirectionRegEx(string)
    
    if match is not None:
        matchString = match.group(0)
        sides = ("left", "right")
        #stringNew = string
        stringNew = matchString
        
        #checks if its left or right
        if matchString[0].lower() == "l":
            stringNew = sides[0]
        elif matchString[0].lower() == "r":
            stringNew = sides[1]
        #Just incase of an Error
        else:
            return ""
        
        #flips the name
        if flip == True:
            if stringNew == "left":
                stringNew = sides[1]
            else:
                stringNew = sides[0]
                
        if len(matchString) == 1:
            stringNew = stringNew[0]
                
        print("getDirection(): %s, %s" % (matchString, stringNew) )
        return stringNew
    else:
        print("getDirection(): Match Fail for %s" % (string) )
        return ""

#Fixes issues with case capitalization, ex. "RiGhT" to "Right", and "rIGHT" to "right"
def fixCaseIssues(string, flip=False):
    
    sides = ("left", "right")
    stringFlip = string
    
    #flips the name
    if flip == True:
        if string[0].lower() == "l":
            stringFlip = sides[1]
        elif string[0].lower() == "r":
            stringFlip = sides[0]
        #Just incase of an Error
        else:
            return None
    #print("String 2: %s, %s" % (string, stringFlip))
    
    #Checks if the string is one character long "l" or "r", or longer "left", "right"
    if len(string) > 1:
        #Checks if 1st and 2nd character are uppercase or lower
        cases = (string[0].isupper(), string[1].isupper() )
        
        #if 1st character is lowercase, make the string lowercase
        if cases[0] == False:
            #string.lower()
            pass
        else:
            #If 1st is uppercase and 2nd is lowercase, make rest of string lowercase
            if cases[1] == False:
                stringFlip = stringFlip[0].upper() + stringFlip[1:]
            #If 1st and 2nd character are uppercase, make all uppercase
            else:
                stringFlip.upper()
                
        #return stringFlip
    else:
        case = string[0].isupper()
        #Makes string only one character long
        stringFlip = stringFlip[0]
        
        #If 1st character is uppercase
        if case == True:
            stringFlip = stringFlip.upper()
            #print("BRUH: %s" % (stringFlip) )
            
    return stringFlip
        
#Takes in a string to check if it is flipabble, and an optional object, to change the name of the object if it is wrong.
#def flipNames(string, object = None):
def flipNames(string):
    #print("flipNames(): %s" % (string) )
    
    match = getDirectionRegEx(string)
    
    if match is not None:
        matchString = match.group(0)
        #Span is the (matchString.start(0), matchString.end(0)) tuple
        span = match.span(0)
        start = match.start(0)
        end = match.end(0)
        #print("Span: %s" % (str(span)) )
        matchFlipped = fixCaseIssues(matchString, flip=True)
        
        #string = string[:index] + replace + string[index+len(sides[side]):]
        string = string[:start] + matchFlipped + string[start+len(matchFlipped):]
        
        #print("Span: %s; matchFlipped: %s; String: %s" % (str(span), matchFlipped, string) ) 
        
        return string
    else:
        return None
        
        
class RIG_DEBUGGER_OT_Debugging(bpy.types.Operator):
    bl_idname = "rig_debugger.debug"
    bl_label = "Iterate Objects Debugging Operators"
    bl_description = "To assist with debugging and development"
    bl_options = {'UNDO',}
    type: bpy.props.StringProperty(default="DEFAULT")
    #index: bpy.props.IntProperty(default=0, min=0)
    
    def endReport(self, reportString):
        print(reportString + "\n")
        self.report({'INFO'}, reportString)
        return {'FINISHED'}
    
    def execute(self, context):
        scene = bpy.context.scene
        context = bpy.context
        data = context.object.data
        props = scene.RD_Props
        
        #Creates animation_data if there isn't none
        if self.type == "CREATE_ANIMATION_DATA":
            ob = bpy.context.object
            anim_data = ob.animation_data
            
            #Checks if object has animation_data
            if anim_data is None:
                ob.animation_data_create()
                #opposite is .animation_data_clear()
                
        #Prints the UI info of all drivers, such as 
        elif self.type == "PRINT_ALL_DRIVER_UI_INFO":
            
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
                
        #Prints Active Bone Info: Direction and flippedName
        elif self.type == "PRINT_ACTIVE_BONE_FLIPPED":
            bone_active = bpy.context.active_pose_bone
            #If there is an active pose bone
            if bone_active != None:
                bone_active_direction = getDirection(bone_active.name)
                
                #Checks if active bone's name can be flipped
                if bone_active_direction != "":
                    flippedName = flipNames(bone_active.name)
                    
                    reportString = "Active Bone Name: \'%s\' to \'%s\', direction: \'%s\' " % (bone_active.name, flippedName, bone_active_direction)
                else:
                    reportString = "Active Bone Name [%s] can\'t be flipped" % (bone_active.name)
                    #self.endReport(reportString)
            else:
                reportString = "No Active Bone found"
                
            self.endReport(reportString)
            
        #Prints the info and flippedName of driver if it were added
        elif self.type == "PRINT_ADD_DRIVER_MIRROR_INFO_TEST":
            
            anim_data = bpy.context.object.animation_data
            
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
                    
                    #New
                    nameFlipped = flipNames( split[1] )
                    
                    if nameFlipped != "":
                        print("The 1st Driver: %s to %s" % (split[1], flipNames(split[1])) )
                    else:
                        print("\tName didn't flip: %s" % (split[1]) )
                    #New
                    
                reportString = "Done!"
                
                print(reportString)
                self.report({'INFO'}, reportString)
            
            else:
                reportString = "Object[%s] has No Drivers" % (bpy.context.object.name)
                
                print(reportString)
                self.report({'INFO'}, reportString)
                
        #Prints the flipped name of active pose bone, and 1st driver
        elif self.type == "MIRROR_DRIVER_TEST_PRINT_V1":
            ob = bpy.context.object
            anim_data = ob.animation_data
            
            print("\nFlipped Names of:")
                
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
                print("\n There were 0 drivers on %s to flip names\n" % (ob.name) )
                
            reportString = "Done!"
            self.report({'INFO'}, reportString)
                
        #Adds a mirrored driver to test it
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
        
        elif self.type == "MIRROR_DRIVER_TEST_PRINT_V2":
            
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
        
class RIG_DEBUGGER_OT_DriverMirror(bpy.types.Operator):
    bl_idname = "rig_debugger.driver_mirror"
    bl_label = "Iterate Objects Debugging Operators"
    bl_description = "To assist with debugging and development"
    bl_options = {'UNDO',}
    type: bpy.props.StringProperty(default="DEFAULT")
    sub: bpy.props.StringProperty(default="DEFAULT")
    #index: bpy.props.IntProperty(default=0, min=0)
    
    def endReport(self, reportString):
        print(reportString + "\n")
        self.report({'INFO'}, reportString)
        return {'FINISHED'}
    
    def execute(self, context):
        scene = bpy.context.scene
        context = bpy.context
        data = context.object.data
        props = scene.RD_Props
        
        #Resets default settings
        def resetSelf():
            self.type == "DEFAULT"
            self.sub == "DEFAULT"
            #self.sub == "DEFAULT"
        
        anim_data = bpy.context.object.animation_data
        """
        self.type == "ARMATURE":
            self.sub == "ACTIVE_BONE_ALL", "FROM_DIRECTION_ALL"
        self.type == "DRIVER_EDITOR":
            self.sub == "ACTIVE_DRIVERS", "ACTIVE_FROM_DIRECTION"
        """
        
        #Note: print() functions after #10 are the ones I commented to not print. Uncomment them to have them as before.
        
        #This checks the self.type and .sub to see if the operator.execute should even continue or end with a return
        #if self.type == "MIRROR_FROM_ACTIVE_BONE" or self.type == "MIRROR_FROM_DIRECTION":
        if self.type == "ARMATURE":
            if self.sub == "ACTIVE_BONE_ALL" or self.type == "FROM_DIRECTION_ALL":
                
                bone_active = bpy.context.active_pose_bone
                #bones_selected = bpy.context.selected_pose_bones_from_active_object
                
                #If there is an active pose bone
                if bone_active != None:
                    bone_active_direction = getDirection(bone_active.name)
                    print("bone_active_direction: %s" % (bone_active_direction) )
                    
                    #Checks if active bone's name can be flipped
                    if bone_active_direction == "":
                        #reportString = "bone_active_direction: %s" % (bone_active_direction)
                        reportString = "Active Bone Name [%s] can\'t be flipped" % (bone_active.name)
                        self.endReport(reportString)
                else:
                    reportString = "No Active Bone found"
                    self.endReport(reportString)
            else:
                reportString = "self.sub type Unrecognized"
                self.endReport(reportString)
                
        #elif self.type == "MIRROR_FROM_ACTIVE_DRIVERS" or self.type == "MIRROR_FROM_DIRECTION_DRIVERS":
        elif self.type == "DRIVER_EDITOR":
            if self.sub == "ACTIVE_DRIVERS" or self.sub == "ACTIVE_FROM_DIRECTION":
                pass
            pass
            
        else:
            reportString = "No recognized .type Mode"
            print(reportString + "\n")
            self.report({'INFO'}, reportString)
            return {'FINISHED'}
                
        #This one builds the dictionaries
        #If there is at least one driver in object
        if anim_data.drivers == None:
            reportString = "Object[%s] has No Drivers" % (bpy.context.object.name)
        else:
            #bone name dictionary from drivers[].datapath
            dict_1 = {}
            
            #dict_direction = []
            dict_direction = {}
            
            #gets all the drivers with .L or .R
            for i in enumerate(anim_data.drivers):
                data_path = i[1].data_path
                
                array_index = i[1].array_index
                
                #Checks if driver is from a "pose.bone"
                if data_path.startswith('pose.bones') == True:
                    
                    split = data_path.split('"', 2)
                    nameNormal = split[1]
                    
                    nameFlipped = flipNames(nameNormal)
                    #10print("nameNormal: %s; nameFlipped: %s;" % (str(nameNormal), str(nameFlipped)) )
                    #splits data_path to get property string name to drive ex. ".rotation_euler"
                    rsplit = data_path.rsplit('.', 1)
                    
                    #name of the bone's property that is driver ex. ".rotation_euler"
                    prop = rsplit[1]
                    
                    #if flippedNames() actually returns a flipped name, else it can't be flipped
                    if nameFlipped != "":
                        #name of bone and index of the bone's driver
                        if nameNormal not in dict_1:
                            dict_1[nameNormal] = {}
                            
                        if prop not in dict_1[nameNormal]:
                            dict_1[nameNormal][prop] = {}
                            
                        dict_1[nameNormal][prop][array_index] = i[0]
                        
                        #if self.type == "MIRROR_FROM_ACTIVE_DRIVERS":
                        if self.type == "DRIVER_EDITOR" and self.sub == "ACTIVE_DRIVERS":
                            #If the driver is selected, add this driver to dict_direction
                            if i[1].select == True:
                                #Section to add Driver location to dict_direction
                                if nameNormal not in dict_direction:
                                    dict_direction[nameNormal] = {}
                                    
                                if prop not in dict_direction[nameNormal]:
                                    dict_direction[nameNormal][prop] = {}
                                    
                                dict_direction[nameNormal][prop][array_index] = i[0]
                        
                    else:
                        pass
                else:
                    #10print("Passed: %s" % (str(i)) )
                    pass
                    
            #These are where the differences in what dict_1 bone names are selected and appended to dict_direction for mirror calculation
            #if self.type == "MIRROR_FROM_ACTIVE_BONE":
            if self.type == "ARMATURE":
                if self.sub == "ACTIVE_BONE_ALL":
                    #for loop to only include selected pose bones in armature, not all of them
                    for i in dict_1:
                        #If bone is selected, add it
                        if data.bones[i].select == True:
                            #checks if the getDirection returned includes ".l", slice is since ".left" has ".l"
                            #if getDirection(i).find(bone_active_direction[0:2]) > -1:
                            if getDirection(i).find(bone_active_direction[0]) > -1:
                                #Adds this bone to the dictionary with its index
                                #dict_direction[i[0]] = i[1]
                                #dict_direction.append(i)
                                dict_direction[i] = {}
                                
                #elif self.type == "MIRROR_FROM_DIRECTION":
                elif self.sub == "FROM_DIRECTION_ALL":
                    #for loop to only include selected pose bones in armature, but takes into account the direction selected in operator
                    #10print("props.mirror_direction: %s" % (props.mirror_direction))
                    mirror_direction = props.mirror_direction
                    #slice will turn "LEFT" to "l" and lowercase it
                    #to_find = mirror_direction[0:1].lower()
                    to_find = mirror_direction[0].lower()
                    #10print("to_find: %s" % (to_find))
                    
                    for i in dict_1:
                        flip_name = flipNames(i)
                        
                        #If bone is selected, or its mirror exists, and its mirror is selected
                        if data.bones[i].select == True or (data.bones.get(flip_name) is not None and data.bones[flip_name].select == True):
                            if getDirection(i).find(to_find) > -1:
                                #Checks if the flipped name is already there
                                boolean = i not in dict_direction
                                if boolean:
                                    #dict_direction[bone_name]
                                    dict_direction[i] = {}
                                
            #elif self.type == "MIRROR_FROM_DIRECTION_DRIVERS":
            elif self.type == "DRIVER_EDITOR":
                #This one requires for dict_1 to be built entirely, in order to find if flipNames() exists
                if self.sub == "ACTIVE_FROM_DIRECTION":
                    #Only mirros drivers that are selected, and takes the props.mirror_direction for what driver to use to mirror
                    #10print("props.mirror_direction: %s" % (props.mirror_direction))
                    mirror_direction = props.mirror_direction
                    #slice will turn "LEFT" to "l" and lowercase it
                    #to_find = mirror_direction[0:1].lower()
                    to_find = mirror_direction[0].lower()
                    #print("to_find: %s" % (to_find))
                    
                    for i in dict_1:
                        nameFlipped = flipNames(i)
                        
                        for j in dict_1[i]:
                            for k in dict_1[i][j]:
                                index_driver = dict_1[i][j][k]
                                driver_to = anim_data.drivers[index_driver]
                                flipped_exists = nameFlipped in dict_1 and j in dict_1[nameFlipped] and k in dict_1[nameFlipped][j]
                                #If driver is selected, or its flipName exists and its flipName is selected
                                if driver_to.select == True or (flipped_exists == True and anim_data.drivers[dict_1[nameFlipped][j][k] ].select == True):
                                    #If selected is 
                                    if getDirection(i).find(to_find) > -1:
                                        #Checks if the flipped name is already there
                                        if i not in dict_direction:
                                            #dict_direction[bone_name]
                                            dict_direction[i] = {}
                                            
                                        if j not in dict_direction[i]:
                                            #dict_direction[bone_name]
                                            dict_direction[i][j] = {}
                                            
                                        dict_direction[i][j][k] = dict_1[i][j][k]
                                
            else:
                pass
                
            #print("\ndict_direction.items(): %s" % (str(dict_direction.items())) )
            #10print("\ndict_direction.items(): %s" % (str(dict_direction)) )
            
            #if self.type != "MIRROR_FROM_ACTIVE_DRIVERS" or self.type != "MIRROR_FROM_DIRECTION_DRIVERS":
            if self.type != "DRIVER_EDITOR":
                if self.sub != "ACTIVE_DRIVERS" or self.sub != "ACTIVE_FROM_DIRECTION":
                    dictionary = dict_1
            else:
                dictionary = dict_direction
            
            #For loop to mirror all drivers, and f-curves of selected bones's drivers in dict_direction
            #If nameFlipped driver exists, it uses that ones, and adds a new one if it doesn't exists
            for i in dict_direction:
                #goes through properties now ex. ".rotation_euler"
                
                nameFlipped = flipNames(i)
                
                #Checks if nameFlipped is a bone in the armature
                if data.bones.get(nameFlipped) is not None:
                
                    for j in dictionary[i]:
                        #10print("j.items(%s): %s" % (j, dictionary[i].items()) )
                        #10print("j: %s" % (j) )
                        
                        for k in dictionary[i][j]:
                            #10print("k: %s" % (k) )
                            
                            index_driver = dict_1[i][j][k]
                            
                            #10print("index_driver Flipped: %r" % (nameFlipped in dict_1 and j in dict_1[nameFlipped] and k in dict_1[nameFlipped][j]) )
                            
                            driver_to_flip = anim_data.drivers[index_driver]
                            
                            data_path = driver_to_flip.data_path
                            
                            #splits data_path to get property string name to drive ex. ".rotation_euler"
                            rsplit = data_path.rsplit('.', 1)
                            
                            #name of the bone's property that is driver ex. ".rotation_euler"
                            prop = rsplit[1]
                            
                            #10print("data_path: %s; index: %d" % (data_path, index_driver) )
                            
                            #exists is if the flipped driver already existed
                            exists = False
                            
                            #If flipped driver doesn't exists, create one, else use existing
                            if nameFlipped not in dict_1:
                                #This adds the new driver
                                driver_new = bpy.context.object.pose.bones[nameFlipped].driver_add(j, k)
                                
                                if len(driver_new.modifiers) > 0:
                                    #Removes the 1 modifier created when adding a new driver
                                    driver_new.modifiers.remove(driver_new.modifiers[0])
                            else:
                                #if dict_1[nameFlipped][j][k] exists:
                                if nameFlipped in dict_1 and j in dict_1[nameFlipped] and k in dict_1[nameFlipped][j]:
                                    exists = True
                                    #index_driver_new = dict_1[flipNames(i) ][j][k]
                                    index_driver_new = dict_1[nameFlipped][j][k]
                                    driver_new = bpy.context.object.animation_data.drivers[index_driver_new]
                                else:
                                    #This adds the new driver
                                    driver_new = bpy.context.object.pose.bones[nameFlipped].driver_add(j, k)
                                    
                                    if len(driver_new.modifiers) > 0:
                                        #Removes the 1 modifier created when adding a new driver
                                        driver_new.modifiers.remove(driver_new.modifiers[0])
                            
                            #10print("New Driver: %s; Prop: %s; Index: %d" % (nameFlipped, j, k))
                            
                            #This changes the driver_new's properties
                            
                            #In "F-Curve" tab panel
                            driver_new.color_mode = driver_to_flip.color_mode
                            driver_new.auto_smoothing = driver_to_flip.auto_smoothing
                            
                            #Extrapolation is Important for the Driver Keyframe's endswith
                            driver_new.extrapolation = driver_to_flip.extrapolation
                            
                            #In "Drivers" tab panel
                            driver_new.driver.type = driver_to_flip.driver.type
                            driver_new.driver.expression = driver_to_flip.driver.expression
                            driver_new.driver.use_self = driver_to_flip.driver.use_self
                            
                            #This bottom section is for 
                            driver_new_vars = driver_new.driver.variables
                            #driver_vars is variables of driver_to_flip
                            driver_vars = driver_to_flip.driver.variables
                            #10print("variables: %d" % (len(driver_vars)))
                            
                            #print("" % ())
                            
                            #If there is at least 1 driver, and override_existing_drivers = True
                            if len(driver_vars) > 0 and props.override_existing_drivers:
                                #This will "Overide"/remove all previous variables in the existing mirrored driver, in order for correct new variables to be copied/duplicated
                                #exists is if the flipped driver already existed
                                if exists == True:
                                    #10print("exists == True")
                                    for m in enumerate(reversed(driver_new_vars)):
                                        #10print("Removed m[1] variable: %s" % (m[1].name))
                                        driver_new_vars.remove(m[1])
                                    
                                #This mirrors the keyframes of the drivers
                                for m in enumerate(driver_to_flip.keyframe_points):
                                    old_frame = m[1].co[0]
                                    old_value = m[1].co[1]
                                    keyf_name = driver_new.keyframe_points.insert(old_frame, old_value)
                                    
                                    keyf_name.interpolation = m[1].interpolation
                                    
                                    #Left/Right handles of keyframe
                                    #handle_left
                                    keyf_name.handle_left_type = m[1].handle_left_type
                                    
                                    keyf_name.handle_left[0] = m[1].handle_left[0]
                                    keyf_name.handle_left[1] = m[1].handle_left[1]
                                    
                                    #handle_right
                                    keyf_name.handle_right_type = m[1].handle_right_type
                                    
                                    keyf_name.handle_right[0] = m[1].handle_right[0]
                                    keyf_name.handle_right[1] = m[1].handle_right[1]
                                        
                                #This mirrors the driver
                                for m in enumerate(driver_vars):
                                    #10print("  Var[%d]: \"%s\"; Targets: %d" % (m[0], m[1].name, len(m[1].targets)))
                                    
                                    new_var = driver_new_vars.new()
                                    
                                    new_var.name = m[1].name
                                    new_var.type = m[1].type
                                    
                                    if new_var.type == 'SINGLE_PROP':
                                        
                                        new_var.targets[0].id_type = m[1].targets[0].id_type
                                        new_var.targets[0].id = m[1].targets[0].id
                                        new_var.targets[0].transform_type = m[1].targets[0].transform_type
                                        new_var.targets[0].data_path = m[1].targets[0].data_path
                                        
                                    #if new_var.type is 'TRANSFORMS, ROTATION_DIFF, or LOC_DIFF'
                                    else:
                                        for p in enumerate(m[1].targets):
                                            #targets of driver_new's targets
                                            target_p = new_var.targets[p[0]]
                                            
                                            target_p.id = p[1].id
                                            
                                            #Checks if target.id has object & object is type "Armature"
                                            if target_p.id is not None and target_p.id.type == 'ARMATURE':
                                                #This one checks if nameFlipped2 of bone exists to flip it
                                                if p[1].bone_target != "":
                                                    nameFlipped2 = flipNames(p[1].bone_target)
                                                    
                                                    #Flips bone name if mirror it exist
                                                    if data.bones.get(nameFlipped2 ) is not None:
                                                        target_p.bone_target = nameFlipped2
                                                    #Uses unflipped bone name if flipped isn't found
                                                    else:
                                                        target_p.bone_target = p[1].bone_target
                                                        print("  \"%s\" isn\'t a bone" % (p[1].bone_target) )
                                                        
                                            #if new_var.type == 'TRANSFORMS':
                                            target_p.transform_type = p[1].transform_type
                                            target_p.rotation_mode = p[1].rotation_mode
                                            target_p.transform_space = p[1].transform_space
                            else:
                                print("No Variables")
                else:
                    print("\"%s\" isn\'t a bone" % (nameFlipped))
            
            reportString = "Done!"
        
        #else:
        #reportString = "Object[%s] has No Drivers" % (bpy.context.object.name)
            
        print(reportString + "\n")
        self.report({'INFO'}, reportString)
        
        #Resets default settings
        self.type == "DEFAULT"
        
        return {'FINISHED'}
        
class RIG_DEBUGGER_OT_DriverOps(bpy.types.Operator):
    bl_idname = "rig_debugger.driver_ops"
    bl_label = "Iterate Objects Debugging Operators"
    bl_description = "To assist with debugging and development"
    bl_options = {'UNDO',}
    type: bpy.props.StringProperty(default="DEFAULT")
    sub: bpy.props.StringProperty(default="DEFAULT")
    #index: bpy.props.IntProperty(default=0, min=0)
    
    def execute(self, context):
        scene = bpy.context.scene
        context = bpy.context
        data = context.object.data
        props = scene.RD_Props
        
        #Creates animation_data if there isn't none
        if self.type == "SELECT_MIRROR_DRIVER":
            reportString = "Done!"
            anim_data = bpy.context.object.animation_data
            
            bone_active = bpy.context.active_pose_bone
            bones_selected = bpy.context.selected_pose_bones_from_active_object
            #If there is at least one driver in object
            if anim_data != None:
                if anim_data.drivers != None:
                    list_nothing = []
                    list_side = []
                    
                    #bone name dictionary from drivers[].datapath
                    dict_1 = {}
                    
                    #instead of a copy of a dictionary, just have a list of strings of the names of the dictionary
                    #dict_direction = []
                    dict_direction = {}
                    
                    #gets all the drivers with .L or .R
                    for i in enumerate(anim_data.drivers):
                        data_path = i[1].data_path
                        
                        array_index = i[1].array_index
                        
                        #Checks if driver is from a "pose.bone"
                        if data_path.startswith('pose.bones') == True:
                            
                            split = data_path.split('"', 2)
                            nameNormal = split[1]
                            
                            nameFlipped = flipNames(nameNormal)
                            print("nameNormal: %s; nameFlipped: %s;" % (str(nameNormal), str(nameFlipped)) )
                            #splits data_path to get property string name to drive ex. ".rotation_euler"
                            rsplit = data_path.rsplit('.', 1)
                            
                            #name of the bone's property that is driver ex. ".rotation_euler"
                            prop = rsplit[1]
                            
                            #"INDEX" Takes into account if Bone name is flipable
                            if self.sub == "INDEX":
                                #if flippedNames() actually returns a flipped name, else it can't be flipped
                                if nameFlipped == "":
                                    continue
                                
                            #Dictionary Schema: dict_1[nameNormal][prop][array_index]
                            if nameNormal not in dict_1:
                                dict_1[nameNormal] = {}
                                
                            if prop not in dict_1[nameNormal]:
                                dict_1[nameNormal][prop] = {}
                                
                            dict_1[nameNormal][prop][array_index] = i[0]
                            
                            #If the driver is selected, add this driver to dict_direction
                            if i[1].select == True:
                                if self.sub == "INDEX":
                                    #Section to add Driver location to dict_direction
                                    if nameNormal not in dict_direction:
                                        dict_direction[nameNormal] = {}
                                        
                                    if prop not in dict_direction[nameNormal]:
                                        dict_direction[nameNormal][prop] = {}
                                        
                                    dict_direction[nameNormal][prop][array_index] = i[0]
                                    
                                elif self.sub == "PROP_BONE":
                                    #Dictionary Schema: dict_direction[nameNormal][prop]
                                    if nameNormal not in dict_direction:
                                        dict_direction[nameNormal] = {}
                                        
                                    if prop not in dict_direction[nameNormal]:
                                        dict_direction[nameNormal][prop] = {}
                                        
                                elif self.sub == "PROP_BONE_ALL":
                                    #Dictionary Schema: dict_direction[nameNormal]
                                    if nameNormal not in dict_direction:
                                        dict_direction[nameNormal] = {}
                                
                                elif self.sub == "PROP_ALL":
                                    #Dictionary Schema: dict_direction[prop]
                                    if prop not in dict_direction:
                                        dict_direction[prop] = {}
                                
                                
                            #else:
                            #    pass
                        else:
                            print("Skipped: %s" % (str(i)) )
                            
                    print("dict_1: %s" % (str(dict_1)))
                    print("dict_direction: %s" % (str(dict_direction)))
                    
                    #Integer to display in UI how many drivers were affected
                    drivers_effected = 0
                    
                    #Selects the mirrored driver
                    if self.sub == "INDEX":
                        for i in dict_direction:
                            flip_name = flipNames(i)
                            
                            for j in dict_direction[i]:
                                for k in dict_direction[i][j]:
                                    
                                    #Checks if opposite driver exists to select it
                                    if flip_name in dict_1 and j in dict_1[flip_name] and k in dict_1[flip_name][j]:
                                        index_new = dict_1[flip_name][j][k]
                                        driver_to = anim_data.drivers[index_new]
                                        if driver_to.select == False:
                                            drivers_effected+=1
                                        #Selects the mirrored driver
                                        driver_to.select = True
                    #Selects all drivers of a bone with the same property, ex. ".rotation_euler"
                    elif self.sub == "PROP_BONE":
                        for i in dict_direction:
                            flip_name = flipNames(i)
                            
                            for j in dict_direction[i]:
                                for k in dict_1[i][j]:
                                    index_new = dict_1[i][j][k]
                                    driver_to = anim_data.drivers[index_new]
                                    if driver_to.select == False:
                                        drivers_effected+=1
                                    #Selects the mirrored driver
                                    driver_to.select = True
                    #Selects all the drivers of a bone
                    elif self.sub == "PROP_BONE_ALL":
                        for i in dict_direction:
                            flip_name = flipNames(i)
                            
                            for j in dict_1[i]:
                                for k in dict_1[i][j]:
                                    index_new = dict_1[i][j][k]
                                    driver_to = anim_data.drivers[index_new]
                                    if driver_to.select == False:
                                        drivers_effected+=1
                                    #Selects the mirrored driver
                                    driver_to.select = True
                                    
                    #Selects all the drivers with the same property
                    elif self.sub == "PROP_ALL":
                        for a in dict_direction:
                            #flip_name = flipNames(i)
                            for i in dict_1:
                                for j in dict_1[i]:
                                    if j == a:
                                        #for m in dict_1:
                                        for k in dict_1[i][j]:
                                            index_new = dict_1[i][j][k]
                                            driver_to = anim_data.drivers[index_new]
                                            if driver_to.select == False:
                                                drivers_effected+=1
                                            #Selects the mirrored driver
                                            driver_to.select = True
                                            
                    if drivers_effected > 0:
                        reportString = "%d Drivers Effected" % (drivers_effected)
                    else:
                        reportString = "%d Drivers Effected. None Effected" % (drivers_effected)
                        
                else:
                    reportString = "Object[%s] has No Drivers" % (bpy.context.object.name)
            else:
                reportString = "Object[%s] has No Animation_Data" % (bpy.context.object.name)
                
            print(reportString)
            self.report({'INFO'}, reportString)
                
        #Fake "Deletes" Iterate Objects without an Object or Collection pointer
        elif self.type == "PRINT_ALL":
            
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
                
        elif self.type == "MIRROR_DRIVER_FROM_BONE_TEST_PRINT" or self.type == "MIRROR_FROM_DIRECTION":
            
            anim_data = bpy.context.object.animation_data
            
            bone_active = bpy.context.active_pose_bone
            bones_selected = bpy.context.selected_pose_bones_from_active_object
            
            #If there is an active pose bone
            if bone_active != None:
                bone_active_direction = getDirection(bone_active.name)
                print("bone_active_direction: %s" % (bone_active_direction))
                
                #Checks if active bone's name can be flipped
                if bone_active_direction != "":
                    #If there is at least one driver in object
                    if anim_data != None and anim_data.drivers != None:
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
                            
                            #Checks if driver is from a "pose.bone"
                            if data_path.startswith('pose.bones') == True:
                                
                                split = data_path.split('"', 2)
                                nameNormal = split[1]
                                
                                nameFlipped = flipNames(nameNormal)
                                print("nameNormal: %s; nameFlipped: %s;" % (str(nameNormal), str(nameFlipped)) )
                                #splits data_path to get property string name to drive ex. ".rotation_euler"
                                rsplit = data_path.rsplit('.', 1)
                                
                                #name of the bone's property that is driver ex. ".rotation_euler"
                                prop = rsplit[1]
                                
                                #if flippedNames() actually returns a flipped name, else it can't be flipped
                                if nameFlipped != "":
                                    #name of bone and index of the bone's driver
                                    if nameNormal not in dict_1:
                                        dict_1[nameNormal] = {}
                                        
                                    if prop not in dict_1[nameNormal]:
                                        dict_1[nameNormal][prop] = {}
                                        
                                    dict_1[nameNormal][prop][array_index] = i[0]
                                    
                                else:
                                    pass
                            else:
                                print("Passed: %s" % (str(i)) )
                                
                        #These are where the differences in what dict_1 bone names are selected and appended to dict_direction for mirror calculation
                        if self.type == "MIRROR_DRIVER_FROM_BONE_TEST_PRINT":
                            #for loop to only include selected pose bones in armature, not all of them
                            for i in dict_1:
                                #If bone is selected, add it
                                if data.bones[i].select == True:
                                    #checks if the getDirection returned includes ".l", slice is since ".left" has ".l"
                                    #if getDirection(i).find(bone_active_direction[0:2]) > -1:
                                    if getDirection(i).find(bone_active_direction[0]) > -1:
                                        #Adds this bone to the dictionary with its index
                                        #dict_direction[i[0]] = i[1]
                                        dict_direction.append(i)
                        else:
                            #for loop to only include selected pose bones in armature, but takes into account the direction selected in operator
                            print("props.mirror_direction: %s" % (props.mirror_direction))
                            mirror_direction = props.mirror_direction
                            #slice will turn "LEFT" to "l" and lowercase it
                            #to_find = mirror_direction[0:1].lower()
                            to_find = mirror_direction[0].lower()
                            print("to_find: %s" % (to_find))
                            
                            for i in dict_1:
                                flip_name = flipNames(i)
                                
                                #print("getDir(\"%s\"): %s; Flip: %s" % (i, getDirection(i), getDirection(i, flip=True)) )
                                #print("flip_name not in dict_direction: %s = %r" % (flip_name, flip_name not in dict_direction))
                                #If bone is selected, or its mirror exists, and its mirror is selected
                                if data.bones[i].select == True or (data.bones.get(flip_name) is not None and data.bones[flip_name].select == True):
                                    #if getDirection(i).find(bone_active_direction[0:2]) > -1:
                                    #if getDirection(i)[1:].find(to_find) > -1:
                                    if getDirection(i).find(to_find) > -1:
                                        #Checks if the flipped name is already there
                                        boolean = i not in dict_direction
                                        if boolean:
                                            dict_direction.append(i)
                                            
                                        #print("%s = %r" % (i, boolean))
                            
                        #print("\ndict_direction.items(): %s" % (str(dict_direction.items())) )
                        print("\ndict_direction.items(): %s" % (str(dict_direction)) )
                        
                        #For loop to mirror all drivers, and f-curves of selected bones's drivers in dict_direction
                        for i in dict_direction:
                            #print("i: %s" % (i))
                            #nameFlipped = flipNames(i[0])
                            nameFlipped = flipNames(i)
                            #if the nameFlipped from dict_direction isn't in dict_1
                            #if nameFlipped not in dict_1:
                            
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
                                        #print("index_driver Flipped: %r" % (dict_1[flipNames(i)][j][k] is not None) )
                                        #print("index_driver Flipped: %r" % (dict_1.get(nameFlipped).get(j).get(k) is not None) )
                                        print("index_driver Flipped: %r" % (nameFlipped in dict_1 and j in dict_1[nameFlipped] and k in dict_1[nameFlipped][j]) )
                                        
                                        driver_to_flip = anim_data.drivers[index_driver]
                                        #driver_to_flip = anim_data.drivers[dict_1[i] ]
                                        
                                        data_path = driver_to_flip.data_path
                                        
                                        #splits data_path to get property string name to drive ex. ".rotation_euler"
                                        rsplit = data_path.rsplit('.', 1)
                                        
                                        #name of the bone's property that is driver ex. ".rotation_euler"
                                        prop = rsplit[1]
                                        
                                        print("data_path: %s; index: %d" % (data_path, index_driver) )
                                        
                                        #exists is if the flipped driver already existed
                                        exists = False
                                        
                                        if nameFlipped not in dict_1:
                                            #This adds the new driver
                                            driver_new = bpy.context.object.pose.bones[nameFlipped].driver_add(j, k)
                                            
                                            if len(driver_new.modifiers) > 0:
                                                #Removes the 1 modifier created when adding a new driver
                                                driver_new.modifiers.remove(driver_new.modifiers[0])
                                        else:
                                            #if dict_1.get(nameFlipped).get(j).get(k) is not None:
                                            if nameFlipped in dict_1 and j in dict_1[nameFlipped] and k in dict_1[nameFlipped][j]:
                                                exists = True
                                                index_driver_new = dict_1[flipNames(i) ][j][k]
                                                driver_new = bpy.context.object.animation_data.drivers[index_driver_new]
                                            else:
                                                #This adds the new driver
                                                driver_new = bpy.context.object.pose.bones[nameFlipped].driver_add(j, k)
                                                
                                                if len(driver_new.modifiers) > 0:
                                                    #Removes the 1 modifier created when adding a new driver
                                                    driver_new.modifiers.remove(driver_new.modifiers[0])
                                        
                                        print("New Driver: %s; Prop: %s; Index: %d" % (nameFlipped, j, k))
                                        
                                        #This changes the driver_new's properties
                                        
                                        #In "F-Curve" tab panel
                                        driver_new.color_mode = driver_to_flip.color_mode
                                        driver_new.auto_smoothing = driver_to_flip.auto_smoothing
                                        
                                        #Extrapolation is Important for the Driver Keyframe's endswith
                                        driver_new.extrapolation = driver_to_flip.extrapolation
                                        
                                        #In "Drivers" tab panel
                                        driver_new.driver.type = driver_to_flip.driver.type
                                        driver_new.driver.expression = driver_to_flip.driver.expression
                                        driver_new.driver.use_self = driver_to_flip.driver.use_self
                                        
                                        #This bottom section is for 
                                        driver_new_vars = driver_new.driver.variables
                                        #driver_vars is variables of driver_to_flip
                                        driver_vars = driver_to_flip.driver.variables
                                        print("variables: %d" % (len(driver_vars)))
                                        
                                        #print("" % ())
                                        
                                        #If there is at least 1 driver, and override_existing_drivers = True
                                        if len(driver_vars) > 0 and props.override_existing_drivers:
                                            #This will "Overide"/remove all previous variables in the existing mirrored driver, in order for correct new variables to be copied/duplicated
                                            #exists is if the flipped driver already existed
                                            if exists == True:
                                                print("exists == True")
                                                for m in enumerate(reversed(driver_new_vars)):
                                                    print("Removed m[1] variable: %s" % (m[1].name))
                                                    driver_new_vars.remove(m[1])
                                                
                                            #This mirrors the keyframes of the drivers
                                            for m in enumerate(driver_to_flip.keyframe_points):
                                                old_frame = m[1].co[0]
                                                old_value = m[1].co[1]
                                                keyf_name = driver_new.keyframe_points.insert(old_frame, old_value)
                                                
                                                keyf_name.interpolation = m[1].interpolation
                                                
                                                #Left/Right handles of keyframe
                                                #handle_left
                                                keyf_name.handle_left_type = m[1].handle_left_type
                                                
                                                keyf_name.handle_left[0] = m[1].handle_left[0]
                                                keyf_name.handle_left[1] = m[1].handle_left[1]
                                                
                                                #handle_right
                                                keyf_name.handle_right_type = m[1].handle_right_type
                                                
                                                keyf_name.handle_right[0] = m[1].handle_right[0]
                                                keyf_name.handle_right[1] = m[1].handle_right[1]
                                                    
                                            #This mirrors the driver
                                            for m in enumerate(driver_vars):
                                                print("  Var[%d]: \"%s\"; Targets: %d" % (m[0], m[1].name, len(m[1].targets)))
                                                
                                                new_var = driver_new_vars.new()
                                                
                                                new_var.name = m[1].name
                                                new_var.type = m[1].type
                                                
                                                if new_var.type == 'SINGLE_PROP':
                                                    
                                                    new_var.targets[0].id_type = m[1].targets[0].id_type
                                                    new_var.targets[0].id = m[1].targets[0].id
                                                    new_var.targets[0].transform_type = m[1].targets[0].transform_type
                                                    new_var.targets[0].data_path = m[1].targets[0].data_path
                                                    
                                                #if new_var.type is 'TRANSFORMS, ROTATION_DIFF, or LOC_DIFF'
                                                else:
                                                    for p in enumerate(m[1].targets):
                                                        #targets of driver_new's targets
                                                        target_p = new_var.targets[p[0]]
                                                        
                                                        target_p.id = p[1].id
                                                        
                                                        #Checks if target.id has object & object is type "Armature"
                                                        if target_p.id is not None and target_p.id.type == 'ARMATURE':
                                                            #This one checks if nameFlipped2 of bone exists to flip it
                                                            if p[1].bone_target != "":
                                                                nameFlipped2 = flipNames(p[1].bone_target)
                                                                
                                                                #Flips bone name if mirror it exist
                                                                if data.bones.get(nameFlipped2 ) is not None:
                                                                    target_p.bone_target = nameFlipped2
                                                                #Uses unflipped bone name if flipped isn't found
                                                                else:
                                                                    target_p.bone_target = p[1].bone_target
                                                                    print("  \"%s\" isn\'t a bone" % (p[1].bone_target) )
                                                                    
                                                        #if new_var.type == 'TRANSFORMS':
                                                        target_p.transform_type = p[1].transform_type
                                                        target_p.rotation_mode = p[1].rotation_mode
                                                        target_p.transform_space = p[1].transform_space
                                                        
                                                        #elif new_var.type == 'LOC_DIFF':
                                                        #    target_p.transform_space = p[1].transform_space
                                                        
                                                        print("  %d: transform_type: %s" % (p[0], p[1].transform_type))
                                                        
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
                        pass
                        
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
        
class RIG_DEBUGGER_OT_DriverExtrapolation(bpy.types.Operator):
    bl_idname = "rig_debugger.driver_extrapolation"
    bl_label = "Iterate Objects Debugging Operators"
    bl_description = "To assist with debugging and development"
    bl_options = {'UNDO',}
    type: bpy.props.StringProperty(default="DEFAULT")
    #sub: bpy.props.StringProperty(default="DEFAULT")
    #index: bpy.props.IntProperty(default=0, min=0)
    
    def execute(self, context):
        scene = bpy.context.scene
        context = bpy.context
        data = context.object.data
        props = scene.RD_Props
        
        #Creates animation_data if there isn't none
        if self.type != "":
            reportString = "Done!"
            anim_data = bpy.context.object.animation_data
            
            props_extrap = props.driver_extrapolation
            
            #If there is at least one driver in object
            if anim_data != None:
                if anim_data.drivers != None:
                    
                    #bone name dictionary from drivers[].datapath
                    dict_1 = {}
                    
                    #instead of a copy of a dictionary, just have a list of strings of the names of the dictionary
                    #dict_direction = []
                    dict_direction = {}
                    dict_selected = []
                    dict_unselected = []
                    
                    #Schema: [selected drivers, total drivers that are 'LINEAR' or 'CONSTANT'
                    linear = [0,0]
                    constant = [0,0]
                    modes = [0,0]
                    total = 0
                    selected = 0
                    
                    if self.type == "UPDATE":
                        #gets all the drivers with .L or .R
                        for i in enumerate(anim_data.drivers):
                            #If the driver is selected, add this driver to dict_direction
                            if i[1].select == True:
                                if i[1].extrapolation != props_extrap:
                                    #modes is a placeholder to set it as the value of variable linear or constant
                                    modes[0]+= 1
                                    #Changes the extrapolation to the mode set
                                    i[1].extrapolation = props_extrap
                                selected+= 1
                                    
                            total+= 1
                            
                        reportString = "%d/%d Drivers Changed to \"%s\" " % (modes[0], total, props_extrap)
                            
                    if self.type == "PRINT_INFO":
                        #gets all the drivers with .L or .R
                        for i in enumerate(anim_data.drivers):
                            #If the driver is selected, add this driver to dict_direction
                            if i[1].select == True:
                                if i[1].extrapolation != props_extrap:
                                    #modes is a placeholder to set it as the value of variable linear or constant
                                    modes[0]+= 1
                                selected+= 1
                            #else:
                            if i[1].extrapolation != props_extrap:
                                modes[1]+= 1
                                    
                            total+= 1
                            
                        #Sets variables in order to print
                        if props_extrap != 'LINEAR':
                            linear[0] = modes[0]
                            constant[0] = selected-modes[0]
                            
                            linear[1] = modes[1]
                            constant[1] = total-modes[1]
                        else:
                            linear[0] = selected-modes[0]
                            constant[0] = modes[0]
                            
                            linear[1] = total-modes[1]
                            constant[1] = modes[1]
                            
                        print("Total Drivers Extrapolation:" )
                        print("  Linear: %d/%d" % (linear[1], total))
                        print("  Constant: %d/%d" % (constant[1], total))
                        
                        print("Selected Drivers Extrapolation:" )
                        print("  Linear: %d/%d" % (linear[0], selected))
                        print("  Constant: %d/%d" % (constant[0], selected))
                        
                        reportString = "Printed Info to Console"
                        
                else:
                    reportString = "Object[%s] has No Drivers" % (bpy.context.object.name)
            else:
                reportString = "Object[%s] has No Animation_Data" % (bpy.context.object.name)
                
            print(reportString)
            self.report({'INFO'}, reportString)
                
        #Resets default settings
        self.type == "DEFAULT"
        
        return {'FINISHED'}
        
        
class RIG_DEBUGGER_OT_VertexGroup_Ops(bpy.types.Operator):
    bl_idname = "rig_debugger.vertex_group_ops"
    bl_label = "Custom Vertex Group Operators"
    bl_description = "To assist with debugging and development"
    bl_options = {'UNDO',}
    type: bpy.props.StringProperty(default="DEFAULT")
    #include: bpy.props.BoolProperty(default=False)
    #mirror: bpy.props.BoolProperty(default=False)
    #sub: bpy.props.StringProperty(default="DEFAULT")
    #index: bpy.props.IntProperty(default=0, min=0)
    
    def execute(self, context):
        scene = bpy.context.scene
        context = bpy.context
        data = context.object.data
        props = scene.RD_Props
        
        #Creates animation_data if there isn't none
        if self.type == "CREATE_EMPTY_BONE_GROUPS":
            
            if len(context.selected_objects) > 0:
                
                selected_bones = context.selected_pose_bones_from_active_object
                
                if len(selected_bones) > 0:
                    
                    selected_object = None
                    groups_added = 0
                    groups_existing = 0
                    
                    #This is the only way to know for sure that this is the object you want to add vertex groups to
                    if context.object.type == 'MESH':
                        selected_object = context.object
                        
                    #If active object is an Amature, you don't know which object is the Mesh of the armature
                    elif context.object.type == 'ARMATURE':
                        for i in context.selected_objects:
                            #If object is a MESH
                            if i.type == 'MESH':
                                #Checks every modifier to see which one has the armature
                                for j in i.modifiers:
                                    if j.type == 'ARMATURE' and j.show_viewport == True:    
                                        #If the armature is set in the Armature Modifier
                                        if j.object is not None and j.object.type == 'ARMATURE':
                                            selected_object = i
                                            
                    else:
                        reportString = "Object to add Empty Vertex Groups to not Found."
                        pass
                    
                    if selected_object != None:
                        #Goes through every selected bone of armature
                        for i in selected_bones:
                            
                            if selected_object.vertex_groups.get(i.name) is None:
                                selected_object.vertex_groups.new(name=i.name)
                                groups_added+= 1
                            else:
                                groups_existing+=1
                                
                        #if groups_added > 0:
                        groups_total = groups_added + groups_existing
                        reportString = "Added %d/%d New Vertex Groups to \"%s\"" % (groups_added, groups_total, selected_object.name)
                    else:
                        pass
                        
                else:
                    reportString = "No Bones Selected!"
            else:
                reportString = "Only one object selected"
                
            print(reportString)
            self.report({'INFO'}, reportString)
                
        #Resets default settings
        self.type == "DEFAULT"
        
        return {'FINISHED'}

class RIG_DEBUGGER_OT_VertexGroupInfluence(bpy.types.Operator):
    bl_idname = "rig_debugger.vertex_group_influence"
    bl_label = "Custom Vertex Group Operators"
    bl_description = "To assist with debugging and development"
    bl_options = {'UNDO',}
    type: bpy.props.StringProperty(default="DEFAULT")
    include: bpy.props.BoolProperty(default=False)
    mirror: bpy.props.BoolProperty(default=False)
    #sub: bpy.props.StringProperty(default="DEFAULT")
    #index: bpy.props.IntProperty(default=0, min=0)
    
    #Resets default settings
    #@classmethod
    #@staticmethod
    def resetSelf(self):
        self.type = "DEFAULT"
        self.include = False
        self.mirror = False
        print("Reset States: %s, %d, %d" % (self.type, self.include, self.mirror) )
        #return None
    
    #This function will check to change/reset the previous mode of the object for operator to work
    def previous_mode(self, prev_mode, object, before=True):
        #sets string prev_mode
        #ob = context.object
        print("prev_mode1: %s" % (prev_mode) )
        ob = object
        #prev_mode = ob.mode
        mode_to_set = 'OBJECT'
        
        #This checks to see if this is before the operator starts or after to reset the previous object mode
        if before == True:
            if prev_mode != mode_to_set:
                #prev_mode = ob.mode
                bpy.ops.object.mode_set(mode = mode_to_set)
                debug = "Changed Mode 2 \"%s\" to \"%s\" " % (prev_mode, mode_to_set)
            else:
                debug = "previous_mode() 2 nothing happened"
        else:
            if prev_mode != mode_to_set:
                #prev_mode = ob.mode
                bpy.ops.object.mode_set(mode = prev_mode)
                debug = "Changed Mode 3 \"%s\" to \"%s\" " % (mode_to_set, prev_mode)
            else:
                debug = "previous_mode() 3 nothing happened"
        
        print(debug)
        #print("prev_mode4: %s" % (ob.mode) )
        return None#prev_mode
        
    
    #Goes to EDIT mode for .select_mirror() poll context, to select the mirror vertices of Mesh Object
    def selectMirror(self, prev_mode, object):
        #sets string prev_mode
        #ob = context.object
        print("prev_mode1: %s" % (prev_mode) )
        ob = object
        #prev_mode = ob.mode
        mode_to_set = 'EDIT'
        
        #This checks to see if this is before the operator starts or after to reset the previous object mode
        if prev_mode != mode_to_set:
            #prev_mode = ob.mode
            bpy.ops.object.mode_set(mode = mode_to_set)
            debug = "Changed Mode 2 \"%s\" to \"%s\" " % (prev_mode, mode_to_set)
            #Selects the mirror vertices of Mesh
            bpy.ops.mesh.select_mirror(axis={'X'}, extend=True)
        else:
            debug = "previous_mode() 2 nothing happened"
        
        print(debug)
        #print("prev_mode4: %s" % (ob.mode) )
        return None#prev_mode
        
    #def index_check(type):
    def index_check(index, type, iterator=None):
        if type == "ADD":
            print("bruh")
        if type == "REMOVE":
            if len(iterator) > 0 and index > 0:
                index-=1
                #print("bruh")
        return index
    
    @classmethod
    def poll(cls, context):
        #scene = bpy.context.scene
        #props = scene.IM_Props
        #The wanted object types
        ob_types = ["MESH"]
        
        #if wanted object type is inside ob_types
        return context.object.type in ob_types
    
    def execute(self, context):
        scene = bpy.context.scene
        #context = bpy.context
        ob = context.object
        #context = bpy.context
        data = context.object.data
        props = scene.RD_Props
        #print("" % () )
        vg = bpy.context.object.vertex_groups
        vg_active = vg.active
        
        reportString = "Done!"
        
        #Function is only needed here, so no reason to have it out. If you do, add "self" parameter to beginning
        #Checks if vertex_group name was already added to props.vertex_groups
        def groupExists(vertex_group_active, groups):
            #groups = props.vertex_groups
            for i in groups:
                if i.name == vertex_group_active.name:
                    return True
                    
            return False
        
        #Gets all selected vertices of object and returns list of vertex indexes
        def getSelectedVertices(mesh_object):
            ob = mesh_object
            verts = []
            
            for i in ob.data.vertices:
                if i.select == True:
                    verts.append(i.index)
                    
            return verts
            
        #Gets list of Vertex Groups indexes from props.vertex_groups
        def getVerGpsProps(propGroup, object):
            ob = object
            vertex_group_index_list = []
            
            for i in propGroup:
                #Checks if name is in vertex_groups
                if i.name in ob.vertex_groups and i.use == True:
                    #Checks if it isn't a duplicate
                    if ob.vertex_groups[i.name].index not in vertex_group_index_list:
                        vertex_group_index_list.append(i.index)
                    
            return vertex_group_index_list
            
        #Creates a dictionary of Vertex Group indexes, to use for Statistical purposes
        def createVerGpsDictStats(vertex_group_index_list):
            dict = {}
            
            for i in vertex_group_index_list:
                dict[i] = {}
                #For the number of vertices in the Vertex Group
                dict[i]["verts"] = 0
                    
            return dict
            
        #Creates a list of Vertex Group indexes that are still needed for Vertex
        def createVerGpsNeeded(groups_in, vg_props):
            #groups_in, an incomplete index list of Vertex Groups of vertex already from vg_props
            #vg_props, complete index list of Vertex Groups from vg_props
            groups_need = vg_props[::]
            
            for m in groups_in:
                if m in groups_need:
                    groups_need.remove(m)
                    
            return groups_need
            
        
        #Creates animation_data if there isn't none
        if self.type == "FROM_SELECTION":
            #previous mode
            prev_mode = context.object.mode
            #print("prev_mode1: %s" % (prev_mode) )
            #Either EXCLUDE or INCLUDE
            inclusion = props.inclusion
            vg_weight = props.vertex_group_weight
            select_mirror = props.include_mirror_selection
            
            if select_mirror:
                self.selectMirror(prev_mode, ob)
            
            #previous_mode(self, prev_mode, context, before=True)
            self.previous_mode(prev_mode, ob, before=True)
            
            verts = getSelectedVertices(ob)
            
            #index list of props.vertex_groups to compare to object vertex_groups
            vg_props = getVerGpsProps(props.vertex_groups, ob)
            
            #dictionary used for statsistics of Vertex Groups and Vertices affected
            vg_stats = createVerGpsDictStats(vg_props)
            
            #If the object has at least 1 vertex group
            if len(context.object.vertex_groups) > 0:
                
                if inclusion == "INCLUDE":
                    if len(vg_props) > 0:
                        #Every selected vertex
                        for i in verts:
                            if len(ob.data.vertices[i].groups) > 0:
                                
                                groups_in = []
                                #Need to find a better solution that having this as a list
                                bruh = [i]
                                
                                #For every Vertex Group of Vertex
                                for j in ob.data.vertices[i].groups:
                                    if j.group in vg_props:
                                        #You need a function to print out the stats, this isn't implemented yet though.
                                        vg_stats[j.group]["verts"] += 1
                                        
                                        groups_in.append(j.group)
                                        #ob.data.vertices[i]
                                        print("Vertex: %d" % (i) )
                                        #ob.vertex_groups[j.group].add(i, vg_weight, 'REPLACE')
                                        #bruh = [i]
                                        ob.vertex_groups[j.group].add(bruh, vg_weight, 'REPLACE')
                                #"""
                                #list of Vertex Groups the Vertex isn't part of
                                groups_need = createVerGpsNeeded(groups_in, vg_props)
                                
                                #Adds Vertex Groups the Vertex still needs to apply a weight value
                                for m in groups_need:
                                    vg_new = ob.vertex_groups.new(name=ob.vertex_groups[m].name)
                                    vg_new.add(bruh, vg_weight, 'REPLACE')
                        
                    else:
                        reportString = "INCLUDE: 0 Vertex Groups"
                elif inclusion == "EXCLUDE":
                    reportString = "EXCLUDE: Function Option Not Implemented Yet. Nothing Happened."
                #bpy.context.object.vertex_groups.active.name
                #bpy.context.object.vertex_groups.active_index
                
                self.previous_mode(prev_mode, ob, before=False)
                
            else:
                reportString = "Object \"%s\" has no Vertex Groups" % (ob.name)
            
        """
        elif self.type == "REMOVE":
            if len(props.vertex_groups) > 0:
                props.vertex_groups.remove(props.RD_ULIndex )
                
                if props.RD_ULIndex >= len(props.vertex_groups):
                    props.RD_ULIndex = len(props.vertex_groups)-1
        #"""
        #Resets default settings
        #self.resetSelf()
        #self.resetSelf(self)
        self.resetSelf()
        
        print(reportString)
        self.report({'INFO'}, reportString)
        return {'FINISHED'}
        
class RIG_DEBUGGER_OT_VertexGroup_UIOps(bpy.types.Operator):
    bl_idname = "rig_debugger.vertex_group_ui_ops"
    bl_label = "Custom Vertex Group Operators"
    bl_description = "To assist with debugging and development"
    bl_options = {'UNDO',}
    type: bpy.props.StringProperty(default="DEFAULT")
    include: bpy.props.BoolProperty(default=False)
    mirror: bpy.props.BoolProperty(default=False)
    #sub: bpy.props.StringProperty(default="DEFAULT")
    #index: bpy.props.IntProperty(default=0, min=0)
    
    #Resets default settings
    #@classmethod
    @staticmethod
    def resetSelf(self):
        self.type = "DEFAULT"
        self.include = False
        self.mirror = False
        print("Reset States: %s, %d, %d" % (self.type, self.include, self.mirror) )
        #return None
        
    def __init__(self):
        print("Start")

    def __del__(self):
        print("End")
        
    #def index_check(type):
    def index_check(index, type, iterator=None):
        if type == "ADD":
            print("bruh")
        if type == "REMOVE":
            if len(iterator) > 0 and index > 0:
                index-=1
                #print("bruh")
        return index
    
    @classmethod
    def poll(cls, context):
        #scene = bpy.context.scene
        #props = scene.IM_Props
        #The wanted object types
        ob_types = ["MESH"]
        
        #if wanted object type is inside ob_types
        return context.object.type in ob_types
    
    def execute(self, context):
        scene = bpy.context.scene
        #context = bpy.context
        data = context.object.data
        props = scene.RD_Props
        #print("" % () )
        vg = bpy.context.object.vertex_groups
        vg_active = vg.active
        
        reportString = "Done!"
        
        def groupExists(vg_active, groups):
            #groups = props.vertex_groups
            for i in groups:
                if i.name == vg_active.name:
                    return True
                    
            return False
        
        #Creates animation_data if there isn't none
        if self.type == "ADD":
            
            if len(context.object.vertex_groups) > 0:
                
                #bpy.context.object.vertex_groups.active.name
                #bpy.context.object.vertex_groups.active_index
                
                if groupExists(vg_active, props.vertex_groups) == False:
                    
                    group_new = props.vertex_groups.add()
                    group_new.name = vg_active.name
                    group_new.index = vg_active.index
                    
                    props.RD_ULIndex = len(props.vertex_groups)-1
                    
                    reportString = "Added: \"%s\" " % (group_new.name)
                else:
                    reportString = "Vertex Group: \"%s\" already added " % (vg_active.name)
            
        elif self.type == "REMOVE":
            if len(props.vertex_groups) > 0:
                props.vertex_groups.remove(props.RD_ULIndex )
                
                if props.RD_ULIndex >= len(props.vertex_groups):
                    props.RD_ULIndex = len(props.vertex_groups)-1
        #Resets default settings
        #self.resetSelf()
        self.resetSelf(self)
        
        print(reportString)
        self.report({'INFO'}, reportString)
        return {'FINISHED'}

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

class RIG_DEBUGGER_WEIGHTGROUPS_UL_items(bpy.types.UIList):
    
    #Checks if the .name is found in the object's Vertex Groups
    def isVertexGroup(self, item, object):
        ob = object
        #props = context.scene.RD_Props
        
        #If props.vertex_group is in object's vertex group
        if item.name in ob.vertex_groups:
            return True
            
        return False
        
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        scene = bpy.context.scene
        data = bpy.data
        props = scene.RD_Props
        
        #active = props.RIA_ULIndex
        RDCollect = props.vertex_groups
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            
            if len(RDCollect) > 0:
                row = layout.row(align=True)
                
                #function to change icon for error
                if self.isVertexGroup(item, context.object) == False:
                    usedIcon = 'ERROR'
                else:
                    usedIcon = 'BLANK1'
                    
                row.label(text="", icon=usedIcon)
                row.prop(item, "use", text="")
                row.prop(item, "name", text="", emboss=False)
                #row.prop(item, "index", text="")
                    
            else:
                row.label(text="No Iterations Here")
                
        #Theres nothing in this layout_type since it isn't intended to be used.
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'

    def invoke(self, context, event):
        pass

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
        
        row = col.row(align=True)
        row.label(text="Mirror Drivers:")
        
        row = col.row(align=True)
        button = row.operator("rig_debugger.driver_mirror", icon="BONE_DATA", text="Active Bone Mirror Driver Test")
        #button.type = "MIRROR_FROM_ACTIVE_BONE"
        button.type = "ARMATURE"
        button.sub = "ACTIVE_BONE_ALL"
        
        col.separator()
        
        row = col.row(align=True)
        button = row.operator("rig_debugger.driver_mirror", icon="BONE_DATA", text="Mirror Driver From Direction")
        #button.type = "MIRROR_FROM_DIRECTION"
        button.type = "ARMATURE"
        button.sub = "FROM_DIRECTION_ALL"
        
        
        row = col.row(align=True)
        row.prop(props, "mirror_direction", emboss= True, expand= True, icon="NONE")
        
        
        row = col.row(align=True)
        row.prop(props, "override_existing_drivers", text="", emboss= True, icon="NONE")#"DECORATE_OVERRIDE")
        row.prop(props, "override_existing_drivers", text="Override Existing Drivers", emboss= False, icon="DECORATE_OVERRIDE")
        
        row = col.row(align=True)
        row.prop(props, "override_existing_fcurves", text="", emboss= True, icon="NONE")#"DECORATE_OVERRIDE")
        row.prop(props, "override_existing_fcurves", text="Override Existing F-Curves", emboss= False, icon="DECORATE_OVERRIDE")
        
        col.separator()
        
        row = col.row(align=True)
        row.prop(props, "debug_mode", text="Debug Panels", icon="DECORATE_OVERRIDE")
        
        #End of CustomPanel
        
class RIG_DEBUGGER_PT_CustomPanel1_Debug(bpy.types.Panel):
    #A Custom Panel in Viewport
    #bl_idname = "RIG_DEBUGGER_PT_CustomPanel1"
    bl_parent_id = "RIG_DEBUGGER_PT_CustomPanel1"
    bl_label = "Debug Operators"
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
        
        row = col.row(align=True)
        row.label(text="Print: ")
        
        row = col.row(align=True)
        row.operator("rig_debugger.debug", icon="INFO", text="Mirror Driver Test V2").type = "MIRROR_DRIVER_TEST_PRINT_V2"
        
        row = col.row(align=True)
        row.operator("rig_debugger.debug", text="Active Bone Direction and Flip").type = "PRINT_ACTIVE_BONE_FLIPPED"
        
        row = col.row(align=True)
        row.operator("rig_debugger.debug", text="Mirror Driver Test V1").type = "MIRROR_DRIVER_TEST_PRINT_V1"
        
        row = col.row(align=True)
        row.operator("rig_debugger.debug", text="All Driver UI Info").type = "PRINT_ALL_DRIVER_UI_INFO"
        
        row = col.row(align=True)
        row.operator("rig_debugger.debug", text="Add Driver Mirror Info Test").type = "PRINT_ADD_DRIVER_MIRROR_INFO_TEST"
        
        #Just to test my FlipNames function
        
        row = col.row(align=True)
        row.label(text="Adding: ")
        
        row = col.row(align=True)
        row.operator("rig_debugger.debug", text="Mirror Driver Test").type = "MIRROR_DRIVER_TEST"
        
        #End of CustomPanel
        
class RIG_DEBUGGER_PT_CustomPanel2(bpy.types.Panel):
    #A Custom Panel in Viewport
    bl_idname = "RIG_DEBUGGER_PT_CustomPanel2"
    bl_label = "Driver Debugger"
    bl_space_type = "GRAPH_EDITOR"
    bl_region_type = 'UI'
    #bl_context = "output"
    bl_category = "Driver Debugger"
    
    # draw function
    def draw(self, context):
                 
        layout = self.layout
        ob = bpy.context.object
        scene = context.scene
        props = scene.RD_Props
        
        #Layout Starts
        col = layout.column()
        
        row = col.row(align=True)
        row.label(text="Mirror Drivers:")
        
        row = col.row(align=True)
        button = row.operator("rig_debugger.driver_mirror", icon= "DRIVER", text="From Active Drivers")
        #button.type = "MIRROR_FROM_ACTIVE_DRIVERS"
        button.type = "DRIVER_EDITOR"
        button.sub = "ACTIVE_DRIVERS"
        
        row = col.row(align=True)
        button = row.operator("rig_debugger.driver_mirror", icon= "DRIVER", text="From Active Drivers and Direction")
        #button.type = "MIRROR_FROM_DIRECTION_DRIVERS"
        button.type = "DRIVER_EDITOR"
        button.sub = "ACTIVE_FROM_DIRECTION"
        
        row = col.row(align=True)
        row.prop(props, "mirror_direction", emboss= True, expand= True, icon="NONE")
        
        row = col.row(align=True)
        row.prop(props, "override_existing_drivers", text="", emboss= True, icon="NONE")#"DECORATE_OVERRIDE")
        row.prop(props, "override_existing_drivers", text="Override Existing Drivers", emboss= False, icon="DECORATE_OVERRIDE")
        
        row = col.row(align=True)
        row.prop(props, "override_existing_fcurves", text="", emboss= True, icon="NONE")#"DECORATE_OVERRIDE")
        row.prop(props, "override_existing_fcurves", text="Override Existing F-Curves", emboss= False, icon="DECORATE_OVERRIDE")
        
        col.separator()
        
        #Debug Operators
        row = col.row(align=True)
        row.label(text="Select Drivers:")
        
        row = col.row(align=True)
        button = row.operator("rig_debugger.driver_ops", text="Mirror Drivers")
        button.type = "SELECT_MIRROR_DRIVER"
        button.sub = "INDEX"
        
        row = col.row(align=True)
        button = row.operator("rig_debugger.driver_ops", text="Select Bone Drivers With Property")
        button.type = "SELECT_MIRROR_DRIVER"
        button.sub = "PROP_BONE"
        
        row = col.row(align=True)
        button = row.operator("rig_debugger.driver_ops", text="From Active Bones")
        button.type = "SELECT_MIRROR_DRIVER"
        button.sub = "PROP_BONE_ALL"
        
        row = col.row(align=True)
        button = row.operator("rig_debugger.driver_ops", text="All Drivers With Property")
        button.type = "SELECT_MIRROR_DRIVER"
        button.sub = "PROP_ALL"
        
        col.separator()
        
        anim_data = ob.animation_data
        
        #row = col.row(align=True)
        
        
        #icon = "IPO_CONSTANT" if props.driver_extrapolation is 'CONSTANT' else "IPO_LINEAR"
        
        row = col.row(align=True)
        row.label(text="Effect Selected Drivers:")
        
        row = col.row(align=True)
        row.operator("rig_debugger.driver_extrapolation", text="Set Extrapolation").type = "UPDATE"
        row.prop(props, "driver_extrapolation", icon="NONE", text="", emboss= True, expand= False)
        
        #End of CustomPanel
        
class RIG_DEBUGGER_PT_CustomPanel2_Debug(bpy.types.Panel):
    #A Custom Panel in Viewport
    #bl_idname = "RIG_DEBUGGER_PT_CustomPanel2"
    bl_parent_id = "RIG_DEBUGGER_PT_CustomPanel2"
    bl_label = "Driver Debugger"
    bl_space_type = "GRAPH_EDITOR"
    bl_region_type = 'UI'
    #bl_context = "output"
    bl_category = "Driver Debugger"
    
    # draw function
    def draw(self, context):
                 
        layout = self.layout
        ob = bpy.context.object
        scene = context.scene
        props = scene.RD_Props
        
        #Layout Starts
        col = layout.column()
        
        row = col.row(align=True)
        row.label(text="Print: ")
        
        row = col.row(align=True)
        row.operator("rig_debugger.driver_extrapolation", icon="INFO", text="Print Active Driver Extrapolation Info").type = "PRINT_INFO"
            
        #End of CustomPanel
        
#Class to inherit the draw() function from for UI Panel
class DriverInfoDraw:
    
    # draw function
    def draw(self, context):
                 
        layout = self.layout
        ob = bpy.context.object
        scene = context.scene
        props = scene.RD_Props
        
        #Layout Starts
        col = layout.column()
        
        #row = col.row(align=True)
        
        anim_data = ob.animation_data
            
        if ob.animation_data is not None:
            drivers = len(ob.animation_data.drivers)
        else:
            drivers = "[No Animation Data]"
            
        row = col.row(align=True)
        row.prop(props, "dropdown_1", text="", icon="DOWNARROW_HLT")
        row.label(icon= "DRIVER", text="Armature Drivers: %s" % (str(drivers)) )
        
        
        
        if props.dropdown_1 == True:
            if type(drivers) != str:
                row = col.row(align=True)
                row.label(icon= "HIDE_OFF", text="Hidden: %d/%d" % (calculateUIALL("hide"), drivers) )
                
                row = col.row(align=True)
                row.label(icon= "CHECKBOX_HLT", text="Muted: %d/%d" % (calculateUIALL("mute"), drivers) )
                
                row = col.row(align=True)
                row.label(icon= "DECORATE_LOCKED", text="Locked: %d/%d" % (calculateUIALL("lock"), drivers) )
                
                row = col.row(align=True)
                row.label(icon= "MODIFIER_ON", text="With Modifiers: %d/%d" % (calculateUIALL("modifiers"), drivers) )
                
            else:
                row = col.row(align=True)
                row.operator("rig_debugger.debug", icon="INFO", text="Create Animation_Data").type = "CREATE_ANIMATION_DATA"
                
    #End of DriverInfoDraw
        
#Class to inherit the draw() function from for UI Panel
class VertexGroupsOpsDraw:
    
    # draw function
    def draw(self, context):
                 
        layout = self.layout
        ob = bpy.context.object
        scene = context.scene
        props = scene.RD_Props
        
        #Layout Starts
        col = layout.column()
        
        row = col.row(align=True)
        row.label(text="Create Vertex Groups:")
        row = col.row(align=True)
        row.operator("rig_debugger.vertex_group_ops", text="Empty Vertex Groups From Bones", icon="GROUP_VERTEX").type = "CREATE_EMPTY_BONE_GROUPS"
        
        col.separator()
        
        row = col.row(align=True)
        row.label(text="Influence Vertex Groups:")
        
        row = col.row(align=True)
        button = row.operator("rig_debugger.vertex_group_influence", text="From Vertex Selection", icon="RESTRICT_SELECT_OFF")
        button.type = "FROM_SELECTION"
        
        col.separator()
        
        row = col.row(align=True)
        row.prop(props, "inclusion", expand=True)
        
        row = col.row(align=True)
        row.prop(props, "vertex_group_weight", expand=True)
        
        row = col.row(align=True)
        row.prop(props, "include_mirror_selection", expand=True)
        
        #col.separator()
        
        #Start of template_list UI
        row = col.row(align=True)
        row.label(text="Selected Vertex Groups:")
        
        #Splitting for the template_list
        split = layout.row(align=False)
        col = split.column(align=True)
        
        row = col.row(align=True)
        row.template_list("RIG_DEBUGGER_WEIGHTGROUPS_UL_items", "custom_def_list", props, "vertex_groups", props, "RD_ULIndex", rows=3)
        
        #Side_Bar Operators
        col = split.column(align=True)
        
        row = col.row(align=True)
        button = row.operator("rig_debugger.vertex_group_ui_ops", text="", icon="X")
        button.type = "REMOVE"
        
        #Reset the col to column
        col = layout.column()
        
        row = col.row(align=True)
        row.label(text="Object Vertex Groups:")
        
        #Splitting for the template_list
        split = layout.row(align=False)
        col = split.column(align=True)
        
        row = col.row(align=True)
        ob = context.object
        row.template_list("MESH_UL_vgroups", "", ob, "vertex_groups", ob.vertex_groups, "active_index", rows=4)
        
        col = split.column(align=True)
        
        row = col.row(align=True)
        button = row.operator("rig_debugger.vertex_group_ui_ops", text="", icon="ADD")
        button.type = "ADD"
        
        
        
        #End of CustomPanel
        
class RIG_DEBUGGER_PT_DriverInfo1(DriverInfoDraw, bpy.types.Panel):
    #A Custom Panel in Viewport
    #bl_idname = "RIG_DEBUGGER_PT_DriverInfo1"
    #bl_parent_id = "RIG_DEBUGGER_PT_CustomPanel2", "RIG_DEBUGGER_PT_CustomPanel1"
    bl_label = "Armature Drivers Info"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    #bl_context = "output"
    bl_category = "Rig Debugger"

#class RIG_DEBUGGER_PT_DriverInfo2(RIG_DEBUGGER_PT_DriverInfo1, bpy.types.Panel):
class RIG_DEBUGGER_PT_DriverInfo2(DriverInfoDraw, bpy.types.Panel):
    bl_label = "Armature Drivers Info"
    bl_space_type = "GRAPH_EDITOR"
    bl_region_type = 'UI'
    #bl_context = "output"
    bl_category = "Driver Debugger"
    

    
class RIG_DEBUGGER_PT_VertexGroups1(VertexGroupsOpsDraw, bpy.types.Panel):
    #A Custom Panel in Viewport
    #bl_idname = "RIG_DEBUGGER_PT_DriverInfo1"
    #bl_parent_id = "RIG_DEBUGGER_PT_CustomPanel2", "RIG_DEBUGGER_PT_CustomPanel1"
    bl_label = "Vertex Groups Ops"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    #bl_context = "output"
    bl_category = "Rig Debugger"
    
#Note: The driver editor doesn't have a use for this panel or its ops
"""
class RIG_DEBUGGER_PT_VertexGroups2(VertexGroupsOpsDraw, bpy.types.Panel):
    bl_label = "Vertex Groups Ops"
    bl_space_type = "GRAPH_EDITOR"
    bl_region_type = 'UI'
    #bl_context = "output"
    bl_category = "Driver Debugger"
#"""

    
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
    

    
class RIG_DEBUGGER_WeightGroups(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="", default="Name")
    index: bpy.props.IntProperty(name="Int", description="", default= 0, min=0)
    use: bpy.props.BoolProperty(name="Use for calculation", description="Toggle if this Vertex Group will be used in caclulation", default=True)
    
def registerDebugPanelClasses(self, context):
    """
    print("self: %s, class: %s" % (self, self.__class__) )
    print("dir: %s" % (str(dir(self)) ) )
    print("dir.__class__: %s" % (str(dir(self.__class__)) ) )
    print("self.__class__.__name__: %s" % (str(self.__class__.__name__) ) )
    print("context: %s" % (context) )
    #"""
    propertyClassName = self.__class__.__name__
    
    attributeName = "debug_mode"
    
    if hasattr(self, attributeName):
        mode = getattr(self, attributeName)
        print("Mode: %s" % (mode) )
        
        registerClassName = "RIG_DEBUGGER_PT_CustomPanel1_Debug"
        
        if mode == False:
            if hasattr(bpy.types, registerClassName) == True:
                bpy.utils.unregister_class(bpy.types.RIG_DEBUGGER_PT_CustomPanel1_Debug)
                print("Unregistered: %s" % (registerClassName) )
            else:
                print("Already UnRegistered: %s" % (registerClassName) )
        else:
            if hasattr(bpy.types, registerClassName) == False:
                #bpy.utils.register_class(bpy.types.RIG_DEBUGGER_PT_CustomPanel1_Debug)
                bpy.utils.register_class(RIG_DEBUGGER_PT_CustomPanel1_Debug)
                print("Registered: %s" % (registerClassName) )
            else:
                print("Already Registered: %s" % (registerClassName) )
        
    else:
        print("Class: %s missing attribute %s" % (propertyClassName, attributeName) )
    
    return None
    
class RIG_DEBUGGER_Props(bpy.types.PropertyGroup):
    #Tries to set collection_parent's default to Master Collection
    override_existing_drivers: bpy.props.BoolProperty(name="Override Existing Drivers", description="Overrides the drivers of the existing flipped driver", default=False)
    
    override_existing_fcurves: bpy.props.BoolProperty(name="Override Existing F-Curves", description="Overrides the F-Curves of drivers of the existing flipped driver", default=False)
    
    listDesc0 =  ["Displays List in order of how many duplicates each object has", "Displays List in the order they were created"]
    
    mirror_direction: bpy.props.EnumProperty(name="Mirror Direction", items= [("LEFT", "Left", listDesc0[0]), ("RIGHT", "Right", listDesc0[1])], description="Bone Name Direction to Mirror Drivers from", default="LEFT")#, update=ListOrderUpdate)
    
    driver_extrapolation: bpy.props.EnumProperty(name="Driver Extrapolation", items= [("CONSTANT", "Constant", listDesc0[1], "IPO_CONSTANT", 0), ("LINEAR", "Linear", listDesc0[0], "IPO_LINEAR", 1)], description="Extrapolation mode of Driver", default="LINEAR")
    
    #Dropdown for Iterate Display
    dropdown_1: bpy.props.BoolProperty(name="Dropdown", description="Show Props of all Drivers", default=True)
    
    dropdown_debugger: bpy.props.BoolProperty(name="Dropdown", description="Show Props of active Driver", default=True)
    
    #collection_active: bpy.props.PointerProperty(name="Collection to add Collections for Object duplicates", type=bpy.types.Collection)
    
    #Booleans for locking default collection of parent
    
    lock_active: bpy.props.BoolProperty(name="Lock Collection of Active", description="When locked, you can now edit the name of the selected collection", default=False)
    
    #For rig_debugger.vertex_group_ops TOP
    vertex_groups: bpy.props.CollectionProperty(type=RIG_DEBUGGER_WeightGroups)
    
    RD_ULIndex: bpy.props.IntProperty(name="List Index", description="UI List Index", default= 0, min=0)
    
    inclusion_desc = ("Bruh Moment", "OOOOOOOF")
    
    inclusion: bpy.props.EnumProperty(name="Inclusion Type", items= [("EXCLUDE", "Exclude", inclusion_desc[0]), ("INCLUDE", "Include", inclusion_desc[1])], description="Inclusion mode of influencing Vertex Groups", default="INCLUDE")
    
    vertex_group_weight: bpy.props.FloatProperty(name="Vertex Group Weight", description="To set the weight", default= 0.0, min=0.0, max=1.0)
    
    include_mirror_selection: bpy.props.BoolProperty(name="Include Mirrored Vertices", description="Also Mirror the selection of the Weights", default=False)
    
    #For rig_debugger.vertex_group_ops BOTTOM
    
    
    
    debug_mode: bpy.props.BoolProperty(name="Display Debug Operators", description="To aid in Debugging Operators. Displayed in \"Display Settings\"", default=True, update=registerDebugPanelClasses)
    
    #For Iterate Collection Settings and Operators
    
    #hide_types_last
    #hide_last: bpy.props.BoolProperty(name="Exclude Recent Iteration", description="When using the operators for toggling \"all objects\"", default=False)
    
#Classes that are registered
classes = (
    RIG_DEBUGGER_WeightGroups,
    RIG_DEBUGGER_Props,
    
    RIG_DEBUGGER_OT_Debugging,
    RIG_DEBUGGER_OT_DriverMirror,
    RIG_DEBUGGER_OT_DriverOps,
    RIG_DEBUGGER_OT_DriverExtrapolation,
    
    RIG_DEBUGGER_OT_VertexGroup_Ops,
    RIG_DEBUGGER_OT_VertexGroupInfluence,
    #RIG_DEBUGGER_OT_UIOperators,
    RIG_DEBUGGER_OT_VertexGroup_UIOps,
    
    #RIG_DEBUGGER_UL_items,
    
    RIG_DEBUGGER_WEIGHTGROUPS_UL_items,
    RIG_DEBUGGER_PT_CustomPanel1,
    RIG_DEBUGGER_PT_CustomPanel1_Debug,
    
    RIG_DEBUGGER_PT_CustomPanel2,
    RIG_DEBUGGER_PT_CustomPanel2_Debug,
    
    RIG_DEBUGGER_PT_DriverInfo1,
    RIG_DEBUGGER_PT_DriverInfo2,
    
    RIG_DEBUGGER_PT_VertexGroups1,
    #RIG_DEBUGGER_PT_VertexGroups2,
    
    RIG_DEBUGGER_PreferencesMenu,
    
    #RIG_DEBUGGER_CollectionObjects,
    #RIG_DEBUGGER_Props,
)

def register():
    #ut = bpy.utils
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
        print("Class Name: %s" % (cls.__name__) )
    
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
