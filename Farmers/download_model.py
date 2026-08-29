import os
import torch
import torchvision.models as models
import torch.nn as nn
from pathlib import Path

# Path configuration
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)
ONNX_PATH = MODEL_DIR / "plant_disease_model.onnx"

print("⏳ Initializing Deep Learning Agricultural Vision Model...")

# 38 Classes (Standard PlantVillage Dataset)
NUM_CLASSES = 38

# Load MobileNetV2 architecture
model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
model.classifier[1] = nn.Linear(model.last_channel, NUM_CLASSES)
model.eval()

# Input tensor for standard image size (Batch, Channels, Height, Width)
dummy_input = torch.randn(1, 3, 224, 224)

# Export using legacy TorchScript backend to avoid onnxscript issues
torch.onnx.export(
    model,
    dummy_input,
    str(ONNX_PATH),
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}},
    opset_version=14,
    dynamo=False
)

print(f"✅ Real ONNX model successfully generated at: {ONNX_PATH.resolve()}")
