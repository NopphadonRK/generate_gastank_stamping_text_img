"""
Utility functions for Gas Tank Stamping Text Image Generator

This module provides helper functions for file I/O, logging, and common operations.

Author: Gas Tank Text Generator Project
Date: July 2025
"""

import os
import logging
from pathlib import Path
from typing import List


def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging configuration for the application."""
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def load_text_dictionary(filepath: str) -> List[str]:
    """
    Load text strings from dictionary file.
    
    Args:
        filepath: Path to the dictionary file (one text string per line)
        
    Returns:
        List of text strings with whitespace stripped
        
    Raises:
        FileNotFoundError: If the dictionary file doesn't exist
        UnicodeDecodeError: If the file contains invalid UTF-8
    """
    
    text_list = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                text = line.strip()
                if text:  # Skip empty lines
                    text_list.append(text)
    except FileNotFoundError:
        raise FileNotFoundError(f"Dictionary file not found: {filepath}")
    except UnicodeDecodeError:
        raise UnicodeDecodeError(f"Invalid UTF-8 encoding in file: {filepath}")
    
    return text_list


def create_output_dirs(output_base: str) -> None:
    """
    Create output directory structure if it doesn't exist.
    
    Args:
        output_base: Base output directory path
    """
    
    dirs_to_create = [
        os.path.join(output_base, 'images'),
        os.path.join(output_base, 'labels')
    ]
    
    for dir_path in dirs_to_create:
        Path(dir_path).mkdir(parents=True, exist_ok=True)


def validate_blender_context() -> bool:
    """
    Validate that we're running within Blender context.
    
    Returns:
        True if running in Blender, False otherwise
    """
    
    try:
        import bpy
        return True
    except ImportError:
        return False


def get_safe_filename(text: str, max_length: int = 50) -> str:
    """
    Convert text to a safe filename by removing/replacing problematic characters.
    
    Args:
        text: Original text string
        max_length: Maximum filename length
        
    Returns:
        Safe filename string
    """
    
    # Replace problematic characters
    safe_chars = []
    for char in text:
        if char.isalnum() or char in '-_':
            safe_chars.append(char)
        elif char in ' /\\:*"<>|':
            safe_chars.append('_')
    
    safe_text = ''.join(safe_chars)
    
    # Truncate if too long
    if len(safe_text) > max_length:
        safe_text = safe_text[:max_length]
    
    return safe_text


def calculate_progress_percentage(current: int, total: int) -> float:
    """
    Calculate progress percentage for batch operations.
    
    Args:
        current: Current item number
        total: Total number of items
        
    Returns:
        Progress percentage (0.0 to 100.0)
    """
    
    if total <= 0:
        return 0.0
    
    return min(100.0, (current / total) * 100.0)


def estimate_remaining_time(elapsed_time: float, current: int, total: int) -> float:
    """
    Estimate remaining time for batch operations.
    
    Args:
        elapsed_time: Time elapsed so far (seconds)
        current: Current item number
        total: Total number of items
        
    Returns:
        Estimated remaining time (seconds)
    """
    
    if current <= 0:
        return 0.0
    
    time_per_item = elapsed_time / current
    remaining_items = total - current
    
    return time_per_item * remaining_items


def format_time_duration(seconds: float) -> str:
    """
    Format time duration in human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted time string (e.g., "2h 30m 45s")
    """
    
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours}h {minutes}m {secs}s"
