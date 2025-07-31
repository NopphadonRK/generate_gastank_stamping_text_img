# Gas Tank Stamping Text Image Generator

A Python-based tool using Blender 3D to generate synthetic datasets of debossed/stamped text on gas cylinder surfaces for OCR model training.

## 🎯 Project Overview

This project creates realistic 3D rendered images of industrial gas cylinders with debossed text markings. The generated dataset is specifically designed for training OCR models to recognize stamped text on curved metallic surfaces under various lighting conditions.

## ✨ Features

- **Realistic 3D Gas Cylinder Models**: Procedurally generated with proper proportions
- **Authentic Debossing Effects**: Text appears physically stamped into the metal surface
- **Dynamic Lighting**: Randomized lighting setups create realistic shadows and highlights
- **Camera Variations**: Multiple viewing angles and perspectives per text sample
- **Material Randomization**: Various metallic and plastic finishes with industrial color schemes
- **Batch Processing**: Automated generation of thousands of training images
- **Ground Truth Generation**: Automatic creation of corresponding text labels

## 🛠️ Technology Stack

- **Blender 3D**: Main rendering engine with Python API
- **Python 3.8+**: Automation and batch processing
- **bpy (Blender Python API)**: 3D modeling and rendering control
- **PIL/Pillow**: Image post-processing (optional)

## 📁 Project Structure

```
generate_gastank_stamping_text_img/
├── data/
│   └── dict.txt                 # Text strings for stamping
├── fonts/
│   ├── industrial/              # Industrial-style fonts
│   ├── monospace/               # Monospaced fonts for stamps
│   └── default/                 # Default system fonts backup
├── output/
│   ├── images/                  # Generated PNG images
│   └── labels/                  # Ground truth text files
├── scripts/
│   ├── main.py                  # Main execution script
│   ├── cylinder_generator.py    # 3D cylinder model creation
│   ├── text_embosser.py         # Text debossing effects
│   ├── lighting_camera.py       # Scene lighting and camera control
│   └── utils.py                 # Helper utilities
├── requirements.txt             # Python dependencies
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
   pip install -r requirements.txt
   ```

### Basic Usage

1. **Prepare Text Dictionary**
   ```bash
   # Create data/dict.txt with your text samples (one per line)
   echo "ACMEGAS123" > data/dict.txt
   echo "FIREEXT1A" >> data/dict.txt
   echo "GASCO-X7Y" >> data/dict.txt
   ```

2. **Setup Fonts (Optional)**
   ```bash
   # Add industrial fonts to fonts/ directory for realistic stamping
   # Recommended: Arial, Helvetica, Courier New, or similar monospace fonts
   # The system will use default fonts if custom fonts are not provided
   ```

3. **Generate Dataset**
   ```bash
   # Generate 100 images with default settings
   blender --background --python scripts/main.py -- --count 100 --dict data/dict.txt
   
   # Or with custom parameters
   blender --background --python scripts/main.py -- \
     --count 1000 \
     --dict data/dict.txt \
     --output output/ \
     --resolution 1024 512 \
     --font-dir fonts/industrial/
   ```

4. **Check Results**
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

Sample naming: `ACMEGAS123_001.png`, `FIREEXT1A_045.png`

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
- **Deboss Depth**: 0.001-0.005 Blender units
- **Materials**: Industrial color palette with PBR properties

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

### Setting up Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Format code
black scripts/
```

### Adding New Features

1. **Custom Materials**: Modify `cylinder_generator.py` to add new surface materials
2. **Text Effects**: Extend `text_embosser.py` for different stamping styles
3. **Scene Variations**: Update `lighting_camera.py` for new camera/lighting setups

## 📈 Performance Notes

- **Rendering Speed**: ~10-30 seconds per image (depends on quality settings)
- **Memory Usage**: ~2-4GB RAM for standard scenes
- **GPU Acceleration**: Supports CUDA/OpenCL for faster rendering
- **Batch Processing**: Designed for unattended generation of large datasets

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
