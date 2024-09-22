from ultralytics import YOLO


class LicencePlateDetector:
    def __init__(self, modelPath):
        self.modelPath = modelPath
        self.model = YOLO(modelPath)

    def detect(self, frame):
        return self.model(frame)
