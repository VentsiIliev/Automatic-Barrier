import cv2

from core_system.API.LicensePlateRecognizer import LicensePlateRecognizer
from core_system.model.LicencePlateDetector import LicencePlateDetector
from core_system.model.LicensePlateReader import LicensePlateReader

source = cv2.VideoCapture('../core_system/assets/videos/sample2.mp4')

license_plates_detector = LicencePlateDetector('assets/license_plate_detector.pt')
license_plate_reader = LicensePlateReader("^[ABEKMHOPCTYX]{1,2}[0123456789]{4}[ABEKMHOPCTYX]{2}$")
license_plate_recognizer = LicensePlateRecognizer(license_plates_detector, license_plate_reader)

while True:
    ret, frame = source.read()
    if not ret:
        print("failed to grab frame")
        break

    license_plate_text = license_plate_recognizer.recognize(frame)
    if license_plate_text is not None:
        print(license_plate_text)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break