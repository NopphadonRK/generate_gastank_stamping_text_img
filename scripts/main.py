#!/usr/bin/env python3
"""
Gas Tank Stamping Text Image Generator - Main Script

This script generates synthetic datasets of debossed/stamped text on gas cylinder 
surfaces for OCR model training using Blender and Python automation.

Usage:
    blender --background --python scripts/main.py -- --count 100 --dict data/dict.txt

Author: Gas Tank Text Generator Project
Date: July 2025
"""

import sys
import os
import argparse
import random
import logging
from pathlib import Path

# Add the scripts directory to Python path for imports
script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

try:
    import bpy
except ImportError:
    print("Error: This script must be run from within Blender")
    print("Usage: blender --background --python scripts/main.py -- [arguments]")
    sys.exit(1)

from cylinder_generator import CylinderGenerator
from text_embosser import TextEmbosser
from lighting_camera import LightingCameraController
from utils import setup_logging, load_text_dictionary, create_output_dirs


def parse_arguments():
    """Parse command line arguments passed after '--' in Blender command."""
    parser = argparse.ArgumentParser(
        description="Generate synthetic gas tank stamping text images"
    )
    
    parser.add_argument(
        "--count", 
        type=int, 
        default=100,
        help="Number of images to generate (default: 100)"
    )
    
    parser.add_argument(
        "--dict", 
        type=str, 
        required=True,
        help="Path to text dictionary file (required)"
    )
    
    parser.add_argument(
        "--output", 
        type=str, 
        default="output/",
        help="Output directory (default: output/)"
    )
    
    parser.add_argument(
        "--resolution", 
        nargs=2, 
        type=int, 
        default=[512, 256],
        help="Image dimensions W H (default: 512 256)"
    )
    
    parser.add_argument(
        "--samples", 
        type=int, 
        default=64,
        help="Render quality samples (default: 64)"
    )
    
    parser.add_argument(
        "--seed", 
        type=int, 
        default=None,
        help="Random seed for reproducibility"
    )
    
    parser.add_argument(
        "--font-dir", 
        type=str, 
        default="fonts/",
        help="Directory containing custom fonts (default: fonts/)"
    )
    
    parser.add_argument(
        "--font-style", 
        type=str, 
        choices=['industrial', 'monospace', 'default'],
        default='industrial',
        help="Font style preference (default: industrial)"
    )
    
    # Parse arguments that come after '--' in Blender command
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
    return args


def main():
    """Main execution function."""
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info(f"Starting Gas Tank Text Image Generation")
    logger.info(f"Parameters: count={args.count}, dict={args.dict}, output={args.output}")
    
    # Set random seed if provided
    if args.seed is not None:
        random.seed(args.seed)
        logger.info(f"Random seed set to: {args.seed}")
    
    # Validate input files
    if not os.path.exists(args.dict):
        logger.error(f"Dictionary file not found: {args.dict}")
        sys.exit(1)
    
    # Load text dictionary
    text_list = load_text_dictionary(args.dict)
    logger.info(f"Loaded {len(text_list)} text strings from dictionary")
    
    # Create output directories
    create_output_dirs(args.output)
    
    # Initialize generators
    cylinder_gen = CylinderGenerator()
    text_embosser = TextEmbosser(args.font_dir, args.font_style)
    lighting_camera = LightingCameraController()
    
    # Setup Blender rendering
    scene = bpy.context.scene
    scene.render.resolution_x = args.resolution[0]
    scene.render.resolution_y = args.resolution[1]
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = args.samples
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = os.path.join(args.output, 'images', 'temp.png')
    
    # Generate images
    generated_count = 0
    
    try:
        for i in range(args.count):
            # Select random text from dictionary
            text_content = random.choice(text_list)
            variant_id = f"{i+1:03d}"
            
            logger.info(f"Generating image {i+1}/{args.count}: {text_content}")
            
            # Clear scene
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete(use_global=False)
            
            # Generate cylinder
            cylinder = cylinder_gen.create_cylinder()
            
            # Apply text debossing
            text_embosser.apply_debossed_text(cylinder, text_content)
            
            # Setup lighting and camera
            lighting_camera.randomize_scene()
            
            # Render image
            image_filename = f"{text_content}_{variant_id}.png"
            label_filename = f"{text_content}_{variant_id}.txt"
            
            image_path = os.path.join(args.output, 'images', image_filename)
            label_path = os.path.join(args.output, 'labels', label_filename)
            
            scene.render.filepath = image_path
            bpy.ops.render.render(write_still=True)
            
            # Write ground truth label
            with open(label_path, 'w', encoding='utf-8') as f:
                f.write(text_content)
            
            generated_count += 1
            
            if generated_count % 10 == 0:
                logger.info(f"Progress: {generated_count}/{args.count} images generated")
    
    except KeyboardInterrupt:
        logger.warning("Generation interrupted by user")
    except Exception as e:
        logger.error(f"Error during generation: {str(e)}")
        raise
    
    logger.info(f"Generation complete! Generated {generated_count} images")
    logger.info(f"Images saved to: {os.path.join(args.output, 'images')}")
    logger.info(f"Labels saved to: {os.path.join(args.output, 'labels')}")


if __name__ == "__main__":
    main()
