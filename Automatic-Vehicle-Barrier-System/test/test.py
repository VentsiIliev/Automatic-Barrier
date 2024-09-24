import cv2
from ultralytics import YOLO
from VehicleDetection import VehicleDetection
from VehicleDetector import VehicleDetector

# run while loop for the camera and perform vehicle detection using the VehicleDetection class

# initialize the camera
camera = cv2.VideoCapture("sample.mp4")
# load the car detection model
car_detector = VehicleDetector('yolov8n.pt')
# initialize the VehicleDetection class
vehicleDetection = VehicleDetection(car_detector)

while True:
    ret, frame = camera.read()
    if not ret:
        print("failed to grab frame")
        break
    frame = cv2.resize(frame, (1280, 720))
    # detect cars
    # cars = vehicleDetection.detect_vehicle(frame)
    cars = car_detector.detect(frame)
    if cars is None or len(cars) == 0:
        print('No cars detected')
        continue
    for car in cars:
        x, y, w, h, score = car
        x, y, w, h = map(int, [x, y, w, h])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # car_region = frame[y:y + h, x:x + w]
    cv2.imshow('frame', frame)
    cv2.waitKey(1)
