import torch
from ultralytics import YOLO

# Load your PyTorch model
model = YOLO('license_plate_detector.pt')  # Load the YOLO model
model.model.eval()  # Set the model to evaluation mode

# Define a dummy input tensor with the correct size
dummy_input = torch.randn(1, 3, 640, 640)  # Adjust to your model's expected input size

# Export the model to ONNX format
torch.onnx.export(model.model, dummy_input, 'license_plate_detector.onnx',
                  export_params=True, opset_version=11,
                  do_constant_folding=True,
                  input_names=['input'],
                  output_names=['output'])

print("Model successfully exported to ONNX format.")
