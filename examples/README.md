# docling-bedrock-plugin Examples

This directory contains example scripts demonstrating how to use the `docling-bedrock-plugin` to process documents and images with AWS Bedrock.

## Prerequisites

Before running these examples, make sure you have:

1. Installed the plugin:
   - From PyPI: `pip install docling-bedrock-plugin`
   - From local source: `pip install -e /path/to/docling-bedrock-plugin`
2. Configured AWS credentials with access to Bedrock
3. Installed dependencies: `pip install docling boto3 python-dotenv pyyaml pillow`

If you're developing the plugin locally, the source installation method (`pip install -e`) is recommended as it allows you to make changes to the code without reinstalling.

## Available Examples

### 1. Document Processing Example

The [`bedrock_image_description.py`](bedrock_image_description.py) script demonstrates how to:

- Process PDF, Word, or PowerPoint documents with Docling
- Extract images from those documents
- Generate descriptions for those images using AWS Bedrock
- Save the processed document with image descriptions

**Usage:**

```bash
python bedrock_image_description.py /path/to/your/document.pdf
# OR
python bedrock_image_description.py /path/to/your/document.docx
# OR
python bedrock_image_description.py /path/to/your/presentation.pptx
```

The script will:

1. Convert the document to a Docling document
2. Extract images from the document
3. Send each image to AWS Bedrock for description
4. Add the descriptions as annotations to the document
5. Save the processed document as Markdown, JSON, and YAML

### 2. Single Image Processing Example

The [`image_description.py`](image_description.py) script demonstrates a simpler use case - generating a description for a single image directly:

**Usage:**

```bash
python image_description.py /path/to/your/image.jpg
```

This script will:

1. Load the image
2. Send it to AWS Bedrock for description
3. Print the generated description

## AWS Bedrock Models

These examples use the `anthropic.claude-3-sonnet-20240229-v1:0` model by default, but you can change this to any other multimodal model available in AWS Bedrock by modifying the `model_id` parameter.

## AWS Credentials

The examples attempt to load AWS credentials from environment variables or other standard locations used by boto3. You can also create a `.env` file with your credentials:

```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
```

## Customizing the Examples

You can customize various aspects of the examples:

### Bedrock Options Parameters

The `PictureDescriptionBedrockApiOptions` class accepts the following parameters:

| Parameter        | Type        | Description                                                 | Default                |
| ---------------- | ----------- | ----------------------------------------------------------- | ---------------------- |
| `model_id`       | `str`       | AWS Bedrock model ID to use (must be a multimodal model)    | Required               |
| `region_name`    | `str`       | AWS region where Bedrock is available                       | Uses boto3 default     |
| `profile_name`   | `str`       | AWS profile name to use for credentials                     | Uses boto3 default     |
| `prompt`         | `str`       | Prompt text to use when describing images                   | "Describe this image." |
| `max_tokens`     | `int`       | Maximum number of tokens to generate in response            | 300                    |
| `temperature`    | `float`     | Controls randomness in generation (0.0-1.0)                 | 0.7                    |
| `top_p`          | `float`     | Controls diversity via nucleus sampling (0.0-1.0)           | 0.9                    |
| `top_k`          | `int`       | Controls diversity via top-k filtering                      | None                   |
| `max_workers`    | `int`       | Number of concurrent workers for processing multiple images | 3                      |
| `stop_sequences` | `List[str]` | Sequences that stop generation when encountered             | []                     |

Example of customizing these parameters in the scripts:

```python
bedrock_options = PictureDescriptionBedrockApiOptions(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    region_name="us-east-1",                     # Optional: AWS region
    profile_name="my-profile",                   # Optional: AWS profile
    prompt="Describe this image in detail, focusing on main elements and colors.",
    max_tokens=500,                              # Longer descriptions
    temperature=0.3,                             # More deterministic output
    top_p=0.95,                                  # Slightly more diverse output
    max_workers=5,                               # Process 5 images concurrently
)
```

Other customization options:

- Change the AWS Bedrock model by modifying the `model_id` parameter
- Adjust generation parameters like `max_tokens` and `temperature`
- Customize the prompt used to generate descriptions
- Modify how descriptions are added to the document

## Error Handling

The examples include basic error handling and logging. If you encounter issues:

1. Check if your AWS credentials are correctly configured
2. Verify that you have access to the AWS Bedrock model being used
3. Ensure you have installed all the required dependencies
