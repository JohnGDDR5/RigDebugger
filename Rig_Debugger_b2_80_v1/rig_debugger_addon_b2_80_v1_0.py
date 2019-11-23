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

        
class RIG_DEBUGGER_OT_Debugging(bpy.types.Operator):
    bl_idname = "rig_debugger.debug"
    bl_label = "Iterate Objects Debugging Operators"
    bl_description = "To assist with debugging and development"
    bl_options = {'UNDO',}
    type: bpy.props.StringProperty(default="DEFAULT")
    #index: bpy.props.IntProperty(default=0, min=0)
    
    def execute(self, context):
        scene = bpy.context.scene
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
                
        elif self.type == "PRINT_DRIVER_TEST":
            
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
                
                reportString = "Done!"
                
                print(reportString)
                self.report({'INFO'}, reportString)
            
            else:
                reportString = "Object[%s] has No Drivers" % (bpy.context.object.name)
                
                print(reportString)
                self.report({'INFO'}, reportString)
                
        elif self.type == "ADD_DRIVER_TEST":
            
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
                    
                    def flipNames(string):
                        
                        case_low = string.lower()
                        
                        #sides = (".l", ".L", ".r", ".R", ".left", ".right", ".Left", ".Right")
                        #sides = (".l", ".r", ".left", ".right")
                        #sides = (".l", ".r")
                        
                        #sides = (".l", ".L", ".r", ".R", ".left", ".right", ".Left", ".Right")
                        sides = (".l", ".r", ".left", ".right")
                        side = -1
                        side2 = 0
                        
                        index = 0
                        
                        #Only needs to use ".l" and ".r"
                        for j in enumerate(sides[0:2]):
                            rfound = case_low.rfind( sides[j[0]] )
                            if rfound > -1:
                                print("rfound: %d" % (rfound))
                                if j[1] == ".l":
                                    #if (rfound+1) == len(string)-1:   
                                    if case_low.rfind( ".left", rfound ) > -1:
                                        side = 2
                                        index = rfound
                                        break
                                    else:
                                        side = 0
                                        index = rfound
                                        break
                                elif j[1] == ".r":
                                    #if (rfound+1) == len(string)-1:   
                                    if case_low.rfind( ".right", rfound ) > -1:
                                        side = 3
                                        index = rfound
                                        break
                                    else:
                                        side = 1
                                        index = rfound
                                        break
                            else:
                                print("Side = -1")
                                pass
                        """
                        def convCase(index1, string1, string2):
                            
                            if string1[1].isupper() != string2[index1+i].isupper():
                            
                            for i in range(string1):
                                if string1[i].isupper() != string2[index1+i].isupper():
                                    string2[index1+i]
                                
                            if side1 == 0:
                                string2 = 
                            if string2.upper """
                        
                        print("Side 1: %d" % (side))
                        
                        if side > -1:
                            if side == 0:
                                #case_flip = ".r"
                                side2 = 1
                            elif side == 1:
                                #case_flip = ".l"
                                side2 = 0
                            elif side == 2:
                                side2 = 3
                            elif side == 3:
                                side2 = 2
                                
                            print("Side 2: %d" % (side2))
                                
                            replace = sides[side2]
                            
                            print("replace 1: %s" % (replace))
                                
                            print("string[index+1]: %s; isUpper: %s" % (string[index+1], string[index+1].isupper()))
                                
                            #if sides[side][1].isupper() != string2[index1+1].isupper():
                            if string[index+1].isupper():
                                
                                
                                replace = "." + sides[side2][1:].capitalize()
                                
                            print("replace 2: %s" % (replace))
                            print("string[:index]: %s" % (string[:index]))
                            print("string[index+len(replace):]: %s" % (string[index+len(replace):]))
                                
                            string = string[:index] + replace + string[index+len(sides[side]):]
                            
                        return string
                    
                    found = str(split[1]).find(".L")
                    rfound = str(split[1]).rfind(".L")
                    
                    #print("split.find(): index: %d; char: %s" % (found, str(split[1])[found]))
                    
                    #print("split.rfind(): index: %d; char: %s" % (rfound, str(split[1])[rfound]))
                    
                    #print("flipNames: %s" % (flipNames( str(split[1]) )) )
                    print("flipNames: %s" % (flipNames( bpy.context.active_pose_bone.name )) )
                
                reportString = "Done!"
                
                print(reportString)
                self.report({'INFO'}, reportString)
            
            else:
                reportString = "Object[%s] has No Drivers" % (bpy.context.object.name)
                
                print(reportString)
                self.report({'INFO'}, reportString)
        """
        #Mass deletion of every Iteration Object & their collections and objects inside them
        elif self.type == "DELETE_NUKE":
            
            if props.collection_active is not None:
                removedObjects = 0
                removedCol = 0
                
                for i in enumerate(reversed(props.collections)):
                    if i[1].collection is not None:
                        for j in i[1].collection.objects:
                            removedObjects += 1
                            i[1].collection.objects.unlink(j)
                            
                        removedCol += 1
                        #Removes collection, but not other links of it incase the user linked it
                        bpy.data.collections.remove(i[1].collection, do_unlink=True)
                        
                    props.collections.remove(len(props.collections)-1)
                    
                colNameActive = props.collection_active.name
                    
                reportString = "Removed: [%s] & %d Objects & %d Collection Groups" % (colNameActive, removedObjects, removedCol)
                
                bpy.data.collections.remove(props.collection_active, do_unlink=True)
                
                print(reportString)
                self.report({'INFO'}, reportString)
            else:
                #Removes scene.RD_Props.collections
                for i in enumerate(reversed(props.collections)):
                    props.collections.remove(len(props.collections)-1)
                
            print(reportString)
            self.report({'INFO'}, reportString)
                    
            print("Before: "+str(before[::]))
            
            #Prints the last ammount of different Iterate Objects calculated
            print("Removed: ( %d/%d ) Iterate Objects \n" % (len_diff, len_previous)) """
            
            
            
        #Resets default settings
        self.type == "DEFAULT"
        
        return {'FINISHED'}
        
