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


from . import charts


def get_polygons_count(scene: bpy.types.Scene) -> str:
    stats = scene.statistics(scene.view_layers['ViewLayer']).split(" | ")
    polygons = stats[3].split(":")[1]

    return polygons


def get_light_count_by_type(lights: bpy.types.bpy_prop_collection, light_type: str) -> int:
    return len([light for light in lights.keys() if light_type in light])


def get_gpu_cpu(context: bpy.types.Context) -> tuple:
    cycles_addon = context.preferences.addons["cycles"].preferences
    device_type = cycles_addon.get_compute_device_type()
    devices = cycles_addon.get_devices_for_type(device_type)

    return (devices[0].name, devices[1].name)


def create_labels(column: bpy.types.UILayout, label: str, value):
    column.label(text=label)
    column.label(text=f"{value}")


def create_data_for_viz(input: list , colors: list):
    total = 0

    for element in input:
        total += element

    data = [(round(element / total, 1), colors[index]) for index, element in enumerate(input)]

    return data


def manage_handler(handler, scene, region, data):
    if handler is not None and scene.render_stats.rays_panel_visible == True:
            bpy.types.SpaceImageEditor.draw_handler_remove(handler, "UI")
            scene.render_stats.rays_panel_visible = False
            handler = None
        
    handler = bpy.types.SpaceImageEditor.draw_handler_add(charts.draw_pie_chart, (region.width / 2, region.height / 2, 40, data), "UI", "POST_PIXEL")


def track_chart_panels(self, context):
    if self.bl_label == "Ray Types":
        context.scene.render_stats.ray_panel_visible = True
    elif self.bl_label == "Light Types":
        context.scene.render_stats.lights_panel_visible = True
    elif self.bl_label == "Object Counts":
        context.scene.render_stats.objects_panel_visible = True
    else:
        context.scene.render_stats.ray_panel_visible = False
        context.scene.render_stats.lights_panel_visible = False
        context.scene.render_stats.objects_panel_visible = False


def patch_panels():
    global original_draw
    global patched_panels
    patched_panels = []

    try:
        for panel in bpy.types.Panel.__subclasses__():
            if panel.bl_space_type == "IMAGE_EDITOR" and panel.bl_region_type == "UI":
                original_draw = panel.draw
                
                def draw(self, context):
                    track_chart_panels(self, context)
                    original_draw(self, context)
                
                panel.draw = draw
                patched_panels.append(panel)
    except AttributeError:
        print("Not a UI panel of Image Editor")


def unpatch_panels():
    for panel in patched_panels:
        panel.draw = original_draw
        patched_panels.remove(panel)