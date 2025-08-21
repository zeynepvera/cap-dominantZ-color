
from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class OutputDominantColor(Output):
    name: Literal["dominantColor"] = "dominantColor"
    value: str
    type: Literal["string"] = "string"

    class Config:
        title = "Dominant Color (RGB)"



class ColorDominantInputs(Inputs):
    inputImage: InputImage

class ColorClusters(Config):
    name: Literal["colorClusters"] = "colorClusters"
    value: int = Field(default=4, ge=1, le=10)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Color Clusters (K)"


class MaxIterations(Config):
    name: Literal["maxIterations"] = "maxIterations"
    value: int = Field(default=100, ge=1, le=500)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Max Iterations"


class TargetSize(Config):
    name: Literal["targetSize"] = "targetSize"
    value: int = Field(default=150, ge=1, le=250)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Downsample Target (px)"


class ColorDominantConfigs(Configs):
    colorClusters: ColorClusters
    maxIterations: MaxIterations
    targetSize: TargetSize




class ColorDominantOutputs(Outputs):
    dominantColor: OutputDominantColor



class ColorDominantRequest(Request):
    inputs: Optional[ColorDominantInputs]
    configs: ColorDominantConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class ColorDominantResponse(Response):
    outputs: ColorDominantOutputs


class ColorDominant(Config):
    name: Literal["ColorDominant"] = "ColorDominant"
    value: Union[ColorDominantRequest, ColorDominantResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "ColorDominant"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[ColorDominant]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        json_schema_extra = {
            "target": "value"
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["ColorDominant"] = "ColorDominant"
