import bpy


class _ListOp(bpy.types.Operator):
    bl_idname = 'io_scene_xray.list'
    bl_label = ''

    operation = bpy.props.StringProperty()
    collection = bpy.props.StringProperty()
    index = bpy.props.StringProperty()

    def execute(self, context):
        data = getattr(context, _ListOp.bl_idname + '.data')
        collection = getattr(data, self.collection)
        index = getattr(data, self.index)
        if self.operation == 'add':
            collection.add().name = ''
        elif self.operation == 'remove':
            collection.remove(index)
            if index > 0:
                setattr(data, self.index, index - 1)
        elif self.operation == 'move_up':
            collection.move(index, index - 1)
            setattr(data, self.index, index - 1)
        elif self.operation == 'move_down':
            collection.move(index, index + 1)
            setattr(data, self.index, index + 1)
        return {'FINISHED'}


def draw_list_ops(layout, dataptr, propname, active_propname):
    def operator(operation, icon, enabled=None):
        lay = layout
        if (enabled is not None) and (not enabled):
            lay = lay.split(align=True)
            lay.enabled = False
        operator = lay.operator(_ListOp.bl_idname, icon=icon)
        operator.operation = operation
        operator.collection = propname
        operator.index = active_propname

    layout.context_pointer_set(_ListOp.bl_idname + '.data', dataptr)
    operator('add', 'ZOOMIN')
    collection = getattr(dataptr, propname)
    index = getattr(dataptr, active_propname)
    operator('remove', 'ZOOMOUT', enabled=(index >= 0) and (index < len(collection)))
    operator('move_up', 'TRIA_UP', enabled=(index > 0) and (index < len(collection)))
    operator('move_down', 'TRIA_DOWN', enabled=(index >= 0) and (index < len(collection) - 1))


class BoneList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        obj = context.object
        stk_data = obj.data.stalker_rig_helper

        if stk_data.bone_collection_index == index:
            icon = 'CHECKBOX_HLT'
        else:
            icon = 'CHECKBOX_DEHLT'

        bone = stk_data.bone_collection[index]
        row = layout.row()
        row.label(text='', icon=icon)
        row.prop_search(bone, 'hand_bone', obj.data, 'bones', text='')
        wpn_obj = bpy.data.objects.get(stk_data.weapon_armature, None)
        row.prop_search(bone, 'wpn_bone', wpn_obj.data, 'bones', text='')
        row.prop_search(bone, 'offset_bone', obj.data, 'bones', text='')


class STALKER_HUD_Rig_Helper_Panel(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}
    bl_label = 'STALKER HUD Rig Helper'

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        return context.object.type == 'ARMATURE'

    def draw(self, context):
        obj = context.object
        stk_data = obj.data.stalker_rig_helper
        lay = self.layout
        row = lay.row()
        wpn_obj = bpy.data.objects.get(stk_data.weapon_armature, None)
        if not wpn_obj:
            row.prop_search(stk_data, 'weapon_armature', bpy.data, 'objects')
            return
        if wpn_obj.type != 'ARMATURE':
            row.prop_search(stk_data, 'weapon_armature', bpy.data, 'objects')
            return
        if wpn_obj.name == obj.name:
            row.prop_search(stk_data, 'weapon_armature', bpy.data, 'objects')
            return
        row.prop_search(stk_data, 'weapon_armature', bpy.data, 'objects')
        row = lay.row()
        row.label('Hand Bones')
        row.label(icon='FORWARD')
        row.label('Weapon Bones')
        row.label(icon='FORWARD')
        row.label('Offset Bones')

        row = lay.row()
        col = row.column()
        col.template_list(
            'BoneList', 'name',
            stk_data, 'bone_collection',
            stk_data, 'bone_collection_index'
        )
        col = row.column(align=True)
        draw_list_ops(
            col, stk_data,
            'bone_collection', 'bone_collection_index',
        )

        lay.operator('stalker_rig_helper.tie_weapon')


def register():
    bpy.utils.register_class(_ListOp)
    bpy.utils.register_class(BoneList)
    bpy.utils.register_class(STALKER_HUD_Rig_Helper_Panel)


def unregister():
    bpy.utils.unregister_class(STALKER_HUD_Rig_Helper_Panel)
    bpy.utils.unregister_class(BoneList)
    bpy.utils.unregister_class(_ListOp)
