import cv2
from ultralytics import YOLO

import util

# camera = cv2.VideoCapture(0)
camera = cv2.VideoCapture('assets/sample2.mp4')
# load car detection model
car_cascade = cv2.CascadeClassifier('assets/cars.xml')
car_detector = YOLO('assets/yolov8n.pt')
# load license plate detection model
license_plate_detector = YOLO('assets/license_plate_detector.pt')

target_classes = [2, 3, 5, 7]


def searchForVehicles(gray):
    vehicles = []
    results = car_detector(gray)[0]
    # filter results
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if int(class_id) in target_classes:
            vehicles.append([x1, y1, x2, y2, score])
    # print(vehicles[0])
    return vehicles


roi_x1, roi_y1, roi_x2, roi_y2 = 100, 100, 500, 500  # adjust these values as needed
roi_color = (0, 0, 255)
while True:
    ret, frame = camera.read()
    if not ret:
        print("failed to grab frame")
        break
    frame = cv2.resize(frame, (1280, 720))
    roi = frame[roi_y1:roi_y2, roi_x1:roi_x2]
    cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), roi_color, 2)
    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    # detect cars
    cars = searchForVehicles(roi)
    if cars is None or len(cars) == 0:
        print('No cars detected')
        roi_color = (0, 0, 255)
        continue

    roi_color = (0, 255, 0)

    for car in cars:
        x, y, w, h, score = car
        x, y, w, h = map(int, [x, y, w, h])  # convert to integers
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        car_region = frame[y:y + h, x:x + w]

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
