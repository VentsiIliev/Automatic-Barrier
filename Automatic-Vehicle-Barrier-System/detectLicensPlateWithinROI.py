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
roi_x1, roi_y1, roi_x2, roi_y2 = 100, 100, 500, 500  # adjust these values as needed


def searchForVehicles(gray):
    vehicles = []
    results = car_detector(gray)[0]
    # filter results
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if int(class_id) in target_classes:
            vehicles.append([x1, y1, x2, y2, score])
    return vehicles


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
    # detect license plates
    license_plates_list = []
    license_plates = license_plate_detector(roi)[0]
    if license_plates is None or len(license_plates) == 0:
        print('No license plates detected')
        roi_color = (0, 0, 255)
        continue

    roi_color = (0, 255, 0)
    # read license plates
    for license_plate in license_plates.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate
        license_plate_region = roi[int(y1):int(y2), int(x1):int(x2)]
        cv2.imwrite('assets/results/raw_license_plate_region.jpg', license_plate_region)

        result = util.read_license_plate(license_plate_region)
        if result is None:
            cv2.imshow('frame', frame)
            cv2.waitKey(1)
            continue
        license_plate_text, license_plate_text_score = result
        print("license_plate_text",license_plate_text)
        frame_text_x1 = roi_x1 + int(x1)
        frame_text_y1 = roi_y1 + int(y1)

        # Put the text on the ROI
        cv2.putText(frame, license_plate_text, (frame_text_x1, frame_text_y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
