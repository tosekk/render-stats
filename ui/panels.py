# Copyright © Zhandos Kadyrkulov 2023 | All Rights Reserved

import platform


import bpy
from bpy.types import Panel


from ..utils import funcs


class RenderStats:
    """Render Stats Parent Panel Class"""
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Render Stats"


class IMAGE_PT_RenderStatsMainPanel(Panel, RenderStats):
    """Render Stats Panel"""
    bl_label = "Render Stats"

    @classmethod
    def poll(cls, context):
        render_engine = context.scene.render.engine
        return render_engine == "CYCLES"

    def draw(self, context):
        layout = self.layout
        scene = context.scene


class IMAGE_PT_RenderStatsGeneral(Panel, RenderStats):
    """Render Stats: General"""
    bl_label = "General"
    bl_parent_id = "IMAGE_PT_RenderStatsMainPanel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        render = scene.render
        cycles = scene.cycles
        data = bpy.data
        anim_encoders = ["FFMPEG", "AVI_RAW", "AVI_JPEG"]

        render_type = "Animation" if render.image_settings.file_format in anim_encoders else "Image"
        cameras = len(data.cameras)
        resolution = f"{render.resolution_x}x{render.resolution_y}"
        samples = cycles.samples

        first_row = layout.row()
        anim_col = first_row.column()
        funcs.create_labels(anim_col, "Render Type", render_type)

        frame_col = first_row.column()
        funcs.create_labels(frame_col, "Frame", scene.frame_current)

        
        if render_type =="Image":
            frame_col.enabled = False

        second_row = layout.row()
        cam_col = second_row.column()
        funcs.create_labels(cam_col, "Cameras", cameras)

        
        res_col = second_row.column()
        funcs.create_labels(res_col, "Resolution", resolution)


        third_row = layout.row()
        samples_col = third_row.column()
        funcs.create_labels(samples_col, "Samples", samples)


class IMAGE_PT_RenderStatsObjects(Panel, RenderStats):
    """Render Stats: Object Counts"""
    bl_label = "Object Counts"
    bl_parent_id = "IMAGE_PT_RenderStatsMainPanel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        data = bpy.data

        meshes = len(data.meshes)
        lights = len(data.lights)
        materials = len(data.materials)

        polygons = funcs.get_polygons_count(scene)

        first_row = layout.row()
        poly_col = first_row.column()
        funcs.create_labels(poly_col, "Polygons", polygons)

        meshes_col = first_row.column()
        funcs.create_labels(meshes_col, "Meshes", meshes)

        second_row = layout.row()
        mats_col = second_row.column()
        funcs.create_labels(mats_col, "Materials", materials)

        lights_col = second_row.column()
        funcs.create_labels(lights_col, "Lights", lights)


class IMAGE_PT_RenderStatsLights(Panel, RenderStats):
    """Render Stats: Light Types"""
    bl_label = "Light Types"
    bl_parent_id = "IMAGE_PT_RenderStatsMainPanel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        lights = bpy.data.lights

        area = funcs.get_light_count_by_type(lights, "Area")
        point = funcs.get_light_count_by_type(lights, "Point")
        spot = funcs.get_light_count_by_type(lights, "Spot")

        first_row = layout.row()
        area_col = first_row.column()
        funcs.create_labels(area_col, "Area", area)

        point_col = first_row.column()
        funcs.create_labels(point_col, "Point", point)

        second_row = layout.row()
        spot_col = second_row.column()
        funcs.create_labels(spot_col, "Spot", spot)


class IMAGE_PT_RenderStatsTime(Panel, RenderStats):
    """Render Stats: Time Spent"""
    bl_label = "Time Spent"
    bl_parent_id = "IMAGE_PT_RenderStatsMainPanel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        cycles = scene.cycles

        row = layout.row()
        col = row.column()
        funcs.create_labels(col, "Dicing", cycles.dicing_rate)


class IMAGE_PT_RenderStatsRays(Panel, RenderStats):
    """Render Stats: Ray Types"""
    bl_label = "Ray Types"
    bl_parent_id = "IMAGE_PT_RenderStatsMainPanel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        cycles = scene.cycles

        first_row = layout.row()
        ao_col = first_row.column()
        funcs.create_labels(ao_col, "Occlusion", cycles.ao_bounces)

        diff_col = first_row.column()
        funcs.create_labels(diff_col, "Diffuse", cycles.diffuse_bounces)

        second_row = layout.row()
        gloss_col = second_row.column()
        funcs.create_labels(gloss_col, "Glossy", cycles.glossy_bounces)
        
        transmission_col = second_row.column()
        funcs.create_labels(transmission_col, 
                            "Transmission", cycles.transmission_bounces)


class IMAGE_PT_RenderStatsHostData(Panel, RenderStats):
    """Render Stats: Host Data"""
    bl_label = "Host Data"
    bl_parent_id = "IMAGE_PT_RenderStatsMainPanel"

    def draw(self, context):
        layout = self.layout
        
        gpu, cpu = funcs.get_gpu_cpu(context)

        hostname = platform.node()
        version = bpy.app.version_string

        first_row = layout.row()
        host_col = first_row.column()
        funcs.create_labels(host_col, "Hostname", hostname)

        version_col = first_row.column()
        funcs.create_labels(version_col, "Version", version)

        second_row = layout.row()
        cpu_col = second_row.column()
        funcs.create_labels(cpu_col, "CPU", cpu)

        gpu_col = second_row.column()
        funcs.create_labels(gpu_col, "GPU", gpu)


classes = [
    IMAGE_PT_RenderStatsMainPanel,
    IMAGE_PT_RenderStatsGeneral,
    IMAGE_PT_RenderStatsObjects,
    IMAGE_PT_RenderStatsLights,
    IMAGE_PT_RenderStatsTime,
    IMAGE_PT_RenderStatsRays,
    IMAGE_PT_RenderStatsHostData,
]


def register_panels():
    for cls in classes:
        bpy.utils.register_class(cls)
    

def unregister_panels():
    for cls in classes:
        bpy.utils.unregister_class(cls)