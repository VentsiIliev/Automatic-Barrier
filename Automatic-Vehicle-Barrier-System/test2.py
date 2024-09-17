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
    print(vehicles[0])
    return vehicles


while True:
    ret, frame = camera.read()
    if not ret:
        print("failed to grab frame")
        break
    frame = cv2.resize(frame, (1280, 720))
    # detect cars
    cars = searchForVehicles(frame)
    if cars is None or len(cars) == 0:
        print('No cars detected')
        continue

    # detect license plates
    license_plates_list = []
    for car in cars:
        x, y, w, h, score = car
        x, y, w, h = map(int, [x, y, w, h])  # convert to integers
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        car_region = frame[y:y + h, x:x + w]
        license_plates = license_plate_detector(car_region)[0]
        license_plates_list.append(license_plates)

    # read license plates
    for license_plate in license_plates.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate

        global_x1 = x + int(x1)
        global_y1 = y + int(y1)
        global_x2 = x + int(x2)
        global_y2 = y + int(y2)

        license_plate_region = car_region[int(y1):int(y2), int(x1):int(x2)]
        cv2.imwrite('assets/results/raw_license_plate_region.jpg', license_plate_region)

        result = util.read_license_plate(license_plate_region)
        if result is None:
            continue
        license_plate_text, license_plate_text_score = result
        cv2.rectangle(frame, (global_x1, global_y1), (global_x2, global_y2), (0, 255, 0), 2)
        cv2.putText(frame, license_plate_text, (global_x1, global_y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
