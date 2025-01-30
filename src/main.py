#!/usr/bin/env python3
"""
Main entry point for the Chinese Family Tree Processing System.
"""
import os
import sys
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
    print("\n2. Add your API keys to the .env file:")
    print("   - Get OpenAI API key from: https://platform.openai.com/api-keys")
    print("   - Get Anthropic API key from: https://console.anthropic.com/account/keys")
    print("   - Get Google API key from: https://makersuite.google.com/app/apikey")
    print("\nSee .env.example for all available configuration options.")
    sys.exit(1)

load_dotenv(env_path)

from models import ModelManager
from utils import TokenTracker, load_image, encode_image_for_vision_models

def process_image(image_path: str, token_tracking: bool = None, realtime_display: bool = None, save_report: bool = None):
    """
    Process a single family tree image through all stages.
    
    Args:
        image_path: Path to the image file
        token_tracking: Override TOKEN_TRACKING_ENABLED env var
        realtime_display: Override DISPLAY_REALTIME_USAGE env var
        save_report: Override SAVE_USAGE_REPORT env var
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
    
    try:
        # Load and preprocess image
        print("\n=== Loading and preprocessing image ===")
        image = load_image(image_path)
        encoded_image = encode_image_for_vision_models(image)
        
        # Initialize model manager
        manager = ModelManager()
        
        # Process image through all stages
        result = manager.process_image(
            image=encoded_image,
            token_tracker=token_tracker
        )
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        output_dir = os.path.join(current_dir, 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        # Save results
        output_base = os.path.join(output_dir, f"transcription_{image_name}_{timestamp}")
        result_path = f"{output_base}.md"
        interim_path = f"{output_base}_interim_analysis.md"
        token_path = f"{output_base}_token_usage.json"
        
        # Format final results as markdown
        markdown_content = "# Chinese Family Tree Transcription Results\n\n"
        
        # Add each stage's result
        if "Stage 5 Final Transcription" in result:
            markdown_content += "## Original Text\n" + result["Stage 5 Final Transcription"] + "\n\n"
        
        if "Stage 6 Punctuated Final Transcription" in result:
            markdown_content += "## Punctuated Text\n" + result["Stage 6 Punctuated Final Transcription"] + "\n\n"
        
        if "Stage 7 English Translation" in result:
            markdown_content += "## English Translation\n" + result["Stage 7 English Translation"] + "\n\n"
        
        if "Stage 8 Historical Commentary" in result:
            markdown_content += "## Historical Commentary\n" + result["Stage 8 Historical Commentary"] + "\n\n"
        
        # Format interim analysis as markdown
        interim_content = "# Chinese Family Tree Analysis Process\n\n"
        
        # Add Stage 1 transcriptions
        interim_content += "## Stage 1: Initial Transcriptions\n\n"
        for i in range(1, 4):  # LLM1-3
            key = f"LLM{i}'s Stage 1 transcription"
            if key in result:
                interim_content += f"### LLM{i}'s Initial Transcription\n" + result[key] + "\n\n"
        
        # Add Stage 2 transcriptions
        interim_content += "## Stage 2: Secondary Transcriptions\n\n"
        for i in range(1, 4):  # LLM1-3
            key = f"LLM{i}'s Stage 2 transcription"
            if key in result:
                interim_content += f"### LLM{i}'s Secondary Transcription\n" + result[key] + "\n\n"
        
        # Add Stage 3 analyses
        interim_content += "## Stage 3: Analysis and Recommendations\n\n"
        for i in range(1, 4):  # LLM1-3
            key = f"LLM{i}'s Stage 3 Analysis and Recommendation"
            if key in result:
                interim_content += f"### LLM{i}'s Analysis\n" + result[key] + "\n\n"
        
        # Add Stage 4 reviews
        interim_content += "## Stage 4: Comprehensive Reviews\n\n"
        for i in range(1, 4):  # LLM1-3
            key = f"LLM{i}'s Stage 4 Comprehensive Review"
            if key in result:
                interim_content += f"### LLM{i}'s Review\n" + result[key] + "\n\n"
        
        # Write both formatted results
        with open(result_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
            
        with open(interim_path, 'w', encoding='utf-8') as f:
            f.write(interim_content)
        
        # Save token usage
        token_tracker.save_to_file(token_path)
        
        # Print summary
        print(f"\nProcessing complete!")
        print(f"Final results saved to: {result_path}")
        print(f"Interim analysis saved to: {interim_path}")
        print(f"Token usage saved to: {token_path}")
        token_tracker.print_summary()
        
    except Exception as e:
        print("\n=== Error Summary ===")
        
        # Check if it's an API key error
        error_str = str(e)
        if "API key" in error_str and "environment variable" in error_str:
            print("\nAPI Key Error:")
            print("1. Create a .env file in the project root")
            print("2. Add your API key to the .env file:")
            if "OPENAI_API_KEY" in error_str:
                print("   OPENAI_API_KEY=your-api-key-here")
                print("   Get your API key from: https://platform.openai.com/api-keys")
            elif "ANTHROPIC_API_KEY" in error_str:
                print("   ANTHROPIC_API_KEY=your-api-key-here")
                print("   Get your API key from: https://console.anthropic.com/account/keys")
            elif "GOOGLE_API_KEY" in error_str:
                print("   GOOGLE_API_KEY=your-api-key-here")
                print("   Get your API key from: https://makersuite.google.com/app/apikey")
            print("\nFull error message:")
        
        print(error_str)
        
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
