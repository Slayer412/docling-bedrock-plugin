#!/usr/bin/env python3
"""
Example script demonstrating how to use the docling-bedrock-plugin to process
documents and generate image descriptions using AWS Bedrock.

Usage:
    python bedrock_image_description.py /path/to/your/document.pdf
    
    # Or for other document types:
    python bedrock_image_description.py /path/to/your/document.docx
    python bedrock_image_description.py /path/to/your/presentation.pptx
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, List
import json
import yaml

# Third-party imports 
import boto3
from dotenv import load_dotenv

# Docling imports
from docling_core.types.doc import DoclingDocument, PictureItem
from docling.datamodel.base_models import (
    InputFormat,
    WordFormatOption,
    PowerpointFormatOption,
)
from docling.datamodel.pipeline_options import AcceleratorOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.simple_pipeline import SimplePipeline
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.backend.msword_backend import MsWordDocumentBackend
from docling.backend.mspowerpoint_backend import MsPowerpointDocumentBackend

# Import the Bedrock plugin
from docling_bedrock_plugin.pipeline_options import (
    PictureDescriptionBedrockApiOptions,
)
from docling_bedrock_plugin.picture_description_model import (
    PictureDescriptionBedrockApiModel,
)
from docling_core.types.doc.document import PictureDescriptionData
from docling_core.types.doc import TextItem, DocItemLabel, RefItem

# Set up logging
logging.basicConfig(level=logging.INFO)
_log = logging.getLogger(__name__)


def add_bedrock_picture_descriptions(
    doc: DoclingDocument,
    bedrock_options: PictureDescriptionBedrockApiOptions,
    enable_remote_services: bool = True,
) -> None:
    """
    Add descriptions to pictures in a DoclingDocument using AWS Bedrock.
    
    Args:
        doc: The DoclingDocument containing pictures to describe
        bedrock_options: Configuration options for the Bedrock API
        enable_remote_services: Whether to allow connection to AWS Bedrock
    """
    if not enable_remote_services:
        _log.warning("Remote services must be enabled to use Bedrock. Skipping.")
        return
    
    _log.info("Initializing Bedrock model for image description...")
    try:
        # Initialize the Bedrock model from the plugin
        bedrock_model = PictureDescriptionBedrockApiModel(
            enabled=True,
            enable_remote_services=enable_remote_services,
            artifacts_path=None,
            options=bedrock_options,
            accelerator_options=AcceleratorOptions(),
        )
    except Exception as e:
        _log.error(f"Failed to initialize Bedrock model: {e}")
        return
    
    _log.info(f"Processing {len(doc.pictures)} images in the document...")
    pictures_to_process = []
    images_to_process = []
    
    # Extract images from the document
    for picture in doc.pictures:
        try:
            img = picture.get_image(doc=doc)
            if img:
                pictures_to_process.append(picture)
                images_to_process.append(img)
            else:
                _log.warning(f"Could not retrieve image for PictureItem {picture.self_ref}")
        except Exception as e:
            _log.error(f"Error getting image: {e}")
    
    if not images_to_process:
        _log.info("No valid images found to process.")
        return
    
    # Process the images using Bedrock
    _log.info(f"Sending {len(images_to_process)} images to Bedrock for description...")
    try:
        results_iterable = bedrock_model._annotate_images(images_to_process)
        descriptions = list(results_iterable)
    except Exception as e:
        _log.error(f"Error during Bedrock image processing: {e}")
        return
    
    # Add the descriptions to the document
    _log.info(f"Adding {len(descriptions)} descriptions to the document...")
    for picture, description in zip(pictures_to_process, descriptions):
        if not description.startswith("Error") and not description.startswith("Unsupported"):
            # Add the description as an annotation
            picture.annotations.append(
                PictureDescriptionData(
                    text=description, 
                    provenance=bedrock_model.provenance
                )
            )
            
            # Add or append to caption for visibility in exports
            caption_ref_list = picture.captions
            description_prefix = "\n\nImage Description: "
            
            if caption_ref_list:
                # Append to existing caption
                caption_item_ref = caption_ref_list[0].ref
                caption_item = next((t for t in doc.texts if t.self_ref == caption_item_ref), None)
                if isinstance(caption_item, TextItem):
                    caption_item.text += description_prefix + description
            else:
                # Create a new caption
                parent_ref = picture.parent.cref if picture.parent else None
                parent_item = doc.body  # Default to document body
                
                # Try to find the parent item
                if parent_ref:
                    parent_item = next((t for t in doc.texts if t.self_ref == parent_ref), None)
                    if parent_item is None:
                        parent_item = next((g for g in doc.groups if g.self_ref == parent_ref), None)
                    if parent_item is None:
                        parent_item = doc.body
                
                # Create the caption
                new_caption_item = doc.add_text(
                    text=description_prefix.strip() + description,
                    label=DocItemLabel.CAPTION,
                    parent=parent_item,
                )
                
                # Link the caption to the picture
                if new_caption_item:
                    picture.captions.append(RefItem(cref=new_caption_item.self_ref))
    
    _log.info("Completed Bedrock image description processing")


def process_document(input_path: Path, output_dir: Path) -> None:
    """Process a document and generate image descriptions using AWS Bedrock."""
    
    # Load potential environment variables from .env file
    load_dotenv()
    
    # Configure the document converter
    doc_converter = DocumentConverter(
        allowed_formats=[InputFormat.PDF, InputFormat.DOCX, InputFormat.PPTX],
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_cls=StandardPdfPipeline,
                backend=PyPdfiumDocumentBackend,
            ),
            InputFormat.DOCX: WordFormatOption(
                pipeline_cls=SimplePipeline,
                backend=MsWordDocumentBackend,
            ),
            InputFormat.PPTX: PowerpointFormatOption(
                pipeline_cls=SimplePipeline,
                backend=MsPowerpointDocumentBackend,
            ),
        },
    )
    
    # Configure AWS Bedrock options
    bedrock_options = PictureDescriptionBedrockApiOptions(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",  # Choose your preferred model
        # region_name="us-east-1",  # Uncomment and set if needed
        prompt="Describe this image concisely. Include main visual elements and context.",
        max_tokens=250,
        temperature=0.3,
        max_workers=3,
    )
    
    # Process the document
    _log.info(f"Processing document: {input_path}")
    conv_results = doc_converter.convert_all([input_path])
    conv_result = conv_results[0]  # Get the first result
    
    if conv_result.status != "success":
        _log.error(f"Failed to convert {conv_result.input.file.name}")
        return
    
    _log.info(f"Successfully converted {conv_result.input.file.name}")
    doc = conv_result.document  # This is the DoclingDocument object
    
    # Process images with Bedrock if they exist
    if doc.pictures:
        _log.info(f"Found {len(doc.pictures)} pictures in the document")
        add_bedrock_picture_descriptions(doc, bedrock_options)
    else:
        _log.info("No pictures found in the document")
    
    # Save outputs
    _log.info(f"Saving outputs to {output_dir}")
    
    # Save markdown
    md_path = output_dir / f"{conv_result.input.file.stem}.md"
    with md_path.open("w", encoding="utf-8") as fp:
        fp.write(doc.export_to_markdown())
    _log.info(f"Saved Markdown to: {md_path}")
    
    # Save JSON (includes Bedrock annotations)
    json_path = output_dir / f"{conv_result.input.file.stem}.json"
    with json_path.open("w", encoding="utf-8") as fp:
        fp.write(doc.model_dump_json(indent=2))
    _log.info(f"Saved JSON to: {json_path}")
    
    # Save YAML
    yaml_path = output_dir / f"{conv_result.input.file.stem}.yaml"
    with yaml_path.open("w", encoding="utf-8") as fp:
        yaml.safe_dump(doc.model_dump(mode="json"), fp, allow_unicode=True, indent=2)
    _log.info(f"Saved YAML to: {yaml_path}")


def main():
    """Main entry point function."""
    # Check for input document
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} /path/to/document.[pdf|docx|pptx]")
        sys.exit(1)
    
    # Get input document path
    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)
    
    # Create output directory
    output_dir = Path("./output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process the document
    process_document(input_path, output_dir)
    

if __name__ == "__main__":
    main() 