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
from bpy.props import BoolProperty, PointerProperty
from bpy.types import PropertyGroup


class RenderStatsProperties(PropertyGroup):
    """
    Render Stats add-on properties.

    A class that stores the properties of the Render Stats add-on.
    """

    lights_panel_visible: BoolProperty(
        name="Lights Panel Visible",
        description="A flag to check if lights panel is visible",
        default=False,
    )

    objects_panel_visible: BoolProperty(
        name="Objects Panel Visible",
        description="A flag to check if objects panel is visible",
        default=False,
    )

    rays_panel_visible: BoolProperty(
        name="Rays Panel Visible",
        description="A flag to check if rays panel is visible",
        default=False,
    )


def register_props() -> None:
    bpy.utils.register_class(RenderStatsProperties)

    bpy.types.Scene.render_stats = PointerProperty(type=RenderStatsProperties)


def unregister_props() -> None:
    bpy.utils.unregister_class(RenderStatsProperties)

    del bpy.types.Scene.render_stats