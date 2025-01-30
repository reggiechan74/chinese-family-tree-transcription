"""Image utility functions for handling and preprocessing images."""

import PIL.Image
import io
import base64
import os
from typing import Union, Tuple, Dict, Any

class ImageUtils:
    """Utility class for image operations."""
    
    @staticmethod
    def validate_format(image_path: str) -> bool:
        """Validate image file format."""
        valid_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp'}
        _, ext = os.path.splitext(image_path.lower())
        return ext in valid_extensions

def encode_image_for_vision_models(image: PIL.Image.Image) -> Dict[str, Any]:
    """
    Encode an image for use with vision models.
    Handles different model requirements (base64, bytes, etc.)
    
    Args:
        image: PIL Image object to encode
        
    Returns:
        Dict containing encoded image in various formats
        
    Raises:
        Exception: If encoding fails
    """
    try:
        return {
            'base64': convert_to_base64(image),
            'bytes': convert_to_bytes(image),
            'pil': image
        }
    except Exception as e:
        raise Exception(f"Error encoding image for vision models: {str(e)}")

def save_image(image: PIL.Image.Image, output_path: str):
    """
    Save an image to a file.
    
    Args:
        image: PIL Image object to save
        output_path: Path where to save the image
        
    Raises:
        Exception: If saving fails
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path)
    except Exception as e:
        raise Exception(f"Error saving image: {str(e)}")

def get_image_info(image: PIL.Image.Image) -> Dict[str, Any]:
    """
    Get information about an image.
    
    Args:
        image: PIL Image object to analyze
        
    Returns:
        Dict containing image information
        
    Raises:
        Exception: If analysis fails
    """
    try:
        return {
            'size': image.size,
            'mode': image.mode,
            'format': image.format,
            'bytes': len(convert_to_bytes(image))
        }
    except Exception as e:
        raise Exception(f"Error getting image info: {str(e)}")

def load_image(image_path: str) -> PIL.Image.Image:
    """
    Load an image from a file path.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        PIL.Image.Image: Loaded image object
        
    Raises:
        Exception: If image loading fails
    """
    try:
        return PIL.Image.open(image_path)
    except Exception as e:
        raise Exception(f"Error loading image: {str(e)}")

def preprocess_image(image: PIL.Image.Image) -> PIL.Image.Image:
    """
    Preprocess an image for optimal OCR performance.
    
    Args:
        image: PIL Image object to preprocess
        
    Returns:
        PIL.Image.Image: Preprocessed image
        
    Raises:
        Exception: If preprocessing fails
    """
    try:
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Ensure reasonable size for OCR
        max_dimension = 4096
        width, height = image.size
        if width > max_dimension or height > max_dimension:
            scale = min(max_dimension/width, max_dimension/height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = image.resize((new_width, new_height), PIL.Image.Resampling.LANCZOS)
        
        return image
    except Exception as e:
        raise Exception(f"Error preprocessing image: {str(e)}")

def validate_image(image: PIL.Image.Image) -> Tuple[bool, str]:
    """
    Validate an image for processing.
    
    Args:
        image: PIL Image object to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, message)
        
    Raises:
        Exception: If validation check fails
    """
    try:
        # Check image mode
        if image.mode not in ['RGB', 'L']:
            return False, f"Unsupported image mode: {image.mode}"
        
        # Check dimensions
        width, height = image.size
        if width < 100 or height < 100:
            return False, f"Image too small: {width}x{height}"
        if width > 10000 or height > 10000:
            return False, f"Image too large: {width}x{height}"
        
        # Check file size
        image_bytes = convert_to_bytes(image)
        size_mb = len(image_bytes) / (1024 * 1024)
        if size_mb > 20:
            return False, f"Image file too large: {size_mb:.1f}MB"
        
        return True, "Image validation passed"
    except Exception as e:
        raise Exception(f"Error validating image: {str(e)}")

def convert_to_bytes(image: PIL.Image.Image) -> bytes:
    """
    Convert a PIL Image to bytes.
    
    Args:
        image: PIL Image object to convert
        
    Returns:
        bytes: Image data as bytes
        
    Raises:
        Exception: If conversion fails
    """
    try:
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=image.format or 'JPEG')
        return img_byte_arr.getvalue()
    except Exception as e:
        raise Exception(f"Error converting image to bytes: {str(e)}")

def convert_to_base64(image: PIL.Image.Image) -> str:
    """
    Convert a PIL Image to base64 string.
    
    Args:
        image: PIL Image object to convert
        
    Returns:
        str: Base64 encoded image string
        
    Raises:
        Exception: If conversion fails
    """
    try:
        # Convert to bytes first
        image_bytes = convert_to_bytes(image)
        
        # Convert bytes to base64
        base64_str = base64.b64encode(image_bytes).decode('utf-8')
        
        return base64_str
    except Exception as e:
        raise Exception(f"Error converting image to base64: {str(e)}")
