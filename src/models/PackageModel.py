from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package,
    Image,
    Inputs,
    Configs,
    Outputs,
    Response,
    Request,
    Output,
    Input,
    Config,
)


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"
        json_schema_extra = {
            "outputStructure": {
                "name": "string",
                "uID": "string",
                "mimeType": "string",
                "encoding": "string",
                "value": "string",
                "r_key": "string",
                "shape_key": "string",
            },
            "outputNotes": [
                "Image frame is stored in Redis (r_key/shape_key); value is empty. Connect only to image inputs.",
                "Resized frame: pixel coordinates of detections computed on the original frame no longer match it.",
            ],
        }


class Width(Config):
    """
    Target width in pixels.
    """

    name: Literal["Width"] = "Width"
    value: int = Field(ge=1, le=8192, default=640)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[1-8192]"] = "[1-8192]"

    class Config:
        title = "Width (px)"
        json_schema_extra = {"shortDescription": "Target Width"}


class Height(Config):
    """
    Target height in pixels.
    """

    name: Literal["Height"] = "Height"
    value: int = Field(ge=1, le=8192, default=640)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[1-8192]"] = "[1-8192]"

    class Config:
        title = "Height (px)"
        json_schema_extra = {"shortDescription": "Target Height"}


class PadColor(Config):
    """
    Colour of the padding added around the image, as #RRGGBB (#000000 black, #FFFFFF white).
    """

    name: Literal["PadColor"] = "PadColor"
    value: str = Field(default="#000000", pattern=r"^#([A-Fa-f0-9]{6})$")
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["#000000"] = "#000000"

    class Config:
        title = "Padding Color"
        json_schema_extra = {"shortDescription": "Padding Color"}


class ResizeInputs(Inputs):
    inputImage: InputImage


class ResizeOutputs(Outputs):
    outputImage: OutputImage


class SizeConfigs(Configs):
    width: Width
    height: Height


class LetterboxConfigs(Configs):
    width: Width
    height: Height
    padColor: PadColor


class StretchRequest(Request):
    inputs: Optional[ResizeInputs]
    configs: SizeConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class StretchResponse(Response):
    outputs: ResizeOutputs


class StretchExecutor(Config):
    """
    Resizes to exactly Width x Height. The aspect ratio is not kept, so the image may look stretched.
    """

    name: Literal["Stretch"] = "Stretch"
    value: Union[StretchRequest, StretchResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Stretch"
        json_schema_extra = {"target": {"value": 0}}


class FitWithinRequest(Request):
    inputs: Optional[ResizeInputs]
    configs: SizeConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class FitWithinResponse(Response):
    outputs: ResizeOutputs


class FitWithinExecutor(Config):
    """
    Shrinks or enlarges the image to the largest size that fits inside Width x Height, keeping the aspect
    ratio. No padding is added, so the output can be smaller than the target on one side.
    """

    name: Literal["FitWithin"] = "FitWithin"
    value: Union[FitWithinRequest, FitWithinResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Fit Within"
        json_schema_extra = {"target": {"value": 0}}


class LetterboxRequest(Request):
    inputs: Optional[ResizeInputs]
    configs: LetterboxConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class LetterboxResponse(Response):
    outputs: ResizeOutputs


class LetterboxExecutor(Config):
    """
    Fits the image inside Width x Height keeping the aspect ratio, then pads the rest with Padding Color.
    The output is always exactly Width x Height.
    """

    name: Literal["Letterbox"] = "Letterbox"
    value: Union[LetterboxRequest, LetterboxResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Fit (Padded)"
        json_schema_extra = {"target": {"value": 0}}


class CenterCropRequest(Request):
    inputs: Optional[ResizeInputs]
    configs: SizeConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class CenterCropResponse(Response):
    outputs: ResizeOutputs


class CenterCropExecutor(Config):
    """
    Fills Width x Height keeping the aspect ratio and cuts what overflows, from the centre.
    The output is always exactly Width x Height; the edges of the image may be lost.
    """

    name: Literal["CenterCrop"] = "CenterCrop"
    value: Union[CenterCropRequest, CenterCropResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Fill (Center Crop)"
        json_schema_extra = {"target": {"value": 0}}


class ConfigExecutor(Config):
    """
    How the image is brought to Width x Height: stretched, fitted inside, fitted with padding, or filled and
    cropped from the centre.
    """

    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[StretchExecutor, FitWithinExecutor, LetterboxExecutor, CenterCropExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        json_schema_extra = {"shortDescription": "Resize Mode"}


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["Resize"] = "Resize"
