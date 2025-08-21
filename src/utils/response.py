
from sdks.novavision.src.helper.package import PackageHelper
from components.Package.src.models.PackageModel import ColorDominantResponse, ColorDominantOutputs, ColorDominant
from components.Package.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, OutputImage

def build_response(context):
    outputImage = OutputImage(value=context.image)
    Outputs = ColorDominantOutputs(outputImage=outputImage)
    colorDominantResponse = ColorDominantResponse(outputs=Outputs)
    colorDominant = ColorDominant(value=colorDominantResponse)
    executor = ConfigExecutor(value=colorDominant)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
