# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Render Stats",
    "author": "Zhandos Kadyrkulov",
    "version": (0, 2, 0),
    "blender": (3, 3, 0),
    "description": "Shows render statistics of the current render",
    "location": "Image Editor > Sidebar",
    "category": "Render"
}


import bpy


from . import __reload__
from . import prefs
from . import ui
from . import utils


__reload__.reload_modules()


def register():
    prefs.register_preferences()
    utils.register_utils()
    ui.register_ui()

    bpy.app.handlers.frame_change_pre.append(utils.funcs.track_ui_changes)


def unregister():
    bpy.app.handlers.frame_change_pre.remove(utils.funcs.track_ui_changes)

    ui.unregister_ui()
    utils.unregister_utils()
    prefs.unregister_preferences()


if __name__ == "__main__":
    register()