bl_info = {
    'name': 'STALKER HUD Rig Helper',
    'author': 'Pavel_Blend',
    'version': (0, 0, 0),
    'blender': (2, 79, 0),
    'category': 'Animation',
    'location': 'Properties > Armature > STALKER HUD Rig Helper'
}


def register():
    import bpy

    from . import props
    from . import ops
    from . import ui

    props.register()
    ops.register()
    ui.register()


def unregister():
    import bpy

    from . import ui
    from . import ops
    from . import props

    ui.unregister()
    ops.unregister()
    props.unregister()
