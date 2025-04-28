from docling_bedrock_plugin.picture_description_model import (
    PictureDescriptionBedrockApiModel,
)


def picture_description():
    return {
        "picture_description": [
            PictureDescriptionBedrockApiModel,
        ]
    }
