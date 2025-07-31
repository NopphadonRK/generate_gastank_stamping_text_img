"""
Text Embossing Module for Gas Cylinder Stamping

This module handles the creation of debossed/stamped text effects on gas cylinder
surfaces using Blender's boolean operations and displacement mapping.

Author: Gas Tank Text Generator Project
Date: July 2025
"""

import os
import glob
import random
import logging
from typing import List, Optional

try:
    import bpy
    from mathutils import Vector
except ImportError:
    print("Warning: bpy not available - this module requires Blender")

logger = logging.getLogger(__name__)


class TextEmbosser:
    """Handles text debossing/stamping effects on cylinder surfaces."""
    
    def __init__(self, font_dir: str = "fonts/", font_style: str = "industrial"):
        """
        Initialize the text embosser with font configuration.
        
        Args:
            font_dir: Directory containing font files
            font_style: Preferred font style (industrial, monospace, default)
        """
        
        self.font_dir = font_dir
        self.font_style = font_style
        self.available_fonts = self._load_available_fonts()
        
        # Text embossing parameters
        self.deboss_depth_range = (0.001, 0.005)  # Depth variation in Blender units
        self.text_size_range = (0.15, 0.25)      # Text size relative to cylinder
        
        logger.info(f"TextEmbosser initialized with {len(self.available_fonts)} fonts")
    
    def _load_available_fonts(self) -> List[str]:
        """
        Load available font files from the fonts directory.
        
        Returns:
            List of font file paths
        """
        
        fonts = []
        font_extensions = ['.ttf', '.otf', '.woff']
        
        # Build search paths based on font style preference
        search_paths = []
        
        if self.font_style == 'industrial':
            search_paths.append(os.path.join(self.font_dir, 'industrial'))
        elif self.font_style == 'monospace':
            search_paths.append(os.path.join(self.font_dir, 'monospace'))
        elif self.font_style == 'default':
            search_paths.append(os.path.join(self.font_dir, 'default'))
        
        # Fallback to all font directories
        search_paths.extend([
            os.path.join(self.font_dir, 'industrial'),
            os.path.join(self.font_dir, 'monospace'),
            os.path.join(self.font_dir, 'default')
        ])
        
        # Search for font files
        for search_path in search_paths:
            if os.path.exists(search_path):
                for ext in font_extensions:
                    pattern = os.path.join(search_path, f"**/*{ext}")
                    fonts.extend(glob.glob(pattern, recursive=True))
        
        # Remove duplicates
        fonts = list(set(fonts))
        
        logger.debug(f"Found fonts: {[os.path.basename(f) for f in fonts]}")
        
        return fonts
    
    def apply_debossed_text(self, 
                           cylinder: bpy.types.Object, 
                           text_content: str,
                           position_height: Optional[float] = None) -> bpy.types.Object:
        """
        Apply debossed text effect to the cylinder surface.
        
        Args:
            cylinder: The gas cylinder object
            text_content: Text string to emboss
            position_height: Vertical position on cylinder (None for random)
            
        Returns:
            The text object created for the debossing effect
        """
        
        logger.info(f"Applying debossed text: '{text_content}'")
        
        # Create text object
        text_obj = self._create_text_object(text_content)
        
        # Position text on cylinder surface
        self._position_text_on_cylinder(text_obj, cylinder, position_height)
        
        # Convert text to mesh for boolean operations
        text_mesh = self._convert_text_to_mesh(text_obj)
        
        # Apply debossing effect using boolean modifier
        self._apply_boolean_deboss(cylinder, text_mesh)
        
        # Clean up temporary objects
        bpy.data.objects.remove(text_obj, do_unlink=True)
        
        return text_mesh
    
    def _create_text_object(self, text_content: str) -> bpy.types.Object:
        """
        Create a Blender text object with specified content and font.
        
        Args:
            text_content: The text string to create
            
        Returns:
            Blender text object
        """
        
        # Create text object
        bpy.ops.object.text_add()
        text_obj = bpy.context.active_object
        text_obj.name = f"Text_{text_content}"
        
        # Set text content
        text_obj.data.body = text_content
        
        # Load and apply font
        font_path = self._select_random_font()
        if font_path and os.path.exists(font_path):
            try:
                font = bpy.data.fonts.load(font_path)
                text_obj.data.font = font
                logger.debug(f"Applied font: {os.path.basename(font_path)}")
            except Exception as e:
                logger.warning(f"Failed to load font {font_path}: {e}")
                # Use default Blender font
                text_obj.data.font = bpy.data.fonts.get('Bfont')
        else:
            # Use default Blender font
            text_obj.data.font = bpy.data.fonts.get('Bfont')
            logger.debug("Using default Blender font")
        
        # Set text properties
        text_obj.data.size = random.uniform(*self.text_size_range)
        text_obj.data.align_x = 'CENTER'
        text_obj.data.align_y = 'CENTER'
        
        return text_obj
    
    def _select_random_font(self) -> Optional[str]:
        """
        Select a random font from available fonts.
        
        Returns:
            Path to selected font file, or None if no fonts available
        """
        
        if not self.available_fonts:
            return None
        
        return random.choice(self.available_fonts)
    
    def _position_text_on_cylinder(self, 
                                  text_obj: bpy.types.Object, 
                                  cylinder: bpy.types.Object,
                                  position_height: Optional[float] = None) -> None:
        """
        Position text object on the cylinder surface.
        
        Args:
            text_obj: The text object to position
            cylinder: The target cylinder
            position_height: Specific height position (None for random)
        """
        
        # Get cylinder dimensions
        cylinder_radius = max(cylinder.dimensions.x, cylinder.dimensions.y) / 2
        cylinder_height = cylinder.dimensions.z
        
        # Calculate text position
        if position_height is None:
            # Random height within middle 60% of cylinder
            margin = cylinder_height * 0.2
            position_height = random.uniform(margin, cylinder_height - margin)
        
        # Random azimuthal angle around cylinder
        azimuth_angle = random.uniform(0, 2 * 3.14159)
        
        # Position text slightly outside cylinder surface
        offset_distance = cylinder_radius + 0.01
        
        x = offset_distance * random.choice([1, -1])  # Front or back of cylinder
        y = 0
        z = position_height
        
        text_obj.location = (x, y, z)
        
        # Rotate text to face inward toward cylinder center
        if x > 0:
            text_obj.rotation_euler = (0, 0, 0)  # Face forward
        else:
            text_obj.rotation_euler = (0, 0, 3.14159)  # Face backward
        
        logger.debug(f"Text positioned at ({x:.3f}, {y:.3f}, {z:.3f})")
    
    def _convert_text_to_mesh(self, text_obj: bpy.types.Object) -> bpy.types.Object:
        """
        Convert text object to mesh for boolean operations.
        
        Args:
            text_obj: The text object to convert
            
        Returns:
            Mesh object created from text
        """
        
        # Select and convert text to mesh
        bpy.context.view_layer.objects.active = text_obj
        bpy.ops.object.convert(target='MESH')
        
        text_mesh = bpy.context.active_object
        text_mesh.name = f"TextMesh_{text_obj.name}"
        
        # Extrude text to give it depth for boolean operation
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Extrude inward for debossing effect
        deboss_depth = random.uniform(*self.deboss_depth_range)
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value": (0, 0, -deboss_depth)}
        )
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        logger.debug(f"Text mesh created with deboss depth: {deboss_depth:.4f}")
        
        return text_mesh
    
    def _apply_boolean_deboss(self, 
                             cylinder: bpy.types.Object, 
                             text_mesh: bpy.types.Object) -> None:
        """
        Apply boolean difference operation to create debossed effect.
        
        Args:
            cylinder: The target cylinder object
            text_mesh: The text mesh to subtract from cylinder
        """
        
        # Add boolean modifier to cylinder
        boolean_mod = cylinder.modifiers.new(name="TextDeboss", type='BOOLEAN')
        boolean_mod.operation = 'DIFFERENCE'
        boolean_mod.object = text_mesh
        boolean_mod.solver = 'EXACT'  # More accurate but slower
        
        # Apply the modifier
        bpy.context.view_layer.objects.active = cylinder
        bpy.ops.object.modifier_apply(modifier="TextDeboss")
        
        # Hide the text mesh (but keep it for reference)
        text_mesh.hide_render = True
        text_mesh.hide_viewport = True
        
        logger.debug("Boolean deboss effect applied to cylinder")
