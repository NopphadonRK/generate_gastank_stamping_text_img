"""
3D Gas Cylinder Generator Module

This module handles the creation of realistic 3D gas cylinder models using Blender's
Python API. It creates procedural cylinders with proper proportions and materials.

Author: Gas Tank Text Generator Project
Date: July 2025
"""

import random
import logging
from typing import Tuple, Optional

try:
    import bpy
    import bmesh
    from mathutils import Vector
except ImportError:
    print("Warning: bpy not available - this module requires Blender")

logger = logging.getLogger(__name__)


class CylinderGenerator:
    """Generates realistic 3D gas cylinder models for text stamping."""
    
    def __init__(self):
        """Initialize the cylinder generator with default parameters."""
        
        # Standard gas cylinder proportions (height:diameter ratios) - increased radius for larger appearance
        self.cylinder_configs = {
            'small': {'height': 2.0, 'radius': 0.6, 'name': 'Small Tank'},      # Increased from 0.4
            'medium': {'height': 3.0, 'radius': 0.8, 'name': 'Medium Tank'},    # Increased from 0.5
            'large': {'height': 4.0, 'radius': 1.0, 'name': 'Large Tank'},      # Increased from 0.6
            'industrial': {'height': 5.0, 'radius': 1.2, 'name': 'Industrial Tank'}  # Increased from 0.7
        }
        
        # Industrial color palette for gas cylinders
        self.industrial_colors = [
            (0.2, 0.4, 0.8, 1.0),  # Blue
            (0.3, 0.5, 0.3, 1.0),  # Green
            (0.6, 0.6, 0.6, 1.0),  # Gray
            (0.7, 0.2, 0.2, 1.0),  # Red
            (0.8, 0.8, 0.2, 1.0),  # Yellow
            (0.4, 0.4, 0.4, 1.0),  # Dark Gray
            (0.8, 0.4, 0.0, 1.0),  # Orange
        ]
    
    def create_cylinder(self, 
                       size_type: Optional[str] = None, 
                       custom_height: Optional[float] = None,
                       custom_radius: Optional[float] = None) -> bpy.types.Object:
        """
        Create a gas cylinder with realistic proportions and materials.
        
        Args:
            size_type: Type of cylinder ('small', 'medium', 'large', 'industrial')
            custom_height: Override height (Blender units)
            custom_radius: Override radius (Blender units)
            
        Returns:
            Blender object representing the gas cylinder
        """
        
        # Select cylinder configuration
        if size_type is None:
            size_type = random.choice(list(self.cylinder_configs.keys()))
        
        config = self.cylinder_configs.get(size_type, self.cylinder_configs['medium'])
        
        # Use custom dimensions if provided
        height = custom_height if custom_height else config['height']
        radius = custom_radius if custom_radius else config['radius']
        
        logger.info(f"Creating {config['name']} (h={height:.2f}, r={radius:.2f})")
        
        # Create perfect geometric cylinder with clean circular bases
        bpy.ops.mesh.primitive_cylinder_add(
            radius=radius,
            depth=height,
            location=(0, 0, height/2),  # Position bottom at origin
            vertices=32  # Optimal vertex count for perfect circular geometry
        )
        
        cylinder = bpy.context.active_object
        cylinder.name = f"GasCylinder_{size_type}"
        
        # Apply smooth shading to the lateral surface only
        bpy.context.view_layer.objects.active = cylinder
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Select all faces and apply smooth shading for clean surface
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.faces_shade_smooth()
        
        # Exit edit mode - keep perfect geometric form
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Create and apply material
        material = self._create_cylinder_material()
        cylinder.data.materials.append(material)
        
        return cylinder
    
    def _create_cylinder_material(self) -> bpy.types.Material:
        """
        Create a realistic PBR material for the gas cylinder with mild surface bumpiness.
        
        Returns:
            Blender material with metallic/plastic properties and surface texture
        """
        
        # Create new material
        material = bpy.data.materials.new(name="CylinderMaterial")
        material.use_nodes = True
        
        # Clear default nodes
        material.node_tree.nodes.clear()
        
        # Add principled BSDF shader
        bsdf = material.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf.location = (300, 0)
        
        # Add material output
        output = material.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (600, 0)
        
        # Connect BSDF to output
        material.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        # Add texture coordinate node
        tex_coord = material.node_tree.nodes.new(type='ShaderNodeTexCoord')
        tex_coord.location = (-600, 0)
        
        # Add mapping node for texture control
        mapping = material.node_tree.nodes.new(type='ShaderNodeMapping')
        mapping.location = (-400, 0)
        mapping.inputs['Scale'].default_value = (8.0, 8.0, 8.0)  # Scale for mild texture detail
        
        # Add noise texture for surface bumpiness
        noise_texture = material.node_tree.nodes.new(type='ShaderNodeTexNoise')
        noise_texture.location = (-200, 0)
        noise_texture.inputs['Scale'].default_value = 15.0      # Fine surface detail
        noise_texture.inputs['Detail'].default_value = 3.0     # Moderate detail level
        noise_texture.inputs['Roughness'].default_value = 0.6  # Balanced roughness in noise
        noise_texture.inputs['Distortion'].default_value = 0.2 # Slight distortion for realism
        
        # Add ColorRamp to control bump intensity
        color_ramp = material.node_tree.nodes.new(type='ShaderNodeValToRGB')
        color_ramp.location = (0, -200)
        
        # Set color ramp for mild bump effect
        color_ramp.color_ramp.elements[0].position = 0.4  # Compress range for subtlety  
        color_ramp.color_ramp.elements[1].position = 0.6
        color_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)  # Black
        color_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)  # White
        
        # Add bump node for surface displacement
        bump_node = material.node_tree.nodes.new(type='ShaderNodeBump')
        bump_node.location = (150, -200)
        bump_node.inputs['Strength'].default_value = 0.1  # Mild bump strength
        
        # Connect texture nodes
        material.node_tree.links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
        material.node_tree.links.new(mapping.outputs['Vector'], noise_texture.inputs['Vector'])
        material.node_tree.links.new(noise_texture.outputs['Fac'], color_ramp.inputs['Fac'])
        material.node_tree.links.new(color_ramp.outputs['Color'], bump_node.inputs['Height'])
        material.node_tree.links.new(bump_node.outputs['Normal'], bsdf.inputs['Normal'])
        
        # Set glossy teal-green material properties
        teal_green_color = (0.188, 0.529, 0.482, 1.0)  # #30877b converted to linear RGB
        roughness = 0.1  # Low roughness for glossy surface
        metallic = 0.8   # High metallic value for reflective appearance
        
        # Set material properties
        bsdf.inputs['Base Color'].default_value = teal_green_color
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
        
        # Standard metallic properties for Blender 4.x
        if 'Specular IOR' in bsdf.inputs:
            bsdf.inputs['Specular IOR'].default_value = 1.5
        elif 'IOR' in bsdf.inputs:
            bsdf.inputs['IOR'].default_value = 1.5
        
        logger.debug(f"Material: color={teal_green_color[:3]}, roughness={roughness:.2f}, metallic={metallic:.2f}, bump=mild")
        
        return material
    
    def get_text_placement_area(self, cylinder: bpy.types.Object) -> Tuple[float, float]:
        """
        Calculate the suitable area for text placement on the cylinder surface.
        
        Args:
            cylinder: The gas cylinder object
            
        Returns:
            Tuple of (min_height, max_height) for text placement
        """
        
        # Get cylinder dimensions
        dimensions = cylinder.dimensions
        height = dimensions.z
        
        # Text should be placed in the middle 60% of the cylinder height
        margin = height * 0.2
        min_height = margin
        max_height = height - margin
        
        return min_height, max_height
    
    def get_cylinder_radius(self, cylinder: bpy.types.Object) -> float:
        """
        Get the radius of the gas cylinder.
        
        Args:
            cylinder: The gas cylinder object
            
        Returns:
            Cylinder radius in Blender units
        """
        
        dimensions = cylinder.dimensions
        radius = max(dimensions.x, dimensions.y) / 2
        
        return radius
