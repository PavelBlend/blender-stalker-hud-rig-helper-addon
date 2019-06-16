import bpy


class STALKER_HUD_Rig_Helper_Op(bpy.types.Operator):
    bl_idname = 'stalker_rig_helper.tie_weapon'
    bl_label = 'Tie Weapon'
    bl_options = {'UNDO'}

    def execute(self, context):
        obj = context.object
        scn = context.scene
        stk_data = bpy.data.objects[obj.name].data.stalker_rig_helper
        wpn = bpy.data.objects[stk_data.weapon_armature]
        offset_bones = []

        def offset_children(parent):
            for child in parent.children:
                child.matrix += wpn_mat - old_matrix
                offset_children(child)

        for bone in stk_data.bone_collection:
            scn.objects.active = wpn
            bpy.ops.object.mode_set(mode='EDIT')
            if bone.wpn_bone and not bone.offset_bone:
                wpn_mat = wpn.data.edit_bones[bone.wpn_bone].matrix
                constraints = wpn.pose.bones[bone.wpn_bone].constraints
                copy_transforms = constraints.get('Copy Transforms')
                if copy_transforms:
                    constraints.remove(copy_transforms)
                copy_transforms = constraints.new('COPY_TRANSFORMS')
                copy_transforms.target = obj
                copy_transforms.subtarget = bone.hand_bone
                bpy.ops.object.mode_set(mode='OBJECT')
                scn.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bone_hand = obj.data.edit_bones[bone.hand_bone]
                old_matrix = bone_hand.matrix.copy()
                bone_hand.matrix = wpn_mat
                offset_children(bone_hand)
            bpy.ops.object.mode_set(mode='OBJECT')

            if bone.offset_bone:
                scn.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bone_hand = obj.data.edit_bones[bone.hand_bone]
                offset_bones.append((bone.offset_bone, bone_hand.name))

        scn.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        for offset_bone_name, bone_hand_name in offset_bones:
            offset_bone = obj.data.edit_bones[offset_bone_name]
            obj.data.edit_bones[bone_hand_name].matrix = offset_bone.matrix
            print(bone_hand.name)
        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}


def register():
    bpy.utils.register_class(STALKER_HUD_Rig_Helper_Op)


def unregister():
    bpy.utils.unregister_class(STALKER_HUD_Rig_Helper_Op)
