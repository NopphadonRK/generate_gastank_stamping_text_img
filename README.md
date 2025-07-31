# Gas Tank Stamping Text Image Generator

A Python-based tool using Blender 3D to generate synthetic datasets of debossed/stamped text on gas cylinder surfaces for OCR model training.

## 🎯 Project Overview

This project creates realistic 3D rendered images of industrial gas cylinders with debossed text markings. The generated dataset is specifically designed for training OCR models to recognize stamped text on curved metallic surfaces under various lighting conditions.

## ✨ Features

- **Large Perfect Geometric Cylinders**: Increased radius (50% larger) for more prominent visual presence
- **Mild Surface Bumpiness**: Realistic noise texture with subtle bump mapping for authentic industrial appearance  
- **Glossy Teal-Green Material**: Distinctive #30877b teal-green color with high-gloss metallic finish (roughness 0.1, metallic 0.8)
- **Balanced Environment Lighting**: Advanced lighting system with gradient environment, ambient light, and optimized three-point lighting
- **Maintained Geometric Integrity**: No subdivision modifiers or deformation - pure geometric form with surface texture
- **Authentic Debossing Effects**: Text appears physically stamped into the metal surface
- **FreesiaUPC Font Integration**: Uses Thai-style FreesiaUPC font for clear numeric text
- **Even Illumination**: Environment lighting and ambient fill eliminate harsh shadows and bright spots
- **Optimized Camera Positioning**: Adjusted distances for larger cylinder dimensions
- **Dynamic Lighting**: Randomized three-point lighting creates realistic shadows and highlights
- **Camera Variations**: Multiple viewing angles and perspectives per text sample
- **Batch Processing**: Automated generation of thousands of training images
- **Ground Truth Generation**: Automatic creation of corresponding text labels
- **Utility Scripts**: Complete set of management and testing tools
- **Pattern Support**: Optimized for xxxx-xxxxxx numeric patterns

## 🛠️ Technology Stack

- **Blender 3D**: Main rendering engine with Python API
- **Python 3.8+**: Automation and batch processing
- **bpy (Blender Python API)**: 3D modeling and rendering control
- **PIL/Pillow**: Image post-processing (optional)

## 📁 Project Structure

```
generate_gastank_stamping_text_img/
├── data/
│   └── dict.txt                 # Text strings for stamping (xxxx-xxxxxx pattern)
├── fonts/
│   ├── industrial/              # Industrial-style fonts
│   ├── monospace/               # Monospaced fonts for stamps
│   ├── default/                 # Default system fonts backup
│   │   ├── FreesiaUPC.ttf      # Thai-style font (included)
│   │   └── FreesiabUPC.ttf     # FreesiaUPC Bold (included)
│   └── README.md               # Font management guide
├── output/
│   ├── images/                  # Generated PNG images
│   ├── labels/                  # Ground truth text files
│   └── README.md               # Dataset usage guide
├── scripts/
│   ├── main.py                  # Main execution script
│   ├── cylinder_generator.py    # 3D cylinder model creation
│   ├── text_embosser.py         # Text debossing effects
│   ├── lighting_camera.py       # Scene lighting and camera control
│   └── utils.py                 # Helper utilities
├── venv/                       # Python virtual environment
├── clean_output.sh             # Remove generated files script
├── quick_commands.sh           # Development utilities menu
├── test.sh                     # Comprehensive test suite
├── requirements.txt            # Python dependencies
└── README.md
```

## 🚀 Quick Start

### Prerequisites

1. **Install Blender 3.0+**
   ```bash
   # macOS (using Homebrew)
   brew install --cask blender
   
   # Or download from https://www.blender.org/download/
   ```

2. **Clone Repository**
   ```bash
   git clone git@github.com:NopphadonRK/generate_gastank_stamping_text_img.git
   cd generate_gastank_stamping_text_img
   ```

3. **Install Python Dependencies**
   ```bash
   # Create and activate virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   # Run comprehensive tests
   ./test.sh
   
   # Or check system status
   ./quick_commands.sh
   ```

### Basic Usage

1. **Prepare Text Dictionary**
   ```bash
   # The project includes dict.txt with 100 xxxx-xxxxxx patterns
   # Example patterns: 6302-844353, 2417-001227, 3634-299252
   head -5 data/dict.txt
   ```

2. **Quick Start - Use Utility Scripts**
   ```bash
   # Interactive menu with common operations
   ./quick_commands.sh
   
   # Clean previous outputs
   ./clean_output.sh
   
   # Run comprehensive tests
   ./test.sh
   ```

3. **Generate Dataset - Small Batch**
   ```bash
   # Generate 5 images (fast test)
   /Applications/Blender.app/Contents/MacOS/Blender \
     --background --python scripts/main.py -- \
     --count 5 --dict data/dict.txt --samples 32
   ```

4. **Generate Dataset - Production**
   ```bash
   # Generate 100+ images with high quality
   /Applications/Blender.app/Contents/MacOS/Blender \
     --background --python scripts/main.py -- \
     --count 100 --dict data/dict.txt \
     --samples 64 --resolution 1024 512
   ```

5. **Check Results**
   ```bash
   ls output/images/    # Generated PNG images
   ls output/labels/    # Corresponding text files
   ```

## 🎨 Generated Image Examples

The tool creates realistic variations including:

- **Multiple Camera Angles**: Frontal, angled, elevated views
- **Lighting Variations**: Different shadow patterns and highlights on debossed text  
- **Material Diversity**: Blue, gray, green, red cylinders with varying surface finishes
- **Text Positioning**: Randomized vertical placement on cylinder surface
- **Deboss Depth**: Subtle variations in stamping depth for realism
- **FreesiaUPC Font**: Clear, readable Thai-style font optimized for numeric patterns

