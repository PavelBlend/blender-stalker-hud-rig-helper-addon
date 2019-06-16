import bpy


class Bone(bpy.types.PropertyGroup):
    hand_bone = bpy.props.StringProperty()
    wpn_bone = bpy.props.StringProperty()
    offset_bone = bpy.props.StringProperty()


class STALKER_HUD_Rig_Helper_Props(bpy.types.PropertyGroup):
    b_type = bpy.types.Armature

    weapon_armature = bpy.props.StringProperty(name='Weapon Armature')
    bone_collection_index = bpy.props.IntProperty()
    bone_collection = bpy.props.CollectionProperty(type=Bone)


def register():
    bpy.utils.register_class(Bone)
    bpy.utils.register_class(STALKER_HUD_Rig_Helper_Props)
    STALKER_HUD_Rig_Helper_Props.b_type.stalker_rig_helper = bpy.props.PointerProperty(type=STALKER_HUD_Rig_Helper_Props)


def unregister():
    del STALKER_HUD_Rig_Helper_Props.b_type.stalker_rig_helper
    bpy.utils.unregister_class(STALKER_HUD_Rig_Helper_Props)
    bpy.utils.unregister_class(Bone)
