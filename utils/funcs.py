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
    """
    Get polygons count in the scene.

    A function that gets the count of all polygons in the current scene.

    Parameters:
    scene (bpy.types.Scene): A scene

    Returns:
    str: The number of polygons in the scene
    """
    stats = scene.statistics(scene.view_layers['ViewLayer']).split(" | ")
    polygons = stats[3].split(":")[1]

    return polygons


def get_light_count_by_type(lights: bpy.types.bpy_prop_collection, light_type: str) -> int:
    """
    Get lights count by type.

    A function that returns the number of lights by specified type.

    Parameters:
    lights (bpy.types.bpy_prop_collection): Collection of lights
    light_type (str): Light type
    """

    return len([light for light in lights.keys() if light_type in light])


def get_gpu_cpu(context: bpy.types.Context) -> tuple:
    """
    Get PC's GPU and CPU models.

    Return the name of GPU and CPU models.

    Parameters:
    context (bpy.types.Context): Panel context

    Returns:
    tuple (str): The GPU and CPU model name
    """

    cycles_addon = context.preferences.addons["cycles"].preferences
    device_type = cycles_addon.get_compute_device_type()
    devices = cycles_addon.get_devices_for_type(device_type)

    return (devices[0].name, devices[1].name)


def create_labels(column: bpy.types.UILayout, label: str, value) -> None:
    """
    Create labels.

    A function that creates labels in the panel's UI.

    Parameters:
    column (bpy.types.UILayout): Column in the UI
    label (str): Label
    value: Display value
    """

    column.label(text=label)
    column.label(text=f"{value}")


def create_data_for_viz(input: list , colors: list) -> list:
    """
    Create data for visualization.

    A function that creates the data for visualization.

    Parameters:
    input (list): An input data
    color (list): Colors of chart segments

    Returns:
    list: Compiled data for visualization
    """

    total = 0

    for element in input:
        total += element

    data = [(round(element / total, 1), colors[index]) for index, element in enumerate(input)]

    return data


def manage_handler(handler, scene: bpy.types.Scene, x: int, y: int, data: list) -> None:
    """
    Manage specified draw handler.

    A function that creates and manages the created handler. Removes duplicate handlers.

    Parameters:
    handler: Draw handler
    scene (bpy.types.Scene): Current scene
    x (int): x-coordinate of the chart center
    y (int): y-coordinate of the chart center
    data (list): Data to be visualized
    """

    if handler is not None and scene.render_stats.rays_panel_visible == True:
            bpy.types.SpaceImageEditor.draw_handler_remove(handler, "UI")
            scene.render_stats.rays_panel_visible = False
            handler = None
        
    handler = bpy.types.SpaceImageEditor.draw_handler_add(charts.draw_pie_chart, (x, y, 40, data), "UI", "POST_PIXEL")


def track_chart_panels(self: bpy.types.Panel, context: bpy.types.Context) -> None:
    """
    Track chart panels' visibility.

    A function that tracks visibility of panels with charts.

    Parameters:
    self (bpy.types.Panel): Panel instance
    context (bpy.types.Context): Context of the panel
    """

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


def patch_panels() -> None:
    """
    Monkey patch panels.

    A function that monkey patchs panels in the Image Editor's UI sidebar.
    """

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


def unpatch_panels() -> None:
    """
    Unpatch panels.

    Return the panels to their original state before monkey patch.
    """

    for panel in patched_panels:
        panel.draw = original_draw
        patched_panels.remove(panel)