Sample naming: `6302-844353_001.png`, `2417-001227_045.png`

## 🛠️ Utility Scripts

### Development Tools

```bash
# Interactive development menu
./quick_commands.sh

# Clean all generated outputs
./clean_output.sh

# Run comprehensive test suite
./test.sh
```

### Quick Commands Menu Options:
1. 🧪 Run tests (validation and benchmarking)
2. 🧹 Clean output (remove all generated files)
3. 📊 Show current status (system and generation stats)
4. 🎯 Generate small batch (5 images - quick test)
5. 🎯 Generate medium batch (20 images)
6. 🎯 Generate large batch (100 images)
7. 🔍 Preview latest generated images
8. 📈 Show generation statistics
9. 🚀 Custom generation (user-defined parameters)

## ⚙️ Configuration Options

### Command Line Arguments

```bash
--count INT           # Number of images to generate (default: 100)
--dict PATH          # Path to text dictionary file (required)
--output PATH        # Output directory (default: output/)
--resolution W H     # Image dimensions (default: 512 256)
--samples INT        # Render quality samples (default: 64)
--seed INT           # Random seed for reproducibility
--font-dir PATH      # Directory containing custom fonts (default: fonts/)
--font-style STR     # Font style preference: industrial, monospace, default
```

### Randomization Parameters

- **Camera Position**: 360° azimuth, ±30° elevation
- **Lighting**: 2-3 randomized light sources with varying intensity
- **Text Placement**: Middle 60% of cylinder height
- **Cylinder Dimensions**: Increased radius by 50% (Small: 0.6, Medium: 0.8, Large: 1.0, Industrial: 1.2)
- **Surface Texture**: Mild noise-based bump mapping with 0.1 strength for realistic industrial surface
- **Deboss Depth**: 0.001-0.005 Blender units
- **Material**: Fixed glossy teal-green (#30877b) with low roughness (0.1) and high metallic (0.8) for reflective appearance
- **Lighting**: Balanced environment lighting with gradient background, ambient fill, and adjusted distances for larger cylinders
- **Camera Positioning**: Increased distance range (4.0-8.0) to accommodate larger cylinder dimensions

## 📊 Dataset Specifications

### Image Properties
- **Format**: PNG with transparency support
- **Resolution**: Configurable (recommended: 512×256 or 1024×512)
- **Quality**: High-quality Cycles renders suitable for OCR training
- **Background**: Neutral studio environment

### Ground Truth Format
- **File Extension**: `.txt`
- **Content**: Exact text string from original dictionary
- **Encoding**: UTF-8
- **Naming**: Matches corresponding image filename

## 🔧 Development

### Development Environment Setup

```bash
# Activate virtual environment
source venv/bin/activate

# Install development dependencies (if needed)
pip install --upgrade pip

# Run all tests before development
./test.sh

# Clean outputs for fresh start
./clean_output.sh
```

### Adding New Features

1. **Material Customization**: Modify `cylinder_generator.py` to adjust teal-green color, surface texture, roughness, and metallic properties
2. **Surface Texture Control**: Adjust noise texture parameters (scale, detail, roughness, distortion) and bump strength for surface variations
3. **Cylinder Dimensions**: Modify radius values in cylinder_configs for different size requirements
4. **Lighting Enhancements**: Update `lighting_camera.py` to adjust environment lighting, ambient fill, and lighting distances
5. **Camera Positioning**: Adjust camera distance ranges to accommodate different cylinder sizes
6. **Text Effects**: Extend `text_embosser.py` for different stamping styles
7. **Scene Variations**: Update camera positioning and lighting setups
8. **New Fonts**: Add font files to appropriate `fonts/` subdirectories
9. **Environment Control**: Modify gradient environment or add HDRI support in lighting setup
10. **Testing**: Always run `./test.sh` after changes
11. **Documentation**: Update README.md when adding new features

## 📈 Performance Notes

- **Rendering Speed**: ~5-15 seconds per image (depends on quality settings and system)
- **Memory Usage**: ~2-4GB RAM for standard scenes
- **GPU Acceleration**: Supports CUDA/OpenCL for faster rendering (if available)
- **Batch Processing**: Designed for unattended generation of large datasets
- **Sample Quality**: 16 samples = fast preview, 32 = balanced, 64+ = high quality
- **Resolution Impact**: 256x128 = 2x faster than 512x256, 4x faster than 1024x512

### Benchmarking Results

The included `test.sh` script provides performance benchmarking:
- **5 images @ 256x128, 16 samples**: ~30-60 seconds total
- **Acceptable performance**: < 60s for 5 images
- **Good performance**: < 30s for 5 images

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-capability`)
3. Commit changes (`git commit -am 'Add new capability'`)
4. Push to branch (`git push origin feature/new-capability`)
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Blender Foundation** for the amazing open-source 3D software
- **OCR Research Community** for inspiration on synthetic data generation
- **Industrial Design References** for realistic gas cylinder modeling

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/NopphadonRK/generate_gastank_stamping_text_img/issues)
- **Discussions**: [GitHub Discussions](https://github.com/NopphadonRK/generate_gastank_stamping_text_img/discussions)
- **Documentation**: [Wiki](https://github.com/NopphadonRK/generate_gastank_stamping_text_img/wiki)

---

**Generated with ❤️ for the OCR and Computer Vision community**
