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
        
        # Standard gas cylinder proportions (height:diameter ratios)
        self.cylinder_configs = {
            'small': {'height': 2.0, 'radius': 0.4, 'name': 'Small Tank'},
            'medium': {'height': 3.0, 'radius': 0.5, 'name': 'Medium Tank'},
            'large': {'height': 4.0, 'radius': 0.6, 'name': 'Large Tank'},
            'industrial': {'height': 5.0, 'radius': 0.7, 'name': 'Industrial Tank'}
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
        
        # Create cylinder mesh
        bpy.ops.mesh.primitive_cylinder_add(
            radius=radius,
            depth=height,
            location=(0, 0, height/2),  # Position bottom at origin
            vertices=32  # Smooth circular cross-section
        )
        
        cylinder = bpy.context.active_object
        cylinder.name = f"GasCylinder_{size_type}"
        
        # Add subdivision surface for smooth appearance
        subdivision_mod = cylinder.modifiers.new(name="Subdivision", type='SUBSURF')
        subdivision_mod.levels = 2
        subdivision_mod.render_levels = 3
        
        # Create and apply material
        material = self._create_cylinder_material()
        cylinder.data.materials.append(material)
        
        # Add top and bottom caps with realistic details
        self._add_cylinder_caps(cylinder, radius, height)
        
        return cylinder
    
    def _create_cylinder_material(self) -> bpy.types.Material:
        """
        Create a realistic PBR material for the gas cylinder.
        
        Returns:
            Blender material with metallic/plastic properties
        """
        
        # Create new material
        material = bpy.data.materials.new(name="CylinderMaterial")
        material.use_nodes = True
        
        # Clear default nodes
        material.node_tree.nodes.clear()
        
        # Add principled BSDF shader
        bsdf = material.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 0)
        
        # Add material output
        output = material.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (300, 0)
        
        # Connect BSDF to output
        material.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        # Randomize material properties
        base_color = random.choice(self.industrial_colors)
        roughness = random.uniform(0.2, 0.8)
        metallic = random.uniform(0.7, 1.0)
        
        # Set material properties
        bsdf.inputs['Base Color'].default_value = base_color
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Specular'].default_value = 0.5
        
        logger.debug(f"Material: color={base_color[:3]}, roughness={roughness:.2f}, metallic={metallic:.2f}")
        
        return material
    
    def _add_cylinder_caps(self, cylinder: bpy.types.Object, radius: float, height: float) -> None:
        """
        Add realistic top and bottom caps to the cylinder.
        
        Args:
            cylinder: The main cylinder object
            radius: Cylinder radius
            height: Cylinder height
        """
        
        # Add top cap (valve area)
        bpy.ops.mesh.primitive_cylinder_add(
            radius=radius * 0.9,
            depth=0.1,
            location=(0, 0, height + 0.05)
        )
        
        top_cap = bpy.context.active_object
        top_cap.name = "TopCap"
        
        # Add bottom cap (base)
        bpy.ops.mesh.primitive_cylinder_add(
            radius=radius * 0.95,
            depth=0.05,
            location=(0, 0, 0.025)
        )
        
        bottom_cap = bpy.context.active_object
        bottom_cap.name = "BottomCap"
        
        # Join caps with main cylinder
        bpy.ops.object.select_all(action='DESELECT')
        cylinder.select_set(True)
        top_cap.select_set(True)
        bottom_cap.select_set(True)
        bpy.context.view_layer.objects.active = cylinder
        
        bpy.ops.object.join()
    
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
