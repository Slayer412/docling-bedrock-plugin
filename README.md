# docling-bedrock-plugin

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0)

<!-- Add PyPI badge once published -->
<!-- [![PyPI version](https://badge.fury.io/py/docling-bedrock-plugin.svg)](https://badge.fury.io/py/docling-bedrock-plugin) -->

> AWS Bedrock integration plugin for the [Docling](https://github.com/docling-project/docling) framework.

This plugin allows Docling users to leverage the powerful multimodal capabilities of AWS Bedrock models directly within their document processing workflows, enabling features like automated image description generation.

## Table of Contents

- [Installation](#installation)
- [AWS Configuration](#aws-configuration)
- [Usage](#usage)
  - [Examples](#examples)
  - [`PictureDescriptionBedrockApiOptions`](#picturedescriptionbedrockapioptions-parameters)
- [Contributing](#contributing)
- [Credits](#credits)

## Installation

Ensure you have **Python >= 3.10** installed.

### 1. Install from Source (Development)

This is the recommended method for now, especially for development or using the latest code:

1.  **Clone the repository:**

    ```bash
    # Replace with the actual repository URL when available
    git clone https://github.com/Slayer412/docling-bedrock-plugin.git
    cd docling-bedrock-plugin
    ```

2.  **Install in editable mode:**
    ```bash
    pip install -e .
    ```
    - This installs the package and its dependencies (`docling`, `boto3`).
    - The `-e` flag means changes you make to the source code are immediately reflected without reinstalling.

### 2. Install from PyPI (Future)

Once published, you will be able to install directly using pip:

```bash
# Coming soon!
# pip install docling-bedrock-plugin
```

## AWS Configuration

This plugin interacts with AWS Bedrock and requires AWS credentials configured for `boto3`. Ensure your environment is set up correctly.

Common methods include:

- **Environment Variables:** `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`.
- **Shared Credential File:** `~/.aws/credentials`.
- **AWS Config File:** `~/.aws/config`.
- **IAM Role:** Attached to your EC2 instance or ECS task.

Refer to the official [Boto3 Credentials Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html) for detailed configuration instructions.
You must also have access granted to the specific Bedrock models you intend to use within your AWS account.

## Usage

This plugin integrates seamlessly with Docling via its entry point mechanism. Once installed, you can configure and use the Bedrock functionalities within your Docling pipelines or scripts.

The primary use case currently implemented is generating descriptions for images within documents.

### Examples

See the `examples/` directory for practical, ready-to-run Python scripts:

- [`bedrock_image_description.py`](examples/bedrock_image_description.py): Processes PDF, Word, or PowerPoint documents, extracts images, gets descriptions via Bedrock, and saves annotated documents.
- [`image_description.py`](examples/image_description.py): A simpler script to process a single image file directly with Bedrock and print the description.

📖 **[View Examples README](examples/README.md)** for detailed usage instructions.

### `PictureDescriptionBedrockApiOptions` Parameters

These options allow you to configure the Bedrock API call for image descriptions. They are typically passed when initializing the `PictureDescriptionBedrockApiModel`.

**Note:** Currently, this plugin specifically supports integration with Anthropic's Claude 3 models (e.g., Sonnet, Haiku) available via Bedrock. Support for other multimodal models may be added in the future.

| Parameter        | Type        | Description                                                 | Default                |
| :--------------- | :---------- | :---------------------------------------------------------- | :--------------------- |
| `model_id`       | `str`       | **Required.** AWS Bedrock model ID (must be multimodal).    | -                      |
| `region_name`    | `str`       | AWS region where Bedrock is available.                      | Uses `boto3` default   |
| `profile_name`   | `str`       | AWS profile name from credentials file.                     | Uses `boto3` default   |
| `prompt`         | `str`       | Prompt guiding the model's image description.               | "Describe this image." |
| `max_tokens`     | `int`       | Max tokens in the generated description.                    | 300                    |
| `temperature`    | `float`     | Controls randomness (0.0-1.0). Lower is more deterministic. | 0.7                    |
| `top_p`          | `float`     | Nucleus sampling probability (0.0-1.0).                     | 0.9                    |
| `top_k`          | `int`       | Top-k filtering diversity control.                          | `None`                 |
| `max_workers`    | `int`       | Max concurrent API calls when processing multiple images.   | 3                      |
| `stop_sequences` | `List[str]` | List of strings that will stop generation.                  | `[]`                   |

#### Example Configuration:

```python
from docling_bedrock_plugin.pipeline_options import PictureDescriptionBedrockApiOptions

bedrock_options = PictureDescriptionBedrockApiOptions(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    region_name="us-east-1",                     # Optional: Specify AWS region
    prompt="Provide a detailed accessibility description for this image.",
    max_tokens=400,
    temperature=0.4,
    max_workers=5
)

# ... then use bedrock_options when initializing the model or pipeline step
```

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these general steps:

1.  **Fork** the repository on GitHub.
2.  **Clone** your fork locally (`git clone <your-fork-url>`).
3.  Create a **new branch** for your feature or fix (`git checkout -b feature/your-new-feature`).
4.  Make your **changes** and **commit** them (`git commit -am 'Add some feature'`).
5.  **Push** your changes to your fork (`git push origin feature/your-new-feature`).
6.  Create a **Pull Request** back to the main repository.

_Please ensure your code includes tests where appropriate and follows existing coding style._

## Credits

- **Author:** Shreyash Patel ([patelshreays007@gmail.com](mailto:patelshreays007@gmail.com))
- **Docling:** [Docling Project on GitHub](https://github.com/docling-project/docling)
- **Boto3:** [AWS SDK for Python](https://github.com/boto/boto3)
- **AWS Bedrock:** [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
