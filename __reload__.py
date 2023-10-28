# Copyright © Zhandos Kadyrkulov 2023 | All Rights Reserved

import sys
from importlib import reload


import bpy


from . import ui
from . import utils


def reload_modules():
    if not bpy.context.preferences.view.show_developer_ui:
        return
    
    reload(sys.modules[__name__])
    reload(utils)
    reload(ui)