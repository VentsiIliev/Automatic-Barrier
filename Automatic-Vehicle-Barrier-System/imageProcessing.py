import cv2
import numpy as np
from ultralytics import YOLO

import util

cascade_src = 'assets/cars.xml'
car_cascade = cv2.CascadeClassifier(cascade_src)
license_plate_detector = YOLO('assets/license_plate_detector.pt')

# img = cv2.imread('assets/images/20240916_15092412321312312312.jpg')
# img = cv2.imread('assets/images/121312.jpg')
# img = cv2.imread('assets/images/20240916_150920.jpg')
img = cv2.imread('assets/images/20240917_101512.jpg')
img = cv2.resize(img, (640, 480))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cars = car_cascade.detectMultiScale(gray, 1.1, 1)
license_plates_list = []
for (x, y, w, h) in cars:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    car_region = img[y:y + h, x:x + w]
    license_plates = license_plate_detector(car_region)[0]
    license_plates_list.append(license_plates)

for license_plate in license_plates.boxes.data.tolist():
    x1, y1, x2, y2, score, class_id = license_plate
    license_plate_region = car_region[int(y1):int(y2), int(x1):int(x2)]
    cv2.imwrite('assets/results/raw_license_plate_region.jpg', license_plate_region)
    # processed = util.preprocess_image(license_plate_region)

    license_plate_text, license_plate_text_score = util.read_license_plate(license_plate_region)
    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    cv2.putText(img, license_plate_text, (int(x1), int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

cv2.imshow("img",img)
cv2.waitKey(0)