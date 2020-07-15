
bl_info = {
    "name": "Rig Debugger",
    "description": "Workflow Addon for easy debugging/ development of a rig in Blender.",
    "author": "Juan Cardenas (JohnGDDR5)",
    "version": (1, 0, 5), 
    "blender": (2, 80, 0),
    "location": "3D View > Side Bar > Rig Debugger",
    "warning": "In Development",
    "support": "COMMUNITY",
    "category": "Scene"
}

import bpy
        
from bpy.props import *

#from . rig_debugger_addon_b2_80_v1_0_1 import classes
from . rig_debugger_addon_b2_80_v1_0_1 import (
    RIG_DEBUGGER_WeightGroups,
    RIG_DEBUGGER_Props,
    
    RIG_DEBUGGER_OT_MirrorCustomBones,
    RIG_DEBUGGER_OT_Debugging,
    RIG_DEBUGGER_OT_DriverMirror,
    RIG_DEBUGGER_OT_DriverOps,
    RIG_DEBUGGER_OT_DriverExtrapolation,
    
    RIG_DEBUGGER_OT_VertexGroupInfluence,
    RIG_DEBUGGER_OT_VertexGroupOps,
    #Ops for selecting vertices with a certain number of Vertex Groups
    RIG_DEBUGGER_OT_SelectVertexGroupCount,
    REGEX_SCANNER_OT_General_UIOps,
    RIG_DEBUGGER_OT_VertexGroup_UIOps,
    
    REGEX_SCANNER_MT_DropdownMenu1,
    REGEX_SCANNER_MT_DropdownMenu2,
    
    RIG_DEBUGGER_WEIGHTGROUPS_UL_items,
    RIG_DEBUGGER_PT_CustomPanel1,
    RIG_DEBUGGER_PT_CustomPanel1_Debug,
    
    RIG_DEBUGGER_PT_CustomPanel2,
    RIG_DEBUGGER_PT_CustomPanel2_Debug,
    
    RIG_DEBUGGER_PT_DriverInfo1,
    RIG_DEBUGGER_PT_DriverInfo2,
    
    RIG_DEBUGGER_PT_VertexGroups1,
    #Subpanel
    RIG_DEBUGGER_PT_VertexGroups1_InfluenceVertGroups,
    
    RIG_DEBUGGER_PreferencesMenu,
)



#print("classes"+str(classes) )
#Yes, I had to do this or else it would not register correctly
classes = (
    RIG_DEBUGGER_WeightGroups,
    RIG_DEBUGGER_Props,
    
    RIG_DEBUGGER_OT_MirrorCustomBones,
    RIG_DEBUGGER_OT_Debugging,
    RIG_DEBUGGER_OT_DriverMirror,
    RIG_DEBUGGER_OT_DriverOps,
    RIG_DEBUGGER_OT_DriverExtrapolation,
    
    RIG_DEBUGGER_OT_VertexGroupInfluence,
    RIG_DEBUGGER_OT_VertexGroupOps,
    #Ops for selecting vertices with a certain number of Vertex Groups
    RIG_DEBUGGER_OT_SelectVertexGroupCount,
    REGEX_SCANNER_OT_General_UIOps,
    RIG_DEBUGGER_OT_VertexGroup_UIOps,
    
    REGEX_SCANNER_MT_DropdownMenu1,
    REGEX_SCANNER_MT_DropdownMenu2,
    
    RIG_DEBUGGER_WEIGHTGROUPS_UL_items,
    RIG_DEBUGGER_PT_CustomPanel1,
    RIG_DEBUGGER_PT_CustomPanel1_Debug,
    
    RIG_DEBUGGER_PT_CustomPanel2,
    RIG_DEBUGGER_PT_CustomPanel2_Debug,
    
    RIG_DEBUGGER_PT_DriverInfo1,
    RIG_DEBUGGER_PT_DriverInfo2,
    
    RIG_DEBUGGER_PT_VertexGroups1,
    #Subpanel
    RIG_DEBUGGER_PT_VertexGroups1_InfluenceVertGroups,
    
    RIG_DEBUGGER_PreferencesMenu,
)

def register():
    #ut = bpy.utils
    #from bpy.utils import register_class
    #"""
    for cls in classes:
        bpy.utils.register_class(cls)
    #"""
    #bpy.utils.register_classes_factory(classes)
        
    bpy.types.Scene.RD_Props =  bpy.props.PointerProperty(type=RIG_DEBUGGER_Props)
    
def unregister():
    #ut = bpy.utils
    #from bpy.utils import unregister_class
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    #bpy.utils.register_classes_factory(classes)
    
    #Just incase to prevent an error
    if hasattr(bpy.types.Scene, "RD_Props") == True:
        del bpy.types.Scene.RD_Props
    
#register, unregister = bpy.utils.register_classes_factory(classes)
#"""
if __name__ == "__main__":
    register()
    
#"""
