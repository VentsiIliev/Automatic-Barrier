import onnx
import onnx_tf
# ​
# Load  ONNX model
onnx_model = onnx.load('license_plate_detector.onnx')
# ​
# Convert ONNX model to TensorFlow format
tf_model = onnx_tf.backend.prepare(onnx_model)
# Export  TensorFlow  model
tf_model.export_graph("license_plate_detector_tf.tf")
