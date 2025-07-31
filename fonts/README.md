# Font Directory Structure

This directory contains fonts used for generating debossed text on gas cylinders.

## Directory Organization

### `industrial/`
Industrial-style fonts suitable for gas tank markings:
- Bold, sans-serif fonts
- High legibility fonts
- Professional industrial typefaces
- Recommended: Arial Bold, Helvetica Bold, Roboto Bold

### `monospace/`
Monospaced fonts for uniform character spacing:
- Courier New
- Monaco
- Consolas
- Source Code Pro
- Useful for serial numbers and codes

### `default/`
Backup fonts and system defaults:
- **FreesiaUPC.ttf**: Thai-style font (included)
- **FreesiabUPC.ttf**: FreesiaUPC Bold version (included)
- Fallback fonts when custom fonts are unavailable
- System-installed fonts
- Blender's default "Bfont"

## Included Fonts

### FreesiaUPC Font Family
The project includes FreesiaUPC fonts which are excellent for industrial stamping:
- **FreesiaUPC Regular**: Clear, readable characters suitable for gas tank markings
- **FreesiaUPC Bold**: Heavier weight for more pronounced stamping effects
- **Character Support**: Numbers (0-9) and hyphens (-) perfect for pattern xxxx-xxxxxx

## Font Installation

1. **Add Custom Fonts**:
   ```bash
   # Copy your .ttf or .otf files to appropriate directories
   cp /path/to/arial-bold.ttf fonts/industrial/
   cp /path/to/courier-new.ttf fonts/monospace/
   ```

2. **Font Requirements**:
   - Supported formats: .ttf, .otf, .woff
   - Clear, high-contrast fonts work best
   - Avoid overly decorative or thin fonts
   - Industrial/technical aesthetics preferred

3. **Font Selection Logic**:
   - The script will randomly select fonts from the specified directory
   - If no custom fonts are found, Blender's default font is used
   - Different font styles create variation in the training dataset

## Notes

- Font licensing: Ensure you have proper licenses for commercial fonts
- Free alternatives: Google Fonts offers many suitable open-source options
- Testing: Preview fonts in Blender before batch generation
- Performance: Too many fonts may slow down the generation process
