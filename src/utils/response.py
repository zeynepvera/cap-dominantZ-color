
from sdks.novavision.src.helper.package import PackageHelper
from capsules.ColorDominant.src.models.PackageModel import ColorDominantResponse, ColorDominantOutputs, ColorDominant, OutputDominantColor
from capsules.ColorDominant.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor

def build_response(context):
    dominant = OutputDominantColor(value=context.dominantColor)
    outputs = ColorDominantOutputs(dominantColor=dominant)
    colorDominantResponse = ColorDominantResponse(outputs=outputs)
    colorDominant = ColorDominant(value=colorDominantResponse)
    executor = ConfigExecutor(value=colorDominant)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
