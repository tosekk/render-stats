# Copyright © Zhandos Kadyrkulov 2023 | All Rights Reserved

import bpy


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