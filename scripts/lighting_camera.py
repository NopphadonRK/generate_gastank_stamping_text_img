"""
Lighting and Camera Controller Module

This module handles scene lighting setup and camera positioning for generating
diverse viewpoints and lighting conditions for the gas cylinder text dataset.

Author: Gas Tank Text Generator Project
Date: July 2025
"""

import random
import math
import logging
from typing import Tuple

try:
    import bpy
    from mathutils import Vector, Euler
except ImportError:
    print("Warning: bpy not available - this module requires Blender")

logger = logging.getLogger(__name__)


class LightingCameraController:
    """Controls lighting and camera setup for diverse scene generation."""
    
    def __init__(self):
        """Initialize the lighting and camera controller."""
        
        # Camera positioning parameters
        self.camera_distance_range = (3.0, 6.0)      # Distance from cylinder
        self.camera_elevation_range = (-30, 30)       # Elevation angle (degrees)
        self.camera_azimuth_range = (0, 360)         # Azimuth angle (degrees)
        
        # Lighting parameters - reduced for balanced lighting with environment
        self.key_light_intensity_range = (300, 800)    # Reduced main light strength
        self.fill_light_intensity_range = (150, 400)   # Reduced fill light strength
        self.rim_light_intensity_range = (200, 600)    # Reduced rim light strength
        
        logger.info("LightingCameraController initialized")
    
    def randomize_scene(self) -> None:
        """
        Randomize both lighting and camera for the current scene.
        """
        
        self.setup_camera()
        self.setup_lighting()
        
        logger.debug("Scene randomization complete")
    
    def setup_camera(self) -> bpy.types.Object:
        """
        Setup and position camera with randomized parameters.
        
        Returns:
            Camera object
        """
        
        # Remove existing camera if present
        if bpy.context.scene.camera:
            bpy.data.objects.remove(bpy.context.scene.camera, do_unlink=True)
        
        # Create new camera
        bpy.ops.object.camera_add()
        camera = bpy.context.active_object
        camera.name = "SceneCamera"
        
        # Set as active camera
        bpy.context.scene.camera = camera
        
        # Randomize camera position
        distance = random.uniform(*self.camera_distance_range)
        elevation = math.radians(random.uniform(*self.camera_elevation_range))
        azimuth = math.radians(random.uniform(*self.camera_azimuth_range))
        
        # Calculate camera position in spherical coordinates
        x = distance * math.cos(elevation) * math.cos(azimuth)
        y = distance * math.cos(elevation) * math.sin(azimuth)
        z = distance * math.sin(elevation) + 1.5  # Offset to look at cylinder center
        
        camera.location = (x, y, z)
        
        # Point camera at cylinder center
        target_location = Vector((0, 0, 1.5))  # Cylinder center height
        self._point_camera_at_target(camera, target_location)
        
        # Set camera properties
        camera.data.lens = random.uniform(35, 85)  # Focal length variation
        camera.data.sensor_width = 36  # Full frame sensor
        
        logger.debug(f"Camera: pos=({x:.2f}, {y:.2f}, {z:.2f}), "
                    f"elev={math.degrees(elevation):.1f}°, "
                    f"azim={math.degrees(azimuth):.1f}°")
        
        return camera
    
    def setup_lighting(self) -> None:
        """
        Setup balanced lighting system with environment lighting.
        """
        
        # Clear existing lights
        self._clear_existing_lights()
        
        # Set up environment lighting first
        self._setup_environment_lighting()
        
        # Create balanced three-point lighting setup
        key_light = self._create_key_light()
        fill_light = self._create_fill_light()
        rim_light = self._create_rim_light()
        
        # Add additional ambient lighting for even illumination
        ambient_light = self._create_ambient_light()
        
        logger.debug("Balanced lighting system with environment lighting created")
    
    def _clear_existing_lights(self) -> None:
        """Remove all existing lights from the scene."""
        
        lights_to_remove = [obj for obj in bpy.context.scene.objects 
                           if obj.type == 'LIGHT']
        
        for light in lights_to_remove:
            bpy.data.objects.remove(light, do_unlink=True)
    
    def _create_key_light(self) -> bpy.types.Object:
        """
        Create the main key light (primary illumination).
        
        Returns:
            Key light object
        """
        
        # Create sun light for directional lighting
        bpy.ops.object.light_add(type='SUN')
        key_light = bpy.context.active_object
        key_light.name = "KeyLight"
        
        # Randomize light properties
        intensity = random.uniform(*self.key_light_intensity_range)
        key_light.data.energy = intensity
        
        # Randomize light position and rotation
        elevation = math.radians(random.uniform(30, 70))
        azimuth = math.radians(random.uniform(0, 360))
        
        # Position light
        distance = 8.0  # Sun lights work at any distance
        x = distance * math.cos(elevation) * math.cos(azimuth)
        y = distance * math.cos(elevation) * math.sin(azimuth)
        z = distance * math.sin(elevation)
        
        key_light.location = (x, y, z)
        
        # Point light toward scene center
        target_location = Vector((0, 0, 1.5))
        self._point_light_at_target(key_light, target_location)
        
        # Light color variation (warm to cool)
        color_temp = random.uniform(0.8, 1.2)
        key_light.data.color = (1.0, color_temp, color_temp * 0.8)
        
        logger.debug(f"Key light: intensity={intensity:.0f}, "
                    f"elev={math.degrees(elevation):.1f}°")
        
        return key_light
    
    def _create_fill_light(self) -> bpy.types.Object:
        """
        Create fill light to soften shadows.
        
        Returns:
            Fill light object
        """
        
        # Create area light for soft fill lighting
        bpy.ops.object.light_add(type='AREA')
        fill_light = bpy.context.active_object
        fill_light.name = "FillLight"
        
        # Set fill light properties
        intensity = random.uniform(*self.fill_light_intensity_range)
        fill_light.data.energy = intensity
        fill_light.data.size = random.uniform(2.0, 4.0)  # Large soft light
        
        # Position fill light opposite to key light
        fill_elevation = math.radians(random.uniform(10, 40))
        fill_azimuth = math.radians(random.uniform(120, 240))  # Opposite side
        
        distance = random.uniform(4.0, 7.0)
        x = distance * math.cos(fill_elevation) * math.cos(fill_azimuth)
        y = distance * math.cos(fill_elevation) * math.sin(fill_azimuth)
        z = distance * math.sin(fill_elevation)
        
        fill_light.location = (x, y, z)
        
        # Point toward cylinder
        target_location = Vector((0, 0, 1.5))
        self._point_light_at_target(fill_light, target_location)
        
        # Cooler color for fill light
        fill_light.data.color = (0.9, 0.95, 1.0)
        
        logger.debug(f"Fill light: intensity={intensity:.0f}")
        
        return fill_light
    
    def _create_rim_light(self) -> bpy.types.Object:
        """
        Create rim light for edge definition.
        
        Returns:
            Rim light object
        """
        
        # Create spot light for rim lighting
        bpy.ops.object.light_add(type='SPOT')
        rim_light = bpy.context.active_object
        rim_light.name = "RimLight"
        
        # Set rim light properties
        intensity = random.uniform(*self.rim_light_intensity_range)
        rim_light.data.energy = intensity
        rim_light.data.spot_size = math.radians(45)  # Focused beam
        rim_light.data.spot_blend = 0.3
        
        # Position behind and above the cylinder
        rim_elevation = math.radians(random.uniform(45, 80))
        rim_azimuth = math.radians(random.uniform(180, 360))
        
        distance = random.uniform(3.0, 5.0)
        x = distance * math.cos(rim_elevation) * math.cos(rim_azimuth)
        y = distance * math.cos(rim_elevation) * math.sin(rim_azimuth)
        z = distance * math.sin(rim_elevation)
        
        rim_light.location = (x, y, z)
        
        # Point toward cylinder edge
        target_location = Vector((0, 0, 2.0))
        self._point_light_at_target(rim_light, target_location)
        
        # Slightly warm rim light color
        rim_light.data.color = (1.0, 0.95, 0.8)
        
        logger.debug(f"Rim light: intensity={intensity:.0f}")
        
        return rim_light
    
    def _point_camera_at_target(self, 
                               camera: bpy.types.Object, 
                               target: Vector) -> None:
        """
        Point camera at target location.
        
        Args:
            camera: Camera object to orient
            target: Target location to look at
        """
        
        # Calculate direction vector
        direction = target - camera.location
        
        # Calculate rotation to point at target
        rot_quat = direction.to_track_quat('-Z', 'Y')
        camera.rotation_euler = rot_quat.to_euler()
    
    def _point_light_at_target(self, 
                              light: bpy.types.Object, 
                              target: Vector) -> None:
        """
        Point light at target location.
        
        Args:
            light: Light object to orient
            target: Target location to illuminate
        """
        
        # Calculate direction vector
        direction = target - light.location
        
        # Calculate rotation to point at target
        rot_quat = direction.to_track_quat('-Z', 'Y')
        light.rotation_euler = rot_quat.to_euler()
    
    def set_world_background(self, color: Tuple[float, float, float] = None) -> None:
        """
        Set world background color or HDRI.
        
        Args:
            color: RGB color tuple (0-1 range). If None, uses random neutral color.
        """
        
        world = bpy.context.scene.world
        if not world:
            world = bpy.data.worlds.new("World")
            bpy.context.scene.world = world
        
        # Enable nodes
        world.use_nodes = True
        
        # Clear existing nodes
        world.node_tree.nodes.clear()
        
        # Add background shader
        background = world.node_tree.nodes.new(type='ShaderNodeBackground')
        background.location = (0, 0)
        
        # Add world output
        output = world.node_tree.nodes.new(type='ShaderNodeOutputWorld')
        output.location = (300, 0)
        
        # Connect background to output
        world.node_tree.links.new(background.outputs['Background'], 
                                 output.inputs['Surface'])
        
        # Set background color
        if color is None:
            # Random neutral background
            gray_value = random.uniform(0.1, 0.3)
            color = (gray_value, gray_value, gray_value)
        
        background.inputs['Color'].default_value = (*color, 1.0)
        background.inputs['Strength'].default_value = 0.5
        
        logger.debug(f"World background set to: {color}")
    
    def _setup_environment_lighting(self) -> None:
        """Setup environment lighting using world shader nodes."""
        
        world = bpy.context.scene.world
        if not world:
            world = bpy.data.worlds.new("World")
            bpy.context.scene.world = world
        
        # Enable nodes
        world.use_nodes = True
        
        # Clear existing nodes
        world.node_tree.nodes.clear()
        
        # Add environment texture node
        env_texture = world.node_tree.nodes.new(type='ShaderNodeTexEnvironment')
        env_texture.location = (-300, 0)
        
        # Add background shader
        background = world.node_tree.nodes.new(type='ShaderNodeBackground')
        background.location = (0, 0)
        
        # Add world output
        output = world.node_tree.nodes.new(type='ShaderNodeOutputWorld')
        output.location = (300, 0)
        
        # Connect nodes
        world.node_tree.links.new(env_texture.outputs['Color'], background.inputs['Color'])
        world.node_tree.links.new(background.outputs['Background'], output.inputs['Surface'])
        
        # Set environment strength for balanced lighting
        background.inputs['Strength'].default_value = 0.3
        
        # Create a simple gradient environment if no HDRI available
        self._create_gradient_environment(world, env_texture)
        
        logger.debug("Environment lighting setup complete")

    def _create_gradient_environment(self, world, env_texture) -> None:
        """Create a simple gradient environment for even lighting."""
        
        # Add color ramp for gradient
        color_ramp = world.node_tree.nodes.new(type='ShaderNodeValToRGB')
        color_ramp.location = (-150, 0)
        
        # Add texture coordinate node
        tex_coord = world.node_tree.nodes.new(type='ShaderNodeTexCoord')
        tex_coord.location = (-600, 0)
        
        # Add mapping node for control
        mapping = world.node_tree.nodes.new(type='ShaderNodeMapping')
        mapping.location = (-450, 0)
        
        # Connect gradient nodes
        world.node_tree.links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
        world.node_tree.links.new(mapping.outputs['Vector'], color_ramp.inputs['Fac'])
        world.node_tree.links.new(color_ramp.outputs['Color'], world.node_tree.nodes['Background'].inputs['Color'])
        
        # Set gradient colors (light gray to darker gray)
        color_ramp.color_ramp.elements[0].color = (0.8, 0.8, 0.8, 1.0)  # Light gray
        color_ramp.color_ramp.elements[1].color = (0.3, 0.3, 0.3, 1.0)  # Darker gray
        
        # Remove the environment texture node as we're using gradient
        world.node_tree.nodes.remove(env_texture)

    def _create_ambient_light(self) -> bpy.types.Object:
        """
        Create ambient light for even overall illumination.
        
        Returns:
            Ambient light object
        """
        
        # Create large area light for ambient illumination
        bpy.ops.object.light_add(type='AREA')
        ambient_light = bpy.context.active_object
        ambient_light.name = "AmbientLight"
        
        # Set ambient light properties for even illumination
        ambient_light.data.energy = 200  # Lower intensity for ambient fill
        ambient_light.data.size = 8.0    # Large size for even coverage
        
        # Position above the scene for overall illumination
        ambient_light.location = (0, 0, 8.0)
        ambient_light.rotation_euler = (0, 0, 0)  # Point downward
        
        # Set neutral color
        ambient_light.data.color = (1.0, 1.0, 1.0)
        
        logger.debug("Ambient light created for even illumination")
        
        return ambient_light
