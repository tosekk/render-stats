# Blender Render Stats
A simple Blender add-on that displays render information in a panel. Works only with Cycles.

Inspired by the render statistics in Houdini 20.

## Displayed Information
1. General
    1. Camera count
    2. Resolution
    3. Render type
        1. Image
        2. Animation
    4. Current  frame
    5. Samples
2. Objects Count
    1. Meshes
    2. Lights
    3. Polygons
    4. Materials
3. Lights
    1. Area
    2. Point
    3. Spot
4. Time 
    1. Dicing
5. Rays
    1. Occlusion
    2. Diffuse
    3. Glossy
    4. Transmission
6. Host
    1. Hostname
    2. Blender version
    3. CPU
    4. GPU

## TO-DO
- [x] Custom pie charts
- [ ] Localize custom charts by panels - currently display in the UI sidebar in different tabs as well, probably gonna use template_preview()
- [ ] Volume rays
- [ ] Curves
- [ ] Web-based dashboard
- [ ] Logging render statistics