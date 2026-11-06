"""
Fills Width x Height keeping the aspect ratio and crops the overflow from the centre.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Resize.src.utils.response import build_response
from components.Resize.src.utils.resize import center_crop
from components.Resize.src.models.PackageModel import PackageModel


class CenterCrop(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.width = self.request.get_param("Width")
        self.height = self.request.get_param("Height")
        self.image = self.request.get_param("inputImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value, _ = center_crop(img.value, self.width, self.height)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        return build_response(context=self, executor_name="CenterCrop")


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
