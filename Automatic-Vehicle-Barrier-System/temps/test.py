import cv2
from ultralytics import YOLO

from utils import util

print(cv2.__version__)

cascade_src = '../assets/models/cars.xml'
# video_src = 'assets/sample.mp4'
# video_src = 'dataset/video2.avi'
# video_src = 'assets/sample2.mp4'

# cap = cv2.VideoCapture(video_src)
car_cascade = cv2.CascadeClassifier(cascade_src)
license_plate_detector = YOLO('../assets/models/license_plate_detector.pt')

img = cv2.imread('../assets/images/20240916_150924.jpg')
img = cv2.resize(img, (1920, 1080))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cars = car_cascade.detectMultiScale(gray, 1.1, 1)

car_region = None
license_plates_list = []
license_plates = license_plate_detector(img)[0]
if license_plates is None or len(license_plates) == 0:
    print('No license plates detected')

    text_size = cv2.getTextSize('No license plates detected', cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]

    # Calculate the center of the image
    x_center = img.shape[1] // 2
    y_center = img.shape[0] // 2

    # Calculate the bottom left corner of the text
    x_text = x_center - text_size[0] // 2
    y_text = y_center + text_size[1] // 2

    # Put the text in the center of the image
    cv2.putText(img, 'No license plates detected', (x_text, y_text), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('video', img)
    cv2.waitKey(0)
    exit()
license_plates_list.append(license_plates)

for license_plate in license_plates.boxes.data.tolist():
    x1, y1, x2, y2, score, class_id = license_plate
    license_plate_region = img.copy()[int(y1):int(y2), int(x1):int(x2)]
    cv2.imshow("license_plate_region",license_plate_region)
    cv2.waitKey(1)
    license_plate_text, license_plate_text_score = util.read_license_plate(license_plate_region)
    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    cv2.putText(img, license_plate_text, (int(x1), int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    # print(license_plate_text)


cv2.imshow('video', img)
cv2.waitKey(0)