class RIG_DEBUGGER_OT_UIOperators(bpy.types.Operator):
    bl_idname = "rig_debugger.ui_list_ops"
    bl_label = "List Operators"
    bl_description = "Operators for moving and deleting list rows"
    bl_options = {'UNDO',}
    type: bpy.props.StringProperty(default="DEFAULT")
    sub: bpy.props.StringProperty(default="DEFAULT")
    #index: bpy.props.IntProperty(default=0, min=0)
    
    def execute(self, context):
        scene = bpy.context.scene
        props = scene.RD_Props
        active = props.IM_ULIndex
        
        #collection_active: 
        #collections:
            #collection:
            #object:
            #duplicates:
            #recent:
            
        #Sets list_order to "CUSTOM" when moving list rows UP or DOWN
        if props.list_order != "CUSTOM" and (self.type == "UP" or self.type == "DOWN"):
            if props.list_reverse == "DESCENDING":
                for i in enumerate(props.collections):
                    i[1].custom = i[0]
            else:
                for i in enumerate(reversed(props.collections)):
                    i[1].custom = i[0]
                
            props.list_order = "CUSTOM"
            print("Mc Bruh")
        
        #Moves list row UP
        if self.type == "UP":
            
            if self.sub == "DEFAULT":
                if active != 0:
                    props.collections.move(active, active-1)
                    props.IM_ULIndex-=1
                    
                else:
                    props.collections.move(0, len(props.collections)-1)
                    props.IM_ULIndex  = len(props.collections)-1
                    
            elif self.sub == "TOP":
                props.collections.move(active, 0)
                props.IM_ULIndex = 0
        
        #Moves list row DOWN
        elif self.type == "DOWN":
            
            if self.sub == "DEFAULT":
                if active != len(props.collections)-1:
                    props.collections.move(active, active+1)
                    props.IM_ULIndex += 1
                    
                else:
                    props.collections.move(len(props.collections)-1, 0)
                    props.IM_ULIndex = 0
                    
            elif self.sub == "BOTTOM":
                props.collections.move(active, len(props.collections)-1)
                props.IM_ULIndex = len(props.collections)-1
                
        elif self.type == "REMOVE" and len(props.collections) > 0:
            if self.sub == "DEFAULT":
                #If active is the last one
                if active == len(props.collections)-1:
                    props.collections.remove(props.IM_ULIndex)
                    
                    if len(props.collections) != 0:
                        props.IM_ULIndex -= 1
                        
                else:
                    props.collections.remove(props.IM_ULIndex)
            #Note: This only removes the props.collections, not the actual collections or objects
            elif self.sub == "ALL":
                props.collections.clear()
        
        #Resets self props into "DEFAULT"
        self.type == "DEFAULT"
        self.sub == "DEFAULT"
        
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
        
