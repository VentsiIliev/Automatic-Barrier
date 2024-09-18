import csv
import os
import time

import cv2
import torch
from ultralytics import YOLO

# import util
from LicencePlateDetector import LicencePlateDetector
from LicensePlate import LicensePlate
from datetime import datetime

from LicensePlateReader import LicensePlateReader

# camera = cv2.VideoCapture(1)
camera = cv2.VideoCapture('assets/sample2.mp4')
# camera = cv2.VideoCapture('assets/vecteezy_the-road-on-the-hill_1798948.mp4')
# camera = cv2.VideoCapture('assets/vecteezy_traffic-cars-passing-in-road-with-asphalt-with-cracks-seen_36990287.mov')
# camera = cv2.VideoCapture('assets/demo.mp4')
# load license plate detection model
# license_plate_detector = YOLO('assets/license_plate_detector.pt')
license_plates_detector = LicencePlateDetector('assets/license_plate_detector.pt')
license_plate_reader = LicensePlateReader("^[ABEKMHOPCTYX]{1,2}[0123456789]{4}[ABEKMHOPCTYX]{2}$")
target_classes = [2, 3, 5, 7]
roi_x1, roi_y1, roi_x2, roi_y2 = 400, 400, 1280, 600  # adjust these values as needed

roi_color = (0, 0, 255)

# Reduce the frame rate
frame_rate = 10
prev = 0


# Define a dummy callback function for the trackbars
def nothing(x):
    pass


# Create a window
cv2.namedWindow('frame')

# Create trackbars for adjusting the ROI
cv2.createTrackbar('roi_x1', 'frame', 400, 1280, nothing)
cv2.createTrackbar('roi_y1', 'frame', 400, 720, nothing)
cv2.createTrackbar('roi_x2', 'frame', 1280, 1280, nothing)
cv2.createTrackbar('roi_y2', 'frame', 600, 720, nothing)
cv2.createTrackbar('confidence', 'frame', 50, 100, nothing)
reg_text = "No license plates detected"
license_plates_detected = []
csv_file = "formatted_results.csv"
while True:
    time_elapsed = time.time() - prev
    ret, frame = camera.read()
    if not ret:
        print("failed to grab frame")
        break

    frame = cv2.resize(frame, (1280, 720))
    # Get the trackbar values
    roi_x1 = cv2.getTrackbarPos('roi_x1', 'frame')
    roi_y1 = cv2.getTrackbarPos('roi_y1', 'frame')
    roi_x2 = cv2.getTrackbarPos('roi_x2', 'frame')
    roi_y2 = cv2.getTrackbarPos('roi_y2', 'frame')

    roi = frame[roi_y1:roi_y2, roi_x1:roi_x2]
    cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 0, 255), 2)
    # Put the text on the ROI
    cv2.putText(frame, reg_text, (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 255), 2)
    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    # if time_elapsed > 1./frame_rate:
    #     prev = time.time()
    # else:
    #     continue
    # detect license plates
    license_plates_list = []
    license_plates = license_plates_detector.detect(roi)[0]
    if license_plates is None or len(license_plates) == 0:
        print('No license plates detected')
        roi_color = (0, 0, 255)
        continue

    roi_color = (0, 255, 0)
    # read license plates
    for license_plate in license_plates.boxes.data.tolist():
        confidence = cv2.getTrackbarPos('confidence', 'frame') / 100.0
        x1, y1, x2, y2, score, class_id = license_plate
        if score < confidence:
            reg_text = "No license plates detected"
            continue
        else:
            reg_text = "License plate detected"
        print("LP-score", score)
        # draw bbox for license plate
        cv2.rectangle(frame, (roi_x1 + int(x1), roi_y1 + int(y1)), (roi_x1 + int(x2), roi_y1 + int(y2)), (0, 255, 0), 2)
        license_plate_region = roi[int(y1):int(y2), int(x1):int(x2)]

        # result = util.read_license_plate(license_plate_region)
        result = license_plate_reader.read_license_plate(license_plate_region)

        license_plate_text, license_plate_text_score = result
        if result[0] is None:
            reg_text = f"INVALID LP-Score{score:.1f} LPT-Score{license_plate_text_score:.1f}"
        else:
            new_license_plate = LicensePlate(license_plate_text, score, license_plate_text_score,license_plate_region)
            # check if license plate is in formated results
            existing = False
            if len(license_plates_detected) != 0:
                for plate in license_plates_detected:
                    print(plate.__eq__(new_license_plate))
                    if plate.__eq__(new_license_plate):
                        existing = True
                        break
            if not existing:
                reg_text = f"{license_plate_text} LP-Score{score:.1f} LPT-Score{license_plate_text_score:.1f}"
                cv2.imshow("license_plate_region", license_plate_region)
                cv2.waitKey(1)
                # format results

                license_plates_detected.append(new_license_plate)
                # Write formatted results to CSV
                # Check if the file is empty
                file_exists = os.path.exists(csv_file) and os.path.getsize(csv_file) > 0

                with open(csv_file, mode='a', newline='') as file:  # Use 'a' for append mode
                    writer = csv.writer(file)

                    # Write the header only if the file is empty
                    if not file_exists:
                        writer.writerow(["License Plate Text", "Score", "License Plate Text Score"])

                        # Get the current date and time
                        current_datetime = datetime.now()
                        current_date = current_datetime.strftime("%Y-%m-%d")
                        current_time = current_datetime.strftime("%H:%M:%S")

                        # Prepare the row with license plate data and the current date and time
                        row = [current_date, current_time] + new_license_plate.__str__()

                        # Write the formatted result as a single row
                        writer.writerow(row)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(f"Results successfully written to {csv_file}")
        break

print(f"Results successfully written to {csv_file}")
