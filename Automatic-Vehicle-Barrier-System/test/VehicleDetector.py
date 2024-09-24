import cv2
from ultralytics import YOLO


class VehicleDetector:
    def __init__(self, modelPath, confidense_threshold=0.5):
        self.modelPath = modelPath
        self.confidense_threshold = confidense_threshold
        self.model = YOLO(modelPath)
        self.target_classes = [2, 3, 5, 7]


    def detect(self, gray):
        # if not grayscale convert
        # if len(gray.shape) > 2:
        #     gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

        vehicles = []
        results = self.model(gray)[0]
        # filter results
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            if int(class_id) in self.target_classes and score > self.confidense_threshold:
                vehicles.append([x1, y1, x2, y2, score])

        return vehicles