class RIG_DEBUGGER_MT_CollectionsMenuActive(bpy.types.Menu):
    bl_idname = "RIG_DEBUGGER_MT_CollectionsMenuActive"
    bl_label = "Select a Collection for Active"
    bl_description = "Dropdown to select an Active Collection to iterate objects to"
    
    # here you specify how they are drawn
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        data = bpy.data
        props = scene.RD_Props
        
        col = layout.column()
        
        row = col.row(align=True)
        
        if len(bpy.data.collections) > 0:
            for i in enumerate(bpy.data.collections):
                button = row.operator("rig_debugger.select_collection", text=i[1].name)
                button.type = "SELECT_ACTIVE"
                button.index = i[0]
                
                row = col.row(align=True)
        else:
            #NEW_COLLECTION
            button = row.operator("rig_debugger.collection_ops", text="Add Collection", icon = "ADD")
            button.type = "NEW_COLLECTION"
            #bpy.data.collections.new("Boi") 
        #row.prop(self, "ui_tab", expand=True)#, text="X")
    
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
        scene = context.scene
        props = scene.RD_Props
        
        #Layout Starts
        col = layout.column()
        
        #Active Collection
        row = col.row(align=True)
        row.label(text="Parent Collection:")
        
        row = col.row(align=True)
        
        MenuName2 = "Select Collection"
        
        if props.collection_active is not None:
            MenuName2 = props.collection_active.name
            
        #Lock Icon
        if props.lock_active == False:
            row.prop(props, "lock_active", icon="UNLOCKED", text="")
        else:
            row.prop(props, "lock_active", icon="LOCKED", text="")
            
        #if props.collection_active is None:
        if props.lock_active == False or props.collection_active is None:
            row.menu("RIG_DEBUGGER_MT_CollectionsMenuActive", icon="GROUP", text=MenuName2)
        else:
            row.prop(props.collection_active, "name", icon="GROUP", text="")
        
        #Separates for extra space between
        col.separator()
        
        #Duplicate Button TOP
        if bpy.context.object != None:
            ob_name_1 = bpy.context.object.name
        else:
            ob_name_1 = "No Object Selected"
            
        #for loop
        ob_name_col_1 = "New Collection"
        #ob_name_iterate = "Iterate"
        iterateNew = False
        
        for i in enumerate(props.collections):
            if i[1].object == bpy.context.object:
                if i[1].collection != None:
                    ob_name_col_1 = i[1].collection.name
                    #changes iterateNew to 
                    iterateNew = True
                    break
        #Changes text from "Iterate" to "Iterate New" if object wasn't found in Iterate Objects
        #ob_name_iterate = "Iterate New" if iterateNew == False else "Iterate"
        
        row = col.row(align=True)
        
        #row.label(text="Collection: "+ob_name_col_1, icon="GROUP")
        row.label(text="Collection: ", icon="GROUP")
        row.label(text=ob_name_col_1)
        
        #if props.dropdown_1 == True:
        row = col.row(align=True)
        
        row.label(text="Object: ", icon="OUTLINER_OB_MESH")
        row.label(text=ob_name_1)
            
        #Duplicate Button BOTTOM
        
        row = col.row(align=True)
        row.label(text="Iteration Objects (%d):" % len(props.collections))
        #TOP
        
        split = layout.row(align=False)
        col = split.column(align=True)
        
        row = col.row(align=True)
        row.template_list("RIG_DEBUGGER_UL_items", "custom_def_list", props, "collections", props, "IM_ULIndex", rows=3)
        
        #Side_Bar Operators
        col = split.column(align=True)
        
        row = col.row(align=True)
        button = row.operator("rig_debugger.ui_list_ops", text="", icon="TRIA_UP")
        button.type = "UP"
        
        row = col.row(align=True)
        button = row.operator("rig_debugger.ui_list_ops", text="", icon="TRIA_DOWN")
        button.type = "DOWN"
        
        row = col.row(align=True)
        button = row.operator("rig_debugger.ui_list_ops", text="", icon="PANEL_CLOSE")
        button.type = "REMOVE"
        
        row = col.row(align=True)
        row.prop(props, "display_icons", text="", icon="OUTLINER_OB_MESH")
        
        #Edit Mode option
        row = col.row(align=True)
        row.prop(props, "display_collections", text="", icon="GROUP")
        
        #End of CustomPanel
        

