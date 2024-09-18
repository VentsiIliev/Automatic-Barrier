from ultralytics import YOLO


class LicencePlateDetector:
    def __init__(self, modelPath):
        self.model = license_plate_detector = YOLO('assets/license_plate_detector.pt')

    def detect(self, frame):
        return self.model(frame)