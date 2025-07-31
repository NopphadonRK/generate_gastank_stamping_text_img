#!/bin/bash
# Lighting GUI Launcher
# Simple script to run the lighting control GUI

echo "🎛️  Starting Gas Tank Lighting Control GUI..."

cd "$(dirname "$0")"

# Check if tkinter is available
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: tkinter not found. Please install python3-tk"
    echo "   On macOS: brew install python-tk"
    echo "   On Ubuntu: sudo apt-get install python3-tk"
    exit 1
fi

# Run the GUI
python3 scripts/lighting_gui.py

echo "GUI closed."
