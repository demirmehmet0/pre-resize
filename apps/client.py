import os
import sys
import cv2
import json
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from components.Resize.src.models.PackageModel import (
    PackageModel, PackageConfigs, ConfigExecutor, LetterboxExecutor, LetterboxRequest, LetterboxConfigs,
    ResizeInputs, InputImage, Width, Height, PadColor,
)
from sdks.novavision.src.base.model import Image
from sdks.novavision.src.media.image import Image as image

ENDPOINT_URL = "http://127.0.0.1:8000/api"


def infer():
    frame = cv2.imread("/opt/project/components/Resize/resources/yorkshire_terrier.jpg")
    image_obj = image.encode64(Image(name="DemoImage", uID="001", mimeType="image/jpg", encoding="bytes",
                                     value=frame, type="Image"))
    configs = LetterboxConfigs(width=Width(value=640), height=Height(value=640), padColor=PadColor(value="#000000"))
    req = LetterboxRequest(inputs=ResizeInputs(inputImage=InputImage(value=image_obj)), configs=configs)
    executor = ConfigExecutor(value=LetterboxExecutor(value=req))
    request = PackageModel(configs=PackageConfigs(executor=executor), name="Resize")
    response = requests.post(ENDPOINT_URL, json=json.loads(request.json()))
    response.raise_for_status()
    print(response.json())


if __name__ == "__main__":
    infer()
