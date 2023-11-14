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

import bpy
from bpy.props import BoolProperty, StringProperty
from bpy.types import AddonPreferences


class RenderStatsPreferences(AddonPreferences):
    """
    Render Stats preferences

    A class that manages Render Stats add-on preferences.
    """
    bl_idname = __package__

    pie_chart: BoolProperty(
        name="Pie",
        description="Chart is displayed in pie chart shape",
        default=True,
        update=lambda self, context: self.update_donut_toggle(context),
    )

    donut_chart: BoolProperty(
        name="Donut",
        description="Chart is displayed in donut chart shape",
        default=False,
        update=lambda self, context: self.update_pie_toggle(context),
    )

    log_name: StringProperty(
        name="Log Filename",
        description="Log file name",
        default="log",
    )

    def update_pie_toggle(self, context):
        if self.donut_chart == True:
            self.pie_chart = False
    
    def update_donut_toggle(self, context):
        if self.pie_chart == True:
            self.donut_chart = False

    def draw(self, context):
        layout = self.layout

        layout.label(text="Render Stats Preferences")

        first_row = layout.row(align=True)
        first_row.label(text="Chart Shape")
        first_row.prop(self, "pie_chart", toggle=True)
        first_row.prop(self, "donut_chart", toggle=True)

        layout.separator()

        second_row = layout.row(align=True)
        second_row.prop(self, "log_name", text="Log Filename")

        layout.separator()


def register_preferences():
    bpy.utils.register_class(RenderStatsPreferences)


def unregister_preferences():
    bpy.utils.unregister_class(RenderStatsPreferences)