class RIG_DEBUGGER_PT_DisplaySettings(bpy.types.Panel):
    bl_label = "Display Settings"
    bl_parent_id = "RIG_DEBUGGER_PT_CustomPanel1"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    #bl_context = "output"
    bl_category = "Rig Debugger"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        data = bpy.data
        props = scene.RD_Props
        
        #collection_active: 
        #collections:
        
        col = layout.column()
        
        #Debug Operators
        row = col.row(align=True)
        row.label(text="Debug Operators:")
        
        row = col.row(align=True)
        row.operator("rig_debugger.debug", text="Print All Drivers").type = "PRINT_ALL"
        
        row = col.row(align=True)
        row.operator("rig_debugger.debug", text="Print Driver Test").type = "PRINT_DRIVER_TEST"
        
        row = col.row(align=True)
        row.operator("rig_debugger.debug", text="Add Driver Test").type = "ADD_DRIVER_TEST"
        
        
        row = col.row(align=True)
        row.label(text="Display Order")
        
        row = col.row(align=True)
        row.prop(scene.RD_Props, "list_order", expand=True)
        
        row = col.row(align=True)
        row.label(text="Sort Order")
        
        row = col.row(align=True)
        row.prop(props, "list_reverse", expand=True)#, text="X")
        
        #row = col.row(align=True)
        #row.separator()
        
        #col = layout.column(align=False)
        
        row = col.row(align=True)
        row.label(text="Display")
        
        row = col.row(align=True)
        row.prop(props, "display_collections", text="Collections", icon="GROUP")
        row.prop(props, "display_icons", text="Icons", icon="OUTLINER_OB_MESH")
        
        col.separator()
        
        row = col.row(align=True)
        
        row.label(text="New Collection")
        
        row = col.row(align=True)

        row.prop(props, "index_to_new", text="Update Active List Index", icon="NONE")
        
        row = col.row(align=True)

        row.prop(props, "group_name_use", text="Use Object Name", icon="NONE")
        
        row = col.row(align=True)
        
        #Grays row out with .active, but you can still change props inside it.
        row.active = not bool(props.group_name_use)
        
        row.prop(props, "group_name", text="New Name", icon="NONE")
        
        """
        if props.debug_mode == True:
            #Debug Operators
            row = col.row(align=True)
            row.label(text="Debug Operators:")
            
            row = col.row(align=True)
            row.operator("rig_debugger.debug", text="Print Different").type = "PRINT_DIFFERENT_1"
            
            #row = col.row(align=True)
            #row.operator("rig_debugger.debug", text="Delete Test").type = "CLEAN"
            
            
            col.separator()
            
            row = col.row(align=True)
            row.operator("rig_debugger.debug", text="Add 3 Objects").type = "TESTING"
            
            col.separator()
            
            row = col.row(align=True)
            row.operator("rig_debugger.debug", text="Delete All").type = "DELETE_NUKE"
            
            row = col.row(align=True)
            row.operator("rig_debugger.debug", text="Print Objects/Collections").type = "PRINT_1" """
            

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

class RIG_DEBUGGER_CollectionObjects(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="", default="")
    collection: bpy.props.PointerProperty(name="Added Collections to List", type=bpy.types.Collection)
    object: bpy.props.PointerProperty(name="Object", type=bpy.types.Object)
    
    #duplicates: bpy.props.IntProperty(name="Int", description="", default= 0, min=0)
    
    recent: bpy.props.IntProperty(name="Int", description="", default= 0, min=0)
    custom: bpy.props.IntProperty(name="Int", description="", default= 0, min=0)
    icon: bpy.props.StringProperty(name="Icon name for object", description="Used to display in the list", default="QUESTION")#, get=)#, update=checkIcon)
    
class RIG_DEBUGGER_Props(bpy.types.PropertyGroup):
    #Tries to set collection_parent's default to Master Collection
    
    collection_active: bpy.props.PointerProperty(name="Collection to add Collections for Object duplicates", type=bpy.types.Collection)
    
    #Booleans for locking default collection of parent
    
    lock_active: bpy.props.BoolProperty(name="Lock Collection of Active", description="When locked, you can now edit the name of the selected collection", default=False)
    
    collections: bpy.props.CollectionProperty(type=RIG_DEBUGGER_CollectionObjects)
    
    IM_ULIndex: bpy.props.IntProperty(name="List Index", description="UI List Index", default= 0, min=0)
    
    clean_leave: bpy.props.IntProperty(name="List Index", description="Ammount of recent Objects to leave when cleaning.", default=2, min=0)
    
    #Dropdown for Iterate Display
    dropdown_1: bpy.props.BoolProperty(name="Dropdown", description="Show Object of Iterate Object", default=False)
    
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
    RIG_DEBUGGER_OT_UIOperators,
    
    RIG_DEBUGGER_UL_items,
    RIG_DEBUGGER_MT_CollectionsMenuActive,
    
    RIG_DEBUGGER_PT_CustomPanel1,
    RIG_DEBUGGER_PT_DisplaySettings,
    
    RIG_DEBUGGER_PreferencesMenu,
    RIG_DEBUGGER_CollectionObjects,
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
