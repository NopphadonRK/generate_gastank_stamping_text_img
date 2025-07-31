# Output Directory

This directory contains the generated synthetic dataset.

## Structure

### `images/`
Generated PNG images of gas cylinders with debossed text:
- High-quality rendered images suitable for OCR training
- Various camera angles and lighting conditions
- Realistic material and surface properties
- Filename format: `[TEXT_CONTENT]_[VARIANT_ID].png`

### `labels/`
Ground truth text files corresponding to each image:
- Plain text files containing the exact stamped text
- UTF-8 encoding
- One text string per file
- Filename format: `[TEXT_CONTENT]_[VARIANT_ID].txt`

## File Naming Convention

Each image and its corresponding label share the same base filename:
- Image: `ACMEGAS123_001.png`
- Label: `ACMEGAS123_001.txt`

The variant ID allows multiple variations of the same text with different:
- Camera angles
- Lighting conditions
- Material properties
- Text positioning

## Usage

These files are ready for use in OCR model training pipelines:
1. Load images from `images/` directory
2. Read corresponding ground truth from `labels/` directory
3. Use standard computer vision training frameworks (PyTorch, TensorFlow, etc.)

## Quality Assurance

Generated images should be manually reviewed for:
- Text legibility and clarity
- Realistic debossing effects
- Proper lighting and shadows
- Consistent naming and pairing with labels
