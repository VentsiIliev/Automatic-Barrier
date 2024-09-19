import cv2


class VehicleDetection:
    def __init__(self, vehicle_detector):
        self.vehicle_detector = vehicle_detector

    def detect_vehicle(self, image):
        vehicles = self.vehicle_detector.detect(image)
        if vehicles is None or len(vehicles) == 0:
            return None
        # sort vehicles by score
        vehicles.sort(key=lambda x: x[1], reverse=True)
        x1, y1, x2, y2, score = vehicles[0]
        # draw rectangle
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        # crop vehicle from image
        vehicle = image[int(y1):int(y2), int(x1):int(x2)]

        return vehicle
