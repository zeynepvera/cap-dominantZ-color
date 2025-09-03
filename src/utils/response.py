
from sdks.novavision.src.helper.package import PackageHelper
from capsules.DominantColor.src.models.PackageModel import DominantColorResponse, DominantColorOutputs, DominantColor, OutputDominantColor
from capsules.DominantColor.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor

def build_response(context):
    dominant = OutputDominantColor(value=context.dominantColor)
    outputs = DominantColorOutputs(dominantColor=dominant)
    dominantColorResponse = DominantColorResponse(outputs=outputs)
    dominantColor = DominantColor(value= dominantColorResponse)
    executor = ConfigExecutor(value= dominantColor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
