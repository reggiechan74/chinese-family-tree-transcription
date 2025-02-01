#!/usr/bin/env python3
"""
Main entry point for the Chinese Family Tree Processing System.
"""
import os
import sys
import time
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Load environment variables from .env file
project_root = Path(current_dir).parent
env_path = project_root / '.env'
env_example_path = project_root / '.env.example'

if not env_path.exists():
    print("\n=== Environment Setup Required ===")
    print("1. Create a .env file in the project root:")
    print(f"   cp {env_example_path} {env_path}")
    print("\n2. Configure your environment:")
    print("   - Copy .env.example to .env")
    print("   - Follow the provider setup instructions in .env.example")
    print("   - Add your API keys to the .env file")
    print("\nSee .env.example for complete configuration details.")
    sys.exit(1)

load_dotenv(env_path)

from models import ModelManager
from utils import TokenTracker, load_image

def process_image(image_path: str, token_tracking: bool = None, realtime_display: bool = None, save_report: bool = None) -> float:
    """
    Process a single family tree image through all stages.
    
    Args:
        image_path: Path to the image file
        token_tracking: Override TOKEN_TRACKING_ENABLED env var
        realtime_display: Override DISPLAY_REALTIME_USAGE env var
        save_report: Override SAVE_USAGE_REPORT env var
        
    Returns:
        float: Total processing time in seconds
    """
    # Set environment variables if provided
    if token_tracking is not None:
        os.environ['TOKEN_TRACKING_ENABLED'] = str(token_tracking).lower()
    if realtime_display is not None:
        os.environ['DISPLAY_REALTIME_USAGE'] = str(realtime_display).lower()
    if save_report is not None:
        os.environ['SAVE_USAGE_REPORT'] = str(save_report).lower()
    
    # Initialize components
    token_tracker = TokenTracker()
    
    # Start timing
    start_time = time.time()
    
    try:
        # Load and encode image
        print("\n=== Loading Image ===")
        image_base64 = load_image(image_path)
        print("- Image loaded and encoded successfully")
        
        # Initialize model manager
        manager = ModelManager()
        
        # Create output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(current_dir, "output", f"run_{timestamp}")
        manager.initialize_run(output_dir)
        
        # Process image through all stages
        result = manager.process_image(
            image_base64=image_base64,
            token_tracker=token_tracker
        )
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Print processing time
        print(f"\n=== Processing Time ===")
        print(f"Total time: {processing_time:.2f} seconds")
        
        # Print token usage summary
        print("\n=== Token Usage Summary ===")
        token_tracker.print_summary()
        
        return processing_time
        
    except Exception as e:
        print("\n=== Error Summary ===")
        
        # Check if it's an authentication error
        error_str = str(e)
        if "API key" in error_str or "Authentication" in error_str:
            print("\nAuthentication Error:")
            print("1. Create a .env file in the project root")
            print("2. Add your API keys following the template in .env.example")
            print("\nAuthentication Error:")
            print("1. Check .env.example for required API keys")
            print("2. Verify your API keys are correctly configured")
            print("\nError details: Authentication failed. Please check your configuration.")
        else:
            # For non-authentication errors, show the error message without sensitive details
            sanitized_error = error_str.replace(os.path.expanduser("~"), "HOME")
            for key in os.environ:
                if "API" in key or "KEY" in key:
                    sanitized_error = sanitized_error.replace(os.environ[key], "[REDACTED]")
            print(f"\nError: {sanitized_error}")
        
        # Print token usage summary before exiting
        print("\n=== Token Usage Summary ===")
        token_tracker.print_summary()
        # Re-raise the exception to preserve the stack trace
        raise

def main():
    parser = argparse.ArgumentParser(
        description='Process Chinese family tree images.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Token Tracking Options:
  By default, token tracking settings are read from environment variables.
  Use these flags to override the environment settings:

  --no-tracking        Disable all token tracking
  --no-display        Hide realtime token usage during processing
  --no-report         Skip saving token usage report
  
  Or enable specific features:
  --tracking          Enable token tracking
  --display          Show realtime token usage
  --report           Save token usage report

Environment Variables (if flags not specified):
  TOKEN_TRACKING_ENABLED    Set to 'false' to disable all token tracking
  DISPLAY_REALTIME_USAGE   Set to 'false' to hide realtime usage
  SAVE_USAGE_REPORT        Set to 'false' to skip saving report
"""
    )
    
    parser.add_argument('image_path', help='Path to the image file to process')
    
    # Token tracking flags
    tracking_group = parser.add_mutually_exclusive_group()
    tracking_group.add_argument('--tracking', action='store_true',
                              help='Enable token tracking')
    tracking_group.add_argument('--no-tracking', action='store_true',
                              help='Disable token tracking')
    
    display_group = parser.add_mutually_exclusive_group()
    display_group.add_argument('--display', action='store_true',
                             help='Show realtime token usage')
    display_group.add_argument('--no-display', action='store_true',
                             help='Hide realtime token usage')
    
    report_group = parser.add_mutually_exclusive_group()
    report_group.add_argument('--report', action='store_true',
                            help='Save token usage report')
    report_group.add_argument('--no-report', action='store_true',
                            help='Skip saving token usage report')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.image_path):
        print(f"Error: Image file not found: {args.image_path}")
        sys.exit(1)
    
    # Convert flags to boolean values for process_image
    token_tracking = True if args.tracking else False if args.no_tracking else None
    realtime_display = True if args.display else False if args.no_display else None
    save_report = True if args.report else False if args.no_report else None
    
    process_image(
        args.image_path,
        token_tracking=token_tracking,
        realtime_display=realtime_display,
        save_report=save_report
    )

if __name__ == '__main__':
    main()
