"""Configuration options specifically for using AWS Bedrock API for image description."""
from typing import ClassVar, Literal, Optional, Dict, Any
from docling.datamodel.pipeline_options import PictureDescriptionBaseOptions


class PictureDescriptionBedrockApiOptions(PictureDescriptionBaseOptions):
    """AWS Bedrock API specific options for the picture description model.

    Inherits from PictureDescriptionBaseOptions and adds Bedrock-specific
    configuration parameters for model selection, AWS connection, concurrency,
    and inference.

    Attributes:
        kind: Identifier for this option type.
        model_id: The specific AWS Bedrock model ID to use (e.g., 'anthropic.claude-3-sonnet-20240229-v1:0').
        region_name: Optional AWS region name. If None, uses boto3 default configuration.
        profile_name: Optional AWS profile name from credentials file. If None, uses boto3 default.
        timeout: Timeout in seconds for API requests.
        max_workers: Maximum number of concurrent API calls for processing images.
        temperature: Controls randomness in generation (0.0-1.0). Lower is more deterministic.
        max_tokens: Maximum number of tokens to generate in the description.
        top_k: Top-k filtering parameter for generation.
        prompt: The prompt template used to instruct the Bedrock model.
        provenance: Identifier indicating the source of the description (e.g., 'amazon-bedrock').
    """
    kind: ClassVar[Literal["bedrock_api"]] = "bedrock_api"

    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    region_name: Optional[str] = None
    profile_name: Optional[str] = None
    timeout: float = 30

    # Concurrency control
    max_workers: int = 3  # Default number of concurrent requests

    # Inference parameters
    temperature: float = 0.5
    max_tokens: int = 200
    top_k: int = 250

    prompt: str = "Describe this image in a few sentences."
    provenance: str = "amazon-bedrock"
