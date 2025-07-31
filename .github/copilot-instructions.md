# Copilot Instructions for Gas Tank Stamping Text Image Generator

## Project Overview
This project generates synthetic datasets of debossed/stamped text on gas cylinder surfaces for OCR model training using Blender and Python automation.

## Key Context for Copilot

### Project Purpose
- Generate diverse images of gas cylinders with realistic debossed/stamped text
- Create training data for OCR models that can read industrial markings
- Simulate various lighting conditions, camera angles, and text placements

### Technology Stack
- **Blender 3D**: Main rendering engine with Python API (bpy)
- **Python**: Automation scripts for batch processing
- **3D Modeling**: Procedural gas cylinder generation
- **Material Rendering**: PBR materials with metallic/plastic finishes
- **Text Processing**: Dynamic text embedding from dictionary files

### Core Components to Understand

#### 1. 3D Modeling (`cylinder_generator.py`)
```python
# Key concepts for gas cylinder creation:
- Cylinder primitive with realistic proportions
- UV mapping for texture application
- Mesh subdivision for smooth surfaces
```

#### 2. Text Debossing (`text_embosser.py`)
```python
# Important debossing techniques:
- Boolean operations for cutting text into surface
- Displacement mapping for subtle depth variations
- Font loading and text-to-mesh conversion
```

#### 3. Scene Randomization (`lighting_camera.py`)
```python
# Randomization parameters:
- Camera: azimuth (0-360°), elevation (-30 to 30°), distance
- Lighting: directional light angles, intensity, fill lights
- Materials: base colors, roughness, metallic properties
```

### Coding Guidelines

#### File Structure Patterns
```
scripts/
├── main.py              # Entry point with CLI arguments
├── cylinder_generator.py # 3D model creation
├── text_embosser.py     # Text debossing effects  
├── lighting_camera.py   # Scene setup and randomization
└── utils.py            # Helper functions

fonts/
├── industrial/          # Industrial-style fonts (.ttf, .otf)
├── monospace/           # Monospaced fonts for stamps
└── default/             # Default system fonts backup

data/
└── dict.txt            # Text strings for stamping

output/
├── images/             # Generated PNG images
└── labels/             # Ground truth text files
```

#### Blender API Best Practices
- Always clear default scene: `bpy.ops.object.select_all(action='SELECT')` → `bpy.ops.object.delete()`
- Use context overrides for operations: `bpy.context.view_layer.objects.active = obj`
- Handle materials properly: Check if material exists before creating
- Use appropriate coordinate systems for text placement on curved surfaces

#### Text Processing Patterns
```python
# Expected dict.txt format:
ACMEGAS123
FIREEXT1A
GASCO-X7Y
ABC-0012
2025-BATCH

# File naming convention:
[TEXT_CONTENT]_[VARIANT_ID].png
[TEXT_CONTENT]_[VARIANT_ID].txt
```

#### Randomization Ranges
- **Camera azimuth**: 0-360 degrees around cylinder
- **Camera elevation**: -30 to +30 degrees
- **Text vertical position**: Middle 60% of cylinder height
- **Deboss depth**: 0.001 to 0.005 Blender units
- **Material colors**: Industrial palette (blues, grays, greens, reds)

### Common Tasks & Code Patterns

#### 1. Loading Text Dictionary
```python
def load_text_dictionary(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]
```

#### 2. Blender Scene Setup
```python
import bpy
import bmesh

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Add cylinder
bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=3)
cylinder = bpy.context.active_object
```

#### 3. Text to 3D Conversion
```python
# Convert text to mesh for boolean operations
bpy.ops.object.text_add()
text_obj = bpy.context.active_object
text_obj.data.body = "SAMPLE_TEXT"

# Load custom font from fonts directory
font_path = "fonts/industrial/arial_bold.ttf"
if os.path.exists(font_path):
    text_obj.data.font = bpy.data.fonts.load(font_path)
else:
    # Use default Blender font
    text_obj.data.font = bpy.data.fonts['Bfont']
```

#### 4. Font Management
```python
def load_fonts_from_directory(font_dir):
    """Load available fonts from specified directory"""
    font_extensions = ['.ttf', '.otf', '.woff']
    fonts = []
    for ext in font_extensions:
        fonts.extend(glob.glob(os.path.join(font_dir, f"**/*{ext}"), recursive=True))
    return fonts

def get_random_font(font_list):
    """Select random font for text variation"""
    return random.choice(font_list) if font_list else None
```

### Output Requirements
- **Image Format**: PNG, 512x256 or 1024x512 resolution
- **Ground Truth**: Corresponding .txt files with exact text content
- **Batch Size**: Configurable (default: 1000-10000 images)
- **Quality**: High-quality renders suitable for OCR training

### Debug & Testing Notes
- Use Blender's viewport for quick preview before final render
- Test with small batches first (10-50 images)
- Verify text readability and deboss effect visibility
- Check file naming consistency and ground truth accuracy

### Performance Considerations
- Use Cycles render engine for realistic materials
- Optimize sample counts for speed vs quality balance
- Implement progress tracking for long batch jobs
- Consider GPU acceleration for faster rendering

### Documentation Management Rules

#### Always Update README.md When:
- Adding new scripts or modules
- Modifying existing functionality
- Adding new dependencies or requirements
- Changing project structure
- Adding new features or capabilities
- Updating installation or usage instructions
- Adding utility scripts or tools

#### README Update Guidelines:
- Keep feature lists current with actual implementation
- Update command examples to reflect real usage
- Document all executable scripts and their purposes
- Maintain accurate project structure diagrams
- Update prerequisites and installation steps
- Include new utility scripts in usage section
- Verify all examples work with current codebase

#### Git Workflow for Documentation:
- Always commit README updates together with code changes
- Use descriptive commit messages that mention documentation updates
- Ensure README reflects the current state of the project
- Review README accuracy before each major commit

## When Helping with This Project
1. Focus on Blender Python API (bpy) usage
2. Emphasize realistic 3D rendering techniques
3. Consider OCR training data quality requirements
4. Maintain consistency in randomization parameters
5. Ensure proper file I/O and batch processing patterns
6. **Always update README.md when adding new features, scripts, or significant changes**
7. **Update documentation to reflect current project capabilities and usage**
8. **Keep README.md synchronized with actual project structure and functionality**
