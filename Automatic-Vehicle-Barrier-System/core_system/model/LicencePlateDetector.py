from ultralytics import YOLO


class LicencePlateDetector:
    def __init__(self, modelPath):
        self.modelPath = modelPath
        self.model = YOLO(modelPath, task="detect", verbose=False)

    def detect(self, frame):
        self.model.info(verbose=True)
        return self.model(frame)
