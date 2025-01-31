"""
Image utility functions for handling and preprocessing images.
"""
import os
import base64
from typing import Dict, Any, Tuple

def encode_image_for_vision_models(image_path: str) -> str:
    """
    Encode an image file to base64 string for vision models.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        str: Base64 encoded image string
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_info(image_path: str) -> Dict[str, Any]:
    """
    Get basic information about an image file.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dict containing:
            - size_bytes: Size of image in bytes
            - size_mb: Size of image in MB
            - format: File extension
    """
    size_bytes = os.path.getsize(image_path)
    return {
        'size_bytes': size_bytes,
        'size_mb': size_bytes / (1024 * 1024),
        'format': os.path.splitext(image_path)[1].lower()[1:]  # Remove the dot
    }

def validate_image(image_path: str) -> Tuple[bool, str]:
    """
    Validate an image file.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    try:
        if not os.path.exists(image_path):
            return False, "Image file not found"
            
        info = get_image_info(image_path)
        
        # Check file size
        if info['size_mb'] > 20:
            return False, f"Image file too large: {info['size_mb']:.1f}MB"
            
        # Check file format
        valid_formats = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
        if info['format'].lower() not in valid_formats:
            return False, f"Unsupported image format: {info['format']}"
            
        # Try to read and encode the file
        try:
            encode_image_for_vision_models(image_path)
        except Exception as e:
            return False, f"Failed to read image file: {str(e)}"
            
        return True, "Image validation passed"
        
    except Exception as e:
        return False, f"Image validation failed: {str(e)}"

def load_image(image_path: str) -> str:
    """
    Load and validate an image file, returning its base64 encoding.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        str: Base64 encoded image string
        
    Raises:
        ValueError: If image validation fails
    """
    # Validate image
    is_valid, message = validate_image(image_path)
    if not is_valid:
        raise ValueError(f"Invalid image: {message}")
        
    # Encode image
    return encode_image_for_vision_models(image_path)
