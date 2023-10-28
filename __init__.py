# Copyright © Zhandos Kadyrkulov 2023 | All Rights Reserved

bl_info = {
    "name": "Render Stats",
    "author": "Zhandos Kadyrkulov",
    "version": (0, 1),
    "blender": (3, 3, 0),
    "description": "Shows render statistics of the current render",
    "location": "Image Editor > Sidebar",
    "category": "Render"
}


from . import __reload__
from . import ui
from . import utils


__reload__.reload_modules()


def register():
    ui.register_ui()


def unregister():
    ui.unregister_ui()


if __name__ == "__main__":
    register()