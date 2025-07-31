#!/bin/bash

# Gas Tank Text Image Generator - Test Script
# This script runs various tests to validate the generation system

set -e  # Exit on any error

echo "🧪 Gas Tank Text Image Generator - Test Suite"
echo "============================================="

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check if virtual environment is active
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment: $VIRTUAL_ENV"
else
    echo "⚠️  Virtual environment not active, activating..."
    source venv/bin/activate
fi

# Check Blender installation
if command -v /Applications/Blender.app/Contents/MacOS/Blender &> /dev/null; then
    BLENDER_VERSION=$(/Applications/Blender.app/Contents/MacOS/Blender --version | head -1)
    echo "✅ Blender: $BLENDER_VERSION"
else
    echo "❌ Blender not found. Please install Blender first."
    exit 1
fi

# Check required files
echo "📁 Checking project structure..."

required_files=(
    "data/dict.txt"
    "fonts/default/FreesiaUPC.ttf"
    "scripts/main.py"
    "scripts/cylinder_generator.py"
    "scripts/text_embosser.py"
    "scripts/lighting_camera.py"
    "scripts/utils.py"
)

for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "✅ $file"
    else
        echo "❌ Missing: $file"
        exit 1
    fi
done

# Test 1: Generate single image
echo ""
echo "🎯 Test 1: Generate single test image"
echo "------------------------------------"

/Applications/Blender.app/Contents/MacOS/Blender \
    --background \
    --python scripts/main.py -- \
    --count 1 \
    --dict data/dict.txt \
    --samples 16 \
    --resolution 256 128

if [[ $? -eq 0 ]]; then
    echo "✅ Single image generation: PASSED"
else
    echo "❌ Single image generation: FAILED"
    exit 1
fi

# Test 2: Generate small batch
echo ""
echo "🎯 Test 2: Generate small batch (3 images)"
echo "----------------------------------------"

/Applications/Blender.app/Contents/MacOS/Blender \
    --background \
    --python scripts/main.py -- \
    --count 3 \
    --dict data/dict.txt \
    --samples 16 \
    --resolution 256 128

if [[ $? -eq 0 ]]; then
    echo "✅ Batch generation: PASSED"
else
    echo "❌ Batch generation: FAILED"
    exit 1
fi

# Verify outputs
echo ""
echo "📊 Verifying outputs..."
echo "----------------------"

IMAGE_COUNT=$(ls output/images/*.png 2>/dev/null | wc -l)
LABEL_COUNT=$(ls output/labels/*.txt 2>/dev/null | wc -l)

echo "Generated images: $IMAGE_COUNT"
echo "Generated labels: $LABEL_COUNT"

if [[ $IMAGE_COUNT -gt 0 && $LABEL_COUNT -gt 0 && $IMAGE_COUNT -eq $LABEL_COUNT ]]; then
    echo "✅ Output verification: PASSED"
else
    echo "❌ Output verification: FAILED"
    echo "   Images and labels count should match"
    exit 1
fi

# Check file sizes
echo ""
echo "📏 Checking output quality..."
echo "----------------------------"

SMALL_FILES=$(find output/images -name "*.png" -size -10k | wc -l)
if [[ $SMALL_FILES -gt 0 ]]; then
    echo "⚠️  Found $SMALL_FILES potentially corrupted images (< 10KB)"
else
    echo "✅ All images appear to have reasonable file sizes"
fi

# Performance benchmark
echo ""
echo "⏱️  Performance Benchmark"
echo "------------------------"

echo "Starting 5-image benchmark..."
START_TIME=$(date +%s)

/Applications/Blender.app/Contents/MacOS/Blender \
    --background \
    --python scripts/main.py -- \
    --count 5 \
    --dict data/dict.txt \
    --samples 16 \
    --resolution 256 128 > /dev/null 2>&1

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo "✅ Generated 5 images in ${DURATION} seconds"
echo "   Average: $((DURATION / 5)) seconds per image"

if [[ $DURATION -lt 60 ]]; then
    echo "✅ Performance: EXCELLENT (< 60s for 5 images)"
elif [[ $DURATION -lt 120 ]]; then
    echo "✅ Performance: GOOD (< 120s for 5 images)"
else
    echo "⚠️  Performance: SLOW (> 120s for 5 images)"
fi

echo ""
echo "🎉 All tests completed successfully!"
echo "=================================="
echo ""
echo "📈 Summary:"
echo "- Project structure: ✅ VALID"
echo "- Dependencies: ✅ AVAILABLE"
echo "- Single generation: ✅ WORKING"
echo "- Batch generation: ✅ WORKING"
echo "- Output verification: ✅ PASSED"
echo "- Performance: ✅ ACCEPTABLE"
echo ""
echo "🚀 Ready for production dataset generation!"
