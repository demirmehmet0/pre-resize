from sdks.novavision.src.helper.package import PackageHelper
from components.Resize.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,
    ResizeOutputs,
    OutputImage,
    StretchResponse,
    StretchExecutor,
    FitWithinResponse,
    FitWithinExecutor,
    LetterboxResponse,
    LetterboxExecutor,
    CenterCropResponse,
    CenterCropExecutor,
)

_EXECUTORS = {
    "Stretch": (StretchResponse, StretchExecutor),
    "FitWithin": (FitWithinResponse, FitWithinExecutor),
    "Letterbox": (LetterboxResponse, LetterboxExecutor),
    "CenterCrop": (CenterCropResponse, CenterCropExecutor),
}


def build_response(context, executor_name):
    response_class, executor_class = _EXECUTORS[executor_name]
    outputs = ResizeOutputs(outputImage=OutputImage(value=context.image))
    executor = ConfigExecutor(value=executor_class(value=response_class(outputs=outputs)))
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    return package.build_model(context)
