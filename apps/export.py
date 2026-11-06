import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from components.Resize.src.models.PackageModel import PackageModel as Package

with open("data.json", "w") as f:
    f.write(Package.schema_json(indent=2))
