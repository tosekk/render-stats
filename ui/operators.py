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

import json
import os
import socket
import subprocess
import sys


import bpy
from bpy.types import Operator


class IMAGE_OT_OpenAnalyzer(Operator):
    """Open external render analyzer"""
    bl_idname = "render.analyzer"
    bl_label = "Open Analyzer"
    
    def execute(self, context):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("localhost", 55645))
        server.listen(1)

        analyzer_dir = bpy.utils.user_resource("SCRIPTS", path="addons/render-stats/ext_gui/dist/")

        if sys.platform == "win32":
            analyzer_path = analyzer_dir + "analyzer.exe"
        else:
            analyzer_path = analyzer_dir + "analyzer"

        subprocess.run([analyzer_path])

        return {"FINISHED"}


classes = [
    IMAGE_OT_OpenAnalyzer,
]


def register_operators():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister_operators():
    for cls in classes:
        bpy.utils.unregister_class(cls)
