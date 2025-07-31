#!/usr/bin/env python3
"""
Simple Lighting Control GUI for Gas Tank Text Generator

Minimal GUI to control lighting settings without modifying existing code.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import tempfile
import os

class LightingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gas Tank Lighting Controller")
        self.root.geometry("400x350")
        
        # Lighting parameters
        self.env_strength = tk.DoubleVar(value=0.8)
        self.key_light = tk.BooleanVar(value=False)
        self.fill_light = tk.BooleanVar(value=False)
        self.rim_light = tk.BooleanVar(value=False)
        self.key_intensity = tk.DoubleVar(value=300)
        self.fill_intensity = tk.DoubleVar(value=150)
        self.rim_intensity = tk.DoubleVar(value=200)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Environment lighting
        ttk.Label(main_frame, text="Environment Light Strength:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Scale(main_frame, from_=0.1, to=2.0, variable=self.env_strength, orient=tk.HORIZONTAL, length=200).grid(row=0, column=1, pady=2)
        ttk.Label(main_frame, textvariable=self.env_strength).grid(row=0, column=2, pady=2)
        
        # Directional lights
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 5))
        ttk.Label(main_frame, text="Directional Lights:", font=('TkDefaultFont', 10, 'bold')).grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=2)
        
        # Key light
        ttk.Checkbutton(main_frame, text="Key Light", variable=self.key_light).grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Scale(main_frame, from_=50, to=800, variable=self.key_intensity, orient=tk.HORIZONTAL, length=150).grid(row=3, column=1, pady=2)
        ttk.Label(main_frame, textvariable=self.key_intensity).grid(row=3, column=2, pady=2)
        
        # Fill light
        ttk.Checkbutton(main_frame, text="Fill Light", variable=self.fill_light).grid(row=4, column=0, sticky=tk.W, pady=2)
        ttk.Scale(main_frame, from_=20, to=400, variable=self.fill_intensity, orient=tk.HORIZONTAL, length=150).grid(row=4, column=1, pady=2)
        ttk.Label(main_frame, textvariable=self.fill_intensity).grid(row=4, column=2, pady=2)
        
        # Rim light
        ttk.Checkbutton(main_frame, text="Rim Light", variable=self.rim_light).grid(row=5, column=0, sticky=tk.W, pady=2)
        ttk.Scale(main_frame, from_=30, to=600, variable=self.rim_intensity, orient=tk.HORIZONTAL, length=150).grid(row=5, column=1, pady=2)
        ttk.Label(main_frame, textvariable=self.rim_intensity).grid(row=5, column=2, pady=2)
        
        # Buttons
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 5))
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Generate Test Image", command=self.generate_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset to Default", command=self.reset_defaults).pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var, foreground="blue").grid(row=8, column=0, columnspan=3, pady=5)
    
    def generate_custom_script(self):
        """Generate temporary custom lighting script"""
        script_content = f'''
import sys
import os
sys.path.append(os.path.dirname(__file__))

from lighting_camera import LightingCameraController
import bpy
import random
import math
from mathutils import Vector

class CustomLightingController(LightingCameraController):
    def setup_lighting(self):
        """Custom lighting setup from GUI"""
        self._clear_existing_lights()
        self._setup_custom_environment({self.env_strength.get()})
        
        if {self.key_light.get()}:
            self._create_custom_key_light({self.key_intensity.get()})
        if {self.fill_light.get()}:
            self._create_custom_fill_light({self.fill_intensity.get()})
        if {self.rim_light.get()}:
            self._create_custom_rim_light({self.rim_intensity.get()})
    
    def _setup_custom_environment(self, strength):
        """Setup environment with custom strength"""
        world = bpy.context.scene.world
        if not world:
            world = bpy.data.worlds.new("World")
            bpy.context.scene.world = world
        
        world.use_nodes = True
        world.node_tree.nodes.clear()
        
        background = world.node_tree.nodes.new(type='ShaderNodeBackground')
        background.location = (0, 0)
        background.inputs['Strength'].default_value = strength
        background.inputs['Color'].default_value = (0.8, 0.8, 0.8, 1.0)
        
        output = world.node_tree.nodes.new(type='ShaderNodeOutputWorld')
        output.location = (300, 0)
        world.node_tree.links.new(background.outputs['Background'], output.inputs['Surface'])
    
    def _create_custom_key_light(self, intensity):
        bpy.ops.object.light_add(type='SUN')
        light = bpy.context.active_object
        light.name = "CustomKeyLight"
        light.data.energy = intensity
        light.location = (3, 3, 5)
    
    def _create_custom_fill_light(self, intensity):
        bpy.ops.object.light_add(type='AREA')
        light = bpy.context.active_object
        light.name = "CustomFillLight"
        light.data.energy = intensity
        light.data.size = 3.0
        light.location = (-2, 1, 4)
    
    def _create_custom_rim_light(self, intensity):
        bpy.ops.object.light_add(type='SPOT')
        light = bpy.context.active_object
        light.name = "CustomRimLight"
        light.data.energy = intensity
        light.location = (-3, -3, 4)

# Replace the original controller
controller = CustomLightingController()
controller.setup_lighting()
controller.setup_camera()
'''
        return script_content
    
    def generate_test(self):
        """Generate a test image with current settings"""
        self.status_var.set("Generating test image...")
        self.root.update()
        
        try:
            # Create a simple Blender script
            script_content = f'''
import bpy
import sys
import os

# Add project path
project_path = "{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}"
sys.path.append(os.path.join(project_path, "scripts"))

# Import modules
from cylinder_generator import CylinderGenerator
from text_embosser import TextEmbosser

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create cylinder and text
cylinder_gen = CylinderGenerator()
cylinder = cylinder_gen.create_cylinder(size_type='medium')

# Create text embosser with correct parameters
text_embosser = TextEmbosser(font_dir=os.path.join(project_path, "fonts"), font_style="default")
text_embosser.apply_debossed_text(cylinder, "GUI-TEST")

# Setup custom lighting
world = bpy.context.scene.world
if not world:
    world = bpy.data.worlds.new("World")
    bpy.context.scene.world = world

world.use_nodes = True
world.node_tree.nodes.clear()

background = world.node_tree.nodes.new(type='ShaderNodeBackground')
background.inputs['Strength'].default_value = {self.env_strength.get()}
background.inputs['Color'].default_value = (0.9, 0.9, 0.9, 1.0)  # Brighter background

output = world.node_tree.nodes.new(type='ShaderNodeOutputWorld')
world.node_tree.links.new(background.outputs['Background'], output.inputs['Surface'])

# Clear existing lights first
for obj in bpy.data.objects:
    if obj.type == 'LIGHT':
        bpy.data.objects.remove(obj, do_unlink=True)

# Add directional lights if enabled
if {self.key_light.get()}:
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 8))
    light = bpy.context.active_object
    light.name = "GUIKeyLight"
    light.data.energy = {self.key_intensity.get()}
    light.rotation_euler = (0.7, 0, 0.78)  # Point toward cylinder
    print(f"Added Key Light with energy: {{light.data.energy}}")

if {self.fill_light.get()}:
    bpy.ops.object.light_add(type='AREA', location=(-3, 2, 6))
    light = bpy.context.active_object
    light.name = "GUIFillLight"
    light.data.energy = {self.fill_intensity.get()}
    light.data.size = 4.0
    light.rotation_euler = (0.5, 0, -0.5)  # Point toward cylinder
    print(f"Added Fill Light with energy: {{light.data.energy}}")

if {self.rim_light.get()}:
    bpy.ops.object.light_add(type='SPOT', location=(-4, -4, 6))
    light = bpy.context.active_object
    light.name = "GUIRimLight"  
    light.data.energy = {self.rim_intensity.get()}
    light.rotation_euler = (0.6, 0, -2.3)  # Point toward cylinder
    print(f"Added Rim Light with energy: {{light.data.energy}}")

# Add basic lighting if no directional lights are enabled
if not ({self.key_light.get()} or {self.fill_light.get()} or {self.rim_light.get()}):
    bpy.ops.object.light_add(type='SUN', location=(3, 3, 6))
    light = bpy.context.active_object
    light.name = "DefaultLight"
    light.data.energy = 2.0
    light.rotation_euler = (0.7, 0, 0.78)
    print("Added default sun light for visibility")

# Debug: Print object info
print("Objects in scene:")
for obj in bpy.data.objects:
    print(f"  - {{obj.name}} ({{obj.type}}) at {{obj.location}}")
    if obj.type == 'MESH':
        print(f"    Dimensions: {{obj.dimensions}}")
        print(f"    Material: {{obj.data.materials[:] if obj.data.materials else 'None'}}")

# Get camera reference for debug info
scene_camera = bpy.context.scene.camera
if scene_camera:
    print(f"Camera location: {{scene_camera.location}}")
    print(f"Camera rotation: {{scene_camera.rotation_euler}}")
else:
    print("No camera found in scene")

print(f"Environment strength: {self.env_strength.get()}")

# Setup camera with proper positioning
if bpy.context.scene.camera:
    bpy.data.objects.remove(bpy.context.scene.camera, do_unlink=True)

bpy.ops.object.camera_add()
camera = bpy.context.active_object
bpy.context.scene.camera = camera

# Position camera to look at cylinder center
camera.location = (4, 4, 3)  # Distance from cylinder
# Point camera at cylinder (which is at origin with height 1.5 center)
import mathutils
direction = mathutils.Vector((0, 0, 1.5)) - camera.location
camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

# Set camera properties
camera.data.lens = 50  # 50mm lens

# Render settings
scene = bpy.context.scene
scene.render.resolution_x = 512
scene.render.resolution_y = 256
scene.render.filepath = os.path.join(project_path, "output", "images", "gui_test.png")

# Set render engine and samples for faster preview
scene.render.engine = 'CYCLES'
scene.cycles.samples = 32  # Reduced for faster GUI testing

# Ensure proper viewport settings
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'MATERIAL'

# Frame the cylinder in camera view - manual positioning since camera_to_view_selected doesn't work in background
cylinder_obj = None
for obj in bpy.data.objects:
    if obj.type == 'MESH' and 'Cylinder' in obj.name:
        cylinder_obj = obj
        break

if cylinder_obj:
    # Calculate camera position to frame the cylinder properly
    cylinder_center = cylinder_obj.location
    cylinder_size = max(cylinder_obj.dimensions)
    
    # Position camera at optimal distance
    distance = cylinder_size * 2.5  # 2.5x the object size
    camera_loc = (distance * 0.7, distance * 0.7, cylinder_center.z + distance * 0.3)
    
    scene_camera = bpy.context.scene.camera
    if scene_camera:
        scene_camera.location = camera_loc
        
        # Point camera at cylinder center
        import mathutils
        direction = cylinder_center - mathutils.Vector(camera_loc)
        scene_camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
        
        print(f"Positioned camera at {{camera_loc}} looking at {{cylinder_center}}")
    else:
        print("No camera found to position")
else:
    print("No cylinder found to frame")

# Render
print("Starting render...")
bpy.ops.render.render(write_still=True)
print("✅ GUI test image saved to output/images/gui_test.png")
'''
            
            # Write to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(script_content)
                temp_script = f.name
            
            # Run Blender
            import subprocess
            cmd = ['blender', '--background', '--python', temp_script]
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                stdout, stderr = process.communicate(timeout=30)
                
                # Cleanup
                os.unlink(temp_script)
                
                if process.returncode == 0 and "GUI test image saved" in stdout:
                    self.status_var.set("✅ Test image generated successfully!")
                else:
                    self.status_var.set("❌ Generation failed")
                    print(f"STDOUT: {stdout}")
                    print(f"STDERR: {stderr}")
                    
            except subprocess.TimeoutExpired:
                process.kill()
                self.status_var.set("❌ Generation timed out")
                os.unlink(temp_script)
                
        except Exception as e:
            self.status_var.set(f"❌ Error: {str(e)[:30]}...")
            print(f"Exception: {e}")
            import traceback
            traceback.print_exc()
    
    def reset_defaults(self):
        """Reset to default values"""
        self.env_strength.set(0.8)
        self.key_light.set(False)
        self.fill_light.set(False)
        self.rim_light.set(False)
        self.key_intensity.set(300)
        self.fill_intensity.set(150)
        self.rim_intensity.set(200)
        self.status_var.set("Reset to defaults")

def main():
    root = tk.Tk()
    app = LightingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
