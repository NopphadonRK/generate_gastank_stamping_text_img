#!/bin/bash

# Clean Output Script - Force remove all generated images and labels
# This script cleans up the output directory while preserving the structure

set -e  # Exit on any error

echo "🧹 Gas Tank Dataset - Clean Output"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if output directories exist
if [[ ! -d "output" ]]; then
    echo -e "${YELLOW}⚠️  Output directory doesn't exist${NC}"
    exit 0
fi

echo "📂 Current output status:"
echo "------------------------"

# Count current files
IMAGE_COUNT=$(find output/images -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" 2>/dev/null | wc -l)
LABEL_COUNT=$(find output/labels -name "*.txt" 2>/dev/null | wc -l)

echo "Images found: $IMAGE_COUNT"
echo "Labels found: $LABEL_COUNT"

if [[ $IMAGE_COUNT -eq 0 && $LABEL_COUNT -eq 0 ]]; then
    echo -e "${GREEN}✅ Output directories are already clean${NC}"
    exit 0
fi

# Prompt for confirmation
echo ""
echo -e "${YELLOW}⚠️  This will permanently delete ALL generated files:${NC}"
echo "   - All PNG/JPG images in output/images/"
echo "   - All TXT labels in output/labels/"
echo ""
read -p "Are you sure you want to continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Operation cancelled."
    exit 0
fi

echo ""
echo "🗑️  Cleaning output directories..."
echo "--------------------------------"

# Remove all image files (force delete)
if [[ -d "output/images" ]]; then
    echo "Removing image files..."
    find output/images -name "*.png" -delete 2>/dev/null || true
    find output/images -name "*.jpg" -delete 2>/dev/null || true
    find output/images -name "*.jpeg" -delete 2>/dev/null || true
    echo "✅ Images cleaned"
fi

# Remove all label files (force delete)
if [[ -d "output/labels" ]]; then
    echo "Removing label files..."
    find output/labels -name "*.txt" -delete 2>/dev/null || true
    echo "✅ Labels cleaned"
fi

# Verify cleanup
echo ""
echo "📊 Cleanup verification:"
echo "-----------------------"

REMAINING_IMAGES=$(find output/images -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" 2>/dev/null | wc -l)
REMAINING_LABELS=$(find output/labels -name "*.txt" 2>/dev/null | wc -l)

echo "Remaining images: $REMAINING_IMAGES"
echo "Remaining labels: $REMAINING_LABELS"

if [[ $REMAINING_IMAGES -eq 0 && $REMAINING_LABELS -eq 0 ]]; then
    echo -e "${GREEN}✅ Cleanup completed successfully!${NC}"
else
    echo -e "${RED}❌ Some files may not have been deleted${NC}"
    echo "You may need to check permissions or delete manually."
    exit 1
fi

# Show preserved structure
echo ""
echo "📁 Preserved directory structure:"
echo "--------------------------------"
ls -la output/ 2>/dev/null || echo "No output directory structure"

echo ""
echo -e "${GREEN}🎉 Output cleanup completed!${NC}"
echo "Ready for fresh dataset generation."
