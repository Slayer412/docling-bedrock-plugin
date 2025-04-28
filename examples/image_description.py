#!/usr/bin/env python3
"""
Simple example script showing how to generate descriptions for images 
using AWS Bedrock through the docling-bedrock-plugin.

Usage:
    python image_description.py /path/to/your/image.jpg
"""

import sys
import logging
from pathlib import Path
from PIL import Image

# Set up logging
logging.basicConfig(level=logging.INFO)
_log = logging.getLogger(__name__)

# Import the Bedrock plugin components
from docling.datamodel.pipeline_options import AcceleratorOptions
from docling_bedrock_plugin.pipeline_options import PictureDescriptionBedrockApiOptions
from docling_bedrock_plugin.picture_description_model import PictureDescriptionBedrockApiModel


def describe_image(image_path: Path) -> str:
    """
    Generate a description for an image using AWS Bedrock.
    
    Args:
        image_path: Path to the image file to describe
        
    Returns:
        The generated description as a string, or an error message
    """
    # Configure AWS Bedrock options
    bedrock_options = PictureDescriptionBedrockApiOptions(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",  # Choose your preferred model
        # region_name="us-east-1",  # Uncomment and set if needed
        prompt="Describe this image concisely. Include main visual elements and context.",
        max_tokens=250,
        temperature=0.3,
    )
    
    try:
        # Initialize the Bedrock model
        _log.info(f"Initializing Bedrock model...")
        bedrock_model = PictureDescriptionBedrockApiModel(
            enabled=True,
            enable_remote_services=True,
            artifacts_path=None,
            options=bedrock_options,
            accelerator_options=AcceleratorOptions(),
        )
        
        # Load the image
        _log.info(f"Loading image: {image_path}")
        img = Image.open(image_path)
        
        # Process the image
        _log.info(f"Sending image to AWS Bedrock for description...")
        results = list(bedrock_model._annotate_images([img]))
        
        if results and len(results) > 0:
            description = results[0]
            _log.info(f"Generated description successfully")
            return description
        else:
            return "No description was generated"
            
    except Exception as e:
        _log.error(f"Error generating description: {e}")
        return f"Error: {str(e)}"


def main():
    """Main entry point function."""
    # Check for input image path
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} /path/to/image.[jpg|png|etc]")
        sys.exit(1)
    
    # Get input image path
    image_path = Path(sys.argv[1])
    if not image_path.exists():
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)
    
    # Generate description
    description = describe_image(image_path)
    
    # Print the result
    print("\n" + "="*80)
    print("IMAGE DESCRIPTION FROM AWS BEDROCK")
    print("="*80)
    print(description)
    print("="*80 + "\n")


if __name__ == "__main__":
    main() 