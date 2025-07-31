#!/bin/bash

# Gas Tank Dataset Generator - Quick Commands
# Collection of useful commands for dataset management

set -e

echo "🚀 Gas Tank Dataset Generator - Quick Commands"
echo "=============================================="

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if we're in the right directory
if [[ ! -f "scripts/main.py" ]]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Show menu
echo ""
echo -e "${BLUE}Available commands:${NC}"
echo "1. 🧪 Run tests (test.sh)"
echo "2. 🧹 Clean output (clean_output.sh)"
echo "3. 📊 Show current status"
echo "4. 🎯 Generate small batch (5 images)"
echo "5. 🎯 Generate medium batch (20 images)"
echo "6. 🎯 Generate large batch (100 images)"
echo "7. 🔍 Preview latest generated images"
echo "8. 📈 Show generation statistics"
echo "9. 🚀 Custom generation"
echo "0. Exit"

echo ""
read -p "Select option (0-9): " choice

case $choice in
    1)
        echo -e "${GREEN}🧪 Running tests...${NC}"
        ./test.sh
        ;;
    2)
        echo -e "${YELLOW}🧹 Cleaning output...${NC}"
        ./clean_output.sh
        ;;
    3)
        echo -e "${BLUE}📊 Current Status${NC}"
        echo "=================="
        
        if [[ -d "venv" && "$VIRTUAL_ENV" != "" ]]; then
            echo "✅ Virtual environment: Active"
        else
            echo "⚠️  Virtual environment: Not active"
        fi
        
        BLENDER_PATH="/Applications/Blender.app/Contents/MacOS/Blender"
        if [[ -f "$BLENDER_PATH" ]]; then
            BLENDER_VERSION=$($BLENDER_PATH --version | head -1)
            echo "✅ Blender: $BLENDER_VERSION"
        else
            echo "❌ Blender: Not found"
        fi
        
        DICT_LINES=$(wc -l < data/dict.txt)
        echo "📝 Dictionary: $DICT_LINES text strings"
        
        IMAGE_COUNT=$(find output/images -name "*.png" 2>/dev/null | wc -l)
        LABEL_COUNT=$(find output/labels -name "*.txt" 2>/dev/null | wc -l)
        echo "🖼️  Generated images: $IMAGE_COUNT"
        echo "🏷️  Generated labels: $LABEL_COUNT"
        
        if [[ $IMAGE_COUNT -gt 0 ]]; then
            TOTAL_SIZE=$(du -sh output/images/ | cut -f1)
            echo "💾 Total size: $TOTAL_SIZE"
        fi
        ;;
    4)
        echo -e "${GREEN}🎯 Generating 5 images (small batch)...${NC}"
        /Applications/Blender.app/Contents/MacOS/Blender \
            --background --python scripts/main.py -- \
            --count 5 --dict data/dict.txt --samples 32
        ;;
    5)
        echo -e "${GREEN}🎯 Generating 20 images (medium batch)...${NC}"
        /Applications/Blender.app/Contents/MacOS/Blender \
            --background --python scripts/main.py -- \
            --count 20 --dict data/dict.txt --samples 32
        ;;
    6)
        echo -e "${GREEN}🎯 Generating 100 images (large batch)...${NC}"
        echo "This may take 30-60 minutes depending on your system..."
        read -p "Continue? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            /Applications/Blender.app/Contents/MacOS/Blender \
                --background --python scripts/main.py -- \
                --count 100 --dict data/dict.txt --samples 32
        fi
        ;;
    7)
        echo -e "${BLUE}🔍 Latest Generated Images${NC}"
        echo "=========================="
        
        if [[ $(find output/images -name "*.png" | wc -l) -eq 0 ]]; then
            echo "No images found. Generate some first!"
        else
            echo "Latest 5 images:"
            ls -lt output/images/*.png | head -5
            echo ""
            echo "To view images, use:"
            echo "open output/images/"
        fi
        ;;
    8)
        echo -e "${BLUE}📈 Generation Statistics${NC}"
        echo "======================="
        
        if [[ $(find output/images -name "*.png" | wc -l) -eq 0 ]]; then
            echo "No images generated yet."
        else
            IMAGE_COUNT=$(find output/images -name "*.png" | wc -l)
            TOTAL_SIZE=$(du -sh output/images/ | cut -f1)
            AVG_SIZE=$(du -sk output/images/*.png | awk '{sum+=$1} END {print sum/NR}')
            
            echo "Total images: $IMAGE_COUNT"
            echo "Total size: $TOTAL_SIZE"
            echo "Average size: ${AVG_SIZE}KB per image"
            
            # Unique text patterns
            UNIQUE_TEXTS=$(ls output/images/*.png | sed 's/.*\///;s/_[0-9]*\.png//' | sort -u | wc -l)
            echo "Unique text patterns: $UNIQUE_TEXTS"
            
            # Recent generation activity
            echo ""
            echo "Recent generation activity:"
            ls -lt output/images/*.png | head -3
        fi
        ;;
    9)
        echo -e "${BLUE}🚀 Custom Generation${NC}"
        echo "==================="
        
        read -p "Number of images: " count
        read -p "Render samples (16/32/64): " samples
        read -p "Resolution width: " width
        read -p "Resolution height: " height
        
        if [[ $count =~ ^[0-9]+$ ]] && [[ $samples =~ ^[0-9]+$ ]] && [[ $width =~ ^[0-9]+$ ]] && [[ $height =~ ^[0-9]+$ ]]; then
            echo "Generating $count images at ${width}x${height} with $samples samples..."
            /Applications/Blender.app/Contents/MacOS/Blender \
                --background --python scripts/main.py -- \
                --count $count --dict data/dict.txt \
                --samples $samples --resolution $width $height
        else
            echo "Invalid input. Please use numbers only."
        fi
        ;;
    0)
        echo "Goodbye! 👋"
        exit 0
        ;;
    *)
        echo "Invalid option. Please select 0-9."
        ;;
esac

echo ""
echo -e "${GREEN}✅ Command completed!${NC}"
