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

import math


import bpy
import gpu
from gpu_extras.batch import batch_for_shader
from mathutils import Vector


def draw_donut_chart(x: int, y: int, inner_radius: int, 
                       outer_radius: int, data: list) -> None:
    """
    Draw donut chart on the screen.

    This function creates the donut chart and its shader then draws it on the screen.
    It takes coordinates of the center of the donut chart center, its inner and outer radius, and data to be displayed.

    Parameters:
    x (int): The x-coordinate of the donut chart center
    y (int):The y-coordinate of the donut chart center
    inner_radius (int): The inner radius of the art
    outer_radius (int): The outer radius of the arc
    data (list(tuple)): The data to be displayed
    """

    segment_count = 20
    start_angle = 0
    
    for percentage, color in data:
        vertices = []
        end_angle = start_angle + 2 * math.pi * percentage

        # Calculate vertices for inner and outer arc
        for i in range(segment_count + 1):
            theta = start_angle + (end_angle - start_angle) * (i / segment_count)
            x_inner = x + math.cos(theta) * inner_radius
            y_inner = y + math.sin(theta) * inner_radius
            x_outer = x + math.cos(theta) * outer_radius
            y_outer = y + math.sin(theta) * outer_radius
            vertices.append((x_inner, y_inner))
            vertices.append((x_outer, y_outer))

        # Create shader and batch for drawing
        shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
        batch = batch_for_shader(shader, 'TRI_STRIP', {"pos": vertices})

        # Draw the segment
        shader.bind()
        shader.uniform_float("color", color)
        batch.draw(shader)
        
        # Reset start angle for each section of the chart
        start_angle = end_angle


def draw_pie_chart(x: int, y: int, radius: int, data: list) -> None:
    """
    Draw pie chart on the screen.

    This function creates the pie chart and its shader then draws it on the screen.
    It takes coordinates of the center of the pie chart, its radius, and data to be displayed.

    Parameters:
    x (int): The x-coordinate of the pie chart center
    y (int):The y-coordinate of the pie chart center
    radius (int): The radius of the pie chart
    data (list(tuple)): The data to be displayed
    """

    segment_count = 20
    prev_angle = 0

    for percentage, color in data:
        angle = 2.0 * math.pi * percentage
        vertices = [Vector((x, y))]

        # Calculate vertices for pie chart segment
        for i in range(segment_count + 1):
            theta = prev_angle + angle * (i / segment_count)
            vertices.append(Vector((x + math.cos(theta) * radius, y + math.sin(theta) * radius)))

        # Create shader and batch for drawing
        shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
        batch = batch_for_shader(shader, 'TRI_FAN', {"pos": vertices})

        # Draw the segment
        shader.bind()
        shader.uniform_float("color", color)
        batch.draw(shader)

        prev_angle += angle